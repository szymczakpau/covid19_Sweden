import pandas as pd
import plotly.graph_objects as go
import plotly
plotly.io.orca.config.executable = '/home/paulina/miniconda3/bin/orca'

if __name__ == "__main__":

    sweden_deaths = pd.read_excel('../data/Folkhalsomyndigheten_Covid19.xlsx', 'Antal avlidna per dag')
    sweden_deaths = sweden_deaths.rename(columns={'Datum_avliden': 'Date', 'Antal_avlidna': 'Number'})
    sweden_deaths.to_csv('../data/sweden_bars_deaths_static.csv')

    # create figure
    fig = go.Figure()

    fig.add_trace(go.Bar(
        x=sweden_deaths['Date'],
        y=sweden_deaths['Number'],
        marker_color='#F75D28'

    )
    )

    fig.update_layout(
        width=1000,
        height=500,
        autosize=False,
        margin=dict(t=0, b=0, l=0, r=0),
        template='plotly_white',
        xaxis_title='Date',
        yaxis_title='Daily new cases',
        font=dict(size=20),
        xaxis_showgrid=False,
        yaxis_showgrid=False,
    )

    # fig.show()
    fig.write_image("../figures_static/sweden_bars.pdf")

