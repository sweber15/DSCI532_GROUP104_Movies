import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output
import pandas as pd
import sqlalchemy
import altair as alt
import vega_datasets

app = dash.Dash(__name__, assets_folder='assets')
server = app.server
app.title = 'Dash app with pure Altair HTML'

movie_df = pd.read_csv('https://raw.githubusercontent.com/UBC-MDS/DSCI532_GROUP104_Movies/master/data/clean/movies_clean_df.csv', index_col = 0)
genres = movie_df.Major_Genre.unique()
directors = movie_df.Director.unique()



def make_plot_1(genre="Action", director="James Cameron"):

    def get_top_director(genre_1="Action"):
        """
        Finds the number of movies of the most productive directors in the selected genre
        """
        mdfg = movie_df.groupby('Major_Genre')
        return (mdfg.get_group(genre_1)
                .groupby('Director')
                .count()
                .sort_values(by = 'Title', ascending = False)
                .head(30)
                .reset_index()
                .iloc[:, :2]
                .rename(columns = {'Title': 'Count'}))

    def get_top_df(chosen_genre="Action"):
        """
        Finds movie information from the most productive directors in the selected genre
        """
        top_director = get_top_director(genre)
        top_director['Major_Genre'] = chosen_genre
        return pd.merge(movie_df, 
                    top_director, 
                    how = "inner", 
                    on = ['Major_Genre', 'Director'])
    
    df_genre = get_top_df(genre)
    df_director = df_genre[(df_genre['Director'] == director)]

    # Create a plot of the Displacement and the Horsepower of the cars dataset
    
    
    chart = alt.Chart(df_director).mark_circle().encode(
                alt.X("Year:O"),
                alt.Y("IMDB_Rating:Q", axis=alt.Axis(title="Mark"), scale=alt.Scale(zero=False)),
                tooltip = ['Title', 'Major_Genre', 'Director', 'IMDB_Rating']
            ).properties(title='Rating',
                        width=500, height=350).interactive()

    return chart

def make_plot_2(genre="Action", director="James Cameron"):

    def get_top_director(genre_1="Action"):
        """
        Finds the number of movies of the most productive directors in the selected genre
        """

        mdfg = movie_df.groupby('Major_Genre')
        return (mdfg.get_group(genre_1)
                .groupby('Director')
                .count()
                .sort_values(by = 'Title', ascending = False)
                .head(30)
                .reset_index()
                .iloc[:, :2]
                .rename(columns = {'Title': 'Count'}))

    def get_top_df(chosen_genre="Action"):
        """
        Finds movie information from the most productive directors in the selected genre
        """
  
        top_director = get_top_director(genre)
        top_director['Major_Genre'] = chosen_genre
        return pd.merge(movie_df, 
                    top_director, 
                    how = "inner", 
                    on = ['Major_Genre', 'Director'])
    
    df_genre = get_top_df(genre)
    df_genre['profit'] = (df_genre['Worldwide_Gross'] - df_genre['Production_Budget'])/1000000
    df_director = df_genre[(df_genre['Director'] == director)]

    # Create a plot of the Displacement and the Horsepower of the cars dataset
    
    
    chart = alt.Chart(df_director).mark_circle().encode(
                alt.X("Year:O"),
                alt.Y("profit:Q", scale=alt.Scale(zero=False), axis=alt.Axis(title="Profit (M USD)")),
                tooltip = ['Title', 'Major_Genre', 'Director', 'IMDB_Rating']
            ).properties(title='Profit',
                        width=500, height=350).interactive()

    return chart

app.layout = html.Div([
    html.Iframe(
        sandbox='allow-scripts',
        id='plot1',
        height='470',
        width='655',
        style={'border-width': '0'},
        ################ The magic happens here
        srcDoc=make_plot_1().to_html()
        ################ The magic happens here
        ),
        ############### Plot 2 ###########
        html.Iframe(
        sandbox='allow-scripts',
        id='plot2',
        height='470',
        width='655',
        style={'border-width': '0'},
        ################ The magic happens here
        srcDoc=make_plot_2().to_html()
        ################ The magic happens here       
    ),

    html.Div([

        html.Div([
            dcc.Dropdown(
        id='genre',
        options=[{'label': i, 'value': i} for i in genres],
        value='Action',
        style=dict(width='45%', verticalAlign="middle"),
        multi=False,
        searchable=True
        ),
        ]),
    
        html.Div([
            dcc.Dropdown(
                id='director',
                options=[{'label': i, 'value': i} for i in directors],
                value='James Cameron',
                style=dict(width='45%',
                    verticalAlign="middle"),
                multi=False,
                searchable=True
        ),
        ])
    ])

    
        
])


@app.callback(
    dash.dependencies.Output('plot1', 'srcDoc'),
    [dash.dependencies.Input('genre', 'value'),
    dash.dependencies.Input('director', 'value')])
def update_plot(genre_value,
                director_value):
    """
    Takes in the genre and director and calls make_plot to update the plot
    """
    updated_chart = make_plot_1(genre_value, director_value).to_html()
    return updated_chart


@app.callback(
    dash.dependencies.Output('plot2', 'srcDoc'),
    [dash.dependencies.Input('genre', 'value'),
    dash.dependencies.Input('director', 'value')])
def update_plot_2(genre_value,
                director_value):
    """
    Takes in the genre and director and calls make_plot to update the plot
    """
    updated_chart_2 = make_plot_2(genre_value, director_value).to_html()
    return updated_chart_2



if __name__ == '__main__':
    app.run_server(debug=True)
