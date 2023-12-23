"""Defines a unique voice
"""
import argparse
import json
import logging
import sys
from collections import defaultdict
from dataclasses import dataclass, field
from pathlib import Path
from typing import Dict, List, Optional, Tuple, Union

import sqlalchemy
from pydub import AudioSegment
from pydub.effects import speedup

log = logging.getLogger(__name__)


@dataclass
class Modifier():
    """Base class for sound modifiers
    """
    IDENTIFIER = ""

    @classmethod
    def from_str(
        cls,
        string: str  # pylint: disable=unused-argument
    ):
        """Create from string representation
        """
        return Modifier()

    def as_str(self) -> str:
        """Convert to string representation
        """
        return ""


@dataclass
class SpeedChangeModifier(Modifier):
    """Modify speed of audio without changing pitch
    """
    IDENTIFIER = "s"

    def __init__(self, speed_parameter: float):
        self.speed_parameter = float(speed_parameter)

    @classmethod
    def from_str(cls, string: str):
        speed_parameter_str = string.strip(SpeedChangeModifier.IDENTIFIER)
        return SpeedChangeModifier(speed_parameter=float(speed_parameter_str))

    def as_str(self) -> str:
        return f"{self.IDENTIFIER}{self.speed_parameter}"

    def modify_audio(self, audio: AudioSegment) -> AudioSegment:
        """Speed up/slow down audio file
        """
        return speedup(seg=audio, playback_speed=self.speed_parameter)


@dataclass
class NoOpModifier1(Modifier):
    """No-op modifier for testing
    """
    IDENTIFIER = "z"

    def __init__(self, parameter: float):
        self.parameter = float(parameter)

    @classmethod
    def from_str(cls, string: str):
        parameter = string.strip(NoOpModifier1.IDENTIFIER)
        return NoOpModifier1(parameter=float(parameter))

    def as_str(self) -> str:
        return f"{self.IDENTIFIER}{self.parameter}"


@dataclass
class NoOpModifier2(Modifier):
    """No-op modifier for testing
    """
    IDENTIFIER = "x"

    def __init__(self, parameter: float):
        self.parameter = float(parameter)

    @classmethod
    def from_str(cls, string: str):
        parameter = string.strip(NoOpModifier2.IDENTIFIER)
        return NoOpModifier2(parameter=float(parameter))

    def as_str(self) -> str:
        return f"{self.IDENTIFIER}{self.parameter}"


MODIFIERS = {
    SpeedChangeModifier.IDENTIFIER: SpeedChangeModifier,
    NoOpModifier1.IDENTIFIER: NoOpModifier1,
    NoOpModifier2.IDENTIFIER: NoOpModifier2,
}


@dataclass
class Word:
    """Represents a word (or punctuation)
    """
    word: str
    voice: Optional[str] = None
    # TODO: can we use a base class here? Hard to keep this updated
    modifiers: List[Union[SpeedChangeModifier, NoOpModifier1, NoOpModifier2]] = field(default_factory=list)
    is_punctuation: bool = False

    def as_str(self, with_voice: bool = False) -> str:
        """Convert to string representation

        Args:
            with_voice (bool, optional): Include voice string. Defaults to False.

        Returns:
            str: string representation
        """
        voice_string = f"{self.voice}:" if (with_voice and self.voice) else ""
        modifiers = self.modifiers
        modifiers.sort(key=lambda m: m.IDENTIFIER)
        modifier_strings = ",".join([modifier.as_str() for modifier in modifiers])
        modifiers_string = f"|{modifier_strings}" if modifiers else ""
        return f"{voice_string}{self.word}{modifiers_string}"

    # TODO: sorting does not take into account modifiers
    def __lt__(self, other) -> bool:
        return self.word < other.word

    def __gt__(self, other) -> bool:
        return self.word > other.word

    def __le__(self, other) -> bool:
        return self.word <= other.word

    def __ge__(self, other) -> bool:
        return self.word >= other.word

    def __eq__(self, other) -> bool:
        return self.word == other.word and self.modifiers == other.modifiers and self.is_punctuation == other.is_punctuation and self.voice == other.voice

    # TODO: test that this matches __eq__ behavior
    def __hash__(self):
        return hash(repr(self))


# How much delay should be added in place of punctuation (in milliseconds)
PUNCTUATION_TIMING = {
    ',': 250,
    '.': 500,
}

DB_NAME = 'db.json'


class NoWordsFound(Exception):
    """Raised when a voice has no words
    """


class DuplicateWords(Exception):
    """Raised when a voice has duplicate words
    """


class InconsistentAudioFormats(Exception):
    """Raised when words have inconsistent audio formats
    """


class NoAudioFormatFound(Exception):
    """Raised when no audio format can be found
    """


class FailedToSplit(Exception):
    """Raised when a sentence cannot be split
    """


class NoVoiceSpecified(Exception):
    """Raised when no voice is specified
    """


class NoDatabaseSpecified(Exception):
    """No database connection was specified during init
    """


class ModifierSyntaxError(Exception):
    """Raised when there is a problem with the modifier syntax
    """


@dataclass
class Sentence:
    """Represents a sentence and it's parts
    """
    sentence: str
    sayable: List[Word]
    unsayable: List[Word]
    sayable_sentence: List[Word]
    audio: Optional[AudioSegment] = None


@dataclass
class DatabaseConnection:
    """Stores info related to database connection
    """
    engine: sqlalchemy.engine.Engine
    metadata: sqlalchemy.MetaData
    sentence_table: sqlalchemy.Table


class Voice:
    """Base class for Voice-like interfaces.
    Intended to involve generation of audio
    files from some source (files, web, etc).
    """

    def __init__(
        self,
        name: str,
        database: Optional[sqlalchemy.engine.Engine],
    ):
        self.name = name

        self._db: Optional[DatabaseConnection] = None
        if database is not None:
            metadata = sqlalchemy.MetaData()
            sentence_table = sqlalchemy.Table(
                self.name,
                metadata,
                sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
                sqlalchemy.Column("sentence", sqlalchemy.String, unique=True, nullable=False),
            )
            metadata.create_all(database)
            self._db = DatabaseConnection(
                metadata=metadata,
                sentence_table=sentence_table,
                engine=database,
            )
        self.words: List[Word] = []
        self.categories: Dict[str, List[str]] = {}

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.exit()

    def exit(self):
        """Clean up and close voice
        """
        if self._db is not None:
            self._db.engine.dispose()

    def _insert_sentence_into_db(self, sentence: str):
        if self._db is None:
            raise NoDatabaseSpecified
        ins = self._db.sentence_table.insert().values(sentence=sentence)
        with self._db.engine.begin() as conn:
            conn.execute(ins)

    def _sentence_exists(self, sentence: str) -> bool:
        if self._db is None:
            raise NoDatabaseSpecified

        sel = self._db.sentence_table.select().where(self._db.sentence_table.c.sentence == sentence)
        with self._db.engine.connect() as conn:
            result = conn.execute(sel)
            # TODO: there should be a way to use `.Count()` here
            return bool(result.all())

    def _get_generated_sentences_list(self) -> list[str]:
        if self._db is None:
            raise NoDatabaseSpecified
        sel = self._db.sentence_table.select()
        with self._db.engine.connect() as conn:
            result = conn.execute(sel)
            return [r.sentence for r in result.all()]

    def _get_generated_sentences_dict(self) -> dict[int, str]:
        if self._db is None:
            raise NoDatabaseSpecified
        sel = self._db.sentence_table.select()
        with self._db.engine.connect() as conn:
            result = conn.execute(sel)
            return {r.id: r.sentence for r in result.all()}

    def _get_sentence_info(self, words: List[Word]) -> Sentence:
        """Get basic sentence info for a given
        split sentence.

        Args:
            words (List[Word]): Words of sentence split into array

        Returns:
            Sentence: Sentence info
        """
        no_modifier_words = [Word(word=word.word, voice=word.voice, is_punctuation=word.is_punctuation) for word in words]
        sayable_words, unsayable_worlds = self.get_sayable_unsayable(no_modifier_words)
        sayable_sent_arr = self._get_sayable_sentence_arr(
            words, sayable_words)
        sayable_sent_str = self._create_sentence_string(sayable_sent_arr)

        return Sentence(
            sentence=sayable_sent_str,
            sayable=sayable_words,
            unsayable=unsayable_worlds,
            sayable_sentence=sayable_sent_arr,
            audio=None,
        )

    def generate_audio_from_array(self, words: List[Word], dry_run=False, save_to_db=True) -> Sentence:
        """Generates audio segment from sentence array.

        Args:
            words (List[str]): Words to try and turn into audio segment.
            dry_run (bool, optional): Skip actual segment generation. Defaults to False.

        Returns:
            Sentence: Sentence with audio segment.
        """
        sentence_info = self._get_sentence_info(words=words)

        if dry_run:
            return sentence_info

        log.debug("Generating %s", sentence_info.sentence)

        # Only create sentence if there are words to put in it
        if len(sentence_info.sayable) == 0:
            log.warning(
                "Can't say any words in %s, not generating", sentence_info.sentence)
            return sentence_info

        # Only bother inserting a sentence into the database if there is more than one word in it
        # TODO: test save_to_db
        if self._db and save_to_db and len(words) > 1:
            if not self._sentence_exists(sentence=sentence_info.sentence):
                self._insert_sentence_into_db(sentence=sentence_info.sentence)
        words_audio = self._create_audio_segments(sentence_info.sayable_sentence)
        sentence_info.audio = self.assemble_audio_segments(words_audio)

        return sentence_info

    def _create_audio_segments(
        self,
        word_array: List[Word],  # pylint: disable=unused-argument
    ) -> List[AudioSegment]:
        """Create audio segments for each entry in an array of words.

        Args:
            word_array (List[str]): Words to turn into audio segments.

        Returns:
            List[AudioSegment]: Audio segments.
        """
        return []

    def generate_audio(self, sentence: str, dry_run=False) -> Sentence:
        """Generates audio from the given sentence

        Args:
            sentence (string): Sentence string to be generated
            dry_run (bool, optional): Don't generate audio. Defaults to False.
        Returns:
            Sentence: Information about generated sentence.
        """
        log.info("Asked to generate %s", sentence)
        split_sentence = self._split_sentence(sentence)
        proc_sentence = self.process_sentence(split_sentence, voice=self.name)
        return self.generate_audio_from_array(
            words=proc_sentence,
            dry_run=dry_run,
        )

    @staticmethod
    def _split_sentence(sentence: str) -> List[Word]:
        return [Word(word=word) for word in sentence.lower().rstrip().split(" ")]

    @staticmethod
    def _extract_modifiers(words: List[Word]) -> List[Word]:
        processed_words = []
        for word in words:
            if "|" not in word.word:
                processed_words.append(word)
                continue
            (word_string, _, modifiers_string) = word.word.rpartition("|")
            modifiers_strings = modifiers_string.split(",")
            modifiers_strings.sort()

            # Dict so we can dedupe
            modifiers = {}
            for modifier_string in modifiers_strings:
                modifier_class = MODIFIERS.get(modifier_string[0])
                # TODO: not bubbling up the invalid modifier doesn't seem right
                if modifier_class:
                    modifier = modifier_class.from_str(modifier_string)
                    modifiers[modifier.IDENTIFIER] = modifier

            word.word = word_string
            word.modifiers = list(modifiers.values())
            processed_words.append(word)
        return processed_words

    @staticmethod
    def process_sentence(split_sent: List[Word], voice=str) -> List[Word]:
        """
        Takes a normally formatted sentence and breaks it into base elements

        Args:
            split_sent (List[str]): words in sentence

        Returns:
            List[Word]: array of elements in sentence
        """
        # TODO: This could use some rethinking. Should be easier to just always break punctuation marks
        # into their own elements, rather than selectively only dealing with trailing ones.
        log.info("Processing sentence '%s'", split_sent)

        # First pass for modifiers
        split_sent = Voice._extract_modifiers(words=split_sent)

        # Pull out punctuation
        reduced_sent = []
        for item in split_sent:
            word_string = item.word
            # find first punctuation mark, if any
            first_punct: Optional[str] = None
            try:
                first_punct = next(
                    (punct for punct in PUNCTUATION_TIMING if punct in word_string))
            except StopIteration:
                pass

            if first_punct:
                # Get its index
                first_punct_ind = word_string.find(first_punct)

                # Special case: If this is a multi voice sentence,
                # we don't want to rip the voice definition out of a singe-punctuation
                # mark. IE vox:.
                # TODO: This is a bit hacky. Would be great if this method doesn't
                # have to know about multi-voice syntax.
                if first_punct_ind >= 2 and word_string[first_punct_ind - 1] == ':':
                    reduced_sent.append(Word(word=word_string[:first_punct_ind + 1], voice=voice, modifiers=item.modifiers))
                    if len(word_string) >= first_punct_ind:
                        first_punct_ind += 1
                else:
                    # Add everything before punct (the word, if any)
                    if word_string[:first_punct_ind]:
                        reduced_sent.append(Word(word=word_string[:first_punct_ind], voice=voice, modifiers=item.modifiers))

                # Add all the punctuation if its actually punctuation
                # TODO: Figure out if I want to deal with types like ".hello" throwing out all the characters after the period.
                for punct in word_string[first_punct_ind:]:
                    if punct in PUNCTUATION_TIMING:
                        reduced_sent.append(Word(word=punct, voice=voice, is_punctuation=True))

            else:
                # TODO: copying from a Word to a Word like this is ugly
                reduced_sent.append(Word(word=word_string, voice=voice, modifiers=item.modifiers))

        # Clean blanks from reduced_sent
        reduced_sent = [value for value in reduced_sent if value.word != '']

        log.info("Sentence processed: '%s'", reduced_sent)
        return reduced_sent

    def get_sayable_unsayable(self, words: List[Word]) -> Tuple[List[Word], List[Word]]:
        """Get words that are sayable or unsayable
        from a list of words.

        Args:
            words (List[Word]): Words to check.

        Returns:
            Tuple[List[Word], List[Word]]: Sayable and unsayable words.
        """
        # TODO: This shouldn't need two separate processings of the same sentence. Sets, people. Sets!
        sayable_words_set = set(self.words)
        sayable_words_set.update([Word(word=punct, voice=self.name, is_punctuation=True) for punct in PUNCTUATION_TIMING])

        words_set = set((dict.fromkeys(words)))  # removes duplicates

        unsayable_set = words_set - sayable_words_set
        sayable_set = words_set - unsayable_set
        unsayable = list(unsayable_set)
        unsayable.sort()
        sayable = list(sayable_set)
        sayable.sort()
        return sayable, unsayable

    def _get_sayable_sentence_arr(self, words: List[Word], sayable_words: List[Word]) -> List[Word]:
        """Removes words from sentence array that are not sayable.

        Args:
            words (List[Word]): Array of words in sentence, in order.
            sayable_words (List[Word]): Words from sentence that can actually be said.

        Returns:
            List[Word]: Words in sentence that are sayable, in order.
        """
        # TODO: This is just a simple set operation. Function probably isn't needed. At least change to using a set.
        return [word for word in words if Word(word=word.word, voice=word.voice, is_punctuation=word.is_punctuation) in sayable_words]

    def _create_sentence_string(self, words: List[Word]) -> str:
        """Joins sentence array into a string.

        Args:
            words (List[str]): Words in sentence, in order.

        Returns:
            str: Sentence string.
        """
        if len(words) == 1:
            return words[0].as_str(with_voice=False)
        return " ".join([word.as_str(with_voice=False) for word in words])

    def get_generated_sentences(self) -> List[str]:
        """Gets the previously generated sentence strings

        Returns:
            List[str]: List of sentence strings generated previously
        """
        return self._get_generated_sentences_list()

    def get_generated_sentences_dict(self) -> Dict[int, str]:
        """Gets the previously generated sentence strings
        along with their corresponding ID in the database

        Returns:
            Dict[int, str]: Dict of sentence and id pairs
        """
        return self._get_generated_sentences_dict()

    @staticmethod
    def assemble_audio_segments(segments: List[AudioSegment]) -> AudioSegment:
        """Assemble audio segments into one audio segment.

        Args:
            segments (List[AudioSegment]): Segments to assemble.

        Returns:
            AudioSegment: Assembled audio segment.
        """
        # We set all audio segments to the lowest common frame rate
        # to avoid some really ugly artifacting when a low frame rate
        # clip is appended to a high frame rate one.
        frame_rates = [word.frame_rate for word in segments]
        frame_rate = min(frame_rates)

        sentence_audio = segments.pop(0)
        sentence_audio = sentence_audio.set_frame_rate(frame_rate)
        for word_audio in segments:
            word_audio = word_audio.set_frame_rate(frame_rate)
            sentence_audio = sentence_audio + word_audio

        return sentence_audio


class SingleVoice(Voice):
    """Comprises all information and methods
    needed to index a folder of voice audio files
    and generate audio from them given a sentence string.
    """

    def __init__(self, name: str, path: Path, database: Optional[DatabaseConnection]):
        """
        Args:
            name: Name of voice
            path (Path): Path to folder of voice audio files.
            database (Optional[DatabaseConnection]): Database connection information.
                If none provided, no database will be used and no data will persist.
        """
        super().__init__(name=name, database=database)
        self.path = path

        self.info_path = self.path.joinpath("info/")
        self.info_name = "info.json"

        self._word_dict, self.categories = self._build_word_dict(self.path)
        self._audio_format = self._find_audio_format(
            self._word_dict)  # TODO: Use properies?

        self.words = self._get_words()

        self._read_info(self.info_path, self.info_name)

    def _build_word_dict(self, path: Path) -> Tuple[Dict[str, Path], Dict[str, List[str]]]:
        """Builds dictionary of all available words and categories.

        Args:
            path (Path): Path to folder of voice audio files, or folders of voices files.

        Raises:
            DuplicateWords: Raised if there are duplicate filenames present.
            NoWordsFound: Raised if no words are found.

        Returns:
            Tuple[Dict[str, Path], Dict[str, List[str]]]: Dict of {filepath: word} associations and {category: [words]}.
        """
        word_dict = {}
        categories = defaultdict(list)

        for word_path in path.glob("**/*"):
            if word_path.is_dir():
                continue
            if word_path.parent.name == 'info':
                continue
            word = word_path
            name = str(word.stem).lower()
            if name in word_dict:
                raise DuplicateWords(f"Word {name} is duplicated")
            category = ''
            if word.parent != path:
                category = word.parent.name

            word_dict[name] = word
            if category:
                categories[category].append(name)
                # This is probably bad
                categories[category].sort()

        if len(word_dict) == 0:
            log.error("No words found")
            raise NoWordsFound

        return word_dict, categories

    def _read_info(self, path: Path, info_name: str):
        """Reads info file (if it exists)
        Args:
            path (Path): Path where info file resides.
            info_name (str): Name of info file.
        """
        # TODO: Allow arbitrary groupings of words
        info_path = path.joinpath(info_name)
        if info_path.exists():
            with open(info_path, 'r', encoding='UTF-8') as info_file:
                # TODO: we don't currently use this. Leaving it be to validate format
                json.load(info_file)

    def _find_audio_format(self, word_dict: Dict[str, Path]) -> str:
        """Determines audio format of voice audio files.

        Args:
            word_dict (Dict[str, Path]): Dict of {filepath: word} associations.

        Raises:
            NoAudioFormatFound: Raised if no audio format can be determined.
            InconsistentAudioFormats: Raised if there are inconsistent audio formats.

        Returns:
            str: Audio format.
        """
        file_format = None
        for path in word_dict.values():
            if file_format is None:
                file_format = path.suffix[1:]
            else:
                if str(file_format) != str(path.suffix[1:]):
                    log.error("Inconsistent audio formats in the word dict. File %s does not match expected format of %s", path, file_format)
                    raise InconsistentAudioFormats
        if not file_format:
            raise NoAudioFormatFound
        log.info("Audio format found: %s", file_format)
        return file_format

    # TODO: sweep docstrings for str -> Word

    def _get_words(self) -> List[Word]:
        """Gets the available words for the voice

        Returns:
            List[Word]: Words available to the voice
        """
        word_list = list(self._word_dict.keys())
        word_list.sort()
        return [Word(word=word, voice=self.name) for word in word_list]

    def get_audio_format(self) -> str:
        """Get the audio format of the voice files as well as generated files
        Returns:
            (string): Audio format
        """
        return self._audio_format

    def _create_audio_segments(self, word_array: List[Word]) -> List[AudioSegment]:
        words_audio: List[AudioSegment] = []
        for word in word_array:
            if word.is_punctuation:
                words_audio.append(AudioSegment.silent(
                    PUNCTUATION_TIMING[word.word]))
            else:
                audio_segment = AudioSegment.from_file(
                    self._word_dict[word.word], self._audio_format)

                for modifier in word.modifiers:
                    match modifier:
                        case SpeedChangeModifier():
                            audio_segment = modifier.modify_audio(audio_segment)

                words_audio.append(audio_segment)
        return words_audio


class MultiVoice(Voice):
    """Voice class that uses other voices to assemble
    multi-voice sentences.

    Example: vox:hello hev:there
    Generates a sentence with one word from a voice
    called "vox" and another from a voice called "hev."
    """

    def __init__(self, voices: Dict[str, SingleVoice], database: Optional[DatabaseConnection]):
        """
        Args:
            voices (Dict[str, SingleVoice]): Voices to use to assemble sentences.
            database (Optional[DatabaseConnection]): Database connection information.
                If none provided, no database will be used and no data will persist.
        """
        super().__init__(name='multi', database=database)
        self._voices = voices

        self.words = self._get_words(voices)

    def _get_words(self, voices: Dict[str, SingleVoice]) -> List[Word]:
        words = []
        for _, voice in voices.items():
            voice_words = voice.words.copy()
            words.extend(voice_words)
        return words

    def _get_sentence_info(self, words: List[Word]) -> Sentence:
        # TODO: There is a good amount of double-processing going on here
        words_and_voices = self._get_word_voice_assignment(words)
        sayable_words, unsayable_words = self.get_sayable_unsayable(
            words)
        sayable_sent_arr = [
            word_voice for word_voice in words_and_voices if word_voice in sayable_words]
        combined_voice_sentences = self.get_combined_voice_sentences(
            words_and_voices)
        sentence_arr = []
        for voice, sentence_words in combined_voice_sentences:
            voice_sentence_segment = f'{voice.name}:{" ".join([word.as_str() for word in sentence_words])}'
            sentence_arr.append(voice_sentence_segment)

        sayable_sent_str = ' '.join(sentence_arr)

        return Sentence(
            sentence=sayable_sent_str,
            sayable=sayable_words,
            unsayable=unsayable_words,
            sayable_sentence=sayable_sent_arr,
            audio=None,
        )

    def get_sayable_unsayable(self, words: List[Word]) -> Tuple[List[Word], List[Word]]:
        sayable = []
        unsayable = []
        words_and_voices = self._get_word_voice_assignment(words=words)
        combined_voice_sentences = self.get_combined_voice_sentences(
            words_and_voices)
        for voice, sentence_words in combined_voice_sentences:
            voice_sayable, voice_unsayable = voice.get_sayable_unsayable(sentence_words)
            sayable.extend(voice_sayable)
            unsayable.extend(voice_unsayable)
        sayable.sort()
        unsayable.sort()
        return sayable, unsayable

    def _create_audio_segments(self, word_array: List[Word]) -> List[AudioSegment]:
        combined_voice_sentences = self.get_combined_voice_sentences(
            word_array)
        return self.get_combined_audio(
            voice_sentences=combined_voice_sentences,
        )

    def _get_word_voice_assignment(self, words: List[Word]) -> List[Word]:
        """Determines voice for each word in a list separated
        from a raw sentence. Only the first word must have a voice
        assignment, further assignments are inferred.

        Example: vox:hello there hev:doctor freeman
        The first two words are assigned to vox, second two to hev

        Args:
            words (List[Word]): Words to determine voice assignment of

        Raises:
            FailedToSplit: Raised if unable to split a word/voice assignment.
            NoVoiceSpecified: Raised if initial voice cannot be determined.

        Returns:
            List[Word]: word:voice assignments
        """
        words_and_voices = []

        current_voice: Optional[SingleVoice] = None
        for word_maybe_voice in words:
            word_split = word_maybe_voice.word.split(':')
            word: Optional[Word] = None
            word_str: Optional[str] = None
            if len(word_split) == 2:
                current_voice = self._voices[word_split[0]]
                word_str = word_split[1]
            elif len(word_split) == 1:
                word_str = word_split[0]

            if not word_str:
                raise FailedToSplit
            if not current_voice:
                raise NoVoiceSpecified

            is_punctuation = word_str in PUNCTUATION_TIMING
            modifiers = word_maybe_voice.modifiers if not is_punctuation else []
            word = Word(word=word_str, voice=current_voice.name, modifiers=modifiers, is_punctuation=is_punctuation)

            words_and_voices.append(word)

        return words_and_voices

    def get_combined_voice_sentences(self, words: List[Word]) -> List[Tuple[SingleVoice, List[Word]]]:
        """Turns individual word:voice assignments into
        combined sentences for each word in sequence:

        Example: vox:hello vox:there hev:doctor hev:freeman vox:boop
        Returns vox:[hello, there] hev:[doctor freeman] vox:[boop]

        Args:
            words (List[Word]): Word:voice assignments

        Returns:
            List[Tuple[SingleVoice, List[Word]]]: Voice:sentence assignments
        """
        current_voice: Optional[SingleVoice] = None
        current_voice_sentence: List[Word] = []
        voice_sentences = []
        for word in words:
            if not current_voice:
                current_voice = self._voices[word.voice]
            if word.voice == current_voice.name:
                current_voice_sentence.append(word)
            else:
                voice_sentences.append((current_voice, current_voice_sentence))
                current_voice = self._voices[word.voice]
                current_voice_sentence = [word]
        if current_voice and current_voice_sentence:
            voice_sentences.append((current_voice, current_voice_sentence))
        return voice_sentences

    def get_combined_audio(self, voice_sentences: List[Tuple[SingleVoice, List[Word]]]) -> List[AudioSegment]:
        """Generates audio segments for each voice sentence

        Args:
            voice_sentences (List[Tuple[SingleVoice, List[str]]]): Voice:sentence assignments

        Returns:
            List[AudioSegment]: List of generated audio segments
        """
        audio_segments = []
        for voice, words in voice_sentences:
            sentence = voice.generate_audio_from_array(
                words, save_to_db=False)
            if sentence.audio:
                audio_segments.append(sentence.audio)
        return audio_segments


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    parser = argparse.ArgumentParser(
        description='Generate a sentence using a voice')
    parser.add_argument('-s', '--voice-dir', type=str, required=True,
                        help='Path to folder with voice audio files')
    parser.add_argument('-f', '--format', type=str, required=False,
                        default='wav', help='Audio format to export as')
    parser.add_argument('sentence', type=str)
    args = parser.parse_args()

    voice_dir = Path(args.voice_dir)
    if not voice_dir.is_dir():
        log.error('Voice dir at %s does not exist!', voice_dir)
        sys.exit(1)

    selected_voice = SingleVoice(name=voice_dir.name, path=voice_dir, database=None)
    generated_sentence = selected_voice.generate_audio(args.sentence)
    if generated_sentence is None or generated_sentence.audio is None:
        sys.exit(1)

    output_path = Path.cwd().joinpath(f"{generated_sentence.sentence}.{args.format}")

    generated_sentence.audio.export(output_path, format=args.format)
