#!/usr/bin/env python
# coding: utf-8

import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import pandas as pd
import plotly.express as px

# Load the data
data = pd.read_csv(
    'https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/'
    'IBMDeveloperSkillsNetwork-DV0101EN-SkillsNetwork/Data%20Files/historical_automobile_sales.csv'
)

# Initialize the Dash app
app = dash.Dash(__name__)

# Dropdown menu options
dropdown_options = [
    {'label': 'Yearly Statistics', 'value': 'Yearly Statistics'},
    {'label': 'Recession Period Statistics', 'value': 'Recession Period Statistics'}
]

# List of years
year_list = data['Year'].unique()

# Layout of the app
app.layout = html.Div([
    # Title
    html.H1("Automobile Sales Statistics Dashboard", style={'textAlign': 'center'}),

    # Dropdown menus
    html.Div([
        html.Label("Select Statistics:"),
        dcc.Dropdown(
            id='select-statistics',
            options=dropdown_options,
            value='Yearly Statistics',
            placeholder='Select Statistics'
        )
    ], style={'width': '50%', 'margin': 'auto'}),

    html.Div([
        html.Label("Select Year:"),
        dcc.Dropdown(
            id='select-year',
            options=[{'label': str(i), 'value': i} for i in year_list],
            value=year_list[0],
            placeholder="Select Year"
        )
    ], style={'width': '50%', 'margin': 'auto'}),

    # Output area for graphs
    html.Div(id='output-container', className='output-container', style={'margin-top': '20px'})
])

# Callback for enabling/disabling year selection
@app.callback(
    Output('select-year', 'disabled'),
    Input('select-statistics', 'value')
)
def update_year_dropdown(selected_statistics):
    return selected_statistics == 'Recession Period Statistics'

# Callback for updating output container based on selection
@app.callback(
    Output('output-container', 'children'),
    [Input('select-statistics', 'value'), Input('select-year', 'value')]
)
def update_output(selected_statistics, input_year):
    if selected_statistics == 'Recession Period Statistics':
        # Filter recession data
        recession_data = data[data['Recession'] == 1]

        # Plot 1: Automobile Sales over Recession Years
        yearly_rec = recession_data.groupby('Year')['Automobile_Sales'].mean().reset_index()
        R_chart1 = dcc.Graph(
            figure=px.line(yearly_rec, x='Year', y='Automobile_Sales',
                           title="Average Automobile Sales Fluctuation During Recession")
        )

        # Plot 2: Average Vehicles Sold by Type
        avg_sales = recession_data.groupby('Vehicle_Type')['Automobile_Sales'].mean().reset_index()
        R_chart2 = dcc.Graph(
            figure=px.bar(avg_sales, x='Vehicle_Type', y='Automobile_Sales',
                          title="Average Vehicles Sold by Type During Recession")
        )

        # Plot 3: Pie Chart of Advertising Expenditure by Vehicle Type
        exp_rec = recession_data.groupby('Vehicle_Type')['Advertising_Expenditure'].sum().reset_index()
        R_chart3 = dcc.Graph(
            figure=px.pie(exp_rec, names='Vehicle_Type', values='Advertising_Expenditure',
                          title="Advertising Expenditure Share During Recession")
        )

        # Plot 4: Effect of Unemployment Rate on Sales
        unemp_data = recession_data.groupby(['unemployment_rate', 'Vehicle_Type'])['Automobile_Sales'].mean().reset_index()
        R_chart4 = dcc.Graph(
            figure=px.bar(unemp_data, x='unemployment_rate', y='Automobile_Sales', color='Vehicle_Type',
                          labels={'unemployment_rate': 'Unemployment Rate', 'Automobile_Sales': 'Average Sales'},
                          title='Effect of Unemployment Rate on Vehicle Type Sales')
        )

        return [
            html.Div(className='chart-item', children=[R_chart1, R_chart2], style={'display': 'flex'}),
            html.Div(className='chart-item', children=[R_chart3, R_chart4], style={'display': 'flex'})
        ]

    elif selected_statistics == 'Yearly Statistics':
        # Filter data for selected year
        yearly_data = data[data['Year'] == input_year]

        # Plot 1: Yearly Automobile Sales
        yas = data.groupby('Year')['Automobile_Sales'].mean().reset_index()
        Y_chart1 = dcc.Graph(
            figure=px.line(yas, x='Year', y='Automobile_Sales', title='Yearly Automobile Sales')
        )

        # Plot 2: Monthly Sales
        mas = yearly_data.groupby('Month')['Automobile_Sales'].sum().reset_index()
        Y_chart2 = dcc.Graph(
            figure=px.line(mas, x='Month', y='Automobile_Sales', title='Total Monthly Automobile Sales')
        )

        # Plot 3: Average Vehicles Sold
        avr_vdata = yearly_data.groupby('Vehicle_Type')['Automobile_Sales'].mean().reset_index()
        Y_chart3 = dcc.Graph(
            figure=px.bar(avr_vdata, x='Vehicle_Type', y='Automobile_Sales',
                          title=f'Average Vehicles Sold by Type in {input_year}')
        )

        # Plot 4: Advertising Expenditure
        exp_data = yearly_data.groupby('Vehicle_Type')['Advertising_Expenditure'].sum().reset_index()
        Y_chart4 = dcc.Graph(
            figure=px.pie(exp_data, names='Vehicle_Type', values='Advertising_Expenditure',
                          title=f'Advertising Expenditure by Vehicle Type in {input_year}')
        )

        return [
            html.Div(className='chart-item', children=[Y_chart1, Y_chart2], style={'display': 'flex'}),
            html.Div(className='chart-item', children=[Y_chart3, Y_chart4], style={'display': 'flex'})
        ]

    else:
        return None

# Run the Dash app
if __name__ == '__main__':
    app.run(debug=True)

