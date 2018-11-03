from bs4 import BeautifulSoup


class TextCleaner:

    def  __init__(self, markup_text, causes):
        self.text = markup_text
        self.causes = causes

    def parse_xml(self):
        self.soup = BeautifulSoup(self.text, 'html.parser')
        #print(self.soup)

    def process_cleaning(self):
        self.parse_xml()
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
