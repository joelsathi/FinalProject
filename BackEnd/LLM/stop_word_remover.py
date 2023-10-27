import nltk
nltk.download('stopwords')


from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

def prompt_without_stop_words(prompt):
    tokens = word_tokenize(prompt.lower())
    english_stopwords = stopwords.words('english')
    tokens_wo_stopwords = [t for t in tokens if t not in english_stopwords]
    return " ".join(tokens_wo_stopwords)