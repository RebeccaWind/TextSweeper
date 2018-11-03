class FileWriter:
    def __init__(self,filename, text):
        '''
        Writes the text to a file.
        :param filename: path and filename where the text should be saved
        :param text:  text to be saved
        '''
        self.out_filename = filename
        with open(self.out_filename, "w") as output:
            output.write(text)
