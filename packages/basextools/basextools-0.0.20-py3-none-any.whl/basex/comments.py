### comments
###
### BASEX module for comments handling

from os import path
import pandas as pd
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
from collections import defaultdict
from unidecode import unidecode
from nltk.tokenize import word_tokenize
import re
import spacy
import pathlib

# Caminho para o diretório do modelo
model_directory = path.join(path.dirname(__file__), 'models/pt_core_news_md/')

nlp = spacy.load(model_directory)

def extract_top_comments(comment_list,
                         n_comments=5, EMBEDDINGS_MODEL=None):
    """
    Extracts the n most representative comments from a list, filters out similar comments, and masks sensitive information.

    Args:
        comment_list: list of comments.
        n_comments: number of comments to extract (default is 5).
        EMBEDDINGS_MODEL: model to be used, default
            is SentenceTransformer('rufimelo/bert-large-portuguese-cased-sts')
        NOT IMPLEMENTED:
            technique: the technique to be used to guide the ranking system.
            entity_types: list of entity types to mask (default is ["PERSON"]).
            mask_char: character to use for masking sensitive information (default is "X").

    Returns:
        A list of the n most representative comments with sensitive information masked.
    """

    if EMBEDDINGS_MODEL is None:
        EMBEDDINGS_MODEL = SentenceTransformer('rufimelo/bert-large-portuguese-cased-sts')
    embeddings = EMBEDDINGS_MODEL.encode(comment_list)

    # computes similarity between comments using cosine distance
    cos_similarities = cosine_similarity(embeddings)
    cos_sim_df = pd.DataFrame(cos_similarities) * 100
    # cos_sim_df.columns = comment_list
    # cos_sim_df.index = comment_list
    top_comments = cos_sim_df.mean().sort_values(ascending=False)
    top_comments_ids_list = list(top_comments.index)

    similarity_therhold = 70
    # similarity threshold based on quantile (increase diversity as always filter out some comments)
    # similarity_therhold = top_comments.quantile(0.9)

    # filter out similar comments
    final_comments_ids = []
    for i, comment_id in enumerate(top_comments_ids_list):

        if i == 0:
            final_comments_ids.append(comment_id)
        else:
            # stop looking
            if len(final_comments_ids) == n_comments:
                break

            comment_similarities = cos_sim_df.loc[comment_id][final_comments_ids].values
            if (comment_similarities > similarity_therhold).any():
                continue
            else:
                final_comments_ids.append(comment_id)

    # retrieving the comments
    final_comments = [comment_list[c] for c in final_comments_ids]

    return final_comments

def _process_text(input_text, show_processed_text=False):
    """

    Parameters
    ----------
    input_text: a complete sentence

    Returns the same sentence in lower case and without punctuation
    -------

    """
    # Step 1 - Convert to lowercase
    text_lower = input_text.lower()

    # Step 2 - Remove punctuation and numbers
    text_without_punctuation_and_numbers = re.sub(r'[^a-zA-Z\sÀ-ÿ]', '', text_lower)
    if show_processed_text:
        print(text_without_punctuation_and_numbers)
    return text_without_punctuation_and_numbers

def _word_counter(words):
    """

    Parameters
    ----------
    words: a list with words

    Returns dictionary with counting the repetition of words
    -------

    """
    word_count = defaultdict(int)

    for word in words:
        word_count[word] += 1

    return word_count

def word_count_model(sentence):
    """
    Receive the complete sentence, send it for treatment, separate it into words and count the repetitions

    Parameters
    ----------
    sentence

    Returns dictionary with counting the repetition of words
    -------

    """
    # Step 1 - Function to process the sentence
    sentence = _process_text(sentence)

    # Step 2 - Split the text into words
    words = word_tokenize(sentence)

    # Step 3 - Count word occurrences
    word_count = _word_counter(words)

    return word_count

def _find_lemma(word):
    """

    Parameters
    ----------
    word: a word to find the lemma

    returns the lemma of the received word
    -------

    """
    doc = nlp(word)
    return doc[0].lemma_


def group_lemma(word_dict):
    """

    Parameters
    ----------
    word_dict: a dictionary with words as keys and repetitions as values

    Returns: groups the dictionary keys by lemma and adds their repetitions
    -------

    """

    grouped_dict = defaultdict(int)

    for word, count in word_dict.items():
        lemma = _find_lemma(word)
        grouped_dict[lemma] += count

    return grouped_dict


def get_main_topics(df, sig_filter=False):
    '''
    Get main topics using a statistical approach

    Parameters
    ----------
    df (pd.DataFrame): the saati dataframe as it is returned by the interface module
    sig_filter (bool, default false): if true, return only statistical significative results

    Returns
    -------
    top_pos_scores (pd.DataFrame): statistical information about the positive sentiment of the topics
    top_neg_scores (pd.DataFrame): statistical information about the negative sentiment of the topics
    '''

    Z_THERSHOLD = 1.645  # threshold for 95% confidence
    df = df.copy()

    # The lists in the 'categories' column need to be joined into comma-separated strings
    df['topics'] = df['topics'].apply(lambda row: ','.join(row.tolist()) if isinstance(row, np.ndarray) else '')

    # Now, let's create dummy variables
    dummies = df['topics'].str.get_dummies(sep=',')

    # Topics to be removed cause they have very strong intrinsic sentiments
    questions_to_remove = ['Motivação e Engajamento',
                           'Gargalos',
                           'Questionamentos e Críticas',
                           'Atrito',
                           'Discordância']

    dummies = dummies.drop([q for q in questions_to_remove if q in dummies.columns], axis=1)

    # Finally, let's join the dummies DataFrame with the original one
    dft = pd.concat([df, dummies], axis=1).drop('topics', axis=1)

    base_rates = dft['sentiment'].value_counts(normalize=True)
    for sent in ['Positivo', 'Negativo', 'Neutro']:
        if not sent in base_rates:
            base_rates[sent] = 0.0

    total_counts = dft.drop(['sentiment', 'intention', 'text', 'user_id'], axis=1).sum()

    dft_reduced = dft.drop(['intention', 'text', 'user_id'], axis=1)
    dft_pos = (dft_reduced[dft_reduced['sentiment'] == 'Positivo']).drop('sentiment', axis=1)
    dft_neg = (dft_reduced[dft_reduced['sentiment'] == 'Negativo']).drop('sentiment', axis=1)

    pos_counts = dft_pos.sum()
    pos_rates = pos_counts / total_counts

    neg_counts = dft_neg.sum()
    neg_rates = neg_counts / total_counts

    pos_scores = []
    neg_scores = []
    for topic in pos_counts.index:
        # if 'Positivo' in base_rates:
        if pos_rates[topic] <= base_rates['Positivo']:
            continue
        z_pos = compare_favorability_with_bench(pos_rates[topic], total_counts[topic], base_rates['Positivo'])
        if z_pos:
            pos_scores.append({
                'topic': topic,
                'proportion': pos_rates[topic],
                'n_answers': total_counts[topic],
                'z': z_pos
            })

    for topic in neg_counts.index:
        # if 'Negativo' in base_rates:
        if neg_rates[topic] <= base_rates['Negativo']:
            continue
        z_neg = compare_favorability_with_bench(neg_rates[topic], total_counts[topic], base_rates['Negativo'])
        if z_neg:
            neg_scores.append({
                'topic': topic,
                'proportion': neg_rates[topic],
                'n_answers': total_counts[topic],
                'z': z_neg
            })

    top_pos_scores = pd.DataFrame(pos_scores)
    top_neg_scores = pd.DataFrame(neg_scores)

    if top_pos_scores.empty:
        top_pos_scores = np.nan
    else:
        top_pos_scores = top_pos_scores.sort_values('z', ascending=False)
        if sig_filter:
            top_pos_scores = top_pos_scores[top_pos_scores['z'] >= Z_THERSHOLD]

    if top_neg_scores.empty:
        top_neg_scores = np.nan
    else:
        top_neg_scores = pd.DataFrame(neg_scores).sort_values('z', ascending=False)
        if sig_filter:
            top_neg_scores = top_neg_scores[top_neg_scores['z'] >= Z_THERSHOLD]

    return top_pos_scores, top_neg_scores