from nltk import pos_tag
from nltk.corpus import stopwords, wordnet
from nltk.tokenize import RegexpTokenizer
from nltk.stem import WordNetLemmatizer

def get_wordnet_pos(treebank_tag):
    '''
    Translate nltk POS to wordnet tags

    Provided by Flatiron School
    '''
    if treebank_tag.startswith('J'):
        return wordnet.ADJ
    elif treebank_tag.startswith('V'):
        return wordnet.VERB
    elif treebank_tag.startswith('N'):
        return wordnet.NOUN
    elif treebank_tag.startswith('R'):
        return wordnet.ADV
    else:
        return wordnet.NOUN

def preprocess(
    texts,sw=None,tokenizer=None,lang='english',
    ret_tokens=False
    ):
    """_summary_

    Args:
        texts (list of strings):
            Text items in an array-like to loop over
            and clean.
        sw (list of strings, optional):
            List of stop words. If this is not defined,
            default stop words are used from the
            provided language. Defaults to None.
        tokenizer (nltk tokenizer object, optional):
            nltk tokenizer object to use when
            tokenizing. Defaults to None.
        lang (str, optional):
            Language to use when getting default stop
            words from nltk. Defaults to 'english'.
        ret_tokens (bool, optional):
            Whether or not to return tokens as well as
            the full strings.

    Returns:
        list:
            Returns a pre-processed list of texts as
            provided and prepared for vectorizing.
        tuple:
            If ret_tokens is true, returns a tuple of
            lists, the first being the full strings
            processed as specified and the second being
            the tokens used in the associated lists.
    """
    if sw==None:
        sw = stopwords.words(lang)
    if tokenizer==None:
        # tokenizer = RegexpTokenizer(r"(\{?\+?[a-zA-Z0-9]+(?:’[a-z0-9]+)?\}?)")
        tokenizer = RegexpTokenizer(r"(\{?[a-zA-Z]+(?:’[a-z]+)?\}?)|([+-]?\d\/[+-]?\d)|(\{\d\d?\})")
    # make texts lowercase
    texts = [str(phrase).lower() for phrase in texts]
    tokens = [tokenizer.tokenize(str(doc)) for doc in texts]
    
    clean_texts = []
    for token in tokens:
        # append an array of tokens to clean_texts if they are not in stop words
        nsw = [token_ for token_ in token if token_ not in sw]
        clean_texts.append(nsw)
    lemmer = WordNetLemmatizer()
    full_cleaned = []
    full_tokens  = []
    for text in clean_texts:
        tagged = pos_tag(text)
        wordnet_tag = [(word[0], get_wordnet_pos(word[1])) for word in tagged]
        token_list_ = [lemmer.lemmatize(word[0],word[1]) for word in wordnet_tag]
        full_cleaned.append(
            ' '.join(token_list_))
        full_tokens.append(token_list_)
    if ret_tokens==True:
        return (full_cleaned, full_tokens)
    return full_cleaned