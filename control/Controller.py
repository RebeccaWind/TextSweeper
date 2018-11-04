import tkinter as tk
from tkinter.messagebox import showerror
from model import Text
from model import Dicts
from model import Markup
from model import MarkupCleaner as MC
from model import TextSplitter as TS
from model import TextAnalyser as TA
from model import TextCleaner as TC
from model import FileWriter as FW
from view import MainWindow
import os


class Controller():
    '''
    The controller class manages the exchange of information between the model and the view.
    Any process within these two packages and within the program is executed by the controller.
    '''
    def __init__(self):
        self.dicts = None
        self.filename = None
        self.raw_text = None
        self.text = None
        self.splitter = None
        self.orig_sents = None
        self.analyser = None
        self.mark_up_type = None
        self.markup = None
        self.output_text = None

    def start(self):
        '''
        This function initialises the TK interface, sets the window size and starts the interface display.
        '''
        root = tk.Tk()
        root.geometry("1024x576")
        self.app = MainWindow.Window(controller=self, master=root)
        self.app.mainloop()

    def load_dicts(self):
        '''
        Loads the reference dictionaries. Currently, only the default dictionaries are available.
        '''
        self.dicts = Dicts.Dicts(f_dist='default', c_f_d='default')

    def start_processing(self):
        '''
        Starts the text processing step.
        Gets the filename and the type of mark-up from the interface so they are available for the processing functions.
        '''
        self.filename = self.app.searchbox.get()
        self.mark_up_type = self.app.mark_up_type
        self.try_process_file()
        if self.markup and self.markup.xml_output:
            self.app.init_clean_up_step(self.markup.xml_output)

    def try_process_file(self):
        '''
        Checks if file at the file path provided by the user can be opened.
        If no, shows error message. If yes, proceeds with processing the file.
        '''
        if not self.filename:
            showerror("Open Source File", "No file selected")
            return

        elif self.filename:
            try:
                # raw_text is one string that contains all the text in the file.
                self.raw_text = Text.Text(self.filename).text
                self.process_file()
            except:
                showerror("Open Source File", "Failed to read file\n'%s'" % self.filename)

    def process_file(self):
        '''
        Initialises objects of the different processing classes.
        Processes the text.
        '''
        self.text = MC.MarkupCleaner(self.raw_text, self.mark_up_type).process_parsing()
        self.splitter = TS.TextSplitter(self.text)
        self.orig_sents = self.splitter.split_text()
        self.analyser = TA.TextAnalyser(self.orig_sents, self.dicts)
        self.analyser.analyse_all()
        self.markup = Markup.Markup(self.analyser)
        self.markup.markup_all()

    def process_clean_up(self, causes):
        '''
        Clean the text according to the user input regarding which causes should be cleaned
        :param causes: dictionary of cause-action-pairs, where actions are given in form of a tk StringVar "0", "1" or "2"
        '''
        self.cleaner = TC.TextCleaner(self.markup.xml_output, causes)
        self.output_text = self.cleaner.process_cleaning()
        # Once the cleaning is done, the interface shows the cleaned text in the text window.
        self.app.show_cleaned_text(self.output_text)

    def write_to_file(self, output_filename):
        '''
        Passes the filename indicated by the user to the FileWriter in order to save the cleaned text.
        :param output_filename: String that contains the full path of where to save the output text.
        '''
        FW.FileWriter(output_filename,self.output_text)

if __name__ == "__main__":
    my_controller = Controller()
    my_controller.start()
