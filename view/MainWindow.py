import tkinter as tk
from tkinter import *
from tkinter.filedialog import askopenfilename
from tkinter.filedialog import asksaveasfile
from tkinter.scrolledtext import ScrolledText


class Window(Frame):
    '''
    This class forms the main window of the TextSweeper user interface.
    '''

    def __init__(self, controller, master=None):
        '''
        :param controller: receives the current controller object on call by the controller
        :param master: master is None if not otherwise specified
        '''
        Frame.__init__(self, master)
        self.controller = controller
        self.master = master
        #call init_window() to show the initial ui window
        self.init_start_window()

    def init_start_window(self):
        # set the title of the master widget
        self.master.title("TextSweeper")
        # allow the widget to expand to the full size of the root window
        self.pack(fill=BOTH, expand=1)
        # add a vertical padding of 10px to the first row
        self.rowconfigure(0, pad=10)
        # add a vertical padding 3px to the other rows
        for x in range(7):
            self.rowconfigure(x + 1, pad=3)
        # initialise text label with welcome message
        self.start_label = tk.Label(self,text = 'Welcome to TextSweeper!\nPress "Start" to load the default dictionaries and get started.')
        self.start_label.config(font=("Times", 12))
        self.start_label.grid(row=0, column=0, columnspan=6)
        # create a button instance
        # once the start button is pressed, the function load_dicts() is called
        self.start_button = Button(self, text="Start", command=self.load_dicts)
        # placing the button on my window
        self.start_button.grid(row=2, column=2, columnspan=2)

    def load_dicts(self):
        '''
        loads the specified or predefined reference dictionaries
        updates the ui window according to the loading progress
        '''
        # remove the start button from the ui
        self.start_button.destroy()
        # set a new text to the text label
        self.start_label.config(text="Please wait till dictionaries have loaded...")
        self.start_label.update()
        # call load_dicts() from the controller class
        self.controller.load_dicts()
        # once the dictionaries are loaded, show new message in the text label
        self.start_label.config(text="Dictionaries loaded. Ready to start.")
        # initialise the text processing selection buttons by calling init_load_button()
        self.init_load_button()

    def init_load_button(self):
        self.file_label = tk.Label(self,text='Please select the file to be processed:')
        self.file_label.config(font=("Times", 11))
        self.file_label.grid(row=1, column=0, columnspan=6)

        self.searchbox = tk.Entry(self)
        self.searchbox.grid(row=2, column=1, columnspan=3)

        self.browse_button = Button(self, text="Browse", command=self.select_file, width=10)
        self.browse_button.grid(row=2, column=4)

        self.gridframe = tk.Frame(self)
        options = ["html","xml","no markup","unknown"]
        Label(self.gridframe, text="mark-up type:", font=("Times", 11)).pack(side=LEFT)
        # needs to be class variable because otherwise radio buttons will not work properly
        self.mark_up_type = StringVar()
        self.mark_up_type.set("0")
        for i, o in enumerate(options):
            Radiobutton(self.gridframe, text=o, variable=self.mark_up_type, value=str(i)).pack(side=LEFT)
        self.gridframe.grid(row=3, column=1, columnspan=4)

        self.process_button = tk.Button(self, text="Process file", command=self.controller.start_processing)
        self.process_button.grid(row=4, column=0, columnspan=6)

        self.reset_button = tk.Button(self, text="Reset", command=self.reset)
        self.reset_button.grid(row=5, column=0, columnspan=6)

    def select_file(self):
        f_n = askopenfilename(title="Select a file:",filetypes=(("Text files","*.txt"),("HTML files","*.html;*.htm"),("XML files",".xml")))
        self.searchbox.delete(0, 'end')
        self.searchbox.focus_set()
        self.searchbox.selection_range(0, tk.END)
        self.searchbox.insert(0, f_n)

    def init_clean_up_step(self, text):
        # remove existing elements
        self.searchbox.destroy()
        self.browse_button.destroy()
        self.process_button.destroy()
        self.reset_button.destroy()
        self.gridframe.destroy()

        # update and add new ones
        self.start_label.config(text="You can see the processed text on the left")
        self.start_label.update()

        self.file_label.config(text="Please choose from the clean up settings on the right and start the clean up")
        self.file_label.update()

        self.text_out = ScrolledText(self, wrap='word')
        self.text_out.grid(row=2, column=0, rowspan=7, columnspan=3)

        # define radiobutton groups
        causes = ["hyphenation","newline","footer","non_sentence"]
        options = ["clean","discard","keep markup"]
        cause_vars = []
        self.variables = {}
        for c in range(len(causes)):
            cause_vars.append(StringVar())

        self.gridframe_list = []
        for x in range(len(causes)):
            cause_vars[x].set("0")
            gridframe = tk.Frame(self)
            Label(gridframe, text=causes[x], font=("Courier", 12)).pack(side=LEFT)
            for i,o in enumerate(options):
                Radiobutton(gridframe, text=o, variable=cause_vars[x], value=str(i)).pack(side=LEFT)
            gridframe.grid(row=x + 2, column=3, columnspan=1)
            self.variables[causes[x]] = cause_vars[x]
            self.gridframe_list.append(gridframe)

        # set the submit button
        self.clean_up_button = Button(self, text="Clean up", command=self.controller_clean_up)
        self.clean_up_button.grid(row=8, column=3)

        self.display_text(text)

    def show_cleaned_text(self,output_text):
        self.gridframe.destroy()
        self.clean_up_button.destroy()
        for gridframe in self.gridframe_list:
            gridframe.destroy()

        self.start_label.config(text="Result")
        self.start_label.update()

        self.file_label.config(text="This is your cleaned text.")
        self.file_label.update()

        self.save_button = Button(self,text = "save text to file", command=self.controller_save)
        self.save_button.grid(row=8, column=3)

        self.text_out.delete('1.0',END)
        self.display_text(output_text)

    def display_text(self, text):
        # do the displaying here

        # define you tags
        self.text_out.tag_config("add", foreground="blue")
        self.text_out.tag_config("del", foreground="red")
        self.text_out.tag_config("hyphenation", background="light green")
        self.text_out.tag_config("newline", background="light blue")
        self.text_out.tag_config("footer", background="light yellow")
        self.text_out.tag_config("non_sentence", background="light pink")

        # list of all tags
        tags_list = ["add", "del", "subst"]
        cause_list = ["hyphenation", "newline", "footer", "non_sentence"]

        active_causes = []
        active_tags = []
        while text:
            # find the first html-tag
            index = text.find("<")
            # if there is none display the rest of the text
            if index == -1:
                self.text_out.insert(END, text, active_tags)
                text = ""
            else:
                # display the text in front of the html-tag with the currently active style-tags
                # and remove it from the text
                self.text_out.insert(END, text[0:index], active_tags)
                text = text[index:]

                # get the whole html-tag and remove it from the text as well
                close_index = text.find(">")
                tag_text = text[0:close_index + 1]
                text = text[close_index + 1:]

                # check which tag we found
                found_tag = ""
                for tag in tags_list:
                    if tag_text.find(tag) > 0:
                        found_tag = tag

                # if we found a substitution find out which
                if found_tag == "subst":
                    subst = ""
                    for cause in cause_list:
                        if tag_text.find(cause) > 0:
                            subst = cause
                    if subst:
                        found_tag = subst
                        active_causes.append(subst)

                    # if there was no cause to be found it is a closing tag,
                    # so we get the last found substitution and remove it
                    else:
                        found_tag = active_causes.pop()

                # add or delete style-tags respectively
                if tag_text.find("/") > 0:
                    active_tags.remove(found_tag)
                else:
                    active_tags.append(found_tag)

        # show the text
        self.text_out.see("1.0")

    def reset(self):
        self.controller.filename = None
        self.controller.raw_text = None
        self.controller.text = None
        self.controller.checker = None
        self.controller.orig_sents = None
        self.controller.cleaner = None
        self.searchbox.delete(0, 'end')

    def controller_clean_up(self):
        self.controller.process_clean_up(self.variables)

    def controller_save(self):
        output_filename = asksaveasfile(mode='w', defaultextension=".txt")
        if output_filename is None:  #TODO # asksaveasfile return `None` if dialog closed with "cancel".
            return
        else:
            self.controller.write_to_file(output_filename.name)
