import nltk.tokenize.punkt as pkt


#https://stackoverflow.com/questions/33139531/preserve-empty-lines-with-nltks-punkt-tokenizer

class CustomLanguageVars(pkt.PunktLanguageVars):

    _period_context_fmt = r"""
        \S*                          # some word material
        %(SentEndChars)s             # a potential sentence ending
        \s*                          # ADDED: consecutive whitespace
        (?=(?P<after_tok>
            %(NonWord)s              # either other punctuation
            |
            (?P<next_tok>\S+)        # <-- Normally you would have \s+ in the beginning here
        ))"""

    # ORIGINAL VARIABLE
    # _period_context_fmt = r"""
    #     \S*                          # some word material
    #     %(SentEndChars)s             # a potential sentence ending
    #     (?=(?P<after_tok>
    #         %(NonWord)s              # either other punctuation
    #         |
    #         \s+(?P<next_tok>\S+)     # or whitespace and some other token
    #     ))"""
