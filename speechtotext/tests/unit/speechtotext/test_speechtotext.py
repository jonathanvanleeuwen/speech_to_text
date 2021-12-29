from speechtotext import SpeechToText


class TestSpeechToText:
    def test_init_no_cred(self):
        speech2txt = SpeechToText(subscription="")

        assert speech2txt._done == True