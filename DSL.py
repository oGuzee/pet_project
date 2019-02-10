''' This is an interactive Python Web-app example. DSL: HTML 
It has found use in the class of Dr. Biessmann " Urban Technologies "'''

import dash
from dash.dependencies import Input, Output, State
import dash_core_components as dcc
import dash_html_components as html
import dash_table_experiments as dt
import json
import pandas as pd
import numpy as np
import plotly
import plotly.graph_objs as go

app = dash.Dash()

app.scripts.config.serve_locally = True

# DFs
results = pd.read_csv('f1db_csv/lap_times.csv', index_col=0)

# Markdown
markdown_title = '''
### Formula 1 Data Visualized
'''
markdown_html_table = '''
### Interactive Data Table
'''
# Function to process dataframe to html table
def generate_table(dataframe, max_rows=10):
    return html.Table(
        # Header
        [html.Tr([html.Th(col) for col in dataframe.columns])] +

        # Body
        [html.Tr([
            html.Td(dataframe.iloc[i][col]) for col in dataframe.columns
        ]) for i in range(min(len(dataframe), max_rows))]
    )

# Interactive Web App begins here
app.layout = html.Div([
    dcc.Markdown('''# DSL Example'''),
    html.Label('by Oguzhan Uyar'),
    html.Label('9.2.19'),
    
    dcc.Markdown(markdown_title),

    
    # Markdown html table
    dcc.Markdown(markdown_html_table),
    generate_table(html_table),
    # Scatter Plot Dangerous
    

    # Interactive Data Table
    dt.DataTable(
        rows=results.to_dict('records'),

        # optional - sets the order of columns
        # columns=sorted(results.columns),

        row_selectable=False,
        filterable=True,
        sortable=True,
        selected_row_indices=[],
        id='datatable'
    ),
    # Responding Graphs
    html.Div(id='selected-indexes'),
    #html.Div(id='selected-indexes'),
    dcc.Graph(
        id='graph'
    )
], className="container")

# Data table interactiveness
@app.callback(
    Output('datatable', 'selected_row_indices'),
    [Input('graph', 'clickData')],
    [State('datatable', 'selected_row_indices')])
def update_selected_row_indices(clickData, selected_row_indices):
    if clickData:
        for point in clickData['points']:
            if point['pointNumber'] in selected_row_indices:
                selected_row_indices.remove(point['pointNumber'])
            else:
                selected_row_indices.append(point['pointNumber'])
    return selected_row_indices

# Bar chart interactiveness
@app.callback(
    Output('graph', 'figure'),
    [Input('datatable', 'rows'),
     Input('datatable', 'selected_row_indices')])
def update_figure(rows, selected_row_indices):
    dff = pd.DataFrame(rows)
    fig = plotly.tools.make_subplots(
        rows=2, cols=1,
        subplot_titles=('F1 Data',),
        shared_xaxes=True)
    marker = {'color': ['#0074D9']*len(dff)}
    for i in (selected_row_indices or []):
        marker['color'][i] = '#FF851B'
    fig.append_trace(go.Bar(
        x=dff['lap'],
        y=dff['lap_milliseconds'],
        text=dff['lap_time'],
        name='lap_time',
        marker={'color': ['#0074D9']*len(dff)}
    ), 1, 1)
    fig.append_trace(go.Bar(
        x=dff['lap'],
        y=dff['lap_milliseconds'],
        text=dff['lap_time'],
        name='lap_time',
        marker={'color': ['#c50a0a']*len(dff)}
    ), 1, 1)
    fig['layout']['showlegend'] = False
    fig['layout']['height'] = 800
    fig['layout']['margin'] = {
        'l': 40,
        'r': 10,
        't': 60,
        'b': 200
    }
    return fig

# HTML stylesheet
app.css.append_css({
    "external_url": "https://codepen.io/chriddyp/pen/bWLwgP.css"
})

if __name__ == '__main__':
    app.run_server(debug=True)