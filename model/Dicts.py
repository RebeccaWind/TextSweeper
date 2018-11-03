import pickle
import os

class Dicts:
    '''
    Makes the reference dictionaried in form of an NLTK.FreqDist and an NLTK.ConditionalFreqDist available to the program.
    The dictionaries need to be ready beforehand and exist in a pickle-version of the respective NLTK objects.
    '''
    def __init__(self, f_dist, c_f_d):
        '''
        Opens the reference dictionaries ate the given filenames.
        Currently only opens the default dictionaries.
        :param f_dist: path to FreqDist pickle file
        :param c_f_d: path to ConditionalFreqDist pickle file
        '''
        if f_dist == 'default':
            self.fd = pickle.load(open(os.path.join(os.path.split(os.path.dirname(__file__))[0], 'resources', 'wiki_new_fd.pkl'), 'rb'))
        else:
            self.fd = pickle.load(open(f_dist, 'rb'))

        if c_f_d == 'default':
            self.cfd = pickle.load(open(os.path.join(os.path.split(os.path.dirname(__file__))[0], 'resources', 'wiki_new_cfd.pkl'), 'rb'))
        else:
            self.cfd = pickle.load(open(c_f_d, 'rb'))

