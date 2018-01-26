import dash_core_components as dcc
import dash_html_components as html
from dash import Dash
from dash.dependencies import Input, Output, State
from flask import Flask, request

server = Flask(__name__)
app = Dash(__name__, server=server)

app.css.append_css({'external_url': 'https://codepen.io/chriddyp/pen/bWLwgP.css'})
# dcc._css_dist[0]['relative_package_path'].append('style.css')

app.layout = html.Div([
    html.Div(
        id='notification'
    ),
    # title
    html.H1('YoutubeStats'),
    # description
    html.Div('''
        A web application that provides statistics on youtube comments
    '''),
    # a div for inputting the data
    html.Div([
        html.Button(children='Submit', id='submit-videoId', style={'margin-right': '1%'}),

        dcc.Input(
            placeholder='Enter a value...',
            type='text',
            value='',
            id='input-videoId'
        )
    ], style={'textAlign': 'center', 'marging-top': '3%'}),
    html.Div(id='output'),

    # a row contains two columns dividing the screen
    html.Div(children=[
        # 1st column
        html.Div(children=[
        ], className='six columns'),
        # 2nd column
        html.Div(children=[
        ], className='six columns')

    ], className='row')
])


@app.callback(Output('output', 'children'),
              [Input('submit-videoId', 'n_clicks')],
              [State('input-videoId', 'value')])
def update_output(n_clicks, videoId):
    return '''comments for video is : {}'''.format(videoId)


@server.route('/youtubestats/api/v1/gender', methods=['POST'])
def genderdata_resuls():
    if request is not None and request.json:
        if request.json['status'] == 'success':
            msg = '''finished loading gender data for comments of youtube video with the ID {} '''.format(
                request.json['videoId'])
        else:
            msg = '''failed to loading gender data for comments of youtube video with the ID {} '''.format(
                request.json['videoId'])
        # pushnotification(msg)
        return 'ok', 200


@app.callback(Output('notification', 'children'))
def pushnotification(message):
    print('push')
    return message


if __name__ == '__main__':
    app.run_server(debug=True)
