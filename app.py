import bs4
import sqlite3
import requests
import numpy as np
import pandas as pd
from sqlite3 import Error
from pandaserd import ERD


db_file = 'assets/hr.db'

try:
    connection = sqlite3.connect(db_file)
except Error as e:
    print(e)


#  below code taken from
#  https://www.sqlitetutorial.net/sqlite-python/sqlite-python-select/
regions = pd.read_sql_query("select * from regions;", connection)
countries = pd.read_sql_query("select * from countries;", connection)
locations = pd.read_sql_query("select * from locations;", connection)
departments = pd.read_sql_query("select * from departments;", connection)
employees = pd.read_sql_query("select * from employees;", connection)
jobs = pd.read_sql_query("select * from jobs;", connection)
job_history = pd.read_sql_query("select * from job_history;", connection)

# duplicate first rows
regions.drop(0, axis=0, inplace=True)
countries.drop(0, axis=0, inplace=True)
jobs.drop(0, axis=0, inplace=True)
job_history.drop(0, axis=0, inplace=True)


#  below code taken from
#  https://pypi.org/project/pandaserd/
#  https://github.com/nabsabraham/pandas-erd#create-erd-diagram-from-pandas-dataframes
erd = ERD()

regions_table = erd.add_table(regions, 'regions', bg_color='lightblue')
countries_table = erd.add_table(countries, 'countries', bg_color='lightblue')
locations_table = erd.add_table(locations, 'locations', bg_color='lightblue')
departments_table = erd.add_table(departments, 'departments', bg_color='lightblue')
employees_table = erd.add_table(employees, 'employees', bg_color='lightblue')
job_history_table = erd.add_table(job_history, 'job_history', bg_color='lightblue')
jobs_table = erd.add_table(jobs, 'jobs', bg_color='lightblue')

erd.create_rel('regions', 'countries', on='region_id', right_cardinality='*')
erd.create_rel('countries', 'locations', on='country_id', right_cardinality='*')
erd.create_rel('departments', 'job_history', on='department_id', right_cardinality='*')
erd.create_rel('locations', 'departments', on='location_id', right_cardinality='*')
erd.create_rel('jobs', 'employees', on='job_id', right_cardinality='*')
erd.create_rel('job_history', 'employees', on='employee_id', right_cardinality='*')
erd.create_rel('jobs', 'job_history', on='job_id', right_cardinality='*')
erd.create_rel('employees', 'departments', on='department_id', left_cardinality='*')

##erd.write_to_file('output.txt')

#  after insterting the DOT code from output.txt in https://edotor.net/
#  the resulting image is graph.png


"""
##EXERCISE 2
"""
from dash import Dash
from dash import dcc
from dash import html
from dash import Input, Output
import dash_bootstrap_components as dbc

import plotly.express as px
import plotly.graph_objects as go


def scrape():

    out = {10: [], 25: [], 75: [], 90: []}

    url = 'https://www.itjobswatch.co.uk/jobs/uk/sqlite.do'
    html = requests.get(url).content
    soup = bs4.BeautifulSoup(html, 'html.parser')

    table = soup.find('table', class_='summary')
    rows = table.find_all('tr')
    for i in rows:
        if "<td>10<sup>th</sup> Percentile</td>" in str(i):
            for b in i.find_all('td', class_='fig'):
                if str(b.text[1:]) != "":
                    out[10].append(int(b.text[1:].replace(",", "")))
                else:
                    out[10].append(None)
        if "<td>25<sup>th</sup> Percentile</td>" in str(i):
            for b in i.find_all('td', class_='fig'):
                if str(b.text[1:]) != "":
                    out[25].append(int(b.text[1:].replace(",", "")))
                else:
                    out[25].append(None)
        if "<td>75<sup>th</sup> Percentile</td>" in str(i):
            for b in i.find_all('td', class_='fig'):
                if str(b.text[1:]) != "":
                    out[75].append(int(b.text[1:].replace(",", "")))
                else:
                    out[75].append(None)
        if "<td>90<sup>th</sup> Percentile</td>" in str(i):
            for b in i.find_all('td', class_='fig'):
                if str(b.text[1:]) != "":
                    out[90].append(int(b.text[1:].replace(",", "")))
                else:
                    out[90].append(None)

    return out

# styling the sidebar
SIDEBAR_STYLE = {
    "position": "fixed",
    "top": 0,
    "left": 0,
    "bottom": 0,
    "width": "16rem",
    "text-color": 'white',
    "padding": "2rem 1rem",
    "background-color": "#23395d",
    "font-family": "Times",
}


# padding for the page content
CONTENT_STYLE = {
    "margin-left": "18rem",
    "margin-right": "2rem",
    "padding": "2rem 1rem",
}

merged = pd.merge(employees, jobs, how='left', on='job_id')
counted = merged.groupby('job_title').count().reset_index()

bar_graph = px.bar(data_frame=counted,
                   x='job_title',
                   y='employee_id',
                   color='job_title',
                   labels = {'job_title': 'Jobs',
                             'employee_id': 'Count'})

bar_graph.update_layout(showlegend=True,
                        plot_bgcolor='#0e2433',
                        paper_bgcolor='#0e2433',
                        font_color="white")

jobs['diff_salary'] = jobs.max_salary - jobs.min_salary


sidebar = html.Div(
    [
        html.H3("Contents", className="display-7 text-white"),
        html.Hr(style={'color':'white'}),
        html.Br(),
        dbc.Nav(
            [
                dbc.NavLink("EXERCISE 1",
                            href="#erd",
                            active="exact",
                            className="text-white",
                            external_link=True),

                dbc.NavLink("EXERCISE 2",
                            href="#exer2",
                            active="exact",
                            className="text-white",
                            external_link=True),

                dbc.NavLink("EXERCISE 3",
                            href="#exer3",
                            active="exact",
                            className="text-white",
                            external_link=True),

                dbc.NavLink("EXERCISE 4",
                            href="#exer4",
                            active="exact",
                            className="text-white",
                            external_link=True),

                dbc.NavLink("EXERCISE 5",
                            href="#exer5",
                            active="exact",
                            className="text-white",
                            external_link=True),
            ],
            vertical=True,
            pills=True,
        ),
    ],
    style=SIDEBAR_STYLE,
)

header = html.Div(children=[html.H3("Final Exam"),html.H5("Shakhansho Sabzaliev")],
                  style={'border':"2px solid black",
                         'margin': 'auto',
                         'width':"100%",
                         'padding':'10px',
                         'margin-bottom':'50px',
                         'text-align':"center",
                         'background':"black",
                         "border-radius": "25px",
                         'color':'white',
                         "word-wrap": "break-word",
                         "font-family": "Times"})

a_desc = html.H5("Entity Relationship Diagram of the Database",
                style={'color':'white',
                       'font-family':'Times',
                       'margin-bottom':'0px',
                       'text-align':'left'},
                 id="erd")

b_desc = html.H5("The number of employees with the same job.",
                style={'color':'white',
                       'font-family':'Times',
                       'margin-bottom':'0px',
                       'text-align':'left'},
                 id="exer2")

c_desc = html.H5("Difference between the job MIN & MAX salaries",
                style={'color':'white',
                       'font-family':'Times',
                       'margin-bottom':'0px',
                       'text-align':'left'},
                 id="exer3")

d_desc = html.H5("Average Employee Salary and 10th, 20th, 75th and 90th Percentile for Salaries in UK",
                style={'color':'white',
                       'font-family':'Times',
                       'margin-bottom':'0px',
                       'text-align':'left'},
                 id="exer4")

e_desc = html.H5([html.Br(),
                  html.Br(),
                  html.Br(),
                  html.Hr(),
                  "Dashboard Deployed Successfully!",
                  html.Br(),
                  "Thank you for the Course",
                  html.Br(),
                  "Learned a lot"],
                style={'color':'white',
                       'font-family':'Times',
                       'margin-bottom':'0px',
                       'text-align':'center'},
                 id="exer5")


content = html.Div(id="page-content",
                   children=[
                       header,
                       
                       a_desc,
                       html.P([html.Img(src=r'assets/graph.png', alt='image', width="80%")], style={'text-align':'center'}),
                       
                       html.Br(),
                       html.Br(),

                       b_desc,
                       dcc.Graph(figure=bar_graph),

                       html.Br(),

                       c_desc,
                       dcc.Graph(id='graph-with-slider'),
                       dcc.Slider(
                           jobs['diff_salary'].min(),
                           jobs['diff_salary'].max(),
                           step=3000,
                           value=jobs['diff_salary'].min(),
                           id='salary-slider'
                           ),

                       html.Br(),

                       d_desc,
                       dcc.Graph(id='graph-year-slider'),
                       dcc.Slider(
                           2020,
                           2022,
                           step=None,
                           value=2020,
                           marks={str(y): str(y) for y in [2020, 2021, 2022]},
                           id='year-slider'
                           ),

                       html.Br(),

                       e_desc,
                       
                       ],
                   style=CONTENT_STYLE)


app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP, dbc.icons.FONT_AWESOME])
server = app.server

app.layout = html.Div([dcc.Location(id="url"),
                       sidebar,
                       content],
                      style={"background": "#0e2433"})

@app.callback(
    Output('graph-with-slider', 'figure'),
    Input('salary-slider', 'value'))
def update_figure(selected_salary):
    filtered_df = jobs[jobs.diff_salary >= selected_salary]

    c_graph = px.bar(data_frame=filtered_df,
                     y='job_title',
                     x='diff_salary',
                     height=700,
                     orientation='h',
                     labels = {'job_title': 'Jobs',
                               'diff_salary': 'Difference in Salary'},
                     color_discrete_sequence=["#029e78"])

    c_graph.update_layout(showlegend=True,
                          plot_bgcolor='#0e2433',
                          paper_bgcolor='#0e2433',
                          font_color="white")
    return c_graph

avg_salary = employees['salary'].mean()
year = np.array([2020, 2021, 2022])
percentiles = scrape()


@app.callback(
    Output('graph-year-slider', 'figure'),
    Input('year-slider', 'value'))
def update_figure2(selected_year):
    filtered = year[year >= selected_year]

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=filtered,
                             y=[avg_salary for i in filtered],
                             name='Average Salary',
                             line=dict(color="black")))

    for i in percentiles:
        fig.add_trace(go.Scatter(x=filtered,
                                 y=percentiles[i],
                                 name=f'{i}th Percentile',
                                 line=dict(color="#30f216")))

    fig["layout"]["legend_title"] = "Labels"
    fig['layout']['paper_bgcolor'] = '#0e2433'
    fig['layout']['plot_bgcolor'] = '#0e2433'
    fig['layout']['font_color'] = 'white'
    fig['layout']['xaxis']['tickvals'] = filtered
    fig['layout']['xaxis']['ticktext'] = list(map(str, list(filtered)))
    
    return fig


if __name__=='__main__':
    app.run_server(debug=True, port=3000)
