"""
@authors: Marcel Hensel & Jochen Vestner
Watch out! This version uses global variables!
The app should therefore only be used from a single user! Not in production!
© Marcel Hensel & Jochen Vestner 2022
"""

import base64
import datetime
import io
import plotly.graph_objs as go
import dash
from dash.dependencies import Input, Output, State
from dash import dcc
from dash import  html
from dash import dash_table
from dash import callback_context
import pandas as pd
from sklearn.preprocessing import StandardScaler, MinMaxScaler, RobustScaler
import plotly.express as px
import dash_draggable

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
server = app.server

colors = {
    "graphBackground": "#ffffff",
    "background": "#ffffff",
    "text": "#000000"
}

app.layout = html.Div([
    html.Div([
        dcc.Upload(
        id='upload-data',
        children=html.Div([
            'Drag and Drop or ',
            html.A('Select Files')
        ]),
        style={
            'width': '100%',
            'height': '60px',
            'lineHeight': '60px',
            'borderWidth': '1px',
            'borderStyle': 'dashed',
            'borderRadius': '5px',
            'textAlign': 'center',
            'margin': '10px'
        },
        # Allow multiple files to be uploaded
        multiple=True
    ),
        
    
        
    ],className='six columns'),
    html.Div([
        dcc.Upload(
        id='meta_data',
        children=html.Div([
            'Drag and Drop or ',
            html.A('Select Metadata File')
        ]),
        style={
            'width': '100%',
            'height': '60px',
            'lineHeight': '60px',
            'borderWidth': '1px',
            'borderStyle': 'dashed',
            'borderRadius': '5px',
            'textAlign': 'center',
            'margin': '10px'
        },
        # Allow multiple files to be uploaded
        multiple=True)
        
    ],className='six columns'),
    
    html.Div([
        html.Div([
            html.H3('Unprocessed Data'),
            html.Button('Update Graph with Metafile',id='update',n_clicks=0),
            dcc.Graph(id='unprocessed_data')
        ], className="six columns"),

        html.Div([
            html.H3('Preprocessed Data'),
            html.Button('Autoscaler',id='Autoscaler',n_clicks=0),
            html.Button('Robustscaler', id='Robustscaler',n_clicks=0),
            html.Button('MinMaxScaler', id='MinMaxScaler',n_clicks=0),
            dcc.Graph(id='preprocessed_data')
        ], className="six columns"),
    ], className="row"),
    html.Div([ 
        dash_draggable.GridLayout(
            id='draggable',
            children=[
                html.Div([ 
                        html.P('Please select a metafile column to sort the graphs'),
                        dcc.Input(id='metafilecolumn',type='number',min=1,value=1,debounce=True),
                        html.Div(id='output-meta-upload'),
                        ]),
                html.Div([
                        html.Div(id='output-data-upload'),
                        ])])
                        
            ],className='six columns'),
    html.Div([
        html.Div([
            html.Div(id="table",)
        ],className='six columns')
        
    ])
    
    
    
])

def parse_data(contents, filename):
    content_type, content_string = contents.split(',')
    decoded = base64.b64decode(content_string)
    try:
        if 'csv' in filename:
            # Assume that the user uploaded a CSV or TXT file
            df = pd.read_csv(
                io.StringIO(decoded.decode('utf-8')))
        elif 'xls' in filename:
            # Assume that the user uploaded an excel file
            df = pd.read_excel(io.BytesIO(decoded))
        elif 'txt' or 'tsv' in filename:
            # Assume that the user upl, delimiter = r'\s+'oaded an excel file
            df = pd.read_csv(
                io.StringIO(decoded.decode('utf-8')), delimiter = r'\s+')
    except Exception as e:
        print(e)
        return html.Div([
            'There was an error processing this file.'
        ])
    return df

def meta_data(contents, filename):
    content_type, content_string = contents.split(',')
    decoded = base64.b64decode(content_string)
    try:
        if 'csv' in filename:
            # Assume that the user uploaded a CSV or TXT file
            df = pd.read_csv(
                io.StringIO(decoded.decode('utf-8')))
        elif 'xls' in filename:
            # Assume that the user uploaded an excel file
            df = pd.read_excel(io.BytesIO(decoded))
        elif 'txt' or 'tsv' in filename:
            # Assume that the user upl, delimiter = r'\s+'oaded an excel file
            df = pd.read_csv(
                io.StringIO(decoded.decode('utf-8')), delimiter = r'\s+')
    except Exception as e:
        print(e)
        return html.Div([
            'There was an error processing this file.'
        ])
    return df

@app.callback(Output('unprocessed_data', 'figure'),
              
                [
                Input('update','n_clicks'),
                Input('metafilecolumn','value'),
                State('upload-data', 'contents'),
                State('upload-data', 'filename'),
                State('meta_data','contents'),
                State('meta_data', 'filename')
            ])
def update_graph(btn,value,contents, filename, meta_contents,meta_filename):
    changed_id = [p['prop_id'] for p in callback_context.triggered][0]
    if 'update' in changed_id:
        pd.options.plotting.backend = "plotly"
        fig = {
            'layout': go.Layout(
                plot_bgcolor=colors["graphBackground"],
                paper_bgcolor=colors["graphBackground"])
        }

        if contents:
            contents = contents[0]
            filename = filename[0]
            meta_contents = meta_contents[0]
            meta_filename = meta_filename[0]
            df = parse_data(contents, filename)
            df1= meta_data(meta_contents,meta_filename)
            df=df.set_index([df.columns[0]])
            df=df.stack().reset_index(name='val')
            df=df.sort_values(by=df.columns[0])
            df_merge= df.merge(df1,left_on=df.columns[0],right_on=df1.columns[0])
            df_merge=df_merge.sort_values(by=df_merge.columns[1])
            fig=df_merge.plot.line(x=df_merge[df_merge.columns[1]],
                                   y=df_merge[df_merge.columns[2]], 
                                   color=df_merge[df_merge.columns[value+2]],
                                   line_group=df_merge[df_merge.columns[0]],
                                   markers=True)
            fig=fig.update_layout(plot_bgcolor='#ffffff')
            fig=fig.update_xaxes(linecolor='#111111',mirror=True,title_text=None)
            fig=fig.update_yaxes(linecolor='#111111',mirror=True,title_text='Value')
        return fig
    elif 'proceed'in changed_id:
        pd.options.plotting.backend = "plotly"
        fig = {
            'layout': go.Layout(
                plot_bgcolor=colors["graphBackground"],
                paper_bgcolor=colors["graphBackground"])
        }

        if contents: 
            contents = contents[0]
            filename = filename[0]
            df = parse_data(contents, filename)
            df=df.set_index([df.columns[0]])
            df=df.stack().reset_index(name='val')
            df=df.sort_values(by=df.columns[1])
            fig=df.plot.line(x=df[df.columns[1]], y=df[df.columns[2]], color=df[df.columns[0]],
            line_group=df[df.columns[0]])
            fig=fig.update_layout(plot_bgcolor='#ffffff')
            fig=fig.update_xaxes(linecolor='#111111',mirror=True,title_text=None)
            fig=fig.update_yaxes(linecolor='#111111',mirror=True,title_text='Value')
            return fig
    else:
        fig = {
            'layout': go.Layout(
                plot_bgcolor=colors["graphBackground"],
                paper_bgcolor=colors["graphBackground"])
        }
        return fig



            
            
    
@app.callback(
    Output('preprocessed_data', 'figure'),
    [
    Input('metafilecolumn','value'),    
    Input('Autoscaler', 'n_clicks'),
    Input('Robustscaler','n_clicks'),
    Input('MinMaxScaler','n_clicks'),
    State('upload-data','contents'),
    State('upload-data', 'filename'),
    State('meta_data','contents'),
    State('meta_data', 'filename')
    ])

def displayClick(value,btn1,btn2,btn3,contents,filename,meta_contents,meta_filename):
    changed_id = [p['prop_id'] for p in callback_context.triggered][0]
    if 'Autoscaler' in changed_id:
#         if 'update' in changed_id:
            pd.options.plotting.backend = "plotly"
            fig = {
                'layout': go.Layout(
                    plot_bgcolor=colors["graphBackground"],
                    paper_bgcolor=colors["graphBackground"])
            }
            if contents:
                contents = contents[0]
                filename = filename[0]
                meta_contents = meta_contents[0]
                meta_filename = meta_filename[0]
                df = parse_data(contents, filename)
                df1= meta_data(meta_contents,meta_filename)
                X=df.set_index(df.columns[0])
                scaler=StandardScaler()
                X_scaled=scaler.fit_transform(X)
                df_scaled=pd.DataFrame(X_scaled,columns=X.columns[0:],index=[df.iloc[0:,0]])

                df_scaled=df_scaled.stack().reset_index(name='val')
                df_scaled=df_scaled.sort_values(by=df_scaled.columns[0])
                df_scaled_merge= df_scaled.merge(df1,left_on=df_scaled.columns[0],right_on=df1.columns[0])
                df_scaled_merge=df_scaled_merge.sort_values(by=df_scaled_merge.columns[1])
                fig=df_scaled_merge.plot.line(x=df_scaled_merge[df_scaled_merge.columns[1]],
                                       y=df_scaled_merge[df_scaled_merge.columns[2]],
                                       color=df_scaled_merge[df_scaled_merge.columns[value+2]],
                                       line_group=df_scaled_merge[df_scaled_merge.columns[0]],markers=True)
                fig=fig.update_layout(plot_bgcolor='#ffffff')
                fig=fig.update_xaxes(linecolor='#111111',mirror=True,title_text=None)
                fig=fig.update_yaxes(linecolor='#111111',mirror=True,title_text='Value')
            return fig
    elif 'Robustscaler' in changed_id:
        pd.options.plotting.backend = "plotly"
        fig = {
            'layout': go.Layout(
                plot_bgcolor=colors["graphBackground"],
                paper_bgcolor=colors["graphBackground"])
        }
        if contents:
            contents = contents[0]
            filename = filename[0]
            meta_contents = meta_contents[0]
            meta_filename = meta_filename[0]
            df = parse_data(contents, filename)
            df1= meta_data(meta_contents,meta_filename)
            X=df.set_index(df.columns[0])
            scaler=RobustScaler()
            X_scaled=scaler.fit_transform(X)
            df_scaled=pd.DataFrame(X_scaled,columns=X.columns[0:],index=[df.iloc[0:,0]])

            df_scaled=df_scaled.stack().reset_index(name='val')
            df_scaled=df_scaled.sort_values(by=df_scaled.columns[0])
            df_scaled_merge= df_scaled.merge(df1,left_on=df_scaled.columns[0],right_on=df1.columns[0])
            df_scaled_merge=df_scaled_merge.sort_values(by=df_scaled_merge.columns[1])
            fig=df_scaled_merge.plot.line(x=df_scaled_merge[df_scaled_merge.columns[1]],
                                   y=df_scaled_merge[df_scaled_merge.columns[2]],
                                   color=df_scaled_merge[df_scaled_merge.columns[value+2]],
                                   line_group=df_scaled_merge[df_scaled_merge.columns[0]],markers=True)
            fig=fig.update_layout(plot_bgcolor='#ffffff')
            fig=fig.update_xaxes(linecolor='#111111',mirror=True,title_text=None)
            fig=fig.update_yaxes(linecolor='#111111',mirror=True,title_text='Value')
        return fig
    elif 'MinMaxScaler' in changed_id:
        pd.options.plotting.backend = "plotly"
        fig = {
            'layout': go.Layout(
                plot_bgcolor=colors["graphBackground"],
                paper_bgcolor=colors["graphBackground"])
        }
        if contents:
            contents = contents[0]
            filename = filename[0]
            meta_contents = meta_contents[0]
            meta_filename = meta_filename[0]
            df = parse_data(contents, filename)
            df1= meta_data(meta_contents,meta_filename)
            X=df.set_index(df.columns[0])
            scaler=MinMaxScaler()
            X_scaled=scaler.fit_transform(X)
            df_scaled=pd.DataFrame(X_scaled,columns=X.columns[0:],index=[df.iloc[0:,0]])

            df_scaled=df_scaled.stack().reset_index(name='val')
            df_scaled=df_scaled.sort_values(by=df_scaled.columns[0])
            df_scaled_merge= df_scaled.merge(df1,left_on=df_scaled.columns[0],right_on=df1.columns[0])
            df_scaled_merge=df_scaled_merge.sort_values(by=df_scaled_merge.columns[1])
            fig=df_scaled_merge.plot.line(x=df_scaled_merge[df_scaled_merge.columns[1]],
                                   y=df_scaled_merge[df_scaled_merge.columns[2]],
                                   color=df_scaled_merge[df_scaled_merge.columns[value+2]],
                                   line_group=df_scaled_merge[df_scaled_merge.columns[0]],markers=True)
            fig=fig.update_layout(plot_bgcolor='#ffffff')
            fig=fig.update_xaxes(linecolor='#111111',mirror=True,title_text=None)
            fig=fig.update_yaxes(linecolor='#111111',mirror=True,title_text='Value')        

        return fig
    else:
        fig = {
            'layout': go.Layout(
                plot_bgcolor=colors["graphBackground"],
                paper_bgcolor=colors["graphBackground"])
        }
        return fig
@app.callback(
    Output('table','children'),
    [
        Input('Autoscaler','n_clicks'),
        Input('Robustscaler','n_clicks'),
        Input('MinMaxScaler','n_clicks'),
        Input('upload-data','contents'),
        Input('upload-data','filename')
    ])
def update_table(btn1,btn2,btn3,contents,filename):
    changed_id = [p['prop_id'] for p in callback_context.triggered][0]
    if 'Autoscaler' in changed_id:
        table = html.Div() 
        if contents: 
            contents = contents[0]
            filename = filename[0]
            df = parse_data(contents, filename)
            X=df.set_index(df.columns[0])
#             X=X.drop(X.columns[0],axis=1)
            scaler=StandardScaler()
            X_scaled=scaler.fit_transform(X)
            df_scaled=pd.DataFrame(X_scaled,columns=X.columns[0:],index=[df.iloc[0:,0]])
            df_scaled=df_scaled.reset_index()
            table = html.Div([
                html.H5(filename),
                dash_table.DataTable(
                    data=df_scaled.to_dict('rows'),
                    columns=[{'name': str(i), 'id': str(i)} for i in df_scaled.columns],
                    export_format='csv'
                    )]),
        return table
    elif 'Robustscaler' in changed_id:
        table = html.Div() 
        if contents: 
            contents = contents[0]
            filename = filename[0]
            df = parse_data(contents, filename)
            X=df.set_index(df.columns[0])
#             X=X.drop(X.columns[0],axis=1)
            scaler=RobustScaler()
            X_scaled=scaler.fit_transform(X)
            df_scaled=pd.DataFrame(X_scaled,columns=X.columns[0:],index=[df.iloc[0:,0]])
            df_scaled=df_scaled.reset_index()
            table = html.Div([
                html.H5(filename),
                dash_table.DataTable(
                    data=df_scaled.to_dict('rows'),
                    columns=[{'name': str(i), 'id': str(i)} for i in df_scaled.columns],
                    export_format='csv'
                    )]),
        return table
    elif 'MinMaxScaler' in changed_id:
        table = html.Div() 
        if contents: 
            contents = contents[0]
            filename = filename[0]
            df = parse_data(contents, filename)
            X=df.set_index(df.columns[0])
#             X=X.drop(X.columns[0],axis=1)
            scaler=MinMaxScaler()
            X_scaled=scaler.fit_transform(X)
            df_scaled=pd.DataFrame(X_scaled,columns=X.columns[0:],index=[df.iloc[0:,0]])
            df_scaled=df_scaled.reset_index()
            table = html.Div([
                html.H5(filename),
                dash_table.DataTable(
                    data=df_scaled.to_dict('rows'),
                    columns=[{'name': str(i), 'id': str(i)} for i in df_scaled.columns],
                    export_format='csv'
                    )]),
        return table
    else:
        print('Empty table')
@app.callback(Output('output-data-upload', 'children'),
            [
                Input('update','n_clicks'),
                State('upload-data', 'contents'),
                State('upload-data', 'filename')
            ])
def update_table(btn,contents, filename):
    changed_id = [p['prop_id'] for p in callback_context.triggered][0]
    if 'update' in changed_id: 
        table = html.Div()

        if contents:
            contents = contents[0]
            filename = filename[0]
            df = parse_data(contents, filename)

            table = html.Div([
                html.H5(filename),
                dash_table.DataTable(
                    data=df.to_dict('rows'),
                    columns=[{'name': i, 'id': i} for i in df.columns]
                ),
                html.Hr(),
                html.Div('Raw Content'),
                html.Pre(contents[0:200] + '...', style={
                    'whiteSpace': 'pre-wrap',
                    'wordBreak': 'break-all'
                })
            ])
        return table

@app.callback(Output('output-meta-upload', 'children'),
            [
                Input('update','n_clicks'),
                State('meta_data', 'contents'),
                State('meta_data', 'filename')
            ])
def update_table(btn,contents, filename):
    changed_id = [p['prop_id'] for p in callback_context.triggered][0]
    if 'update' in changed_id: 
        table = html.Div()

        if contents:
            contents = contents[0]
            filename = filename[0]
            df = meta_data(contents, filename)

            table = html.Div([
                html.H5(filename),
                dash_table.DataTable(
                    data=df.to_dict('rows'),
                    columns=[{'name': i, 'id': i} for i in df.columns]
                ),
                html.Hr(),
                html.Div('Raw Content'),
                html.Pre(contents[0:200] + '...', style={
                    'whiteSpace': 'pre-wrap',
                    'wordBreak': 'break-all'
                })
            ])
        return table

if __name__ == '__main__':
    app.run_server(debug=True, use_reloader=False, port=8080)
