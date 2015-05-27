from app import app


class Language(object):
    def __init__(self, language=None):
        """ Object to set language preference desired language to a
        redefined set of languages
        """

        self.language = language
        self.languages = {
                'es_mx': 'es-MX',
                'en_us': 'en-US'}

    def setLanguage(self, language=None):
        """ Set language to correct language code to utilize the proper
        language libraries
        """
        if not language:
            language = self.language
        if language in self.languages:
            lang = self.languages[language]
        else:
            lang = 'en-US'
        return lang
