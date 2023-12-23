"""Test voice
"""
# NOTE: since these tests use sqlite as their DB backend, indexes for results
# start at 1. This may differ if using postgresql in actual use.

# pylint: disable=missing-function-docstring,disable=missing-class-docstring
# pylint: disable=too-few-public-methods
# TODO: This isn't great and implies some re-architecting is needed
# pylint: disable=protected-access
import sys
from pathlib import Path
from typing import List

import pytest
import sqlalchemy

import hlvox
from hlvox import NoOpModifier1, SpeedChangeModifier, Word

from . import utils as th

# Stand-in files for testing
normal_files = ["hello.wav", "my.wav", "name.wav", "is.wav", "vox.wav"]
normal_files_words = [Word(word=word[:-4], voice="test") for word in normal_files]
inconst_format_files = ["hello.mp3", "my.wav", "name", "is.wav", "vox.mp4"]
no_format_files = ["imatextfile", "whatami"]
alph_files = ["a.wav", "b.wav", "c.wav"]
alph_files_words = [Word(word=word[:-4], voice="test") for word in alph_files]
category_files = {'bad': ["stop.wav", "bad.wav",
                          "no.wav"], 'good': ["go.wav", "yes.wav"]}


def words_from_strings(word_strings: List[str], voice=None, punctuation=False) -> List[Word]:
    return [Word(word=word, voice=voice, is_punctuation=punctuation) for word in word_strings]


class TestWord():
    def test_sorting(self):
        words = ["hi", "a", "zebra", "bit", "me"]
        word_classes = words_from_strings(words)
        word_classes.sort()

        words_sorted = words.copy()
        words_sorted.sort()
        word_classes_sorted = words_from_strings(words_sorted)

        assert word_classes == word_classes_sorted

    def test_list(self):
        # This is a really roundabout way to test equality and such,
        # but its something I ran into so _shrug_
        word1 = Word(word="hello")
        word2 = Word(word="hello")

        word_list = [word1]
        assert word2 in word_list

    def test_as_str(self):
        simple = Word(word="hello")
        assert simple.as_str() == "hello"
        assert simple.as_str(with_voice=True) == "hello"

        voice = Word(word="hello", voice="voice")
        assert voice.as_str() == "hello"
        assert voice.as_str(with_voice=True) == "voice:hello"

        modifier = Word(word="hello", voice="voice", modifiers=[NoOpModifier1("1.0")])
        assert modifier.as_str() == "hello|z1.0"
        assert modifier.as_str(with_voice=True) == "voice:hello|z1.0"

        modifiers = Word(word="hello", voice="voice", modifiers=[
            NoOpModifier1(parameter=2),
            SpeedChangeModifier(speed_parameter=0.1),
        ])
        assert modifiers.as_str() == "hello|s0.1,z2.0"
        assert modifiers.as_str(with_voice=True) == "voice:hello|s0.1,z2.0"


class TestFileHandling():
    def test_empty_files(self, tmp_path: Path):
        voice_dir = th.create_voice_files(tmp_path, [])
        with pytest.raises(hlvox.NoWordsFound):
            hlvox.SingleVoice(name='test', path=voice_dir,
                              database=None)

    def test_inconsistent_format(self, tmp_path: Path):
        voice_dir = th.create_voice_files(tmp_path, inconst_format_files)
        with pytest.raises(hlvox.InconsistentAudioFormats):
            hlvox.SingleVoice(name='test', path=voice_dir,
                              database=None)

    def test_no_format(self, tmp_path: Path):
        voice_dir = th.create_voice_files(tmp_path, no_format_files)
        with pytest.raises(hlvox.NoAudioFormatFound):
            hlvox.SingleVoice(name='test', path=voice_dir,
                              database=None)

    def test_audio_format(self, tmp_path: Path):
        voice_dir = th.create_voice_files(tmp_path, normal_files)
        with hlvox.SingleVoice(name='test', path=voice_dir, database=None) as unit:
            assert unit.get_audio_format() == "wav"


class TestDictContents():
    def test_basic_dict(self, tmp_path: Path):
        voice_dir = th.create_voice_files(tmp_path, normal_files)

        expected_names = normal_files_words
        expected_names.sort()

        with hlvox.SingleVoice(name='test', path=voice_dir, database=None) as unit:
            assert expected_names == unit.words

    def test_alphab(self, tmp_path: Path):
        voice_dir = th.create_voice_files(tmp_path, alph_files)

        expected_names = alph_files_words
        expected_names.sort()

        with hlvox.SingleVoice(name='test', path=voice_dir, database=None) as unit:
            assert expected_names == unit.words

    def test_caps(self, tmp_path: Path):
        word_strings = [
            "Cap.wav",
            "Cappa.wav",
        ]
        voice_dir = th.create_voice_files(tmp_path, word_strings)

        expected_words = [Word(word=word.lower()[:-4], voice="test") for word in word_strings]
        expected_words.sort()

        with hlvox.SingleVoice(name='test', path=voice_dir, database=None) as unit:
            assert expected_words == unit.words

    def test_categories(self, tmp_path: Path):
        voice_dir = th.create_category_files(tmp_path, category_files)
        expected_names = [item[:-4]
                          for sublist in category_files.values() for item in sublist]
        expected_words = words_from_strings(expected_names, voice="test")
        expected_words.sort()
        with hlvox.SingleVoice(name='test', path=voice_dir, database=None) as unit:
            assert expected_words == unit.words

            for category, words in category_files.items():
                category_words = [word[:-4] for word in words]
                category_words.sort()
                assert unit.categories[category] == category_words

    @pytest.mark.skipif(sys.platform == "win32", reason="Windows is not case sensitive so duplicates cant exist")
    def test_duplicates(self, tmp_path: Path):
        words = [
            "Cap.wav",
            "cAP.wav",
        ]
        voice_dir = th.create_voice_files(tmp_path, words, touch_only=True)

        with pytest.raises(hlvox.DuplicateWords):
            hlvox.SingleVoice(name='test', path=voice_dir,
                              database=None)


class TestDatabase():
    def test_reuse(self, tmp_path: Path):
        voice_dir = th.create_voice_files(tmp_path, normal_files)
        database = sqlalchemy.create_engine(f'sqlite:///{tmp_path}/db.sqlite')
        voice = hlvox.SingleVoice(
            name='test', path=voice_dir, database=database)

        voice.generate_audio(sentence="hello hello")
        voice.exit()

        voice = hlvox.SingleVoice(
            name='test', path=voice_dir, database=database)
        assert voice.get_generated_sentences() == ["hello hello"]


@pytest.fixture(name="voice")
def voice_fixture(tmp_path: Path):
    voice_dir = th.create_voice_files(tmp_path, normal_files)
    database = sqlalchemy.create_engine(f'sqlite:///{tmp_path}/db.sqlite')
    voice = hlvox.SingleVoice(
        name='test', path=voice_dir, database=database)
    yield voice
    voice.exit()


class TestSayableUnsayable():
    def test_empty_sent(self, voice: hlvox.SingleVoice):
        ret_say, ret_unsay = voice.get_sayable_unsayable([])

        assert ret_say == []
        assert ret_unsay == []

    def test_simple_sent(self, voice: hlvox.SingleVoice):
        words = words_from_strings(["hello"], voice="test")
        ret_say, ret_unsay = voice.get_sayable_unsayable(words)

        assert ret_say == [Word(word="hello", voice="test")]
        assert ret_unsay == []

    def test_duplicates(self, voice: hlvox.SingleVoice):
        words = words_from_strings(["hello", "hello", "world", "world", "duplicates!", "duplicates"], voice="test")
        words.extend(words_from_strings([",", ",", ".", "."], voice="test", punctuation=True))

        ret_say, ret_unsay = voice.get_sayable_unsayable(words)
        expected_ret_say = [
            Word(word="hello", voice="test"),
            Word(word=",", voice="test", is_punctuation=True),
            Word(word=".", voice="test", is_punctuation=True),
        ]
        expected_ret_say.sort()
        expected_ret_unsay = words_from_strings(["world", "duplicates", "duplicates!"], voice="test")
        expected_ret_unsay.sort()

        assert not set(ret_say) ^ set(expected_ret_say)
        assert not set(ret_unsay) ^ set(expected_ret_unsay)

    def test_comp_sent(self, voice: hlvox.SingleVoice):
        words = [
            Word(word="hello", voice="test"),
            Word(word=",", voice="test", is_punctuation=True),
            Word(word="world", voice="test"),
            Word(word=".", voice="test", is_punctuation=True),
            Word(word="vox", voice="test"),
            Word(word="can't", voice="test"),
            Word(word="say", voice="test"),
            Word(word="some", voice="test"),
            Word(word="of", voice="test"),
            Word(word="this", voice="test"),
            Word(word=".", voice="test", is_punctuation=True),
        ]

        ret_say, ret_unsay = voice.get_sayable_unsayable(words)
        expected_ret_say = [
            Word(word="hello", voice="test"),
            Word(word=",", voice="test", is_punctuation=True),
            Word(word="vox", voice="test"),
            Word(word=".", voice="test", is_punctuation=True),
        ]
        expected_ret_unsay = [
            Word(word="world", voice="test"),
            Word(word="can't", voice="test"),
            Word(word="say", voice="test"),
            Word(word="some", voice="test"),
            Word(word="of", voice="test"),
            Word(word="this", voice="test")
        ]
        assert not set(ret_say) ^ set(expected_ret_say)
        assert not set(ret_unsay) ^ set(expected_ret_unsay)

    def test_dup_punct(self, voice: hlvox.SingleVoice):
        words = [
            Word(word="hello", voice="test"),
            Word(word=".", voice="test", is_punctuation=True),
            Word(word=".", voice="test", is_punctuation=True),
            Word(word=".", voice="test", is_punctuation=True),
            Word(word="world", voice="test"),
        ]

        ret_say, ret_unsay = voice.get_sayable_unsayable(words)
        expected_ret_say = [
            Word(word="hello", voice="test"),
            Word(word=".", voice="test", is_punctuation=True)
        ]
        expected_ret_unsay = [
            Word(word="world", voice="test"),
        ]

        assert not set(ret_say) ^ set(expected_ret_say)
        assert not set(ret_unsay) ^ set(expected_ret_unsay)


class TestSentenceGeneration():
    def test_empty_sent(self, voice: hlvox.SingleVoice):
        ret = voice.generate_audio("")

        assert ret.sentence == ""
        assert ret.sayable == []
        assert ret.unsayable == []
        assert ret.audio is None

        assert voice.get_generated_sentences_dict() == {}

    def test_unsayable_sent(self, voice: hlvox.SingleVoice):
        ret = voice.generate_audio("whatthefuckdidyoujustsaytome")

        assert ret.sentence == ""
        assert ret.sayable == []
        assert ret.unsayable == [Word(word="whatthefuckdidyoujustsaytome", voice="test")]
        assert ret.audio is None

        assert voice.get_generated_sentences_dict() == {}

    def test_sayable_sent(self, voice: hlvox.SingleVoice):
        sentence = "hello, my name is vox"
        ret = voice.generate_audio(sentence)
        expected_sayable = [
            Word(",", voice="test", is_punctuation=True),
            Word("hello", voice="test"),
            Word("is", voice="test"),
            Word("my", voice="test"),
            Word("name", voice="test"),
            Word("vox", voice="test"),
        ]

        assert ret.sentence == "hello , my name is vox"
        assert ret.sayable == expected_sayable
        assert ret.unsayable == []
        assert ret.audio is not None

        assert voice.get_generated_sentences_dict() == {
            1: "hello , my name is vox"}

    def test_duplicate_sent(self, voice: hlvox.SingleVoice):
        voice.generate_audio("hello hello")
        voice.generate_audio("hello hello")

        assert voice.get_generated_sentences_dict() == {1: "hello hello"}
        assert len(voice._get_generated_sentences_list()) == 1

    def test_duplicate_words(self, voice: hlvox.SingleVoice):
        ret = voice.generate_audio("hello hello hello")

        assert ret.sentence == "hello hello hello"
        assert ret.sayable == [Word(word="hello", voice="test")]
        assert ret.unsayable == []
        assert ret.audio is not None

    def test_dup_punct(self, voice: hlvox.SingleVoice):
        ret = voice.generate_audio("hello... hello")

        assert ret.sentence == "hello . . . hello"
        assert ret.sayable == [Word(word=".", voice="test", is_punctuation=True), Word(word="hello", voice="test")]
        assert ret.unsayable == []
        assert ret.audio is not None

    def test_multiple_sent(self, voice: hlvox.SingleVoice):
        voice.generate_audio("hello hello")
        voice.generate_audio("vox hello")

        assert voice.get_generated_sentences_dict() == {
            1: "hello hello",
            2: "vox hello",
        }

    def test_dry_run(self, voice: hlvox.SingleVoice):
        ret = voice.generate_audio("hello", dry_run=True)
        assert ret.audio is None

    def test_one_word(self, voice: hlvox.SingleVoice):
        # We don't bother saving single words to the database
        voice.generate_audio("hello")

        assert voice.get_generated_sentences_dict() == {}


class TestModifiers():
    def test_basic_modifier(self, voice: hlvox.SingleVoice):
        ret = voice.generate_audio("hello|z1.0")

        assert ret.sayable_sentence == [
            Word(
                word="hello",
                voice="test",
                modifiers=[
                    hlvox.NoOpModifier1(parameter=1.0)
                ],
                is_punctuation=False,
            )]

    def test_duplicates(self, voice: hlvox.SingleVoice):
        ret = voice.generate_audio("hello|z1.0,x3,z2,z2.1,x0.1")

        assert ret.sayable_sentence == [
            Word(
                word="hello",
                voice="test",
                modifiers=[
                    # We should only get the first instance of a modifier
                    hlvox.NoOpModifier2(parameter=3.0),
                    hlvox.NoOpModifier1(parameter=1.0),
                ],
                is_punctuation=False,
            )]

    def test_invalid_modifier(self, voice: hlvox.SingleVoice):
        ret = voice.generate_audio("hello|z1.0 my|k2")

        assert ret.sayable_sentence == [
            Word(
                word="hello",
                voice="test",
                modifiers=[
                    hlvox.NoOpModifier1(parameter=1.0)
                ],
                is_punctuation=False,
            ),
            # For now, we just ignore invalid modifiers
            Word(
                word="my",
                voice="test",
            ),
        ]

    def test_complicated(self, voice: hlvox.SingleVoice):
        ret = voice.generate_audio("hello.|z1.0,x2 my, .|z0.1 name|z2 is, vox")

        assert ret.sayable_sentence == [
            Word(
                word="hello",
                voice="test",
                modifiers=[
                    # Sorted alphabetically, which is not the same order it was written in
                    hlvox.NoOpModifier2(parameter=2.0),
                    hlvox.NoOpModifier1(parameter=1.0),
                ],
                is_punctuation=False,
            ),
            # This punctuation gets pulled out from the modified portion, it doesn't get modified
            Word(
                word=".",
                voice="test",
                is_punctuation=True
            ),
            Word(
                word="my",
                voice="test",
            ),
            Word(
                word=",",
                voice="test",
                is_punctuation=True,
            ),
            # Again, punctuation doesn't get modified
            Word(
                word=".",
                voice="test",
                is_punctuation=True,
            ),
            Word(
                word="name",
                voice="test",
                modifiers=[
                    hlvox.NoOpModifier1(parameter=2.0),
                ]
            ),
            Word(
                word="is",
                voice="test",
            ),
            Word(
                word=",",
                voice="test",
                is_punctuation=True,
            ),
            Word(
                word="vox",
                voice="test",
            )
        ]
        assert ret.sentence == "hello|x2.0,z1.0 . my , . name|z2.0 is , vox"


class TestGetGeneratedSentences():
    def test_no_sentences(self, voice: hlvox.SingleVoice):
        ret = voice.get_generated_sentences()

        assert ret == []

    def test_single_sentences(self, voice: hlvox.SingleVoice):
        voice.generate_audio("hello hello")

        ret = voice.get_generated_sentences()

        assert ret == ["hello hello"]

    def test_multiple_sentences(self, voice: hlvox.SingleVoice):
        voice.generate_audio("hello hello")
        voice.generate_audio("vox hello")

        ret = voice.get_generated_sentences()

        assert ret == ["hello hello", "vox hello"]


class TestGetGeneratedSentencesDict():
    def test_no_sentences(self, voice: hlvox.SingleVoice):
        ret = voice.get_generated_sentences_dict()

        assert ret == {}

    def test_single_sentences(self, voice: hlvox.SingleVoice):
        voice.generate_audio("hello hello")

        ret = voice.get_generated_sentences_dict()

        assert ret == {1: "hello hello"}

    def test_multiple_sentences(self, voice: hlvox.SingleVoice):
        voice.generate_audio("hello hello")
        voice.generate_audio("vox hello")

        ret = voice.get_generated_sentences_dict()

        assert ret == {1: "hello hello", 2: "vox hello"}


@pytest.fixture(name="multi_voice")
def multi_voice_fixture(tmp_path: Path):
    norm_voice_dir = th.create_voice_files(
        tmp_path, normal_files, voice_name='norm')
    alph_voice_dir = th.create_voice_files(
        tmp_path, alph_files, voice_name='alph')
    alph_2_voice_dir = th.create_voice_files(
        tmp_path, alph_files, voice_name='alph2')
    norm_voice = hlvox.SingleVoice(
        name='norm',
        path=norm_voice_dir,
        database=sqlalchemy.create_engine(f'sqlite:///{tmp_path}/norm.sqlite')
    )
    alph_voice = hlvox.SingleVoice(
        name='alph',
        path=alph_voice_dir,
        database=sqlalchemy.create_engine(f'sqlite:///{tmp_path}/alph.sqlite')
    )
    alph_2_voice = hlvox.SingleVoice(
        name='alph2',
        path=alph_2_voice_dir,
        database=sqlalchemy.create_engine(f'sqlite:///{tmp_path}/alph2.sqlite')
    )
    voices = {
        'norm': norm_voice,
        'alph': alph_voice,
        'alph2': alph_2_voice,
    }
    multi_voice = hlvox.MultiVoice(
        voices=voices,
        database=sqlalchemy.create_engine(f'sqlite:///{tmp_path}/multi.sqlite'),
    )
    yield multi_voice
    multi_voice.exit()
    for voice in voices.values():
        voice.exit()


EXPECTED_MULTI_VOICE_WORDS = [
    Word(word="hello", voice="norm"),
    Word(word="is", voice="norm"),
    Word(word="my", voice="norm"),
    Word(word="name", voice="norm"),
    Word(word="vox", voice="norm"),
    Word(word="a", voice="alph"),
    Word(word="b", voice="alph"),
    Word(word="c", voice="alph"),
    Word(word="a", voice="alph2"),
    Word(word="b", voice="alph2"),
    Word(word="c", voice="alph2"),
]

# Multi-voice tests


class TestMultiWords:
    def test_normal(self, multi_voice: hlvox.MultiVoice):
        assert multi_voice.words == EXPECTED_MULTI_VOICE_WORDS


class TestMultiProcessSentence:
    # Just want to check that punctuation works as expected
    def test_normal(self, multi_voice: hlvox.MultiVoice):
        words = [
            Word(word="norm:hello,"),
            Word(word=","),
            Word(word="norm:my"),
            Word(word="norm:name"),
            Word(word="alph:a,"),
            Word(word="alph2:b"),
            Word(word=".")
        ]
        exp_words = [
            Word(word="norm:hello"),
            Word(word=",", is_punctuation=True),
            Word(word=",", is_punctuation=True),
            Word(word="norm:my"),
            Word(word="norm:name"),
            Word(word="alph:a"),
            Word(word=",", is_punctuation=True),
            Word(word="alph2:b"),
            Word(word=".", is_punctuation=True),
        ]
        ret = multi_voice.process_sentence(words, voice=None)
        assert ret == exp_words


class TestMultiSayableUnsayable:
    def test_empty(self, multi_voice: hlvox.MultiVoice):
        sayable, unsayable = multi_voice.get_sayable_unsayable(words=[])
        assert not sayable
        assert not unsayable

    def test_all_sayable(self, multi_voice: hlvox.MultiVoice):
        words = [
            Word(word="norm:hello"),
            Word(word="norm:my"),
            Word(word="alph:a"),
            Word(word="alph2:a"),
        ]
        exp_words = [
            Word(word="hello", voice="norm"),
            Word(word="my", voice="norm"),
            Word(word="a", voice="alph"),
            Word(word="a", voice="alph2"),
        ]
        exp_words.sort()
        sayable, unsayable = multi_voice.get_sayable_unsayable(words=words)
        words.sort()
        assert sayable == exp_words
        assert not unsayable

    def test_some_unsayable(self, multi_voice: hlvox.MultiVoice):
        words = words_from_strings(["norm:nope", "alph:butter", "alph2:404", "norm:vox", "alph:c", "alph2:c"])
        exp_unsayable = [
            Word(word="nope", voice="norm"),
            Word(word="butter", voice="alph"),
            Word(word="404", voice="alph2"),
        ]
        exp_sayable = [
            Word(word="vox", voice="norm"),
            Word(word="c", voice="alph"),
            Word(word="c", voice="alph2"),
        ]
        sayable, unsayable = multi_voice.get_sayable_unsayable(words=words)
        exp_sayable.sort()
        exp_unsayable.sort()
        assert sayable == exp_sayable
        assert unsayable == exp_unsayable

    def test_punctuation(self, multi_voice: hlvox.MultiVoice):
        words = [
            Word(word="norm:hello"),
            Word(word=",", is_punctuation=True),
            Word(word="alph:a", voice="alph"),
            Word(word=".", is_punctuation=True),
        ]
        exp_sayable = [
            Word(word="hello", voice="norm"),
            Word(word=",", voice="norm", is_punctuation=True),
            Word(word="a", voice="alph"),
            Word(word=".", voice="alph", is_punctuation=True),
        ]
        exp_sayable.sort()
        sayable, unsayable = multi_voice.get_sayable_unsayable(words=words)
        assert sayable == exp_sayable
        assert not unsayable


class TestMultiWordVoiceAssignment:
    def test_empty(self, multi_voice: hlvox.MultiVoice):
        assert not multi_voice._get_word_voice_assignment(words=[])

    def test_no_initial_voice(self, multi_voice: hlvox.MultiVoice):
        words = words_from_strings(["hello", "norm:my"])

        with pytest.raises(hlvox.NoVoiceSpecified):
            multi_voice._get_word_voice_assignment(words=words)

    def test_normal(self, multi_voice: hlvox.MultiVoice):
        words = words_from_strings(["norm:hello", "my", "alph:a", "a",
                                    "alph2:a", "norm:vox", "is", "alph:b"])
        exp_words_and_voices = [
            Word(word="hello", voice="norm"),
            Word(word="my", voice="norm"),
            Word(word="a", voice="alph"),
            Word(word="a", voice="alph"),
            Word(word="a", voice="alph2"),
            Word(word="vox", voice="norm"),
            Word(word="is", voice="norm"),
            Word(word="b", voice="alph"),
        ]

        assert multi_voice._get_word_voice_assignment(
            words=words) == exp_words_and_voices

    def test_punctuation(self, multi_voice: hlvox.MultiVoice):
        words = words_from_strings(["norm:hello", ",", "alph:a", "a",
                                    ".", "alph2:a", "norm:vox", "is", "alph:b"])
        exp_words_and_voices = [
            Word(word="hello", voice="norm"),
            Word(word=",", voice="norm", is_punctuation=True),
            Word(word="a", voice="alph"),
            Word(word="a", voice="alph"),
            Word(word=".", voice="alph", is_punctuation=True),
            Word(word="a", voice="alph2"),
            Word(word="vox", voice="norm"),
            Word(word="is", voice="norm"),
            Word(word="b", voice="alph"),
        ]

        assert multi_voice._get_word_voice_assignment(
            words=words) == exp_words_and_voices


class TestMultiCombinedVoiceSentences:
    def test_empty(self, multi_voice: hlvox.MultiVoice):
        assert not multi_voice.get_combined_voice_sentences(
            words=[])

    def test_single(self, multi_voice: hlvox.MultiVoice):
        voices = multi_voice._voices
        words_and_voices = [
            Word(word="hello", voice="norm")
        ]

        exp = [(voices["norm"], [Word(word="hello", voice="norm")])]
        assert multi_voice.get_combined_voice_sentences(
            words=words_and_voices) == exp

    def test_multiple(self, multi_voice: hlvox.MultiVoice):
        voices = multi_voice._voices

        words_and_voices = [
            Word(word="hello", voice="norm"),
            Word(word="my", voice="norm"),
            Word(word="a", voice="alph"),
            Word(word="a", voice="alph"),
            Word(word="a", voice="alph2"),
            Word(word="vox", voice="norm"),
            Word(word="is", voice="norm"),
            Word(word="b", voice="alph"),
        ]

        exp = [
            (voices["norm"], words_from_strings(["hello", "my"], voice="norm")),
            (voices["alph"], words_from_strings(["a", "a"], voice="alph")),
            (voices["alph2"], words_from_strings(["a"], voice="alph2")),
            (voices["norm"], words_from_strings(["vox", "is"], voice="norm")),
            (voices["alph"], words_from_strings(["b"], voice="alph")),
        ]
        assert multi_voice.get_combined_voice_sentences(
            words=words_and_voices) == exp


class TestMultiGenerateAudio:
    def test_normal(self, multi_voice: hlvox.MultiVoice):
        sentence = "norm:hello, my name is vox. alph:a b c"
        ret = multi_voice.generate_audio(sentence=sentence)

        exp_sentence = "norm:hello , my name is vox . alph:a b c"
        assert ret.sentence == exp_sentence
        # Sentence should not be saved into the individual voice's database
        assert len(multi_voice._voices["norm"].get_generated_sentences()) == 0
        assert len(multi_voice._voices["alph"].get_generated_sentences()) == 0


class TestDifficultSentences:
    def test_ellipse(self, multi_voice: hlvox.MultiVoice):
        sentence = "norm:hello norm:. norm:. norm:."
        ret = multi_voice.generate_audio(sentence=sentence)

        exp_sentence = "norm:hello . . ."
        assert ret.sentence == exp_sentence

        sentence = "norm:hello..."
        ret = multi_voice.generate_audio(sentence=sentence)
        exp_sentence = "norm:hello . . ."
        assert ret.sentence == exp_sentence

    def test_start_ellipse(self, multi_voice: hlvox.MultiVoice):
        sentence = "norm:."
        ret = multi_voice.generate_audio(sentence=sentence)

        exp_sentence = "norm:."
        assert ret.sentence == exp_sentence

        sentence = "norm:. . ."
        ret = multi_voice.generate_audio(sentence=sentence)

        exp_sentence = "norm:. . ."
        assert ret.sentence == exp_sentence

        sentence = "norm:..."
        ret = multi_voice.generate_audio(sentence=sentence)
        assert ret.sentence == exp_sentence


class TestMultiModifiers:
    def test_normal(self, multi_voice: hlvox.MultiVoice):
        sentence = "norm:hello|z1 norm:.|x2.0 norm:. norm:."
        ret = multi_voice.generate_audio(sentence=sentence)

        exp_sentence = "norm:hello|z1.0 . . ."
        assert ret.sentence == exp_sentence
