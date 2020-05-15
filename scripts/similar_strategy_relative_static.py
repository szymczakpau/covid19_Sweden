import pandas as pd
import plotly.graph_objects as go
import plotly
plotly.io.orca.config.executable = '/home/paulina/miniconda3/bin/orca'

"""
Data comes from COVID-19 Data Repository by the Center for Systems Science and Engineering (CSSE)at Johns Hopkins University: 
https://github.com/CSSEGISandData/COVID-19/blob/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_global.csv
"""

def clean_data(df):
    df = df[df['Country/Region'].isin(['Sweden', 'Netherlands', 'Switzerland', 'Poland', 'United Kingdom'])]
    df = df[df.isnull().any(axis=1)]
    df = df.drop(['Province/State', 'Lat', 'Long'], axis=1)
    cols = [i for i in range(1, 9)]
    df.drop(df.columns[cols],axis=1,inplace=True)
    # Change format from wide to long for plotting
    df = df.rename(columns={'Country/Region': 'Country'})
    df = pd.melt(df, id_vars=['Country'], var_name='Date', value_name='Number')
    # Change data column for time series
    df['Date'] = df['Date'].astype('datetime64[ns]')
    return df

def make_relative(df):
    populations = {
        'Netherlands': 17.28,
        'Poland': 37.97,
        'Sweden': 10.23,
        'Switzerland': 8.57,
        'United Kingdom': 66.65,
    }
    new_df = df.copy()
    for country, number in populations.items():
        indexes = new_df[new_df['Country'] == country]['Number'].index.values
        new_df.iloc[indexes, 2] = new_df.iloc[indexes, 2].apply(lambda x: (int(x)/number))
    return new_df

if __name__ == "__main__":

    world_cases = pd.read_csv('../data/time_series_covid19_confirmed_global.csv')
    strategy_cases = clean_data(world_cases)
    strategy_cases_relative = make_relative(strategy_cases)
    strategy_cases_relative.to_csv('../data/similar_strategy_relative_cases_static.csv')

    # PLOTTING
    fig = go.Figure()

    countries = ['Sweden', 'Netherlands', 'Switzerland', 'Poland', 'United Kingdom']
    colors = ['#F75D28', '#7FB800', '#00A6ED', "#EAC435", "#0D2C54"]

    for name, color in zip(countries, colors):
        visibility = True

        fig.add_trace(go.Scatter(
            x=strategy_cases_relative[(strategy_cases_relative["Country"] == name)]['Date'],
            y=strategy_cases_relative[(strategy_cases_relative["Country"] == name)]["Number"],
            mode='lines',
            name=name,
            marker=dict(color=color),
            visible=visibility,



        )
        )

    fig.update_layout(
        width=1000,
        height=600,
        autosize=False,
        margin=dict(t=0, b=0, l=0, r=0),
        template='plotly_white',
        xaxis_title='Date',
        yaxis_title='Number of cases per 1M of inhabitants',
        title='Relative',
        font=dict(size=20)
    )

    fig.update_layout(showlegend=True)
    fig.write_image("../figures_static/similar_strategy_relative.pdf")
