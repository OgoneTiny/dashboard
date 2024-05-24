import dash
from dash import html, dcc
from dash.dependencies import Input, Output
import pandas as pd
import plotly.express as px
import os
import dash_auth
from collections import Counter

USER_PASS_MAP = {
    'Admin': 'Admin',
    'Admin2': 'Admin2'
}

# Initialize the Dash app
app = dash.Dash(__name__, external_stylesheets=['assets/style.css'])
app.config.suppress_callback_exceptions = True

auth = dash_auth.BasicAuth(app, USER_PASS_MAP)

# Load the web server logs from the CSV file
file_path = 'web_server_logsfile.csv'
if not os.path.exists(file_path):
    raise FileNotFoundError(f"Error: The file at path {file_path} does not exist.")
else:
    df = pd.read_csv(file_path)

# Convert 'Timestamp' to datetime
df['Timestamp'] = pd.to_datetime(df['Timestamp'])

# Extract hour from timestamp for analysis
df['Hour'] = df['Timestamp'].dt.hour

# Navigation bar layout
navbar = html.Div(className='navbar', children=[
    dcc.Link('Home', href='/', className='nav-link'),
    dcc.Link('Demographics Analysis', href='/demographics', className='nav-link'),
    dcc.Link('Time Analysis', href='/time-analysis', className='nav-link'),
    dcc.Link('Geographic Analysis', href='/geographic-analysis', className='nav-link'),
    dcc.Link('Concurrent Viewership', href='/concurrent-viewership', className='nav-link'),
    dcc.Link('Main Interests', href='/main-interests', className='nav-link'),
    dcc.Link('Website Visits', href='/website-visits', className='nav-link')
])

# Define the layout of the homepage
home_layout = html.Div(className='home-layout', children=[
    html.H1("2024 FunOlympic Games Dashboard", className='header'),
    navbar,
    html.Hr(),
    # Overview Graphs
    html.Div(className='graphs-container', children=[
        html.Div(className='graph-wrapper', children=[
            html.H2("Main Interests by Sport", className='sub-header'),
            dcc.Graph(id='main-interests-graph', className='graph')
        ]),
        html.Div(className='graph-wrapper', children=[
            html.H2("Viewership by Demographics", className='sub-header'),
            dcc.Graph(id='viewership-demographics-graph', className='graph')
        ]),
        html.Div(className='graph-wrapper', children=[
            html.H2("Viewership by Time of Day", className='sub-header'),
            dcc.Graph(id='viewership-time-graph', className='graph')
        ]),
        html.Div(className='graph-wrapper', children=[
            html.H2("Website Visit Statistics", className='sub-header'),
            dcc.Graph(id='visit-statistics-graph', className='graph')
        ]),
        html.Div(className='graph-wrapper', children=[
            html.H2("Concurrent Event Viewership", className='sub-header'),
            dcc.Graph(id='concurrent-viewership-graph', className='graph')
        ]),
        html.Div(className='graph-wrapper', children=[
            html.H2("Geographic Viewership Distribution", className='sub-header'),
            dcc.Graph(id='geographic-viewership-graph', className='graph')
        ])
    ])
])

# Define the layout for demographics analysis page
demographics_layout = html.Div(className='page-layout', children=[
    html.H1("Demographics Analysis", className='header'),
    navbar,
    html.Br(),
    dcc.Graph(id='demographics-pie-chart', className='graph'),
    dcc.Dropdown(
        id='continent-dropdown',
        options=[{'label': continent, 'value': continent} for continent in df['Continent'].unique()],
        value=df['Continent'].unique()[0],
        className='dropdown'
    ),
    dcc.Dropdown(
        id='country-dropdown',
        className='dropdown'
    ),
    dcc.Dropdown(
        id='sport-dropdown',
        options=[{'label': continent, 'value': continent} for continent in df['Sport'].unique()],
        value=df['Sport'].unique()[0],
        className='dropdown'
    )
])

# Define the layout for time analysis page
time_analysis_layout = html.Div(className='page-layout', children=[
    html.H1("Time Analysis", className='header'),
    navbar,
    html.Br(),
    dcc.Graph(id='time-box-plot', className='graph'),
    dcc.Dropdown(
        id='time-dropdown',
        options=[{'label': sport, 'value': sport} for sport in df['Sport'].unique()],
        value=df['Sport'].unique()[0],
        className='dropdown'
    ), 
    dcc.Dropdown(
        id='continent-dropdown',
        options=[{'label': continent, 'value': continent} for continent in df['Continent'].unique()],
        value=df['Continent'].unique()[0],
        className='dropdown'
    ),
    dcc.Dropdown(
        id='country-dropdown',
        className='dropdown'
    )
])

# Define the layout for geographic analysis page
geographic_layout = html.Div(className='page-layout', children=[
    html.H1("Geographic Analysis", className='header'),
    navbar,
    html.Br(),
    dcc.Graph(id='geographic-viewership-map', className='graph'),
    dcc.Dropdown(
        id='continent-dropdown',
        options=[{'label': continent, 'value': continent} for continent in df['Continent'].unique()],
        value=df['Continent'].unique()[0],
        className='dropdown'
    ),
    dcc.Dropdown(
        id='country-dropdown',
        className='dropdown'
    ),
    dcc.Dropdown(
        id='sport-dropdown',
        options=[{'label': continent, 'value': continent} for continent in df['Sport'].unique()],
        value=df['Sport'].unique()[0],
        className='dropdown'
    )

])

# Define the layout for concurrent viewership page
concurrent_layout = html.Div(className='page-layout', children=[
    html.H1("Concurrent Event Viewership", className='header'),
    navbar,
    html.Br(),
    dcc.Graph(id='concurrent-viewership-graph-page', className='graph')
])

# Define the layout for main interests page
main_interests_layout = html.Div(className='page-layout', children=[
    html.H1("Main Interests by Sport", className='header'),
    navbar,
    html.Br(),
    dcc.Graph(id='main-interests-graph-page', className='graph')
])

# Define the layout for website visits page
website_visits_layout = html.Div(className='page-layout', children=[
    html.H1("Website Visit Statistics", className='header'),
    navbar,
    html.Br(),
    dcc.Graph(id='visit-statistics-graph-page', className='graph')
])

# Define the callback to update the homepage graphs
@app.callback(
    [Output('main-interests-graph', 'figure'),
     Output('viewership-demographics-graph', 'figure'),
     Output('viewership-time-graph', 'figure'),
     Output('visit-statistics-graph', 'figure'),
     Output('concurrent-viewership-graph', 'figure'),
     Output('geographic-viewership-graph', 'figure')],
    [Input('url', 'pathname')]
)
def update_home_graphs(pathname):
    # Main interests by sport
    main_interests_fig = px.histogram(df, x='Sport', title='Main Interests by Sport')
    
    # Viewership by demographics (e.g., country and gender) - using pie chart
    demographics_df = df.groupby(['Country', 'Gender']).size().reset_index(name='Count')
    demographics_fig = px.pie(demographics_df, names='Gender', values='Count', color='Gender', 
                              title='Viewership by Demographics', color_discrete_sequence=px.colors.qualitative.Prism)
    
    # Viewership by time of day - using box plot
    time_fig = px.box(df, x='Sport', y='Hour', title='Viewership by Time of Day')
    
    # Website visit statistics (e.g., user visits) - using bubble chart
    visit_stats_df = df.groupby(['User', 'Country']).size().reset_index(name='Visits')
    visit_stats_fig = px.scatter(visit_stats_df, x='User', y='Visits', size='Visits', color='Country', 
                                 hover_name='User', title='Website Visit Statistics', size_max=60)
    
    # Concurrent event viewership
    concurrent_fig = px.histogram(df, x='Sport', y='Hour', title='Concurrent Event Viewership')
    
    # Aggregate DataFrame to get count of viewerships per country
    geographic_df = df.groupby('Country').size().reset_index(name='Count')
    geographic_fig = px.scatter_geo(geographic_df, locations="Country", locationmode="country names", color="Count",
                                 hover_name="Country", title="Geographic Viewership Distribution",
                                 projection="natural earth")
  
    return main_interests_fig, demographics_fig, time_fig, visit_stats_fig, concurrent_fig, geographic_fig

# Define the callback to update the country dropdown based on the selected continent
@app.callback(
    Output('country-dropdown', 'options'),
    [Input('continent-dropdown', 'value')]
)
def set_country_options(selected_continent):
    filtered_df = df[df['Continent'] == selected_continent]
    return [{'label': country, 'value': country} for country in filtered_df['Country'].unique()]

# Define the callback to update the country dropdown value based on the selected continent
@app.callback(
    Output('country-dropdown', 'value'),
    [Input('country-dropdown', 'options')]
)
def set_country_value(available_options):
    return available_options[0]['value']

@app.callback(
    Output('demographics-pie-chart', 'figure'),
    [Input('continent-dropdown', 'value'),
     Input('country-dropdown', 'value'),
     Input('sport-dropdown', 'value')]
)
def update_demographics_graph(selected_continent, selected_country, selected_sport):
    print("Selected Continent:", selected_continent)
    print("Selected Country:", selected_country)
    print("Selected Sport:", selected_sport)
    
    # Filter DataFrame based on selected inputs
    filtered_df = df[(df['Continent'] == selected_continent) & 
                     (df['Country'] == selected_country) & 
                     (df['Sport'] == selected_sport)]
    
    print("Filtered DataFrame:")
    print(filtered_df.head())  # Print first few rows of filtered DataFrame
    
    # Perform groupby operation and create pie chart
    demographics_df = filtered_df.groupby(['Country', 'Gender']).size().reset_index(name='Count')
    demographics_fig = px.pie(demographics_df, names='Gender', values='Count', color='Gender', 
                              title=f'Viewership by Demographics in {selected_country}', color_discrete_sequence=px.colors.qualitative.Prism)
    return demographics_fig


# Define the callback to update the time analysis graph with country dropdown
@app.callback(
    Output('time-box-plot', 'figure'),
    [Input('time-dropdown', 'value'),
     Input('country-dropdown', 'value')]
)
def update_time_graph(selected_sport, selected_country):
    if selected_country:
        filtered_df = df[(df['Sport'] == selected_sport) & (df['Country'] == selected_country)]
    else:
        filtered_df = df[df['Sport'] == selected_sport]
    
    print("Filtered DataFrame:")
    print(filtered_df)
    
    time_fig = px.box(filtered_df, x='Sport', y='Hour', title=f'Viewership by Time of Day for {selected_sport} in {selected_country if selected_country else "All Countries"}')
    
    print("Plotly Figure:")
    print(time_fig)
    
    return time_fig



# Define the callback to update the geographic analysis graph
@app.callback(
    Output('geographic-viewership-map', 'figure'),
    [Input('continent-dropdown', 'value'),
     Input('country-dropdown', 'value'),
     Input('sport-dropdown', 'value')]
)
def update_geographic_graph(selected_continent, selected_country, selected_sport):
    # Filter DataFrame based on selected continent, country, and sport
    filtered_df = df[(df['Continent'] == selected_continent) & 
                     (df['Country'] == selected_country) &
                     (df['Sport'] == selected_sport)]
    
    # Aggregate DataFrame to get count of viewerships per country
    geographic_df = filtered_df.groupby('Country').size().reset_index(name='Count')
    
    # Include the sports viewed in the hover information
    geographic_df['Sports'] = selected_sport
    
    geographic_fig = px.scatter_geo(geographic_df, locations="Country", locationmode="country names", color="Count",
                                     hover_name="Country", title=f"Geographic Viewership Distribution for {selected_sport}",
                                     projection="natural earth")
    return geographic_fig



from collections import Counter

@app.callback(
    Output('concurrent-viewership-graph-page', 'figure'),
    [Input('url', 'pathname')]
)
def update_concurrent_graph(pathname):
    # Filter DataFrame to include only sports occurring at the same time but from different countries
    concurrent_sports = []
    concurrent_countries = {}
    for hour in df['Hour'].unique():
        sports_by_hour = df[df['Hour'] == hour]['Sport']
        countries_by_hour = df[df['Hour'] == hour]['Country']
        sports_counter = Counter(sports_by_hour)
        concurrent_sports.extend([sport for sport, count in sports_counter.items() if count > 1])
        
        for sport, country in zip(sports_by_hour, countries_by_hour):
            if sport in concurrent_sports:
                if sport not in concurrent_countries:
                    concurrent_countries[sport] = set()
                concurrent_countries[sport].add(country)
    
    filtered_df = df[df['Sport'].isin(concurrent_sports)]
    
    # Create histogram of concurrent event viewership with country information
    concurrent_fig = px.histogram(filtered_df, x='Sport', y='Hour', color='Country',
                                   title='Concurrent Event Viewership', 
                                   labels={'Hour': 'Concurrent Hours', 'Sport': 'Sport', 'Country': 'Country'})
    
    # Update legend orientation for better visibility
    concurrent_fig.update_layout(legend=dict(orientation="h", yanchor="top", y=1.15, xanchor="right", x=1.15))
    
    
    # Add text annotations for sum of hours
    for sport in concurrent_sports:
        hour_sum = filtered_df[filtered_df['Sport'] == sport]['Hour'].sum()
        concurrent_fig.add_annotation(x=sport, y=hour_sum, text=str(hour_sum), showarrow=False)
    
    # Update y-axis to be discrete for better visualization
    concurrent_fig.update_yaxes(title='Concurrent Hours', type='category')
    
    # Update hover information to display sum of hours
    hovertemplate = 'Sport: %{x}<br>Sum of Hours: %{y}<extra></extra>'
    concurrent_fig.update_traces(hovertemplate=hovertemplate)
    
    return concurrent_fig




# Define the callback to update the main interests graph
@app.callback(
    Output('main-interests-graph-page', 'figure'),
    [Input('url', 'pathname')]
)
def update_main_interests_graph(pathname):
    main_interests_fig = px.histogram(df, x='Sport', title='Main Interests by Sport')
    return main_interests_fig

# Define the callback to update the website visits graph
@app.callback(
    Output('visit-statistics-graph-page', 'figure'),
    [Input('url', 'pathname')]
)
def update_website_visits_graph(pathname):
    visit_stats_df = df.groupby(['User', 'Country']).size().reset_index(name='Visits')
    visit_stats_fig = px.scatter(visit_stats_df, x='User', y='Visits', size='Visits', color='Country', 
                                 hover_name='User', title='Website Visit Statistics', size_max=60)
    return visit_stats_fig

# Define the layout for the entire app
app.layout = html.Div(className='app-layout', children=[
    dcc.Location(id='url', refresh=False),
    html.Div(id='page-content', className='page-content')
])

# Define the callback to render the appropriate page layout
@app.callback(
    Output('page-content', 'children'),
    [Input('url', 'pathname')]
)
def display_page(pathname):
    if pathname == '/demographics':
        return demographics_layout
    elif pathname == '/time-analysis':
        return time_analysis_layout
    elif pathname == '/geographic-analysis':
        return geographic_layout
    elif pathname == '/concurrent-viewership':
        return concurrent_layout
    elif pathname == '/main-interests':
        return main_interests_layout
    elif pathname == '/website-visits':
        return website_visits_layout
    else:
        return home_layout

# Run the Dash app
if __name__ == '__main__':
    app.run_server(debug=True)
