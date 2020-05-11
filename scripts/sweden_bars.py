import pandas as pd
import plotly.graph_objects as go

if __name__ == "__main__":

    sweden_cases = pd.read_excel('../data/Folkhalsomyndigheten_Covid19.xlsx', 'Antal per dag region')
    sweden_deaths = pd.read_excel('../data/Folkhalsomyndigheten_Covid19.xlsx', 'Antal avlidna per dag')
    sweden_cases = sweden_cases.iloc[:, 0:2]
    sweden_cases  = sweden_cases.rename(columns={'Statistikdatum': 'Date', 'Totalt_antal_fall': 'Number'})
    sweden_cases.to_csv('../data/sweden_bars_cases.csv')
    sweden_deaths = sweden_deaths.rename(columns={'Datum_avliden': 'Date', 'Antal_avlidna': 'Number'})
    sweden_deaths.to_csv('../data/sweden_bars_deaths.csv')

    # create figure
    fig = go.Figure()

    fig.add_trace(go.Bar(
        x=sweden_cases['Date'],
        y=sweden_cases['Number'],
        marker_color='#F75D28'

    )
    )

    fig.update_layout(
        width=480,
        height=500,
        autosize=False,
        margin=dict(t=0, b=0, l=0, r=0),
        template='plotly_white',
        xaxis_title='Date',
        yaxis_title='Daily new cases'
    )

    buttons = []

    for name, df, y_title in zip(
            ['Number of cases', 'Number of deaths'],
            [sweden_cases, sweden_deaths],
            ['Daily new cases', 'Daily confirmed deaths']
    ):
        buttons.append(dict(method='update',
                            label=name,
                            visible=True,
                            args=[
                                {'x': [df['Date']],
                                 'y': [df['Number']]},
                                {'yaxis': {'title': y_title}}
                            ],
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
        x=0.15,
        xanchor="left",
        y=1.1,
        yanchor="top"
    )

    fig.update_layout(showlegend=False, updatemenus=updatemenu)

    fig.update_layout(
        annotations=[
            dict(text="Category: ", showarrow=False,
                 x=0, y=1.06, xref="paper", yref="paper", align="left")
        ]
    )

    # fig.show()
    fig.write_html("../figures/sweden_bars.html")

