class Text:

    def __init__(self, path):
        '''
        opens the file at the given path as one string
        :param path: string path to file
        '''
        self.text = open(path, 'r', encoding='utf8').read()
