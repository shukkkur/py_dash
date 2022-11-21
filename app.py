import os
import numpy as np
import pandas as pd
from datetime import date

from dash import Dash
from dash import dcc
from dash import html
from dash import Input, Output

import plotly.express as px


df = pd.read_excel('assets/dashboard.xlsx',
                   sheet_name='data',
                   parse_dates=['Date'])
##print(df.head(), end='\n\n')

################  a) #######################
df_dt_indexed = df.set_index('Date')
df_dt_grouped = df.groupby('Date').count()

df_dt_grouped['Total'] = df_dt_grouped.Outcome

df_date_outcome_grouped = df.groupby(['Date', 'Outcome']).count()
df_dt_grouped['Success'] = df_date_outcome_grouped.xs('Success', level=1).iloc[:, 0]
df_dt_grouped['Failure'] = df_date_outcome_grouped.xs('Failure', level=1).iloc[:, 0]

nan_rows = df_dt_grouped[df_dt_grouped.Success.isna()]
df_dt_grouped.loc[nan_rows.index, ['Success']] = nan_rows['Total'] - nan_rows['Failure']
##print(df_dt_grouped.isna().sum(), end='\n\n')


#### To have the same dtype, converting Success column from float64 to int64
df_dt_grouped.Success = df_dt_grouped['Success'].astype('int64')
##print(df_dt_grouped[['Total', 'Success', 'Failure']], end='\n\n')


#### Plotting  a) 
df_dt_grouped.reset_index(inplace = True)


#### b) Data
df_state_grouped = df.groupby(['State', 'Outcome']).count()
b_df = pd.DataFrame(df_state_grouped.xs('Success', level=1).iloc[:, 0])
b_df.columns = ['Success']
b_df['Failure'] = df_state_grouped.xs('Failure', level=1).iloc[:, 0]
b_df = b_df.fillna(0).astype('int64').reset_index()
##print(b_df, end='\n\n')



#### c)
c_df = df.Outcome.value_counts()
##print(c_df, end='\n\n')


##### DASHBOARD #######
app = Dash(__name__)
server = app.server
app.layout = html.Div(children=[

        html.H2("Dynamic & Interactive", style={'textAlign': 'center'}),
        html.H2('Dashboard', style={'textAlign': 'center'}),

        html.Hr(),
        
        dcc.Dropdown(id='task_dd',
                     options=[{'label': 'a)', 'value': 'task_a'},
                              {'label': 'b)', 'value': 'task_b'},
                              {'label': 'c)', 'value': 'task_c'},
                              {'label': 'd)', 'value': 'task_d', 'disabled': True},
                              {'label': 'f)', 'value': 'task_f', 'disabled': True}],
                     placeholder="Select the task",
                     searchable=False, value = "task_a"),
        dcc.Graph(id="my_graph"),
        html.Div(children=[dcc.DatePickerSingle(id='date_picker',
                                                min_date_allowed=df_dt_grouped.Date.min(),
                                                max_date_allowed=df_dt_grouped.Date.max(),
                                                placeholder="Start Date",
                                                display_format="DD/MM/YYYY")],
                 id='date_container')
        ])

@app.callback(
    Output(component_id='date_container', component_property='style'),
    Input(component_id='task_dd', component_property='value'))
def show_hide_element(visibility_state):
    if visibility_state == 'task_a':
        return {'margin': 'auto', 'width': '25%', 'text-align': 'center'}
    else:
        return {'display': 'none'}


@app.callback(
    Output(component_id="my_graph", component_property="figure"),
    Input("task_dd", "value"),
    Input("date_picker", "date"))
def update_plot(selection, date):
    title = 'Empty'
    
    if selection:
        title = selection

    if title == "task_b":
        bar_graph = px.bar(data_frame=b_df,
                           x='State',
                           y=['Success', 'Failure'],
                           barmode='group',
                           labels = {'variable': '',
                                     'value': 'Number of Calls'},
                           )
        bar_graph.update_layout(title='b) Number of calls per State',
                                title_x=0.5,
                                showlegend=True,)
        return bar_graph

    elif title == "task_c":
        pie_graph = px.pie(values=c_df,
                           names=c_df.index,
                           color_discrete_sequence=px.colors.sequential.Rainbow)

        pie_graph.update_layout(title='c) Failure/Success/TimeOut',
                                title_x=0.5,
                                showlegend=True)
        return pie_graph

    elif title == "task_a":
        df = df_dt_grouped.copy(deep=True)
        
        if date:
            df = df_dt_grouped[df_dt_grouped.Date >= date]
            
        line_graph = px.line(data_frame = df,
                             x = 'Date',
                             y = ['Total', 'Success', 'Failure'],
                             labels = {'Date': 'Date',
                                       'variable': '',
                                       'value': 'Number of Calls'},
                             )
        line_graph.update_layout(title="a) Success/Total as a function of Date",
                                 title_x=0,
                                 template='seaborn',
                                 showlegend=True,
                                 legend=dict(
                                     orientation="h",
                                     yanchor="bottom",
                                     y=1.02,
                                     xanchor="right",
                                     x=1,
                                     bordercolor="Black",
                                     borderwidth=2)
                                 )
        return line_graph



app.title = "shukkkur"

if __name__ == "__main__":
  app.run_server("0.0.0.0", debug=False, port=int(os.environ.get('PORT', 8000)))
