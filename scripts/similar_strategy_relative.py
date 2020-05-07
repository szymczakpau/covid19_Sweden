import pandas as pd
import plotly.graph_objects as go

"""
Data comes from COVID-19 Data Repository by the Center for Systems Science and Engineering (CSSE)at Johns Hopkins University: 
https://github.com/CSSEGISandData/COVID-19/blob/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_global.csv
"""

if __name__ == "__main__":

    world = pd.read_csv('../data/time_series_covid19_confirmed_global.csv')
    similar_strategy = world[world['Country/Region'].isin(['Sweden', 'Netherlands', 'Switzerland', 'Poland', 'United Kingdom'])]
    # ABSOLUTE
    # Remove Provinces and Lat, Long
    similar_strategy = similar_strategy[similar_strategy.isnull().any(axis=1)]
    similar_strategy = similar_strategy.drop(['Province/State', 'Lat', 'Long'], axis=1)

    # Forward to first cases in Sweden and United Kingdom
    cols = [i for i in range(1, 40)]
    similar_strategy.drop(similar_strategy.columns[cols],axis=1,inplace=True)

    # Change format from wide to long for plotting
    similar_strategy_relative = pd.DataFrame.copy(similar_strategy, deep=True)
    similar_strategy_relative.iloc[0, 1:] = similar_strategy_relative.iloc[0, 1:].apply(
        lambda x: x / 17.28)  # Netherlands
    similar_strategy_relative.iloc[1, 1:] = similar_strategy_relative.iloc[2, 1:].apply(
        lambda x: x / 37.97)  # Poland
    similar_strategy_relative.iloc[2, 1:] = similar_strategy_relative.iloc[2, 1:].apply(
        lambda x: x / 10.23)  # Sweden
    similar_strategy_relative.iloc[3, 1:] = similar_strategy_relative.iloc[3, 1:].apply(
        lambda x: x / 8.57)  # Switzerland
    similar_strategy_relative.iloc[4, 1:] = similar_strategy_relative.iloc[4, 1:].apply(
        lambda x: x / 66.65)  # UK


    similar_strategy_relative = pd.melt(
        similar_strategy_relative,
        id_vars=['Country/Region'],
        var_name='Date',
        value_name='Number of cases'
    )

    # Change data column for time series
    similar_strategy_relative['Date'] = similar_strategy_relative['Date'].astype('datetime64[ns]')
    similar_strategy_relative.to_csv('../data/similar_strategy_relative_cases.csv')

    # Read test data
    tests = pd.read_csv('../data/full-list-total-tests-for-covid-19.csv')
    tests = tests[tests['Entity'].isin(['Sweden', 'Netherlands', 'Switzerland', 'Poland', 'United Kingdom'])]
    tests['Date'] = tests['Date'].astype('datetime64[ns]')
    tests = tests.reset_index()

    netherland_indexes = tests[tests['Entity'] == 'Netherlands']['Total tests'].index.values
    tests.iloc[netherland_indexes, 4] = tests.iloc[netherland_indexes, 4].apply(
        lambda x: x/17.28)  # Netherlands
    poland_indexes = tests[tests['Entity'] == 'Poland']['Total tests'].index.values
    tests.iloc[poland_indexes, 4] = tests.iloc[poland_indexes, 4].apply(
        lambda x: x/37.97)  # Poland
    switzerland_indexes = tests[tests['Entity'] == 'Switzerland']['Total tests'].index.values
    tests.iloc[switzerland_indexes, 4] = tests.iloc[switzerland_indexes, 4].apply(
        lambda x: x /8.57)  # Switzerland
    sweden_indexes = tests[tests['Entity'] == 'Sweden']['Total tests'].index.values
    tests.iloc[sweden_indexes, 4] = tests.iloc[sweden_indexes, 4].apply(
        lambda x: x/10.23)  # Sweden
    uk_indexes = tests[tests['Entity'] == 'United Kingdom']['Total tests'].index.values
    tests.iloc[uk_indexes, 4] = tests.iloc[uk_indexes, 4].apply(
        lambda x: x/66.65)  # UK

    tests.to_csv('../data/similar_strategy_relative_tests.csv')

    # Rename columns for plotting purposes
    similar_strategy_relative = similar_strategy_relative.rename(
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
        x=similar_strategy_relative[(similar_strategy_relative["Entity"] == "Netherlands")]['Date'],
        y=similar_strategy_relative[(similar_strategy_relative["Entity"] == "Netherlands")]["Number"],
        mode='lines',
        name="Netherlands",
        marker=dict(color="#7FB800"),
        visible='legendonly'
    )
    )

    fig.add_trace(go.Scatter(
        x=similar_strategy_relative[(similar_strategy_relative["Entity"] == "Poland")]['Date'],
        y=similar_strategy_relative[(similar_strategy_relative["Entity"] == "Poland")]["Number"],
        mode='lines',
        name="Poland",
        marker=dict(color="#EAC435"),
        visible='legendonly'
    )
    )

    fig.add_trace(go.Scatter(
        x=similar_strategy_relative[(similar_strategy_relative["Entity"] == "Sweden")]['Date'],
        y=similar_strategy_relative[(similar_strategy_relative["Entity"] == "Sweden")]["Number"],
        mode='lines',
        name="Sweden",
        line=dict(color="#F75D28"),
    )
    )

    fig.add_trace(go.Scatter(
        x=similar_strategy_relative[(similar_strategy_relative["Entity"] == "Switzerland")]['Date'],
        y=similar_strategy_relative[(similar_strategy_relative["Entity"] == "Switzerland")]["Number"],
        mode='lines',
        name="Switzerland",
        line=dict(color="#00A6ED"),
        visible='legendonly',
    )
    )

    fig.add_trace(go.Scatter(
        x=similar_strategy_relative[(similar_strategy_relative["Entity"] == "United Kingdom")]['Date'],
        y=similar_strategy_relative[(similar_strategy_relative["Entity"] == "United Kingdom")]["Number"],
        mode='lines',
        name="United Kingdom",
        marker=dict(color="#0D2C54"),
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
        yaxis_title='Number of cases per 1M of the population',
        title='Relative'
    )

    buttons = []

    for name, df, y_title in zip(
            ['Number of cases', 'Number of tests'],
            [similar_strategy_relative, tests],
            ['Number of cases per 1M of the population', 'Number of tests per 1M of the population']
    ):
        buttons.append(dict(method='update',
                            label=name,
                            visible=True,
                            args=[{'x': [
                                df[(df["Entity"] == "Netherlands")]['Date'],
                                df[(df["Entity"] == "Poland")]['Date'],
                                df[(df["Entity"] == "Sweden")]['Date'],
                                df[(df["Entity"] == "Switzerland")]['Date'],
                                df[(df["Entity"] == "United Kingdom")]['Date'],
                            ],
                                'y': [
                                    df[(df["Entity"] == "Netherlands")]['Number'],
                                    df[(df["Entity"] == "Poland")]['Number'],
                                    df[(df["Entity"] == "Sweden")]['Number'],
                                    df[(df["Entity"] == "Switzerland")]['Number'],
                                    df[(df["Entity"] == "United Kingdom")]['Number'],
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



    fig.write_html("../figures/similar_strategy_relative.html")
