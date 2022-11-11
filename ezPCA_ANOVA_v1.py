#!/usr/bin/env python
# coding: utf-8

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
import statsmodels.api as sm
from statsmodels.formula.api import ols
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
server = app.server
colors = {
    "graphBackground": "#F5F5F5",
    "background": "#ffffff",
    "text": "#000000"
}

app.layout = html.Div([
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
    html.Div([
         html.Div([
            html.H3('Anova-Output'),
            dcc.Input(id='variables', type='number',placeholder='Set ID'),
            dcc.Input(id='anova',type='number',placeholder='set number of factors '),
            dcc.Input(id='alpha',type='number',placeholder='set significance level'),
            
            html.Button('Submit',id='submit',n_clicks=0),
            html.Div(id='ANOVA_df'),
        ], className="six columns",),
        
        html.Div([
            html.H3('Significant features'),
            html.Div(id='sigdiff'),
        ], className="six columns",),
    ], className="row"),
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
@app.callback(
    Output('ANOVA_df','children'),  
    Input('upload-data','contents'),
    Input('upload-data','filename'), 
    Input('submit','n_clicks'),
    State('anova','value'),
    State('variables','value'),   
)

def update_table(contents,filename,n_clicks,anova,variables,):
    changed_id = [p['prop_id'] for p in callback_context.triggered][0]
    if 'submit' in changed_id:
        if variables==0:
            return html.Div([
            'Please select the factors'
            ])

        if variables==1:
            if anova ==1:
                table = html.Div()
                if contents:
                    contents = contents[0]
                    filename = filename[0]
                    df = parse_data(contents, filename)
                    df=df.set_index([df.columns[0]])
                    df_plotting= df.stack().reset_index(name='value')
                    df_plotting.columns =['factor','compound', 'value']
                    alpha_anova = 0.1

                    keys = []
                    tables =  []
                    X = df_plotting
                    for variable in df_plotting['compound'].unique():
                        model = ols('value ~ C(factor)', data=X[X['compound']==variable]).fit()
                        anova_table = sm.stats.anova_lm(model, typ=2)
                        keys.append(variable)
                        tables.append(anova_table)
                    df_anova = pd.concat(tables, keys=keys, axis=0)
                    df_anova['PR(>F)'] = round(df_anova['PR(>F)'], 3)#.apply(round())
                    df_anova['F'] = round(df_anova['F'], 1)#.apply(round())
                    df_anova[df_anova == 'NaN'] 
                    df_anova = df_anova.reset_index()
                    df_anova = df_anova[df_anova['level_1'] == 'C(factor)']	
                    table = html.Div([
                        html.H5(filename),
                        dash_table.DataTable(
                            data=df_anova.to_dict('rows'),
                            columns=[{'name': i, 'id': i} for i in df_anova.columns]
                        ),
                        html.Hr(),
                        html.Div('Raw Content'),
                        html.Pre(contents[0:200] + '...', style={
                            'whiteSpace': 'pre-wrap',
                            'wordBreak': 'break-all'
                        })
                    ])
                return table
            else:
                return html.Div([     
                'Not enough variables to perform {}-factor ANOVA'.format(anova)
                ])
        elif variables ==2:
            if anova ==1:
                table = html.Div()
                if contents:
                    contents = contents[0]
                    filename = filename[0]
                    df = parse_data(contents, filename)
                    df=df.set_index([df.columns[0],df.columns[1]])
                    df_plotting = df.stack().reset_index() 
                    df_plotting.columns = ['factor', 'factor2', 'compound', 'value']
                    alpha_anova = 0.1

                    keys = []
                    tables =  []
                    X = df_plotting
                    for variable in df_plotting['compound'].unique():
                        model = ols('value ~ C(factor)', data=X[X['compound']==variable]).fit()
                        anova_table = sm.stats.anova_lm(model, typ=2)
                        keys.append(variable)
                        tables.append(anova_table)
                    df_anova = pd.concat(tables, keys=keys, axis=0)
                    df_anova['PR(>F)'] = round(df_anova['PR(>F)'], 3)#.apply(round())
                    df_anova['F'] = round(df_anova['F'], 1)#.apply(round())
                    df_anova[df_anova == 'NaN'] 
                    df_anova = df_anova.reset_index()
                    df_anova = df_anova[df_anova['level_1'] == 'C(factor)']	
                    table = html.Div([
                        html.H5(filename),
                        dash_table.DataTable(
                            data=df_anova.to_dict('rows'),
                            columns=[{'name': i, 'id': i} for i in df_anova.columns]
                        ),
                        html.Hr(),
                        html.Div('Raw Content'),
                        html.Pre(contents[0:200] + '...', style={
                            'whiteSpace': 'pre-wrap',
                            'wordBreak': 'break-all'
                        })
                    ])
                return table
            elif anova ==2:
                table = html.Div()
                if contents:
                    contents = contents[0]
                    filename = filename[0]
                    df = parse_data(contents, filename)
                    df=df.set_index([df.columns[0],df.columns[1]])
                    df_plotting = df.stack().reset_index() 
                    df_plotting.columns = ['factor', 'factor2', 'compound', 'value']
                    alpha_anova = 0.1

                    keys = []
                    tables =  []
                    X = df_plotting
                    for variable in df_plotting['compound'].unique():
                        model = ols('value ~ C(factor):C(factor2)', data=X[X['compound']==variable]).fit()
                        anova_table = sm.stats.anova_lm(model, typ=2)
                        keys.append(variable)
                        tables.append(anova_table)
                    df_anova = pd.concat(tables, keys=keys, axis=0)
                    df_anova['PR(>F)'] = round(df_anova['PR(>F)'], 3)#.apply(round())
                    df_anova['F'] = round(df_anova['F'], 1)#.apply(round())
                    df_anova[df_anova == 'NaN'] 
                    df_anova = df_anova.reset_index()
                    df_anova = df_anova[df_anova['level_1'] == 'C(factor):C(factor2)']	
                    table = html.Div([
                        html.H5(filename),
                        dash_table.DataTable(
                            data=df_anova.to_dict('rows'),
                            columns=[{'name': i, 'id': i} for i in df_anova.columns]
                        ),
                        html.Hr(),
                        html.Div('Raw Content'),
                        html.Pre(contents[0:200] + '...', style={
                            'whiteSpace': 'pre-wrap',
                            'wordBreak': 'break-all'
                        })
                    ])
                return table
            else:
                return html.Div([
                    'Not enough variables to perform {}-factor ANOVA'.format(anova)
                ])
                
        elif variables==3:
            if anova ==1:
                table = html.Div()
                if contents:
                    contents = contents[0]
                    filename = filename[0]
                    df = parse_data(contents, filename)
                    df=df.set_index([df.columns[0],df.columns[1],df.columns[2]])
                    df_plotting = df.stack().reset_index() 
                    df_plotting.columns = ['factor', 'factor2','factor3', 'compound', 'value']
                    alpha_anova = 0.1

                    keys = []
                    tables =  []
                    X = df_plotting
                    for variable in df_plotting['compound'].unique():
                        model = ols('value ~ C(factor)', data=X[X['compound']==variable]).fit()
                        anova_table = sm.stats.anova_lm(model, typ=2)
                        keys.append(variable)
                        tables.append(anova_table)
                    df_anova = pd.concat(tables, keys=keys, axis=0)
                    df_anova['PR(>F)'] = round(df_anova['PR(>F)'], 3)#.apply(round())
                    df_anova['F'] = round(df_anova['F'], 1)#.apply(round())
                    df_anova[df_anova == 'NaN'] 
                    df_anova = df_anova.reset_index()
                    df_anova = df_anova[df_anova['level_1'] == 'C(factor)']	
                    table = html.Div([
                        html.H5(filename),
                        dash_table.DataTable(
                            data=df_anova.to_dict('rows'),
                            columns=[{'name': i, 'id': i} for i in df_anova.columns]
                        ),
                        html.Hr(),
                        html.Div('Raw Content'),
                        html.Pre(contents[0:200] + '...', style={
                            'whiteSpace': 'pre-wrap',
                            'wordBreak': 'break-all'
                        })
                    ])
                return table
            elif anova ==2:
                table = html.Div()
                if contents:
                    contents = contents[0]
                    filename = filename[0]
                    df = parse_data(contents, filename)
                    df=df.set_index([df.columns[0],df.columns[1],df.columns[2]])
                    df_plotting = df.stack().reset_index() 
                    df_plotting.columns = ['factor', 'factor2','factor3', 'compound', 'value']
                    alpha_anova = 0.1

                    keys = []
                    tables =  []
                    X = df_plotting
                    for variable in df_plotting['compound'].unique():
                        model = ols('value ~ C(factor):C(factor2)', data=X[X['compound']==variable]).fit()
                        anova_table = sm.stats.anova_lm(model, typ=2)
                        keys.append(variable)
                        tables.append(anova_table)
                    df_anova = pd.concat(tables, keys=keys, axis=0)
                    df_anova['PR(>F)'] = round(df_anova['PR(>F)'], 3)#.apply(round())
                    df_anova['F'] = round(df_anova['F'], 1)#.apply(round())
                    df_anova[df_anova == 'NaN'] 
                    df_anova = df_anova.reset_index()
                    df_anova = df_anova[df_anova['level_1'] == 'C(factor):C(factor2)']	
                    table = html.Div([
                        html.H5(filename),
                        dash_table.DataTable(
                            data=df_anova.to_dict('rows'),
                            columns=[{'name': i, 'id': i} for i in df_anova.columns]
                        ),
                        html.Hr(),
                        html.Div('Raw Content'),
                        html.Pre(contents[0:200] + '...', style={
                            'whiteSpace': 'pre-wrap',
                            'wordBreak': 'break-all'
                        })
                    ])
                return table
            elif anova==3:
                table = html.Div()
                if contents:
                    contents = contents[0]
                    filename = filename[0]
                    df = parse_data(contents, filename)
                    df=df.set_index([df.columns[0],df.columns[1],df.columns[2]])
                    df_plotting = df.stack().reset_index() 
                    df_plotting.columns = ['factor', 'factor2','factor3', 'compound', 'value']
                    alpha_anova = 0.1

                    keys = []
                    tables =  []
                    X = df_plotting
                    for variable in df_plotting['compound'].unique():
                        model = ols('value ~ C(factor):C(factor2):C(factor3)', data=X[X['compound']==variable]).fit()
                        anova_table = sm.stats.anova_lm(model, typ=2)
                        keys.append(variable)
                        tables.append(anova_table)
                    df_anova = pd.concat(tables, keys=keys, axis=0)
                    df_anova['PR(>F)'] = round(df_anova['PR(>F)'], 3)#.apply(round())
                    df_anova['F'] = round(df_anova['F'], 1)#.apply(round())
                    df_anova[df_anova == 'NaN'] 
                    df_anova = df_anova.reset_index()
                    df_anova = df_anova[df_anova['level_1'] == 'C(factor):C(factor2):C(factor3)']	
                    table = html.Div([
                        html.H5(filename),
                        dash_table.DataTable(
                            data=df_anova.to_dict('rows'),
                            columns=[{'name': i, 'id': i} for i in df_anova.columns]
                        ),
                        html.Hr(),
                        html.Div('Raw Content'),
                        html.Pre(contents[0:200] + '...', style={
                            'whiteSpace': 'pre-wrap',
                            'wordBreak': 'break-all'
                        })
                    ])
                return table
            else:
                return html.Div([
                    'Not enough variables to perform {}-factor ANOVA'.format(anova)
                ])
        else:
            return html.Div([
                    'Number of variables out of bounds'
                ]) 
                
                

                
@app.callback(
    Output('sigdiff','children'),  
    Input('upload-data','contents'),
    Input('upload-data','filename'), 
    Input('submit','n_clicks'),
    State('variables','value'),
    State('anova','value'),
    State('alpha','value'),   
)

def update_table(contents,filename,n_clicks,variables,anova,alpha):
    changed_id = [p['prop_id'] for p in callback_context.triggered][0]
    if 'submit' in changed_id:
        if variables==1:
            if anova==1:
                table = html.Div()
                if contents:
                    contents = contents[0]
                    filename = filename[0]
                    df = parse_data(contents, filename)
                    df=df.set_index([df.columns[0]])
                    df_plotting= df.stack().reset_index(name='value')
                    df_plotting.columns =['factor','compound', 'value']
                    alpha_anova = alpha
                    keys = []
                    tables =  []
                    X = df_plotting
                    for variable in df_plotting['compound'].unique():
                        model = ols('value ~ C(factor)', data=X[X['compound']==variable]).fit()
                        anova_table = sm.stats.anova_lm(model, typ=2)
                        keys.append(variable)
                        tables.append(anova_table)
                    df_anova = pd.concat(tables, keys=keys, axis=0)
                    df_anova['PR(>F)'] = round(df_anova['PR(>F)'], 3)#.apply(round())
                    df_anova['F'] = round(df_anova['F'], 1)#.apply(round())
                    df_anova[df_anova == 'NaN'] 
                    df_anova = df_anova.reset_index()
                    df_anova = df_anova[df_anova['level_1'] == 'C(factor)']	
                    sigdiff = df_anova[df_anova['PR(>F)'] < alpha_anova]['level_0']
                    df_anova=df[sigdiff]
                    df_anova=df_anova.reset_index()
                    table = html.Div([
                        html.H5(filename),
                        dash_table.DataTable(
                            data=df_anova.to_dict('rows'),
                            columns=[{'name': i, 'id': i} for i in df_anova.columns],
                            export_format='csv'
                        ),
                        html.Hr(),
                        html.Div('Raw Content'),
                        html.Pre(contents[0:200] + '...', style={
                            'whiteSpace': 'pre-wrap',
                            'wordBreak': 'break-all'
                        })
                    ])
                return table
            else:
                return None
        
        elif variables ==2:
            if anova ==1:
                
                table = html.Div()
                if contents:
                    contents = contents[0]
                    filename = filename[0]
                    df = parse_data(contents, filename)
                    df=df.set_index([df.columns[0],df.columns[1]])
                    df_plotting = df.stack().reset_index() 
                    df_plotting.columns = ['factor', 'factor2', 'compound', 'value']
#                     df_plotting['factor']=df_plotting['factor'].astype(str)+'_'+df_plotting['factor2'].astype(str)
#                     df_plotting=df_plotting.drop(['factor2'],axis=1)
                    alpha_anova = alpha

                    keys = []
                    tables =  []
                    X = df_plotting

                    for variable in df_plotting['compound'].unique():
                        model = ols('value ~ C(factor)', data=X[X['compound']==variable]).fit()
                        anova_table = sm.stats.anova_lm(model, typ=2)
                        keys.append(variable)
                        tables.append(anova_table)
                    df_anova = pd.concat(tables, keys=keys, axis=0)
                    df_anova['PR(>F)'] = round(df_anova['PR(>F)'], 3)#.apply(round())
                    df_anova['F'] = round(df_anova['F'], 1)#.apply(round())
                    df_anova[df_anova == 'NaN'] 
                    df_anova = df_anova.reset_index()
                    df_anova = df_anova[df_anova['level_1'] == 'C(factor)']	
                    sigdiff = df_anova[df_anova['PR(>F)'] < alpha_anova]['level_0']
                    df_sigdiff=df[sigdiff]
                    df_sigdiff=df_sigdiff.reset_index()
                    df_sigdiff['Output_ID']=df_sigdiff[df_sigdiff.columns[0]].astype(str)+'_'+df_sigdiff[df_sigdiff.columns[1]].astype(str)
                    df_sigdiff=df_sigdiff.drop([df_sigdiff.columns[0],df_sigdiff.columns[1]],axis=1)
                    newcol=df_sigdiff.pop('Output_ID')
                    df_sigdiff.insert(0,'Output_ID',newcol)
                    table = html.Div([
                        html.H5(filename),
                        dash_table.DataTable(
                            data=df_sigdiff.to_dict('rows'),
                            columns=[{'name': i, 'id': i} for i in df_sigdiff.columns],
                            export_format='csv'
                        ),
                        html.Hr(),
                        html.Div('Raw Content'),
                        html.Pre(contents[0:200] + '...', style={
                            'whiteSpace': 'pre-wrap',
                            'wordBreak': 'break-all'
                        })
                    ])
                return table
            elif anova==2:
                table = html.Div()
                if contents:
                    contents = contents[0]
                    filename = filename[0]
                    df = parse_data(contents, filename)
                    df=df.set_index([df.columns[0],df.columns[1]])
                    df_plotting = df.stack().reset_index() 
                    df_plotting.columns = ['factor', 'factor2', 'compound', 'value']
                    alpha_anova = alpha

                    keys = []
                    tables =  []
                    X = df_plotting
                    for variable in df_plotting['compound'].unique():
                        model = ols('value ~ C(factor):C(factor2)', data=X[X['compound']==variable]).fit()
                        anova_table = sm.stats.anova_lm(model, typ=2)
                        keys.append(variable)
                        tables.append(anova_table)
                    df_anova = pd.concat(tables, keys=keys, axis=0)
                    df_anova['PR(>F)'] = round(df_anova['PR(>F)'], 3)#.apply(round())
                    df_anova['F'] = round(df_anova['F'], 1)#.apply(round())
                    df_anova[df_anova == 'NaN'] 
                    df_anova = df_anova.reset_index()
                    df_anova = df_anova[df_anova['level_1'] == 'C(factor):C(factor2)']
                    sigdiff = df_anova[df_anova['PR(>F)'] < alpha_anova]['level_0']
                    df_sigdiff=df[sigdiff]
                    df_sigdiff=df_sigdiff.reset_index()
                    df_sigdiff['Output_ID']=df_sigdiff[df_sigdiff.columns[0]].astype(str)+'_'+df_sigdiff[df_sigdiff.columns[1]].astype(str)
                    df_sigdiff=df_sigdiff.drop([df_sigdiff.columns[0],df_sigdiff.columns[1]],axis=1)
                    newcol=df_sigdiff.pop('Output_ID')
                    df_sigdiff.insert(0,'Output_ID',newcol)
                    table = html.Div([
                        html.H5(filename),
                        dash_table.DataTable(
                            data=df_sigdiff.to_dict('rows'),
                            columns=[{'name': i, 'id': i} for i in df_sigdiff.columns],
                            export_format='csv'
                        ),
                        html.Hr(),
                        html.Div('Raw Content'),
                        html.Pre(contents[0:200] + '...', style={
                            'whiteSpace': 'pre-wrap',
                            'wordBreak': 'break-all'
                        })
                    ])
                return table
            else:
                return None
                
        elif variables ==3:
            if anova ==1:
                
                table = html.Div()
                if contents:
                    contents = contents[0]
                    filename = filename[0]
                    df = parse_data(contents, filename)
                    df=df.set_index([df.columns[0],df.columns[1],df.columns[2]])
                    df_plotting = df.stack().reset_index() 
                    df_plotting.columns = ['factor', 'factor2','factor3', 'compound', 'value']
#                     df_plotting['factor1+factor2+factor3']=df_plotting['factor'].astype(str)+'_'+df_plotting['factor2'].astype(str)+'_'+df_plotting['factor3']
#                     df_plotting=df_plotting.drop(['factor','factor2','factor3'],axis=1)
#                     df_plotting=df_plotting[['factor1+factor2+factor3','rep','compound','value']]
#                     df_plotting.columns=['factor','rep','compound','value']
                    alpha_anova = alpha

                    keys = []
                    tables =  []
                    X = df_plotting

                    for variable in df_plotting['compound'].unique():
                        model = ols('value ~ C(factor)', data=X[X['compound']==variable]).fit()
                        anova_table = sm.stats.anova_lm(model, typ=2)
                        keys.append(variable)
                        tables.append(anova_table)
                    df_anova = pd.concat(tables, keys=keys, axis=0)
                    df_anova['PR(>F)'] = round(df_anova['PR(>F)'], 3)#.apply(round())
                    df_anova['F'] = round(df_anova['F'], 1)#.apply(round())
                    df_anova[df_anova == 'NaN'] 
                    df_anova = df_anova.reset_index()
                    df_anova = df_anova[df_anova['level_1'] == 'C(factor)']	
                    sigdiff = df_anova[df_anova['PR(>F)'] < alpha_anova]['level_0']
                    df_sigdiff=df[sigdiff]
                    df_sigdiff=df_sigdiff.reset_index()
                    df_sigdiff['Output_ID']=df_sigdiff[df_sigdiff.columns[0]].astype(str)+'_'+df_sigdiff[df_sigdiff.columns[1]].astype(str)+'_'+df_sigdiff[df_sigdiff.columns[2]].astype(str)
                    df_sigdiff=df_sigdiff.drop([df_sigdiff.columns[0],df_sigdiff.columns[1],df_sigdiff.columns[2]],axis=1)
                    newcol=df_sigdiff.pop('Output_ID')
                    df_sigdiff.insert(0,'Output_ID',newcol)

                    table = html.Div([
                        html.H5(filename),
                        dash_table.DataTable(
                            data=df_sigdiff.to_dict('rows'),
                            columns=[{'name': i, 'id': i} for i in df_sigdiff.columns],
                            export_format='csv'
                        ),
                        html.Hr(),
                        html.Div('Raw Content'),
                        html.Pre(contents[0:200] + '...', style={
                            'whiteSpace': 'pre-wrap',
                            'wordBreak': 'break-all'
                        })
                    ])
                return table
            elif anova==2:
                table = html.Div()
                if contents:
                    contents = contents[0]
                    filename = filename[0]
                    df = parse_data(contents, filename)
                    df=df.set_index([df.columns[0],df.columns[1],df.columns[2]])
                    df_plotting = df.stack().reset_index() 
                    df_plotting.columns = ['factor', 'factor2','factor3', 'compound', 'value']
#                     df_plotting['factor1+factor2']=df_plotting['factor'].astype(str)+'_'+df_plotting['factor2'].astype(str)
#                     df_plotting=df_plotting.drop(['factor','factor2'],axis=1)
#                     df_plotting=df_plotting[['factor1+factor2','factor3','compound','value']]
#                     df_plotting.columns=['factor','factor2','compound','value']
                    alpha_anova = alpha

                    keys = []
                    tables =  []
                    X = df_plotting
                    for variable in df_plotting['compound'].unique():
                        model = ols('value ~ C(factor):C(factor2)', data=X[X['compound']==variable]).fit()
                        anova_table = sm.stats.anova_lm(model, typ=2)
                        keys.append(variable)
                        tables.append(anova_table)
                    df_anova = pd.concat(tables, keys=keys, axis=0)
                    df_anova['PR(>F)'] = round(df_anova['PR(>F)'], 3)#.apply(round())
                    df_anova['F'] = round(df_anova['F'], 1)#.apply(round())
                    df_anova[df_anova == 'NaN'] 
                    df_anova = df_anova.reset_index()
                    df_anova = df_anova[df_anova['level_1'] == 'C(factor):C(factor2)']	
                    sigdiff = df_anova[df_anova['PR(>F)'] < alpha_anova]['level_0']
                    df_sigdiff=df[sigdiff]
                    df_sigdiff=df_sigdiff.reset_index()
                    df_sigdiff['Output_ID']=df_sigdiff[df_sigdiff.columns[0]].astype(str)+'_'+df_sigdiff[df_sigdiff.columns[1]].astype(str)+'_'+df_sigdiff[df_sigdiff.columns[2]].astype(str)
                    df_sigdiff=df_sigdiff.drop([df_sigdiff.columns[0],df_sigdiff.columns[1],df_sigdiff.columns[2]],axis=1)
                    newcol=df_sigdiff.pop('Output_ID')
                    df_sigdiff.insert(0,'Output_ID',newcol)

                    table = html.Div([
                        html.H5(filename),
                        dash_table.DataTable(
                            data=df_sigdiff.to_dict('rows'),
                            columns=[{'name': i, 'id': i} for i in df_sigdiff.columns],
                            export_format='csv'
                        ),
                        html.Hr(),
                        html.Div('Raw Content'),
                        html.Pre(contents[0:200] + '...', style={
                            'whiteSpace': 'pre-wrap',
                            'wordBreak': 'break-all'
                        })
                    ])
                return table
            elif anova==3:
                table = html.Div()
                if contents:
                    contents = contents[0]
                    filename = filename[0]
                    df = parse_data(contents, filename)
                    df=df.set_index([df.columns[0],df.columns[1],df.columns[2]])
                    df_plotting = df.stack().reset_index() 
                    df_plotting.columns = ['factor', 'factor2','factor3', 'compound', 'value']
                    alpha_anova = alpha

                    keys = []
                    tables =  []
                    X = df_plotting
                    for variable in df_plotting['compound'].unique():
                        model = ols('value ~ C(factor):C(factor2):C(factor3)', data=X[X['compound']==variable]).fit()
                        anova_table = sm.stats.anova_lm(model, typ=2)
                        keys.append(variable)
                        tables.append(anova_table)
                    df_anova = pd.concat(tables, keys=keys, axis=0)
                    df_anova['PR(>F)'] = round(df_anova['PR(>F)'], 3)#.apply(round())
                    df_anova['F'] = round(df_anova['F'], 1)#.apply(round())
                    df_anova[df_anova == 'NaN'] 
                    df_anova = df_anova.reset_index()
                    df_anova = df_anova[df_anova['level_1'] == 'C(factor):C(factor2):C(factor3)']
                    sigdiff = df_anova[df_anova['PR(>F)'] < alpha_anova]['level_0']
                    df_sigdiff=df[sigdiff]
                    df_sigdiff=df_sigdiff.reset_index()
                    df_sigdiff['Output_ID']=df_sigdiff[df_sigdiff.columns[0]].astype(str)+'_'+df_sigdiff[df_sigdiff.columns[1]].astype(str)+'_'+df_sigdiff[df_sigdiff.columns[2]].astype(str)
                    df_sigdiff=df_sigdiff.drop([df_sigdiff.columns[0],df_sigdiff.columns[1],df_sigdiff.columns[2]],axis=1)
                    newcol=df_sigdiff.pop('Output_ID')
                    df_sigdiff.insert(0,'Output_ID',newcol)

                    table = html.Div([
                        html.H5(filename),
                        dash_table.DataTable(
                            data=df_sigdiff.to_dict('rows'),
                            columns=[{'name': i, 'id': i} for i in df_sigdiff.columns],
                            export_format='csv'
                        ),
                        html.Hr(),
                        html.Div('Raw Content'),
                        html.Pre(contents[0:200] + '...', style={
                            'whiteSpace': 'pre-wrap',
                            'wordBreak': 'break-all'
                        })
                    ])
                return table
            else: return None
        else: return None
                
    
    
    

if __name__ == '__main__':
    app.run_server(debug=True, use_reloader=False,port=8000)