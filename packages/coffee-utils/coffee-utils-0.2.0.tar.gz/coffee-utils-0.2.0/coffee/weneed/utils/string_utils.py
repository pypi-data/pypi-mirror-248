import string


class StringUtils:

    @staticmethod
    def get_ascii_chars():
        """
        Returns a set of ASCII characters.
        """
        return set(string.ascii_letters + string.digits + string.punctuation + string.whitespace)
