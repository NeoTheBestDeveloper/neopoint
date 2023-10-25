from enum import IntEnum


class HttpStatus(IntEnum):
    HTTP_200_OK = 200
    HTTP_404_NOT_FOUND = 404
    HTTP_500_INTERNAL_SERVER_ERROR = 500

    def _word_to_camel_case(self, word: str) -> str:
        lowered_word = word.lower()
        return lowered_word[0].capitalize() + lowered_word[1:]

    @property
    def status_code(self) -> int:
        return self.value

    @property
    def status_msg(self) -> str:
        msg = self.name.split("_", 2)[2]

        words_in_camel_case = (self._word_to_camel_case(word) for word in msg.split("_"))

        return " ".join(words_in_camel_case)
