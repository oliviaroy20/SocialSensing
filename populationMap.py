import plotly
import plotly.graph_objs as go
import pandas as pd
from plotly.offline import init_notebook_mode
import plotly.graph_objs as go
plotly.offline.init_notebook_mode(connected=True)

df = pd.read_csv('USPopulation.csv', sep="\t")

totalPopulation = 0
for index, row in enumerate(df["Population"]):
	row = row.replace(',','')
	df.iloc[index, 1] = row
	totalPopulation += int(row)

print(totalPopulation)
df["Percent"] = df["Population"]

for index, row in enumerate(df["Population"]):
	percent = int(row)/totalPopulation
	df.iloc[index, 2]= percent

state_codes = {
    'District of Columbia' : 'dc','Mississippi': 'MS', 'Oklahoma': 'OK',
    'Delaware': 'DE', 'Minnesota': 'MN', 'Illinois': 'IL', 'Arkansas': 'AR',
    'New Mexico': 'NM', 'Indiana': 'IN', 'Maryland': 'MD', 'Louisiana': 'LA',
    'Idaho': 'ID', 'Wyoming': 'WY', 'Tennessee': 'TN', 'Arizona': 'AZ',
    'Iowa': 'IA', 'Michigan': 'MI', 'Kansas': 'KS', 'Utah': 'UT',
    'Virginia': 'VA', 'Oregon': 'OR', 'Connecticut': 'CT', 'Montana': 'MT',
    'California': 'CA', 'Massachusetts': 'MA', 'West Virginia': 'WV',
    'South Carolina': 'SC', 'New Hampshire': 'NH', 'Wisconsin': 'WI',
    'Vermont': 'VT', 'Georgia': 'GA', 'North Dakota': 'ND',
    'Pennsylvania': 'PA', 'Florida': 'FL', 'Alaska': 'AK', 'Kentucky': 'KY',
    'Hawaii': 'HI', 'Nebraska': 'NE', 'Missouri': 'MO', 'Ohio': 'OH',
    'Alabama': 'AL', 'Rhode Island': 'RI', 'South Dakota': 'SD',
    'Colorado': 'CO', 'New Jersey': 'NJ', 'Washington': 'WA',
    'North Carolina': 'NC', 'New York': 'NY', 'Texas': 'TX',
    'Nevada': 'NV', 'Maine': 'ME'}

df["StatesAbb"] = df["State"]
for index, row in enumerate(df["State"]):
	df.iloc[index, 3] = state_codes[row]

data = [go.Choropleth(
    colorscale = 'Greens',
    autocolorscale = False,
	reversescale = True,
    locations = df['StatesAbb'],
    z = df['Population'].astype(float),
    locationmode = 'USA-states',
    # text = df['Population'],
    marker = go.choropleth.Marker(
        line = go.choropleth.marker.Line(
            color = 'rgb(255,255,255)',
            width = 2
        )),
    colorbar = go.choropleth.ColorBar(
        title = "Population")
)]

layout = go.Layout(
    title = go.layout.Title(
        text = 'Population by State in 2017<br>(Hover for breakdown)'
    ),
    geo = go.layout.Geo(
        scope = 'usa',
        projection = go.layout.geo.Projection(type = 'albers usa'),
        showlakes = True,
        lakecolor = 'rgb(255, 255, 255)'),
)

fig = go.Figure(data = data, layout = layout)
plotly.offline.plot(fig)
