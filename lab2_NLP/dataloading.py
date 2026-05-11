from torch.utils.data import Dataset
from tqdm import tqdm
import numpy as np
from nltk.tokenize import TweetTokenizer
import string
from nltk.corpus import stopwords
from nltk import word_tokenize

DATASET = "MR"  # options: "MR", "Semeval2017A"

class SentenceDataset(Dataset):
    """
    Our custom PyTorch Dataset, for preparing strings of text (sentences)
    What we have to do is to implement the 2 abstract methods:

        - __len__(self): in order to let the DataLoader know the size
            of our dataset and to perform batching, shuffling and so on...

        - __getitem__(self, index): we have to return the properly
            processed data-item from our dataset with a given index
    """

    def __init__(self, X, y, word2idx):
        """
        In the initialization of the dataset we will have to assign the
        input values to the corresponding class attributes
        and preprocess the text samples

        -Store all meaningful arguments to the constructor here for debugging
         and for usage in other methods
        -Do most of the heavy-lifting like preprocessing the dataset here


        Args:
            X (list): List of training samples
            y (list): List of training labels
            word2idx (dict): a dictionary which maps words to indexes
        """

        self.data = X
        # Tokenize the sentences using nltk tokenizer
        self.tokenized_data = [word_tokenize(sentence) for sentence in self.data]
        self.labels = y
        self.word2idx = word2idx

 

    
    def __len__(self):
        """
        Must return the length of the dataset, so the dataloader can know
        how to split it into batches

        Returns:
            (int): the length of the dataset
        """

        return len(self.data)

    def __getitem__(self, index):
        """
        Returns the _transformed_ item from the dataset

        Args:
            index (int):

        Returns:
            (tuple):
                * example (ndarray): vector representation of a training example
                * label (int): the class label
                * length (int): the length (tokens) of the sentence

        Examples:
            For an `index` where:
            ::
                self.data[index] = ['this', 'is', 'really', 'simple']
                self.target[index] = "neutral"

            the function will have to return something like:
            ::
                example = [  533  3908  1387   649   0     0     0     0]
                label = 1
                length = 4
        """

        example = self.tokenized_data[index]
        max_length = 10
        # map tokens to ids according to word2idx
        example = [self.word2idx.get(token, self.word2idx['<unk>']) for token in example]
        label = self.labels[index]
        length = len(example) 
        
        # zero padding using the maximum length from initialization
        # or truncation in case a larger example is found
        if length < max_length:
            example += [0] * (max_length - length)
        else:
            example = example[:max_length]

            # Now the length is safe
        length = min(len(self.tokenized_data[index]), max_length)

        label = self.labels[index]
        return np.array(example), label, length

        
        

        # return example, label, length
