from nltk.stem import WordNetLemmatizer
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
import string
import nltk
import re

nltk.download('stopwords')
nltk.download('wordnet')
nltk.download('punkt')

lemmatizer = WordNetLemmatizer()


def preprocess(text, is_sw_remove=True):
    # Steps:
    # 1. lowercase
    # 2. Lammetize. (It does not stem. Try to preserve structure not to overwrap with potential acronym).
    # 3. Remove stop words.
    # 4. Remove punctuations.
    # 5. Remove character with the length size of 1.

    lowered = str.lower(text)
    lowered = re.sub(r"[^a-zA-Z0-9 ]", "", lowered)

    if is_sw_remove:
        stop_words = set(stopwords.words('english'))
    else:
        stop_words = set()

    word_tokens = word_tokenize(lowered)

    words = []
    for w in word_tokens:
        if w not in stop_words:
            if w not in string.punctuation:
                if len(w) > 1:
                    lemmatized = lemmatizer.lemmatize(w)
                    words.append(lemmatized)

    return words
