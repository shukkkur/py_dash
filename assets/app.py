import numpy as np
import pandas as pd
from datetime import date

from dash import Dash
from dash import dcc
from dash import html
from dash import Input, Output
import dash_bootstrap_components as dbc

import plotly.express as px
import plotly.graph_objects as go


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



df = pd.read_excel('assets/dashboard.xlsx',
                   sheet_name='data',
                   parse_dates=['Date'])


################  a) #######################
df_dt_indexed = df.set_index('Date')
df_dt_grouped = df.groupby('Date').count()
df_dt_grouped['Total'] = df_dt_grouped.Outcome
df_date_outcome_grouped = df.groupby(['Date', 'Outcome']).count()
df_dt_grouped['Success'] = df_date_outcome_grouped.xs('Success', level=1).iloc[:, 0]
df_dt_grouped['Failure'] = df_date_outcome_grouped.xs('Failure', level=1).iloc[:, 0]
nan_rows = df_dt_grouped[df_dt_grouped.Success.isna()]
df_dt_grouped.loc[nan_rows.index, ['Success']] = nan_rows['Total'] - nan_rows['Failure']
df_dt_grouped.Success = df_dt_grouped['Success'].astype('int64')
df_dt_grouped.reset_index(inplace = True)


#### b) Data
df_state_grouped = df.groupby(['State', 'Outcome']).count()
b_df = pd.DataFrame(df_state_grouped.xs('Success', level=1).iloc[:, 0])
b_df.columns = ['Success']
b_df['Failure'] = df_state_grouped.xs('Failure', level=1).iloc[:, 0]
b_df = b_df.fillna(0).astype('int64').reset_index()


bar_graph = px.bar(data_frame=b_df,
                   x='State',
                   y=['Success', 'Failure'],
                   barmode='group',
                   labels = {'variable': '',
                             'value': 'Number of Calls'})

bar_graph.update_layout(showlegend=True,
                        plot_bgcolor='#0e2433',
                        paper_bgcolor='#0e2433',
                        font_color="white",)

#### c)
c_df = df.Outcome.value_counts()

c_graph = px.pie(values=c_df,
                   names=c_df.index,
                   color_discrete_sequence=px.colors.sequential.Rainbow)

c_graph.update_layout(showlegend=True,
                        plot_bgcolor='#0e2433',
                        paper_bgcolor='#0e2433',
                        font_color="white",)

#### d)
d_graph = go.Figure()

totac = df.groupby("State")["Outcome"].count()
totsuc = df[df["Outcome"] == "Success"].groupby("State")["Outcome"].count()

state_success = (totsuc / totac * 100).sort_values(ascending=False)

d_graph.add_trace(
    go.Bar(
        x=state_success.index,
        y=state_success.values,
        name="State success",
        marker_color='orange',
    )
)

d_graph["layout"]["xaxis"]["title"] = "State"
d_graph["layout"]["yaxis"]["title"] = "Success"
d_graph["layout"]["legend_title"] = "Legends"
d_graph['layout']['paper_bgcolor'] = '#0e2433'
d_graph['layout']['plot_bgcolor'] = '#0e2433'
d_graph['layout']['font_color'] = 'white'


#### e)
e_graph = go.Figure()

e_graph.add_trace(
    go.Pie(
        labels=totac.index,
        values=totac.values,
        textinfo="none",
        name="total calls",
        hole=0.6,
    ),
)

e_graph.add_trace(
    go.Pie(
        labels=totsuc.index,
        values=totsuc.values,
        textinfo="none",
        name="success calls",
        hole=0.45,
    ),
)
e_graph.data[0].domain = {"x": [0, 1], "y": [1, 1]}
e_graph.data[1].domain = {"x": [0, 1], "y": [0.22, 0.78]}
e_graph.update_traces(hoverinfo="label+percent+name")
e_graph["layout"]["legend_title"] = "Labels"
e_graph['layout']['paper_bgcolor'] = '#0e2433'
e_graph['layout']['plot_bgcolor'] = '#0e2433'
e_graph['layout']['font_color'] = 'white'


#### f)
df["Success"] = df["Outcome"].apply(lambda outcome: 1 if outcome == "Success" else 0)
time_period = df[df.Success == 1]
time_period["Time_Period"] = time_period["Time_Period"].apply(
    lambda time_period: "0" + time_period
    if len(time_period.split("h")[0]) == 1
    else time_period)
x = time_period.groupby("Time_Period")["Success"].sum()

f_graph = go.Figure()
f_graph.add_trace(
    go.Bar(
        x=x.index,
        y=x.values,
        name="Time Period",
        marker_color='green',
    )
)
f_graph["layout"]["xaxis"]["title"] = "Hours/Time"
f_graph["layout"]["yaxis"]["title"] = "Success calls"
f_graph['layout']['paper_bgcolor'] = '#0e2433'
f_graph['layout']['plot_bgcolor'] = '#0e2433'
f_graph['layout']['font_color'] = 'white'

######################################################


sidebar = html.Div(
    [
        html.H3("Menu", className="display-7 text-white"),
        html.Hr(style={'color':'white'}),
        html.Br(),
        dbc.Nav(
            [
                dbc.NavLink("1) Graph as function of Time",
                            href="#adesc",
                            active="exact",
                            className="text-white",
                            external_link=True),
                
                dbc.NavLink("2) Number of calls per State",
                            href="#bdesc",
                            active="exact",
                            className="text-white",
                            external_link=True),
                
                dbc.NavLink("3) Failure/Success/TimeOut",
                            href="#cdesc",
                            active="exact",
                            className="text-white",
                            external_link=True),
                
                dbc.NavLink("4) Most Successfull States",
                            href="#ddesc",
                            active="exact",
                            className="text-white",
                            external_link=True),
                
                dbc.NavLink("5) Total Number of Actions",
                            href="#edesc",
                            active="exact",
                            className="text-white",
                            external_link=True),
                
                dbc.NavLink("6) Successes by Time_Period",
                            href="#fdesc",
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


header = html.Div(children=[html.H3("Calls Dashboard  📞"),html.H5("Analyze Successfull/Failed calls")],
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

a_desc = html.H5("a) We want to see this data in a graph with a time series legend. Then we want to see in the same graph the ratio of success /total calls as a function of date.",
                style={'color':'white',
                       'font-family':'Times',
                       'margin-bottom':'0px',
                       'text-align':'left'},
                 id="adesc")

b_desc = html.H5("b) We want to see another graph that presents the success and failure by State in the form of a bar graph.",
                style={'color':'white',
                       'font-family':'Times',
                       'margin-bottom':'0px',
                       'text-align':'left'},
                 id="bdesc")

c_desc = html.H5("c) We want to see at the end which state was the most ' successful ' in share ratios.",
                style={'color':'white',
                       'font-family':'Times',
                       'margin-bottom':'0px',
                       'text-align':'left'},
                 id="cdesc")

d_desc = html.H5("d) We want to see at the end which state was the most ' successful ' in share ratios.",
                style={'color':'white',
                       'font-family':'Times',
                       'margin-bottom':'0px',
                       'text-align':'left'},
                 id="ddesc")

e_desc = html.H5("e) We also want to see a double piechart that displays the total number of actions/ State and number ofsuccess / state.",
                style={'color':'white',
                       'font-family':'Times',
                       'margin-bottom':'0px',
                       'text-align':'left'},
                 id="edesc")

f_desc = html.H5("f) We want to know the number of succes by Time_Period.",
                style={'color':'white',
                       'font-family':'Times',
                       'margin-bottom':'0px',
                       'text-align':'left'},
                 id="fdesc")


content = html.Div(id="page-content",
                   children=[
                       header,
                       a_desc,
                       dcc.Graph(id="line_plot"),
                       html.Div(children=[dcc.DatePickerSingle(id='date_picker',
                                                               min_date_allowed=df_dt_grouped.Date.min(),
                                                               max_date_allowed=df_dt_grouped.Date.max(),
                                                               placeholder="Date",
                                                               display_format="DD/MM/YYYY")],
                                style={"margin-left":"45%",
                                       "margin-top":"-40px"}),

                       html.Br(),

                       b_desc,
                       dcc.Graph(figure=bar_graph),

                       html.Br(),

                       c_desc,
                       dcc.Graph(figure=c_graph),

                       html.Br(),

                       d_desc,
                       dcc.Graph(figure=d_graph),

                       html.Br(),

                       e_desc,
                       dcc.Graph(figure=e_graph),

                       html.Br(),

                       f_desc,
                       dcc.Graph(figure=f_graph),
                       
                       ],
                   style=CONTENT_STYLE)


app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP,
                                           dbc.icons.FONT_AWESOME])
server = app.server

app.layout = html.Div([
    dcc.Location(id="url"),
    sidebar,
    content
], style={"background": "#0e2433"})



@app.callback(
    Output(component_id="line_plot", component_property="figure"),
    Input("date_picker", "date"))
def update_plot(date):
    df = df_dt_grouped.copy(deep=True)
    
    if date:
        df = df_dt_grouped[df_dt_grouped.Date >= date]

    line_graph = px.line(data_frame = df,
                     x = 'Date',
                     y = ['Total', 'Success', 'Failure'],
                     labels = {'Date': '',
                               'variable': '',
                               'value': 'Number of Calls'})

    line_graph.update_layout(template='seaborn',
                         showlegend=True,
                         plot_bgcolor='#0e2433',
                         paper_bgcolor='#0e2433',
                         font_color="white",
                         legend=dict(
                             orientation="h",
                             yanchor="bottom",
                             y=1.02,
                             xanchor="right",
                             x=1,
                             bordercolor="White",
                             borderwidth=2))
    return line_graph

if __name__=='__main__':
    app.run_server(debug=True, port=3000)
