from bs4 import BeautifulSoup


class TextCleaner:
    '''
    Processes the cleaning steps indicated by the list of causes as defined by the user
    '''
    def  __init__(self, markup_text, causes):
        '''
        :param markup_text: text with XML-style mark-up according to the occurrences to be cleaned
        :param causes: dictionary of cause-value pairs
        '''
        self.text = markup_text
        self.causes = causes

    def process_cleaning(self):
        '''
        Parse the text as XML, then clean the <subst> nodes by replacing them with the content of the <add> node
        or the <del> node, depending on the values in the causes dictionary.
        "0" stands for cleaning, i.e. replace with <add>; "1" stands for dismiss changes, i.e. replace with <del>;
        anything else stands for keeping the markup as it is, therefore nothing gets deleted.
        :return:
        '''
        self.soup = BeautifulSoup(self.text, 'html.parser')
        for key,value in self.causes.items():
            if value.get() == "0":
                for sub in self.soup.find_all("subst", {'@cause': key}):
                    a = sub.find("add")
                    sub.replace_with(a.text)
            elif value.get() == "1":
                for sub in self.soup.find_all("subst", {'@cause': key}):
                    a = sub.find("del")
                    sub.replace_with(a.text)
        return str(self.soup)

    # def clear_hyphenation(self):
    #     for sub in self.soup.find_all("subst", {'@cause':'hyphenation'}):
    #         a = sub.find("add")
    #         sub.replace_with(a.text)
    #     print(self.soup)
    #
    # def clear_newlines(self):
    #     for sub in self.soup.find_all("subst", {"@cause":"newline"}):
    #         sub.decompose()
    #     print(self.soup)
    #
    # def clear_footers(self):
    #     for sub in self.soup.find_all("subst", {"@cause":"footer"}):
    #         sub.decompose()
    #     print(self.soup)
    #
    # def clear_non_sentences(self):
    #     s = self.soup
    #     for sub in s.find_all("subst", {"@cause":"non_sentence"}):
    #         sub.decompose()
    #     print(s)
    #     self.soup = s
    #
    # def clear_all(self):
    #     self.parse_xml()
    #     self.clear_hyphenation()
    #     self.clear_newlines()
    #     self.clear_footers()
    #     self.clear_non_sentences()
    #     return self.text
