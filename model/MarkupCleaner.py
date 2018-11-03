from bs4 import BeautifulSoup
import re


class MarkupCleaner:
    '''
    Cleans the string input from HTML or XML mark-up if it has any.
    Finds continuous text within HTML or XML files and returns that text.
    '''
    def __init__(self, text, mark_up_type):
        '''
        Initialises the text and gets_parsed variables; sets the is_html and is_xml variables in accordance to the user
        input provided by mark_up_type and the content of the first 20 characters in the file.
        :param text: string that contains all content of the imported file
        :param mark_up_type: StringVar that provides the file type as indicated by the user
        '''
        self.text = text
        self.gets_parsed = False

        # check if user input is the same as actual file type
        if mark_up_type.get() == "0" or re.search("html",self.text[:20].lower()):
            self.is_html = True
        else:
            self.is_html = False

        if mark_up_type.get() == "1" or re.search("xml", self.text[:20].lower()):
            self.is_xml = True
        else:
            self.is_xml = False

    def check_to_parse(self):
        '''
        Checks if the text can be parsed as XML of HTML parse tree using BeautifulSoup.
        If it can be parsed, variable gets_parsed is set to True.
        '''
        if self.is_xml:
            try:
                self.soup = BeautifulSoup(self.text,'lxml')
                self.gets_parsed = True
            except:
                print("The text could not be parsed as XML. Other options will be tested.")
        elif self.is_html:
            try:
                self.soup = BeautifulSoup(self.text,'html.parser')
                self.gets_parsed = True
            except:
                print("The text could not be parsed as HTML. Other options will be tested.")
        else:
            try:
                self.soup = BeautifulSoup(self.text,'lxml')
                self.gets_parsed = True
            except:
                print("The text could not be parsed. It will be handled as a raw string instead of an HTML or XML tree.")

    def find_text(self):
        '''
        Identifies the continuous text within an HTML or XML parse tree. We expect the continuous text to be the sum
        of content of the nodes with the longest string content (in XML for example all content of all <p> tags)
        :return: string of continuous text
        '''
        # find all nodes that contain string content
        list_texts = [(d.name,d.string) for d in self.soup.descendants if d.string is not None and d.name is not None]
        # find the name of the tag that contains the longest string;
        max_tag = max([(len(str(s)),n)for (n,s) in list_texts])[1]
        # join all content from all nodes with the given name
        text = "\n".join([str(entry) for entry in self.soup.find(max_tag)])
        return text

    def process_parsing(self):
        '''
        processes the file parsing and markup cleaning steps
        :return: string of continuous text, either cleaned of markup or original text if no markup was detected.
        '''
        self.check_to_parse()
        if self.gets_parsed:
            return self.find_text()
        else:
            return self.text
