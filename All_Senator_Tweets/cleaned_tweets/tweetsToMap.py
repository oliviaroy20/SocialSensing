import pandas as pd
import numpy as np
import plotly
import plotly.graph_objs as go
from plotly.offline import init_notebook_mode
import plotly.graph_objs as go
plotly.offline.init_notebook_mode(connected=True)

file = open ("../../Senators.csv", "r")
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

d = ['dc', 'MS', 'OK','DE', 'MN', 'IL', 'AR',
	'NM', 'IN', 'MD', 'LA','ID', 'WY', 'TN', 'AZ','IA', 'MI', 'KS', 'UT',
    'VA',  'OR', 'CT', 'MT','CA','MA', 'WV','SC', 'NH', 'WI','VT',  'GA', 'ND',
    'PA', 'FL', 'AK', 'KY', 'HI', 'NE','MO', 'OH', 'AL', 'RI', 'SD',
    'CO', 'NJ', 'WA', 'NC', 'NY', 'TX', 'NV', 'ME']
s = [0] * 51

# nay=["SenatorCollins", "SenBobCorker", "TomCotton", "LindseyGraham", "SenDeanHeller", "SenMikeLee", "JerryMoran", "LisaMurkowski", "RandPaul", "SenateMajLdr"]
nay=["RandPaul", "SenateMajLdr"]
state_data = pd.DataFrame({'States': d, 'Tweets': s})
for line in file:
		line = line.strip().split(';')
		state = state_codes[line[0]]
		if line[-1] in nay:
			continue
		senator_num_Tweets = sum(1 for line in open(line[2]+"_cleaned.csv"))
		current_tweets = state_data.loc[state_data['States']==state, "Tweets"].values[0]
		if current_tweets:
			state_data.loc[state_data['States']==state, "Tweets"] = current_tweets +senator_num_Tweets
		else:
			state_data.loc[state_data['States']==state, "Tweets"] =  senator_num_Tweets


data = [go.Choropleth(
    colorscale = 'Greens',
    autocolorscale = False,
	reversescale = True,
    locations = state_data['States'],
    z = state_data['Tweets'].astype(float),
    locationmode = 'USA-states',
    # text = state_data['Tweets'],
    marker = go.choropleth.Marker(
        line = go.choropleth.marker.Line(
            color = 'rgb(255,255,255)',
            width = 2
        )),
    colorbar = go.choropleth.ColorBar(
        title = "Tweets")
)]

layout = go.Layout(
    title = go.layout.Title(
        text = 'Tweets by State to Senator in July 2017 about Obamacare/Healthcare<br>Without KY Senators<br>(Hover for breakdown)'
    ),
    geo = go.layout.Geo(
        scope = 'usa',
        projection = go.layout.geo.Projection(type = 'albers usa'),
        showlakes = True,
        lakecolor = 'rgb(255, 255, 255)'),
)

fig = go.Figure(data = data, layout = layout)
plotly.offline.plot(fig, filename="TweetsMapwithoutNayRAvg.html")
