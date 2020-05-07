import pandas as pd
import plotly.graph_objects as go

"""
Data comes from COVID-19 Data Repository by the Center for Systems Science and Engineering (CSSE)at Johns Hopkins University: 
https://github.com/CSSEGISandData/COVID-19/blob/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_global.csv
"""

if __name__ == "__main__":

    world = pd.read_csv('../data/time_series_covid19_confirmed_global.csv')
    similar_country = world[world['Country/Region'].isin(['Sweden', 'Denmark', 'Finland', 'Norway'])]

    # Remove Provinces and Lat, Long
    similar_country = similar_country[similar_country.isnull().any(axis=1)]
    similar_country = similar_country.drop(['Province/State', 'Lat', 'Long'], axis=1)

    # Forward to first cases in Sweden and United Kingdom
    cols = [i for i in range(1, 40)]
    similar_country.drop(similar_country.columns[cols],axis=1,inplace=True)

    # Change format from wide to long for plotting
    similar_country_long = pd.melt(
        similar_country,
        id_vars=['Country/Region'],
        var_name='Date',
        value_name='Number of cases'
    )

    # Change data column for time series
    similar_country_long['Date'] = similar_country_long['Date'].astype('datetime64[ns]')
    similar_country_long.to_csv('../data/similar_country_absolute_cases.csv')

    # Read test data
    tests = pd.read_csv('../data/full-list-total-tests-for-covid-19.csv')
    tests = tests[tests['Entity'].isin(['Sweden', 'Denmark', 'Finland', 'Norway'])]
    tests['Date'] = tests['Date'].astype('datetime64[ns]')
    similar_country_long.to_csv('../data/similar_country_absolute_tests.csv')

    # Rename columns for plotting purposes
    similar_country_long = similar_country_long.rename(
        columns={
            'Country/Region': 'Entity',
            'Number of cases': 'Number'
        }
    )
    tests = tests.rename(
        columns={
        'Total tests': 'Number'
        }
    )

    # PLOTTING
    # create figure
    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x=similar_country_long[(similar_country_long["Entity"] == "Sweden")]['Date'],
        y=similar_country_long[(similar_country_long["Entity"] == "Sweden")]["Number"],
        mode='lines',
        name="Sweden",
        marker=dict(color="#F75D28"),
    )
    )

    fig.add_trace(go.Scatter(
        x=similar_country_long[(similar_country_long["Entity"] == "Denmark")]['Date'],
        y=similar_country_long[(similar_country_long["Entity"] == "Denmark")]["Number"],
        mode='lines',
        name="Denmark",
        marker=dict(color="#EAC435"),
        visible='legendonly'
    )
    )

    fig.add_trace(go.Scatter(
        x=similar_country_long[(similar_country_long["Entity"] == "Norway")]['Date'],
        y=similar_country_long[(similar_country_long["Entity"] == "Norway")]["Number"],
        mode='lines',
        name="Norway",
        marker=dict(color="#0D2C54"),
        visible='legendonly'
    )
    )

    fig.add_trace(go.Scatter(
        x=similar_country_long[(similar_country_long["Entity"] == "Finland")]['Date'],
        y=similar_country_long[(similar_country_long["Entity"] == "Finland")]["Number"],
        mode='lines',
        name="Finland",
        marker=dict(color="#00A6ED"),
        visible='legendonly'
    )
    )


    fig.update_layout(
        width=580,
        height=500,
        autosize=False,
        margin=dict(t=0, b=0, l=0, r=0),
        template='plotly_white',
        xaxis_title='Date',
        yaxis_title='Number of cases',
        title='Absolute'
    )

    buttons = []

    for name, df, y_title in zip(
            ['Number of cases', 'Total tests'],
            [similar_country_long, tests],
            ['Number of cases', 'Total tests']
    ):
        buttons.append(dict(method='update',
                            label=name,
                            visible=True,
                            args=[{'x': [
                                df[(df["Entity"] == "Sweden")]['Date'],
                                df[(df["Entity"] == "Denmark")]['Date'],
                                df[(df["Entity"] == "Norway")]['Date'],
                                df[(df["Entity"] == "Finland")]['Date'],
                            ],
                                'y': [
                                    df[(df["Entity"] == "Sweden")]['Number'],
                                    df[(df["Entity"] == "Denmark")]['Number'],
                                    df[(df["Entity"] == "Norway")]['Number'],
                                    df[(df["Entity"] == "Finland")]['Number'],
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


    fig.write_html("../figures/similar_country_absolute.html")
