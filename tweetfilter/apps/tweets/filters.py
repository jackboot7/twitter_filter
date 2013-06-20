BANNED_WORDS = [
    ' chavez ',
    ' maduro ',
    ' mierda ',
]

class BannedWordsFilter():

    def filter_text(self, txt):
        for word in BANNED_WORDS:
            if txt.find(word):
                return False
        return True