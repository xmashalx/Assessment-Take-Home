"""load in romance book data and produce a png of keywords frequency bar chart"""

import pandas as pd
import altair as alt

if __name__ == "__main__":
    books = pd.read_csv('data/processed_data.csv')
