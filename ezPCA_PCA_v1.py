"""
@authors: Marcel Hensel & Jochen Vestner
Watch out! This version uses global variables!
The app should therefore only be used from a single user! Not in production!
© Marcel Hensel & Jochen Vestner 2022
"""

import itertools
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
import plotly.express as px
from sklearn.decomposition import PCA
import numpy as np
import plotly.express as px
import dash_draggable
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
server = app.server
colors = {
    "graphBackground": "#F5F5F5",
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
        )],className='six columns'),
    html.Div([
        dcc.Upload(
            id='upload-meta-data',
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
            multiple=True
        )],className='six columns'),
    html.Div([
        html.Div([  
            html.H3('PCA Output with selection of principal components'),
            html.Button('2D plot',id='2d',n_clicks=0),
            html.Button('3D plot',id='3d',n_clicks=0),
            dcc.RadioItems(
                id='show-text',
                options=[{'label': i, 'value': i} for i in ['Show data labels', 'Hide data labels']],
                value='Hide data labels',
                labelStyle={'display': 'inline-block'})
        ])],className='row'),
        html.Div([
            html.Div([
                dcc.Graph(id='scores',config=dict({'editable':True,'edits':dict({'annotationPosition':True}),}))
            ],className='six columns'),
        html.Div([
            dcc.Graph(id='loadings',config=dict({'editable':True,'edits':dict({'annotationPosition':True})}))
        ],className='six columns')
    ],className='row'),
    html.Div([html.H4('Choose principal components and color the PCA after metafile')],className='row'),
    html.Div([           
            html.Div([   
                html.P('Choose x-Axis'),
                dcc.Slider(id='PC_selectorx',min=1,max=5,value=1,step=1),
                html.P('Choose y-Axis'),
                dcc.Slider(id='PC_selectory',min=1,max=5,value=2,step=1),
                html.P('Choose z-axis (if 3D plot is enabled)'),
                dcc.Slider(id='PC_selectorz',min=1,max=5,value=3,step=1)],className='six columns'),
            html.Div([ 
                html.P('Please select a metafile column to color the graphs'),
                dcc.Input(id='metafilecolumn',type='number',min=1,value=1,debounce=True),
                html.Div(id='output-meta-upload'),
                html.Div(id='table')],className='six columns'
                )]), 
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
@app.callback(
    Output('scores','figure'), 
    [
    Input('2d','n_clicks'),
    Input('3d','n_clicks'),
    Input('show-text','value'),
    Input('PC_selectorx','value'),
    Input('PC_selectory','value'),
    Input('PC_selectorz','value'),
    Input('metafilecolumn','value'),
    Input('upload-data','contents'),
    Input('upload-data','filename'),
    Input('upload-meta-data','contents'),
    Input('upload-meta-data','filename')
    ])

def displayClick(btn1,btn2,toggle_value,xaxis,yaxis,zaxis,value,contents,filename,meta_contents,meta_filename):
    changed_id = [p['prop_id'] for p in callback_context.triggered][0]
    if '2d' in changed_id: 
        if toggle_value =='Show data labels':
            fig = {
                'layout': go.Layout(
                plot_bgcolor=colors["graphBackground"],
                paper_bgcolor=colors["graphBackground"])
            }
            if contents:
                contents = contents[0]
                filename = filename[0]
                meta_contents=meta_contents[0]
                meta_filename=meta_filename[0]
                df = parse_data(contents, filename)
                df1=df.set_index([df.columns[0]])
                X_scaled=df1.to_numpy()
                df2=meta_data(meta_contents,meta_filename)
                pca = PCA(n_components=5)
                scores = pd.DataFrame(pca.fit_transform(X_scaled), index = df1.index)
                loadings = pca.components_.T * np.sqrt(pca.explained_variance_)
                loadings = pd.DataFrame(loadings, index=df1.columns)
                PCx=xaxis
                PCy=yaxis
                alpha=1
                trace1=go.Scatter(
                    x = scores.iloc[0:,xaxis-1],
                    y = scores.iloc[0:,yaxis-1],
                    text=df1.index,
                    mode='markers+text')
                fig=px.scatter(x=scores.iloc[0:,xaxis-1],y=scores.iloc[0:,yaxis-1],color=df2[df2.columns[value-1]].astype(str),)
                maxxyscores = np.max([abs(np.min([trace1['x'],trace1['y']])), abs(np.max([trace1['x'],trace1['y']]))])
                fig.update_layout(title_text="PCA Output"+' (expl. var. ' + str(round(pca.explained_variance_ratio_[PCx-1]*100 + pca.explained_variance_ratio_[PCy-1]*100,1)) +'%)',)

                fig.update_xaxes(linecolor='#111111', mirror=True,zerolinecolor='lightgrey',range=[-maxxyscores-.5,maxxyscores+.5],title='PC' + str(PCx) + ' (expl. var. ' + str(round(pca.explained_variance_ratio_[PCx-1]*100,1)) + '%)')
                fig.update_yaxes(linecolor='#111111', mirror=True,zerolinecolor='lightgrey',range=[-maxxyscores-.5,maxxyscores+.5],title='PC' + str(PCy) + ' (expl. var. ' + str(round(pca.explained_variance_ratio_[PCy-1]*100,1)) + '%)')
                fig.update_coloraxes(showscale=True)
                fig.update_layout(height=750,width=900,showlegend=True,plot_bgcolor='#ffffff',legend=dict(title=df2.columns[value-1]))
                for i,j,k in zip(scores.iloc[0:,xaxis-1],scores.iloc[0:,yaxis-1],df2[df2.columns[0]]):
                               fig.add_annotation(x=i,y=j,text=k)
            return fig            
        else:
            fig = {
                'layout': go.Layout(
                    plot_bgcolor=colors["graphBackground"],
                    paper_bgcolor=colors["graphBackground"])
            }
            if contents:
                contents = contents[0]
                filename = filename[0]
                meta_contents=meta_contents[0]
                meta_filename=meta_filename[0]
                df = parse_data(contents, filename)
                df1=df.set_index([df.columns[0]])
                X_scaled=df1.to_numpy()
                df2=meta_data(meta_contents,meta_filename)
                pca = PCA(n_components=5)
                scores = pd.DataFrame(pca.fit_transform(X_scaled), index = df1.index)
                loadings = pca.components_.T * np.sqrt(pca.explained_variance_)
                loadings = pd.DataFrame(loadings, index=df1.columns)
                PCx=xaxis
                PCy=yaxis
                alpha=1
                trace1=go.Scatter(
                    x = scores.iloc[0:,xaxis-1],
                    y = scores.iloc[0:,yaxis-1],
                    text=df1.index,
                    mode='markers+text')
                fig=px.scatter(x=scores.iloc[0:,xaxis-1],y=scores.iloc[0:,yaxis-1],color=df2[df2.columns[value-1]].astype(str))
                maxxyscores = np.max([abs(np.min([trace1['x'],trace1['y']])), abs(np.max([trace1['x'],trace1['y']]))])
                fig.update_layout(title_text="PCA Output"+' (expl. var. ' + str(round(pca.explained_variance_ratio_[PCx-1]*100 + pca.explained_variance_ratio_[PCy-1]*100,1)) +'%)',)

                fig.update_xaxes(linecolor='#111111', mirror=True,zerolinecolor='lightgrey',range=[-maxxyscores-.5,maxxyscores+.5],title='PC' + str(PCx) + ' (expl. var. ' + str(round(pca.explained_variance_ratio_[PCx-1]*100,1)) + '%)')
                fig.update_yaxes(linecolor='#111111', mirror=True,zerolinecolor='lightgrey',range=[-maxxyscores-.5,maxxyscores+.5],title='PC' + str(PCy) + ' (expl. var. ' + str(round(pca.explained_variance_ratio_[PCy-1]*100,1)) + '%)')
                fig.update_coloraxes(showscale=True)
                fig.update_layout(height=750,width=900,showlegend=True,plot_bgcolor='#ffffff',legend=dict(title=df2.columns[value-1]))
            return fig
    elif '3d' in changed_id:
        if toggle_value =='Show data labels':
            fig = {
                'layout': go.Layout(
                    plot_bgcolor=colors["graphBackground"],
                    paper_bgcolor=colors["graphBackground"])
            }

            if contents:
                contents = contents[0]
                filename = filename[0]
                meta_contents=meta_contents[0]
                meta_filename=meta_filename[0]
                df = parse_data(contents, filename)
                df1=df.set_index([df.columns[0]])
                X_scaled=df1.to_numpy()
                df2=meta_data(meta_contents,meta_filename)
                pca = PCA(n_components=5)
                scores = pd.DataFrame(pca.fit_transform(X_scaled), index = df1.index)
                loadings = pca.components_.T * np.sqrt(pca.explained_variance_)
                loadings = pd.DataFrame(loadings, index=df1.columns)
                PCx=xaxis
                PCy=yaxis
                PCz=zaxis
                alpha=1
                trace1=go.Scatter3d(
                    x = scores.iloc[0:,xaxis-1],
                    y = scores.iloc[0:,yaxis-1],
                    z = scores.iloc[0:,zaxis-1],
                    text=df1.index,
                    mode='markers+text')
                fig=px.scatter_3d(x=scores.iloc[0:,xaxis-1],y=scores.iloc[0:,yaxis-1],z=scores.iloc[0:,zaxis-1],color=df2[df2.columns[value-1]].astype(str),text=df2[df2.columns[0]])
                maxxyscores = np.max([abs(np.min([trace1['x'],trace1['y'],trace1['z']])), abs(np.max([trace1['x'],trace1['y'],trace1['z']]))])
                fig.update_layout(title_text="PCA Output"+' (expl. var. ' + str(round(pca.explained_variance_ratio_[PCx-1]*100 + pca.explained_variance_ratio_[PCy-1]*100,1)) +'%)',showlegend=True)
                fig.update_scenes(xaxis = dict(autorange=False,
                                              backgroundcolor="rgba(0, 0, 0,0)",
                                              gridcolor="lightgrey",
                                              showbackground=True,
                                              zerolinecolor="black",linecolor='black',mirror=True),
                                      yaxis = dict(autorange=False,
                                              backgroundcolor="rgba(0, 0, 0,0)",
                                              gridcolor="lightgrey",
                                              showbackground=True,
                                              zerolinecolor="black",linecolor='black',mirror=True),
                                      zaxis = dict(autorange=False,
                                              backgroundcolor="rgba(0, 0, 0,0)",
                                              gridcolor="lightgrey",
                                              showbackground=True,
                                              zerolinecolor="black",linecolor='black',mirror=True),
                                     xaxis_title='PC'+ str(PCx) + ' (expl. var. ' + str(round(pca.explained_variance_ratio_[PCx-1]*100,1)) + '%)',
                                     yaxis_title='PC' + str(PCy) + ' (expl. var. ' + str(round(pca.explained_variance_ratio_[PCy-1]*100,1)) + '%)',
                                     zaxis_title='PC' + str(PCz) + ' (expl. var. ' + str(round(pca.explained_variance_ratio_[PCz-1]*100,1)) + '%)',)
                fig.update_layout(scene = dict( aspectmode='cube'))
                fig.update_layout(autosize=False,scene = dict(
                    xaxis = dict(range=[-maxxyscores-.5,maxxyscores+.5]),
                    yaxis = dict(range=[-maxxyscores-.5,maxxyscores+.5]),
                    zaxis = dict(range=[-maxxyscores-.5,maxxyscores+.5])))
                fig.update_layout(height=750,width=900,showlegend=True,plot_bgcolor='#ffffff',legend=dict(title=df2.columns[value-1]))

            return fig
        else:
            fig = {
                'layout': go.Layout(
                    plot_bgcolor=colors["graphBackground"],
                    paper_bgcolor=colors["graphBackground"])
            }

            if contents:
                contents = contents[0]
                filename = filename[0]
                meta_contents=meta_contents[0]
                meta_filename=meta_filename[0]
                df = parse_data(contents, filename)
                df1=df.set_index([df.columns[0]])
                X_scaled=df1.to_numpy()
                df2=meta_data(meta_contents,meta_filename)
                pca = PCA(n_components=5)
                scores = pd.DataFrame(pca.fit_transform(X_scaled), index = df1.index)
                loadings = pca.components_.T * np.sqrt(pca.explained_variance_)
                loadings = pd.DataFrame(loadings, index=df1.columns)
                PCx=xaxis
                PCy=yaxis
                PCz=zaxis
                alpha=1
                trace1=go.Scatter3d(
                    x = scores.iloc[0:,xaxis-1],
                    y = scores.iloc[0:,yaxis-1],
                    z = scores.iloc[0:,zaxis-1],
                    text=df1.index,
                    mode='markers+text')
                fig=px.scatter_3d(x=scores.iloc[0:,xaxis-1],y=scores.iloc[0:,yaxis-1],z=scores.iloc[0:,zaxis-1],color=df2[df2.columns[value-1]].astype(str))
                maxxyscores = np.max([abs(np.min([trace1['x'],trace1['y'],trace1['z']])), abs(np.max([trace1['x'],trace1['y'],trace1['z']]))])
                fig.update_layout(title_text="PCA Output"+' (expl. var. ' + str(round(pca.explained_variance_ratio_[PCx-1]*100 + pca.explained_variance_ratio_[PCy-1]*100,1)) +'%)',showlegend=True)
                fig.update_scenes(xaxis = dict(autorange=False,
                                              backgroundcolor="rgba(0, 0, 0,0)",
                                              gridcolor="lightgrey",
                                              showbackground=True,
                                              zerolinecolor="black",linecolor='black',mirror=True),
                                      yaxis = dict(autorange=False,
                                              backgroundcolor="rgba(0, 0, 0,0)",
                                              gridcolor="lightgrey",
                                              showbackground=True,
                                              zerolinecolor="black",linecolor='black',mirror=True),
                                      zaxis = dict(autorange=False,
                                              backgroundcolor="rgba(0, 0, 0,0)",
                                              gridcolor="lightgrey",
                                              showbackground=True,
                                              zerolinecolor="black",linecolor='black',mirror=True),
                                     xaxis_title='PC'+ str(PCx) + ' (expl. var. ' + str(round(pca.explained_variance_ratio_[PCx-1]*100,1)) + '%)',
                                     yaxis_title='PC' + str(PCy) + ' (expl. var. ' + str(round(pca.explained_variance_ratio_[PCy-1]*100,1)) + '%)',
                                     zaxis_title='PC' + str(PCz) + ' (expl. var. ' + str(round(pca.explained_variance_ratio_[PCz-1]*100,1)) + '%)',)
                fig.update_layout(scene = dict( aspectmode='cube'))
                fig.update_layout(autosize=False,scene = dict(
                    xaxis = dict(range=[-maxxyscores-.5,maxxyscores+.5]),
                    yaxis = dict(range=[-maxxyscores-.5,maxxyscores+.5]),
                    zaxis = dict(range=[-maxxyscores-.5,maxxyscores+.5])))
                fig.update_layout(height=750,width=900,showlegend=True,plot_bgcolor='#ffffff',legend=dict(title=df2.columns[value-1]))

            return fig

            

    else:
        fig = {
            'layout': go.Layout(
                plot_bgcolor=colors["graphBackground"],
                paper_bgcolor=colors["graphBackground"])
        }
        return fig
@app.callback(
    Output('loadings','figure'), 
    [
    Input('2d','n_clicks'),
    Input('3d','n_clicks'),
    Input('PC_selectorx','value'),
    Input('PC_selectory','value'),
    Input('PC_selectorz','value'),
    Input('upload-data','contents'),
    Input('upload-data','filename'),
    Input('upload-meta-data','contents'),
    Input('upload-meta-data','filename')
    ])
def displayClick(btn1,btn2,xaxis,yaxis,zaxis,contents,filename,meta_contents,meta_filename):
    changed_id = [p['prop_id'] for p in callback_context.triggered][0]
    if '2d' in changed_id: 
        fig = {
            'layout': go.Layout(
                plot_bgcolor=colors["graphBackground"],
                paper_bgcolor=colors["graphBackground"])
        }
        if contents:
            contents = contents[0]
            filename = filename[0]
            meta_contents=meta_contents[0]
            meta_filename=meta_filename[0]
            df = parse_data(contents, filename)
            df1=df.set_index([df.columns[0]])
            X_scaled=df1.to_numpy()
            df2=meta_data(meta_contents,meta_filename)
            pca = PCA(n_components=5)
            scores = pd.DataFrame(pca.fit_transform(X_scaled), index = df1.index)
            loadings = pca.components_.T * np.sqrt(pca.explained_variance_)
            loadings = pd.DataFrame(loadings, index=df1.columns)
            PCx=xaxis
            PCy=yaxis
            alpha=1
            trace2=go.Scatter(
                x = loadings.iloc[0:,xaxis-1],
                y = loadings.iloc[0:,yaxis-1],
                text=df1.index,
                mode='markers+text')
            fig=px.scatter(x=loadings.iloc[0:,xaxis-1],y=loadings.iloc[0:,yaxis-1])
            maxxyloadings=np.max([abs(np.min([trace2['x'],trace2['y']])), abs(np.max([trace2['x'],trace2['y']]))])
            fig.update_layout(title_text="PCA Output"+' (expl. var. ' + str(round(pca.explained_variance_ratio_[PCx-1]*100 + pca.explained_variance_ratio_[PCy-1]*100,1)) +'%)',showlegend=True)
            
            fig.update_xaxes(linecolor='#111111', mirror=True,zerolinecolor='lightgrey',range=[-maxxyloadings-.5,maxxyloadings+.5],title='PC' + str(PCx) + ' (expl. var. ' + str(round(pca.explained_variance_ratio_[PCx-1]*100,1)) + '%)')
            fig.update_yaxes(linecolor='#111111', mirror=True,zerolinecolor='lightgrey',range=[-maxxyloadings-.5,maxxyloadings+.5],title='PC' + str(PCy) + ' (expl. var. ' + str(round(pca.explained_variance_ratio_[PCy-1]*100,1)) + '%)')
            fig.update_coloraxes(showscale=True)
            fig.update_layout(height=750,width=900,showlegend=True,plot_bgcolor='#ffffff')
            for i,j,k in zip(loadings.iloc[0:,xaxis-1],loadings.iloc[0:,yaxis-1],loadings.reset_index()['index']):
                fig.add_annotation(x=i,y=j,text=k)

        return fig
    elif '3d' in changed_id:
        fig = {
            'layout': go.Layout(
                plot_bgcolor=colors["graphBackground"],
                paper_bgcolor=colors["graphBackground"])
                      
        }
        
        if contents:
            contents = contents[0]
            filename = filename[0]
            meta_contents=meta_contents[0]
            meta_filename=meta_filename[0]
            df = parse_data(contents, filename)
            df1=df.set_index([df.columns[0]])
            X_scaled=df1.to_numpy()
            df2=meta_data(meta_contents,meta_filename)
            pca = PCA(n_components=5)
            scores = pd.DataFrame(pca.fit_transform(X_scaled), index = df1.index)
            loadings = pca.components_.T * np.sqrt(pca.explained_variance_)
            loadings = pd.DataFrame(loadings, index=df1.columns)
            PCx=xaxis
            PCy=yaxis
            PCz=zaxis
            alpha=1
            trace1=go.Scatter3d(
                x = loadings.iloc[0:,xaxis-1],
                y = loadings.iloc[0:,yaxis-1],
                z = loadings.iloc[0:,zaxis-1],
                text=df1.index,
                mode='markers+text')
            fig=px.scatter_3d(x=loadings.iloc[0:,xaxis-1],y=loadings.iloc[0:,yaxis-1],z=loadings.iloc[0:,zaxis-1],text=loadings.index)
            maxxyloadings = np.max([abs(np.min([trace1['x'],trace1['y'],trace1['z']])), abs(np.max([trace1['x'],trace1['y'],trace1['z']]))])
            fig.update_layout(title_text="PCA Output"+' (expl. var. ' + str(round(pca.explained_variance_ratio_[PCx-1]*100 + pca.explained_variance_ratio_[PCy-1]*100,1)) +'%)',showlegend=True)
            fig.update_scenes(xaxis = dict(autorange=False,
                                          backgroundcolor="rgba(0, 0, 0,0)",
                                          gridcolor="lightgrey",
                                          showbackground=True,
                                          zerolinecolor="black",linecolor='black',mirror=True),
                                  yaxis = dict(autorange=False,
                                          backgroundcolor="rgba(0, 0, 0,0)",
                                          gridcolor="lightgrey",
                                          showbackground=True,
                                          zerolinecolor="black",linecolor='black',mirror=True),
                                  zaxis = dict(autorange=False,
                                          backgroundcolor="rgba(0, 0, 0,0)",
                                          gridcolor="lightgrey",
                                          showbackground=True,
                                          zerolinecolor="black",linecolor='black',mirror=True),
                                  xaxis_title='PC'+ str(PCx) + ' (expl. var. ' + str(round(pca.explained_variance_ratio_[PCx-1]*100,1)) + '%)',
                                  yaxis_title='PC' + str(PCy) + ' (expl. var. ' + str(round(pca.explained_variance_ratio_[PCy-1]*100,1)) + '%)',
                                  zaxis_title='PC' + str(PCz) + ' (expl. var. ' + str(round(pca.explained_variance_ratio_[PCz-1]*100,1)) + '%)',)

            fig.update_layout(autosize=False,scene = dict(
                xaxis = dict(range=[-maxxyloadings-.5,maxxyloadings+.5]),
                yaxis = dict(range=[-maxxyloadings-.5,maxxyloadings+.5]),
                zaxis = dict(range=[-maxxyloadings-.5,maxxyloadings+.5])))
            fig.update_layout(height=750,width=900,showlegend=True,plot_bgcolor='#ffffff',scene = dict( aspectmode='cube'))
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
    Input('upload-meta-data','contents'),
    Input('upload-meta-data','filename'), 
      
)
def update_table(contents, filename):
    table = html.Div()

    if contents:
        contents = contents[0]
        filename = filename[0]
        df = meta_data(contents, filename)

        table = html.Div([
            html.H5(filename),
            dash_table.DataTable(
                data=df.to_dict('rows'),
                columns=[{'name': i, 'id': i,} for i in df.columns]
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
    app.run_server(debug=True, use_reloader=False)
