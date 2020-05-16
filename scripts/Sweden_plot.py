from urllib.request import urlopen
import json
import pandas as pd
import plotly.offline as offline

data_xls = pd.read_excel('../data/Folkhalsomyndigheten_Covid19.xlsx', 'Antal per dag region', index_col=1)
data_xls.to_csv('../data/Sweden_covid.csv', encoding='utf-8')
df_sweden = pd.read_csv('../data/Sweden_covid.csv')

for region in df_sweden.drop(["Statistikdatum"], axis = 1).columns:
    df_sweden[region] = df_sweden[region].cumsum()

with urlopen('https://raw.githubusercontent.com/codeforamerica/click_that_hood/master/public/data/sweden-counties.geojson') as response:
    counties = json.load(response)

sweden_counties = []
for x in range(len(counties['features'])):
    sweden_counties.append(counties['features'][x]['properties']['name'])

data_slider = []

scl = [[0.0, '#ffffff'],[0.2, '#ff9999'],[0.4, '#ff4d4d'],        [0.6, '#ff1a1a'],[0.8, '#cc0000'],[1.0, '#4d0000']] # reds

for date in df_sweden["Statistikdatum"].unique():
    
    sweden_one_date = df_sweden[df_sweden["Statistikdatum"] == date].drop(["Statistikdatum", "Totalt_antal_fall"], axis = 1).T
    
    new_df = pd.DataFrame({"county": sweden_one_date.index,
                           "infected": sweden_one_date.T.values.tolist()[0]})
    
    new_df.loc[new_df["county"] == "Jämtland_Härjedalen", "county"] = "Jämtland"
    new_df.loc[new_df["county"] == "Sörmland", "county"] = "Södermanland"
    new_df.loc[new_df["county"] == "Västra_Götaland", "county"] = "Västra Götaland"
    
    data_one_date = dict(
                        type='choropleth', 
                        geojson = counties, 
                        colorscale = scl, 
                        locations = new_df["county"],
                        featureidkey = 'properties.name',
                        z=new_df["infected"],
                        locationmode='geojson-id',
                        text = new_df["county"],
                        zmin = 0,
                        zmax = 8100,
        
                        marker = dict(
                            # for the lines separating states
                            line = dict (color = 'rgb(0,0,0)', width = 0.5) 
                        ),
                        colorbar = dict(title = "Number of infected people") 
                        )

    data_slider.append(data_one_date)  # I add the dictionary to the list of dictionaries for the slider


steps = []

for i in range(len(data_slider)):
    step = dict(method='restyle',
                args=['visible', [False] * len(data_slider)],
                label= "Day {}".format(i))
    step['args'][1][i] = True
    steps.append(step)


##  I create the 'sliders' object from the 'steps' 

sliders = [dict(active=0, steps=steps, ticklen = 10)]

layout = dict(
    width = 580,
    height = 500, 
    hovermode = "closest",
    geo=dict(scope='europe',
             showlakes = True, 
             lakecolor = 'rgb(73, 216, 230)',
             lataxis = {"range": [55.5, 70]}, 
             lonaxis = {"range": [11, 24.0]}, 
             showland = False,
             countrycolor = 'white'
            ),
    sliders=sliders,
    margin=dict(l=20, r=0, t=0, b=100),

)

fig = dict(data=data_slider, layout=layout)

# plotly.offline.iplot(fig)

offline.plot(fig, auto_open=False, image_width=580, image_height=500, 
              filename='../figures_html/sweden_covid.html', validate=True)
