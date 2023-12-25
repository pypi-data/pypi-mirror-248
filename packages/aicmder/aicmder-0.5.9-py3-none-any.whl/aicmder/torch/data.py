# src: https://github.com/facebookresearch/DrQA/blob/master/drqa/reader/data.py
import unicodedata
import numpy as np
import random
PAD = 0
UNK = 1
BOS = 2
EOS = 3

PAD_WORD = '<blank>'
UNK_WORD = '<unk>'
BOS_WORD = '<s>'
EOS_WORD = '</s>'


class Vocabulary(object):
    def __init__(self, no_special_token=False):
        if no_special_token:
            self.tok2ind = {PAD_WORD: PAD,
                            UNK_WORD: UNK}
            self.ind2tok = {PAD: PAD_WORD,
                            UNK: UNK_WORD}
        else:
            self.tok2ind = {PAD_WORD: PAD,
                            UNK_WORD: UNK,
                            BOS_WORD: BOS,
                            EOS_WORD: EOS}
            self.ind2tok = {PAD: PAD_WORD,
                            UNK: UNK_WORD,
                            BOS: BOS_WORD,
                            EOS: EOS_WORD}

    @staticmethod
    def normalize(token):
        return unicodedata.normalize('NFD', token)

    def __len__(self):
        return len(self.tok2ind)

    def __iter__(self):
        return iter(self.tok2ind)

    def __contains__(self, key):
        if type(key) == int:
            return key in self.ind2tok
        elif type(key) == str:
            return self.normalize(key) in self.tok2ind

    def __getitem__(self, key):
        if type(key) == int:
            return self.ind2tok.get(key, UNK_WORD)
        elif type(key) == str:
            return self.tok2ind.get(self.normalize(key),
                                    self.tok2ind.get(UNK_WORD))
        else:
            raise RuntimeError('Invalid key type.')

    def __setitem__(self, key, item):
        if type(key) == int and type(item) == str:
            self.ind2tok[key] = item
        elif type(key) == str and type(item) == int:
            self.tok2ind[key] = item
        else:
            raise RuntimeError('Invalid (key, item) types.')

    def add(self, token):
        token = self.normalize(token)
        if token not in self.tok2ind:
            index = len(self.tok2ind)
            self.tok2ind[token] = index
            self.ind2tok[index] = token

    def add_tokens(self, token_list):
        assert isinstance(token_list, list)
        for token in token_list:
            self.add(token)

    def tokens(self):
        """Get dictionary tokens.
        Return all the words indexed by this dictionary, except for special
        tokens.
        """
        tokens = [k for k in self.tok2ind.keys()
                  if k not in {PAD_WORD, UNK_WORD}]
        return tokens

    def remove(self, key):
        if key in self.tok2ind:
            ind = self.tok2ind[key]
            del self.tok2ind[key]
            del self.ind2tok[ind]
            return True
        return False


class UnicodeCharsVocabulary(Vocabulary):
    """Vocabulary containing character-level and word level information.
    Has a word vocabulary that is used to lookup word ids and
    a character id that is used to map words to arrays of character ids.
    The character ids are defined by ord(c) for c in word.encode('utf-8')
    This limits the total number of possible char ids to 256.
    To this we add 5 additional special ids: begin sentence, end sentence,
        begin word, end word and padding.
    """

    def __init__(self, words, max_word_length,
                 no_special_token):
        super(UnicodeCharsVocabulary, self).__init__(no_special_token)
        self._max_word_length = max_word_length

        # char ids 0-255 come from utf-8 encoding bytes
        # assign 256-300 to special chars
        self.bow_char = 256  # <begin word>
        self.eow_char = 257  # <end word>
        self.pad_char = 258  # <padding>

        for w in words:
            self.add(w)
        num_words = len(self.ind2tok)

        self._word_char_ids = np.zeros([num_words, max_word_length],
                                       dtype=np.int32)

        for i, word in self.ind2tok.items():
            self._word_char_ids[i] = self._convert_word_to_char_ids(word)

    @property
    def word_char_ids(self):
        return self._word_char_ids

    @property
    def max_word_length(self):
        return self._max_word_length

    def _convert_word_to_char_ids(self, word):
        code = np.zeros([self.max_word_length], dtype=np.int32)
        code[:] = self.pad_char

        word_encoded = word.encode('utf-8', 'ignore')[:(self.max_word_length - 2)]
        code[0] = self.bow_char
        for k, chr_id in enumerate(word_encoded, start=1):
            code[k] = chr_id
        code[k + 1] = self.eow_char

        return code

    def word_to_char_ids(self, word):
        if word in self.tok2ind:
            return self._word_char_ids[self.tok2ind[word]]
        else:
            return self._convert_word_to_char_ids(word)

    def encode_chars(self, sentence, split=True):
        '''
        Encode the sentence as a white space delimited string of tokens.
        '''
        if split:
            chars_ids = [self.word_to_char_ids(cur_word)
                         for cur_word in sentence.split()]
        else:
            chars_ids = [self.word_to_char_ids(cur_word)
                         for cur_word in sentence]

        return chars_ids


class RandomGenerator:
    """Randomly draw among {1, ..., n} according to n sampling weights."""

    def __init__(self, sampling_weights):
        """Defined in :numref:`sec_word2vec_data`"""
        # Exclude
        self.population = list(range(1, len(sampling_weights) + 1))
        self.sampling_weights = sampling_weights
        self.candidates = []
        self.i = 0

    def draw(self):
        if self.i == len(self.candidates):
            # Cache `k` random sampling results
            self.candidates = random.choices(
                self.population, self.sampling_weights, k=10000)
            self.i = 0
        self.i += 1
        return self.candidates[self.i - 1]


def get_negatives(all_contexts, vocab, counter, K):
    """Return noise words in negative sampling.

    Defined in :numref:`sec_word2vec_data`"""
    # Sampling weights for words with indices 1, 2, ... (index 0 is the
    # excluded unknown token) in the vocabulary
    sampling_weights = [counter[vocab.to_tokens(i)]**0.75
                        for i in range(1, len(vocab))]
    all_negatives, generator = [], RandomGenerator(sampling_weights)
    for contexts in all_contexts:
        negatives = []
        while len(negatives) < len(contexts) * K:
            neg = generator.draw()
            # Noise words cannot be context words
            if neg not in contexts:
                negatives.append(neg)
        all_negatives.append(negatives)
    return all_negatives


reshape = lambda x, *args, **kwargs: x.reshape(*args, **kwargs)


def batchify(data):
    """Return a minibatch of examples for skip-gram with negative sampling.

    Defined in :numref:`sec_word2vec_data`"""
    max_len = max(len(c) + len(n) for _, c, n in data)
    centers, contexts_negatives, masks, labels = [], [], [], []
    for center, context, negative in data:
        cur_len = len(context) + len(negative)
        centers += [center]
        contexts_negatives += [context + negative + [0] * (max_len - cur_len)]
        masks += [[1] * cur_len + [0] * (max_len - cur_len)]
        labels += [[1] * len(context) + [0] * (max_len - len(context))]
    return (reshape(torch.tensor(centers), (-1, 1)), torch.tensor(
        contexts_negatives), torch.tensor(masks), torch.tensor(labels))


if __name__ == "__main__":
    words = set()
    words.add("hello")
    words.add("world")

    dictioanry = UnicodeCharsVocabulary(words, 30, True)
    print(dictioanry, len(dictioanry))
