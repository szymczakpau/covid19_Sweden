import pandas as pd
import plotly.graph_objects as go

"""
Data comes from COVID-19 Data Repository by the Center for Systems Science and Engineering (CSSE)at Johns Hopkins University: 
https://github.com/CSSEGISandData/COVID-19/blob/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_global.csv
"""

def clean_data(df):
    df = df[df['Country/Region'].isin(['Sweden', 'Denmark', 'Finland', 'Norway'])]
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

if __name__ == "__main__":

    world_cases = pd.read_csv('../data/time_series_covid19_confirmed_global.csv')
    world_deaths = pd.read_csv('../data/time_series_covid19_deaths_global.csv')
    country_deaths = clean_data(world_deaths)
    country_cases = clean_data(world_cases)
    country_deaths.to_csv('../data/similar_country_absolute_deaths.csv')
    country_cases.to_csv('../data/similar_country_absolute_cases.csv')

    tests = pd.read_csv('../data/full-list-total-tests-for-covid-19.csv')
    tests = tests.drop(['Code'], axis=1)
    tests = tests.rename(columns={'Entity': 'Country', 'Total tests': 'Number'})
    tests = tests[tests['Country'].isin(['Sweden', 'Denmark', 'Finland', 'Norway'])]
    tests = tests.reset_index(drop=True)
    tests['Date'] = tests['Date'].astype('datetime64[ns]')
    tests.to_csv('../data/similar_country_absolute_tests.csv')

    # PLOTTING
    fig = go.Figure()

    countries = ['Sweden', 'Denmark', 'Norway', 'Finland']
    colors = ['#F75D28', '#EAC435', '#0D2C54', "#00A6ED"]

    for name, color in zip(countries, colors):
        visibility = 'legendonly'
        if name == 'Sweden':
            visibility = True

        fig.add_trace(go.Scatter(
            x=country_cases[(country_cases["Country"] == name)]['Date'],
            y=country_cases[(country_cases["Country"] == name)]["Number"],
            mode='lines',
            name=name,
            marker=dict(color=color),
            visible=visibility

        )
        )

    fig.update_layout(
        width=580,
        height=500,
        autosize=False,
        margin=dict(t=0, b=0, l=0, r=0),
        template='plotly_white',
        xaxis_title='Date',
        yaxis_title='Cumulative number of cases',
        title='Absolute'
    )

    buttons = []

    for name, df, y_title in zip(
            ['Cases', 'Deaths', 'Tests'],
            [country_cases, country_deaths, tests],
            ['Cumulative number of cases', 'Cumulative number of deaths', 'Cumulative number of tests']
    ):
        buttons.append(dict(method='update',
                            label=name,
                            visible=True,
                            args=[{'x': [
                                df[(df["Country"] == "Sweden")]['Date'],
                                df[(df["Country"] == "Denmark")]['Date'],
                                df[(df["Country"] == "Norway")]['Date'],
                                df[(df["Country"] == "Finland")]['Date'],
                            ],
                                'y': [
                                    df[(df["Country"] == "Sweden")]['Number'],
                                    df[(df["Country"] == "Denmark")]['Number'],
                                    df[(df["Country"] == "Norway")]['Number'],
                                    df[(df["Country"] == "Finland")]['Number'],
                                ]
                            },
                                {
                                    'yaxis': {'title': y_title}
                                }],
                            )
                       )

    updatemenu = []
    your_menu = dict()
    updatemenu.append(your_menu)

    updatemenu[0] = dict(
        buttons=buttons,
        direction="down",
        pad={"r": 10, "t": 10},
        showactive=True,
        x=0.40,
        xanchor="left",
        y=1.2,
        yanchor="top"
    )

    fig.update_layout(showlegend=True, updatemenus=updatemenu)

    fig.update_layout(
        annotations=[
            dict(text="Y axis:", showarrow=False,
                 x=0.25, y=1.15, xref="paper", yref="paper", align="left")
        ]
    )

    fig.write_html("../figures_html/similar_country_absolute.html")
