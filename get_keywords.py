"""load in romance book data and produce a png of keywords frequency bar chart"""

import pandas as pd
import altair as alt


def get_all_words(books: pd.DataFrame) -> list:
    """extract all the words in book titles from the book dataframe"""
    all_words = []
    for title in books['title']:
        words = title.split()
        all_words.extend(words)
    return all_words


def filter_stop_words(words: list) -> list:
    """filter out common stop words from a list of words"""
    stop_words = ['the', 'and', 'of', 'a', 'to', 'in', 'is', 'it', 'that', 'part',
                  'for', 'on', 'with', 'as', 'by', 'at', 'is', 'an', 'be',
                  'this', 'from', 'or', 'are', 'but', 'not', 'his', 'her',
                  'its', 'he', 'she', 'they', 'you', 'we', 'my', 'your', 'their',
                  'all', 'some', 'no', 'if', 'when', 'what', 'which', 'who',
                  'so', 'about', 'into', 'than', 'then', 'there', 'i', 'me',
                  'do', 'does', 'did', 'have', 'has', 'had', 'one', 'two', 'three', 'didn\'t',
                  'can', 'could', 'would', 'should', 'will', 'just', 'more', '&', 'after', 'other', 'before', 'volume']
    filtered_words = [word.lower()
                      for word in words if word.lower() not in stop_words]
    return filtered_words


def get_word_frequencies(words: list) -> pd.DataFrame:
    """get the frequency of each word in a list of words"""
    word_series = pd.Series(words)
    word_counts = word_series.value_counts().reset_index()
    word_counts.columns = ['word', 'frequency']
    return word_counts


def plot_word_frequencies(word_counts: pd.DataFrame, top_n: int = 20):
    """plot the top N word frequencies as a bar chart and save as png"""
    top_words = word_counts.head(top_n)
    chart = alt.Chart(top_words).mark_bar().encode(
        x=alt.X('frequency:Q', title='Frequency'),
        y=alt.Y('word:N', sort='-x', title='Word')
    ).properties(
        title=f'Top {top_n} Keywords in Romance Book Titles',
        width=600,
        height=400
    )
    chart.save('visuals/top_keywords.png')


if __name__ == "__main__":
    books = pd.read_csv('data/processed_data.csv')
    all_words = get_all_words(books)
    filtered_words = filter_stop_words(all_words)
    word_counts = get_word_frequencies(filtered_words)
    plot_word_frequencies(word_counts, top_n=20)
