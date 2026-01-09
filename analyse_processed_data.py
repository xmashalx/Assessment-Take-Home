"""A script to analyse book data."""

import pandas as pd
import altair as alt


def add_decade_column(df: pd.DataFrame) -> pd.DataFrame:
    """Adds a decade column based on the year column."""
    df['decade'] = (df['year'] // 10) * 10
    return df


def create_decade_pie_chart(df: pd.DataFrame):
    """Creates a pie chart showing the distribution of books released by decade."""
    decade_counts = df.groupby('decade').size().reset_index(name='count')

    pie_chart = alt.Chart(decade_counts).mark_arc().encode(
        theta=alt.Theta('count:Q', stack=True),
        color=alt.Color('decade:N', legend=alt.Legend(title='Decade')),
        tooltip=['decade:N', 'count:Q']
    ).properties(
        title='Proportion of Romance Novels released by Decade',
        width=400,
        height=400
    )
    pie_chart.save('visuals/decade_releases.png')


def create_top_authors_bar_chart(df: pd.DataFrame):
    """Creates a bar chart showing the top 10 authors by number of books."""
    author_ratings = df.groupby('author_name')[
        'ratings'].sum().reset_index()

    top_10_authors = author_ratings.nlargest(10, 'ratings')
    chart = alt.Chart(top_10_authors).mark_bar().encode(
        x=alt.X('ratings:Q', title='Total Number of Ratings'),
        y=alt.Y('author_name:N', sort='-x', title='Author'),
        tooltip=['author_name:N', 'ratings:Q']
    ).properties(
        title='Top 10 Most-Rated Authors',
        width=600,
        height=400
    )

    chart.save('visuals/top_authors.png')


def create_trends_in_release_count_over_time_chart(df: pd.DataFrame):
    """Creates a line chart showing trends in book release counts over time."""

    yearly_counts = books.groupby('year').size().reset_index(name='count')

    chart = alt.Chart(yearly_counts).mark_line(
        color='steelblue',
        strokeWidth=3,
        point=alt.OverlayMarkDef(color='steelblue', size=50)
    ).encode(
        x=alt.X('year:O',
                title='Year',
                axis=alt.Axis(labelAngle=-45)),
        y=alt.Y('count:Q',
                title='Number of Romance Books Published'),
        tooltip=[
            alt.Tooltip('year:O', title='Year'),
            alt.Tooltip('count:Q', title='Romance Books Published')
        ]
    ).properties(
        title={
            "text": "Romance Books Published Over Time",
            "fontSize": 18,
            "font": "Arial",
            "fontWeight": "bold"
        },
        width=700,
        height=400
    ).configure_view(
        strokeWidth=0
    ).configure_axis(
        grid=True,
        gridOpacity=0.3
    )

    chart.save('visuals/release_trends_over_time.png')


if __name__ == "__main__":
    books = pd.read_csv('data/processed_data.csv')
    books = add_decade_column(books)
    create_decade_pie_chart(books)
    create_top_authors_bar_chart(books)
    create_trends_in_release_count_over_time_chart(books)
