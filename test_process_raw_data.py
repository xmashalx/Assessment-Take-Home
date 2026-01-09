"""test suite for process_raw_data.py"""

import pandas as pd
import sqlite3
import pytest
from process_raw_data import (
    remove_unnecessary_columns,
    drop_empty_book_titles,
    drop_empty_authors,
    reformat_rating_column,
    reformat_ratings_column,
    convert_data_types,
    rename_columns,
    reorder_columns,
    clean_titles,
    sort_dataframe,
    replace_authors_id_with_name
)


@pytest.fixture
def sample_data():
    data = {
        'book_title': ['Book A', '', 'Book C', 'Book D (Special Edition)'],
        'author_id': [1, 2, None, 4],
        'Rating': ['4,5', '3,8', '5,0', '2,7'],
        'ratings': ['1`000', '500`', '2`500', '300`'],
        'Year released': ['2001', '1999', '2010', '2005'],
        'index': [0, 1, 2, 3],
        'Unnamed: 0': [0, 1, 2, 3]
    }
    return pd.DataFrame(data)


@pytest.fixture
def authors_data():
    data = {
        'id': [1, 2, 3, 4],
        'name': ['Author A', 'Author B', 'Author C', 'Author D']
    }
    return pd.DataFrame(data)


@pytest.fixture
def merged_data(sample_data, authors_data):
    merged_df = replace_authors_id_with_name(sample_data.copy(), authors_data)
    merged_df = rename_columns(merged_df)
    return merged_df


def test_remove_unnecessary_columns(sample_data):
    cleaned_df = remove_unnecessary_columns(
        sample_data.copy(), ['index', 'Unnamed: 0'])
    assert 'index' not in cleaned_df.columns
    assert 'Unnamed: 0' not in cleaned_df.columns


def test_drop_empty_book_titles(sample_data):
    cleaned_df = drop_empty_book_titles(sample_data.copy())
    assert cleaned_df['book_title'].isnull().sum() == 0
    assert (cleaned_df['book_title'] == '').sum() == 0


def test_drop_empty_authors(sample_data):
    cleaned_df = drop_empty_authors(sample_data.copy())
    assert cleaned_df['author_id'].isnull().sum() == 0


def test_reformat_rating_column(sample_data):
    cleaned_df = reformat_rating_column(sample_data.copy())
    assert cleaned_df['Rating'].dtype == float
    assert all(cleaned_df['Rating'] == pd.to_numeric(
        cleaned_df['Rating'], errors='coerce'))


def test_reformat_ratings_column(sample_data):
    cleaned_df = reformat_ratings_column(sample_data.copy())
    assert pd.api.types.is_numeric_dtype(cleaned_df['ratings'])
    assert all(cleaned_df['ratings'] == pd.to_numeric(
        cleaned_df['ratings'], errors='coerce'))


def test_convert_data_types(sample_data):
    df = reformat_rating_column(sample_data.copy())
    df = reformat_ratings_column(df)
    cleaned_df = convert_data_types(df)
    assert cleaned_df['Year released'].dtype.name == 'Int64'
    assert cleaned_df['Rating'].dtype == float
    assert cleaned_df['ratings'].dtype.name == 'Int64'


def test_rename_columns(sample_data):
    renamed_df = rename_columns(sample_data.copy())
    assert 'title' in renamed_df.columns
    assert 'year' in renamed_df.columns
    assert 'rating' in renamed_df.columns


def test_reorder_columns(merged_data):
    reordered_df = reorder_columns(merged_data)
    expected_order = ['title', 'author_name', 'year', 'rating', 'ratings']
    assert list(reordered_df.columns) == expected_order


def test_clean_titles(sample_data):
    df = rename_columns(sample_data.copy())
    cleaned = clean_titles(df)
    assert all(
        '(' not in title and ')' not in title for title in cleaned['title'])


def test_sort_dataframe(sample_data):
    df = reformat_rating_column(sample_data.copy())
    df = rename_columns(df)
    sorted_df = sort_dataframe(df)
    expected_order = ['Book C', 'Book A', '', 'Book D (Special Edition)']
    assert list(sorted_df['title']) == expected_order


def test_replace_authors_id_with_name(sample_data, authors_data):
    merged_df = replace_authors_id_with_name(sample_data.copy(), authors_data)
    assert 'author_name' in merged_df.columns
    assert 'author_id' not in merged_df.columns
    assert all(name in authors_data['name'].values or pd.isnull(name)
               for name in merged_df['author_name'])
