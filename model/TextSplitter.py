import re
import nltk.tokenize.punkt as pkt
import nltk.tokenize.regexp as ret
from model import CustomLanguageVars

# https://www.regular-expressions.info/email.html


class TextSplitter:

    def __init__(self,text):
        '''
        Initialise the NLTK PunktSentenceTokenizer with our custom language variable for sentence splitting.
        Initialise a RegEx pattern for use in the NLTK RegexpTokenizer.
        :param text: string of raw continuous text
        '''
        self.text = text
        self.custom_tknzr = pkt.PunktSentenceTokenizer(lang_vars=CustomLanguageVars.CustomLanguageVars())
        self.pattern = r'''(?x)
            \b[a-zA-Z0-9._%+-]+@\s*?[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}\b          # Email addresses
            |\s+                   # any consecutive whitespace characters
            |\b(?:[a-zA-Z]\.)+\b   # abbreviations, e.g. U.S.A.
            |\d+(?:\.\d+)?%?       # numbers, incl. percentages
            |\w+(?:[-']\w+)*       # words with optional internal hyphen/apostrophe
            |[.,;:!?"'()\[\]]      # specific punctuation characters
            |\S+                   # any consecutive non-whitespace characters
            '''
        self.regex_tknzr = ret.RegexpTokenizer(self.pattern)

    def sent_splitter(self):
        '''
        Use a customised version of the NLTK PunktSentenceTokenizer to split the text into sentences,
        keeping all whitespace
        :return: list of sentences within the text.
        '''
        sents = self.custom_tknzr.tokenize(self.text)
        sents_newlines = []
        newlines = re.compile('\n{2,}')
        # Any entry that contains two or more consecutive newlines is split into separate entries at those newlines.
        for s in sents:
            slice_counter = 0
            if re.finditer(newlines,s):
                for match in re.finditer(newlines,s):
                    sents_newlines.append(s[slice_counter:match.span()[1]])
                    slice_counter = match.span()[1]
                # append the rest if there is a rest
                if s[slice_counter:] is not '':
                    sents_newlines.append(s[slice_counter:])
            else:
                sents_newlines.append(s)
        fixed_sents = []
        skip = False
        # Any entries that have mistakenly been cut at one of the following abbreviations but actually make up one
        # sentence with the next entry in the list are added back together here.
        for i,s in enumerate(sents_newlines):
            if skip:
                skip = False
            else:
                if s.endswith("e.g. ") or s.endswith("et al. ") or s.endswith("etc. ") or s.endswith("i.e. "):
                    fixed_sents.append(s+sents_newlines[i+1])
                    skip = True
                else:
                    fixed_sents.append(s)
        return fixed_sents

    def tokenize_sentences(self, sents):
        '''
        Tokenize the sentences according to the RegexpTokenizer initialised above.
        :param sents: list of sentences as returned by sent_splitter
        :return: list of lists of tokens; all tokens of all lists concatenated make up the original text.
        '''
        output = []
        for s in sents:
            output.append(self.regex_tknzr.tokenize(s))
        return output

    def split_text(self):
        return self.tokenize_sentences(self.sent_splitter())


