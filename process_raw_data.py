"""A script to process book data. takes a csv file path as an CLI argument"""

import pandas as pd
import argparse


def read_raw_data(file_path) -> pd.DataFrame:
    """Reads raw book data from a file."""
    return pd.read_csv(file_path)


def get_db_connection(db_name: str):
    """Establishes a database connection."""
    import sqlite3
    conn = sqlite3.connect(db_name)
    return conn


def get_authors_df(conn) -> pd.DataFrame:
    """Fetches authors data from the database."""
    query = "SELECT * FROM authors"
    with conn.cursor() as cursor:
        authors_df = cursor.execute(query).fetchall()
    return pd.DataFrame(authors_df, columns=['id', 'name'])


def remove_unnecessary_columns(df: pd.DataFrame, columns_to_remove: list) -> pd.DataFrame:
    """Removes unnecessary columns from the DataFrame."""
    return df.drop(columns=columns_to_remove, errors='ignore')


def drop_empty_book_titles(df: pd.DataFrame) -> pd.DataFrame:
    """Drops rows with empty book titles."""
    return df[df['book_title'].notna() & (df['book_title'] != '')]


def drop_empty_author_names(df: pd.DataFrame) -> pd.DataFrame:
    """Drops rows with empty author names."""
    return df[df['author_name'].notna() & (df['author_name'] != '')]


def reformat_rating_column(df: pd.DataFrame) -> pd.DataFrame:
    """Reformats the rating column to be numeric."""
    df['Rating'] = pd.to_numeric(df['Rating'], errors='coerce')
    return df


def reformat_ratings_column(df: pd.DataFrame) -> pd.DataFrame:
    """Reformats the ratings_count column to be numeric."""
    df['Ratings'] = pd.to_numeric(df['Ratings'], errors='coerce')
    return df


def convert_data_types(df: pd.DataFrame) -> pd.DataFrame:
    """Converts data types year to integer rating to float, and ratings as an integer."""
    df['year'] = pd.to_numeric(df['year'], errors='coerce').astype('Int64')
    df['Rating'] = df['Rating'].astype('float')
    df['Ratings'] = df['Ratings'].astype('Int64')
    return df


def replace_authors_id_with_name(df: pd.DataFrame, authors_df: pd.DataFrame) -> pd.DataFrame:
    """merge the authors' names into the main dataframe based on author_id
    then drop the author_id column"""
    merged_df = df.merge(authors_df, left_on='author_id',
                         right_on='id', how='left')
    merged_df = merged_df.drop(columns=['author_id', 'id'])
    merged_df = merged_df.rename(columns={'name': 'author_name'})
    return merged_df


def rename_columns(df: pd.DataFrame) -> pd.DataFrame:
    """Renames columns book_title to title, year released to year, Rating to rating."""
    return df.rename(columns={
        'book_title': 'title',
        'year released': 'year',
        'Rating': 'rating'
    })


def reorder_columns(df: pd.DataFrame) -> pd.DataFrame:
    """Reorders columns to a preferred order."""
    preferred_order = ['title', 'author_name', 'year', 'rating', 'ratings']
    return df[preferred_order]


def clean_titles(df: pd.DataFrame) -> pd.DataFrame:
    """remove any information in parentheses from book titles"""
    df['title'] = df['title'].str.replace(r'\s*\(.*?\)\s*', '', regex=True)
    return df


def sort_dataframe(df: pd.DataFrame) -> pd.DataFrame:
    """sort by descending order of rating"""
    return df.sort_values(by='rating', ascending=False)


def process_raw_data(file_path: str) -> pd.DataFrame:
    """Processes raw book data from a CSV file and returns a cleaned DataFrame."""
    # Read raw data
    df = read_raw_data(file_path)
    # Establish database connection
    conn = get_db_connection('authors.db')
    # Fetch authors data
    authors_df = get_authors_df(conn)
    # Data cleaning steps
    df = remove_unnecessary_columns(
        df, ['index', 'unnamed: 0'])
    df = drop_empty_book_titles(df)
    df = drop_empty_author_names(df)
    df = reformat_rating_column(df)
    df = reformat_ratings_column(df)
    df = convert_data_types(df)
    df = replace_authors_id_with_name(df, authors_df)
    df = rename_columns(df)
    df = reorder_columns(df)
    df = clean_titles(df)
    df = sort_dataframe(df)
    return df


if __name__ == "__main__":
    print("Processing raw book data...")
    parser = argparse.ArgumentParser(
        description="Process raw book data from a CSV file.")
    parser.add_argument('file_path', type=str,
                        help='Path to the raw book data CSV file.')
    args = parser.parse_args()
    processed_df = process_raw_data(args.file_path)
    print("Processed DataFrame:")
