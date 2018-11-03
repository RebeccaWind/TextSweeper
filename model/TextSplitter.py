import re
import nltk.tokenize.punkt as pkt
import nltk.tokenize.regexp as ret
from model import CustomLanguageVars

#             |\b[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}\b     # Email addresses
# https://www.regular-expressions.info/email.html


class TextSplitter:

    def __init__(self,text):
        self.text = text
        self.custom_tknzr = pkt.PunktSentenceTokenizer(lang_vars=CustomLanguageVars.CustomLanguageVars())
        #TODO add lower case character abbreviations?
        self.pattern = r'''(?x)
            \b[a-zA-Z0-9._%+-]+@\s*?[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}\b          #Email addresses
            |\s+                # any consecutive whitespace characters
            |\b(?:[A-Z]\.)+\b   # abbreviations, e.g. U.S.A.
            |\d+(?:\.\d+)?%?    # numbers, incl. percentages
            |\w+(?:[-']\w+)*    # words w/ optional internal hyphens/apostrophe
            |[.,;:!?"'()\[\]]   # punctuation
            |\S+                # any consecutive non-whitespace characters
            '''

        self.regex_tknzr = ret.RegexpTokenizer(self.pattern)

    def sent_splitter(self):
        '''
        use a customised version of the nltk punkt tokenizer to split the text into sentences,
        keeping all whitespace
        :return:
        '''
        sents = self.custom_tknzr.tokenize(self.text)
        sents_newlines = []
        newlines = re.compile('\n{2,}')
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
        output = []
        for s in sents:
            output.append(self.regex_tknzr.tokenize(s))
        return output

    def split_text(self):
        return self.tokenize_sentences(self.sent_splitter())


