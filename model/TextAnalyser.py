import re

class TextAnalyser:
    '''
    analyses the text for possible occurrences that need to be cleaned
    '''
    def __init__(self, sents_list, dicts):
        '''
        Initialises the list of sentences and dicts from the passed objects.
        Initialises empty index lists for each of the possible cleaning steps.
        :param sents_list: list of lists of tokens that make up the whole text to be analysed
        :param dicts: instance of class Dicts that contains the reference dictionaries in form of NLTK FreqDist and
                        NLTK ConditionalFreqDist
        '''
        self.sents_list = sents_list
        self.dicts = dicts
        self.non_sentences_idx = []
        self.footer_idx = []
        self.hyphen_idx = []
        self.newlines_idx = []

    def find_non_sentences(self):
        '''
        Basic function to identify whether the content of one list within the sents_list is a sentence (in the
        grammatical sense) by calculating the ratio between alphabetic and non-alphabetic characters.
        The assumption is that if the content of the list contains at least twice as many alphabetic characters than
        non-alphabetic ones, it can be considered a sentence.
        Saves the index of any non-sentence in the non_sentences_idx list.
        '''
        for i,s in enumerate(self.sents_list):
            letters = 0
            non_letters = 0
            for token in s:
                for c in token:
                    if c.isalpha():
                        letters += 1
                    else:
                        non_letters += 1
            if letters == 0:
                letters = 1
            if non_letters/letters > 0.5:
                self.non_sentences_idx.append(i)

    def find_footers(self):
        '''
        Identifies footers or any other repeating lines that are probably not part of the continuous text.
        All sentences are compared to each other by pair; two sentences that have a similarity of 90% or higher on
        basis of character comparison are counted as repeating footers/headers/... The respective sentence index is
        saved in the Footer_idx list.
        '''
        idx = []
        for i,s in enumerate(self.sents_list):
            if not i in idx:
                join_s = "".join(s)
                for j,t in enumerate(self.sents_list):
                    if i < j:
                        if not j in idx:
                            join_t = "".join(t)
                            min_len = min(len(join_s),len(join_t))
                            sim = sum([1 if join_s[k] == join_t[k] else 0 for k in range(min_len)]) / min_len
                            if sim >= 0.9:
                                idx.extend([i,j])
        self.footer_idx = list(sorted(set(idx)))

    def fix_hyphenated(self):
        '''
        Identifies occurrences where words are hyphenated across linebreaks.
        Saves the indices of the first part and the second part of the word in the hyphen_idx list, along with the
        fixed word entry if that word can be found in the reference dictionary, or the two word parts connected by a
        hyphen if the word without hyphen cannot be found on the reference dictionary.
        One list entry is added for each sentence within sents_list; the entries of hyphen_ids that correspond to
        those sentences that do not contain any hyphenation across line breaks are left empty.
        '''
        for i,s in enumerate(self.sents_list):
            sent = []
            if i not in self.footer_idx:
                for idx,token in enumerate(s):
                    if token is "-" and 1 <= idx < len(s)-2:
                        if re.search("\w+",s[idx-1]) and re.search("\n",s[idx+1]) and re.search("\w+",s[idx+2]):
                            combined_word = s[idx-1]+s[idx+2]
                            if combined_word in self.dicts.fd.keys():
                                sent.append((idx-1,idx+2,combined_word))
                            else:
                                sent.append((idx-1,idx+2,s[idx-1]+s[idx]+s[idx+2]))
            self.hyphen_idx.append(sent)

    def fix_newlines_in_sentences(self):
        '''
        Finds all newlines within sentences and saves their indices in newlines_idx list.
        Skips lines if they are already included in the hyphen_idx list.
        '''
        for i,s in enumerate(self.sents_list):
            sent = []
            for idx,token in enumerate(s):
                check_hyphen = (self.hyphen_idx[i] is not [] and any([h[0] <= idx <= h[1] for h in self.hyphen_idx[i]]))
                if check_hyphen:
                    continue
                elif re.search("\n", token) and idx is not len(s) - 1:
                    sent.append((idx," "))
                elif re.search("\n{2,}",token) and idx is len(s) - 1:
                    sent.append((idx,"\n\n"))
            self.newlines_idx.append(sent)

    def analyse_all(self):
        self.find_non_sentences()
        self.find_footers()
        self.fix_hyphenated()
        self.fix_newlines_in_sentences()

    # def check_words(self):
    #     for s in self.sents_list:
    #         sent = []
    #         for i,entry in s:
    #             if any(c.isalpha() for c in entry):
    #                 if entry.lower() not in self.dicts.fd.keys() and entry.lower() not in self.dicts.cfd.keys():
    #                     sent.append((i,entry))
    #         self.defect_words.append(sent)
