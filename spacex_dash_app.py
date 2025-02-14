# Import required libraries
import pandas as pd
import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output
import plotly.express as px

# Read the airline data into pandas dataframe
spacex_df = pd.read_csv("spacex_launch_dash.csv")
max_payload = spacex_df['Payload Mass (kg)'].max()
min_payload = spacex_df['Payload Mass (kg)'].min()

launch_sites = [
    {'label': 'All Sites', 'value': 'ALL'},
    {'label': 'CCAFS LC-40', 'value': 'CCAFS LC-40'},
    {'label': 'CCAFS SLC-40', 'value': 'CCAFS SLC-40'},
    {'label': 'KSC LC-39A', 'value': 'KSC LC-39A'},  # Fixed quote
    {'label': 'VAFB SLC-4E', 'value': 'VAFB SLC-4E'},
]

# Create a dash application
app = dash.Dash(__name__)


# Create an app layout
app.layout = html.Div(children=[html.H1('SpaceX Launch Records Dashboard',
                                        style={'textAlign': 'center', 'color': '#503D36',
                                               'font-size': 40}),
                                
                                dcc.Dropdown(
                                            id='site-dropdown',
                                             options=launch_sites,
                                             value='ALL',
                                             placeholder="Select a Launch Site",
                                             searchable=True),
         
                                dcc.RangeSlider(
                                               id='payload-slider',
                                               min=0,
                                               max=10000,
                                                step=1000,
                                             marks={0: '0',100: '100'},
                                              value=[min_payload, max_payload]),
    dcc.Graph(id='success-payload-scatter-chart'),
    dcc.Graph(id='success-pie-chart')
])
                                # TASK 1: Add a dropdown list to enable Launch Site selection
                                # The default select value is for ALL sites
                                # dcc.Dropdown(id='site-dropdown',...)
                                # html.Br(),

                                # TASK 2: Add a pie chart to show the total successful launches count for all sites
                                # If a specific launch site was selected, show the Success vs. Failed counts for the site
                                #html.Div(dcc.Graph(id='success-pie-chart')),
                               # html.Br(),

                               # html.P("Payload range (Kg):"),
                                # TASK 3: Add a slider to select payload range
                                #dcc.RangeSlider(id='payload-slider',...)

                                # TASK 4: Add a scatter chart to show the correlation between payload and launch success
                               #html.Div(dcc.Graph(id='success-payload-scatter-chart')),
                             

# TASK 2:
# Add a callback function for `site-dropdown` as input, `success-pie-chart` as output

# TASK 4:
# Add a callback function for `site-dropdown` and `payload-slider` as inputs, `success-payload-scatter-chart` as output

# Callback for pie chart
@app.callback(
    Output('success-pie-chart', 'figure'),
    Input('site-dropdown', 'value')
)
def get_pie_chart(entered_site):
    filtered_df = spacex_df
    if entered_site == 'ALL':
        success_counts = filtered_df['class'].value_counts().reindex([1, 0], fill_value=0)  # Ensure order
        fig = px.pie(
            names=['Success', 'Failure'],
            values=success_counts,
            title='Success Counts for All Sites'
        )
        return fig
    else:
        filtered_df = filtered_df[filtered_df['Launch Site'] == entered_site]
        success_counts = filtered_df['class'].value_counts().reindex([1, 0], fill_value=0)  # Ensure order
        fig = px.pie(
            names=['Success', 'Failure'],
            values=success_counts,
            title=f'Success Counts for {entered_site}'
        )
        return fig

# Callback for scatter plot
@app.callback(
    Output('success-payload-scatter-chart', 'figure'),
    [Input('site-dropdown', 'value'),
     Input("payload-slider", "value")]
)
def update_scatter_chart(selected_site, payload_range):
    filtered_df = spacex_df

    # Filter by selected site
    if selected_site != 'ALL':
        filtered_df = filtered_df[filtered_df['Launch Site'] == selected_site]

    # Filter by payload range
    filtered_df = filtered_df[(filtered_df['Payload Mass (kg)'] >= payload_range[0]) & 
                              (filtered_df['Payload Mass (kg)'] <= payload_range[1])]

    # Create scatter plot
    fig = px.scatter(
        filtered_df,
        x='Payload Mass (kg)',
        y='class',
        color='Booster Version Category',
        title='Payload vs Launch Outcome'
    )
    
    fig.update_layout(yaxis=dict(tickvals=[0, 1], ticktext=['Failed', 'Succeeded']))
    return fig

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)



