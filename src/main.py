import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
from flask import Flask, request

from src.controller import Controller
from src.services.etl import ETLService
from src.services.statisticsService import StatisticsService

server = Flask(__name__)
app = dash.Dash(__name__, server=server)
app.scripts.config.serve_locally = True
app.css.append_css({'external_url': 'https://codepen.io/chriddyp/pen/bWLwgP.css'})

app.layout = html.Div([
    ################################  HIDEN INPUT  #####################################
    html.Div(children=[], id='intermediate-data', style={'display': 'none'}),
    html.Div(children=[], id='gender-results'),
    dcc.Input(value='', type='text', id='submit-gender-results', style={'display': 'none'}),
    #################################  HEAD OF PAGE ####################################
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
    ], style={'textAlign': 'center', 'marging-top': '5%', 'marging-bottom': '5%'}),
    ###################################  TABS  #########################################
    dcc.Tabs(
        tabs=[
            {'label': 'General Information', 'value': 1},
            {'label': 'Top Comments', 'value': 2},
            {'label': 'Top Words', 'value': 3},
        ],
        value=3,
        id='tabs',
        vertical=False
    ),
    html.Div(id='tab-output')
], style={
    'fontFamily': 'Sans-Serif',
    'margin-left': 'auto',
    'margin-right': 'auto',
    'marging-top': '5%'
})


# if load etl is a success the video id is put in the div with id=intermediate-data
@app.callback(Output('intermediate-data', 'children'),
              [Input('submit-videoId', 'n_clicks')],
              [State('input-videoId', 'value')])
def etl(n_clicks, videoId):
    res = False
    if videoId:
        res = controller.etl(videoId)
        if not res:
            return "failed"
        return videoId
    return "failed"


@app.callback(Output('tab-output', 'children'),
              [Input('intermediate-data', 'children'),
               Input('tabs', 'value')])
def tabs_controllergeneraldata(children, value):
    if children != "failed":
        if value == 1:
            return general_data_tab(children)

        if value == 2:
            return first_quarter_tab(children)

        if value == 3:
            return frequent_words_tab(children)


def frequent_words_tab(children):
    top_words = controller.get_frequent_words(children)
    words=list(top_words.keys())
    count=list(top_words.values())
    return html.Div([
        html.H3('Top 10 frequent words video with ID ({})'.format(children),
                style={'textAlign': 'center'}),
        dcc.Graph(
            id='example-graph',
            figure={
                'data': [
                    {'x': words, 'y': count, 'type': 'bar', 'name': 'Words Count'},
                ],
                'layout': {
                    'title': 'Top 10 Words'
                }
            }
        )
        ,
        html.Div([
            html.Div([
                html.Div([
                    html.Label('Note* :', style={'color':'green'}),
                    html.P('Top ten frequent words in comments for a video', style={'color': 'green'})
                ], style=style_horGroup),
                html.Div([
                    html.Label('Note* :', style={'color': 'red'}),
                    html.P('''this list doesn't take in account stop words and punctuation''', style={'color': 'green'})
                ], style=style_horGroup),
                html.Div([
                    html.Label('Note* :', style={'color': 'green'}),
                    html.P('''Stemming is performed for supported languages''', style={'color': 'green'})
                ], style=style_horGroup)
            ], id='general-data', style=style_card)
        ], id='tab-container', className='container')
    ])


def general_data_tab(children):
    count = controller.get_comments_count(children)
    most_popular = controller.get_popular_comment(children)
    return html.Div([
        html.H4('General Information', style={'textAlign': 'center'}),
        html.Div([
            # comments count card
            html.Div([
                html.Div([
                    html.Label('Comments count :', style=style_label),
                    html.P(str(count), style=style_label)
                ], style=style_horGroup)
            ], id='general-data', style=style_card),
            # popular comment card
            html.H4('Most popular comment'),
            html.Div(children=generate_commente_card([most_popular], 'most-popular-card'))
        ], id='cards', style={'textAlign': 'center'})
    ], id='tab-container', className='container')


def first_quarter_tab(children):
    quarter = controller.get_first_quarter(children)
    return html.Div([
        html.Div([
            html.H4('Most popular comment'),
            # comments count card
            html.Div([
                html.Div([
                    html.Label('Number of comments :', style=style_label),
                    html.P(str(quarter['length']), style=style_label)
                ], style=style_horGroup)
            ], id='general-data', style=style_card),
            # 1st quarter cards
            html.Div(generate_commente_card(quarter['first_qr'], 'comment'))
        ], id='cards', style={'textAlign': 'center'})
    ], id='tab-container', className='container')


def generate_commente_card(comments: list, id: str):
    cards = []
    for index, comment in enumerate(comments):
        cards.append(
            html.Div([
                html.Div([
                    html.Label('Likes count :', style=style_label),
                    html.P(comment['likes'], style=style_label)
                ], style=style_horGroup),
                html.Div([
                    html.Label('Author :', style=style_label),
                    html.P(comment['author'], style=style_label)
                ], style=style_horGroup),
                html.Div([
                    html.Label('Posting date :', style=style_label),
                    html.P(comment['created_at'].strftime("%B %d, %Y at %H:%M:%S"), style=style_label)
                ], style=style_horGroup),
                html.Div([
                    html.Label('Comment :', style=style_label),
                    html.P(comment['original_comment'], style=style_label)
                ], style=style_horGroup)
            ], id=str(index) + id, style=style_card)
        )
    return cards


msg = ""


#
# message when getting gender data is loaded
@server.route('/youtubestats/api/v1/gender', methods=['POST'])
def genderdata_resuls():
    print('target')
    global msg
    if request.json:
        msg = '''finished '''
    else:
        msg = '''failed  '''
    return 'ok', 200


if __name__ == '__main__':
    stat_service = StatisticsService()
    etl = ETLService()
    controller = Controller(etl, stat_service)
    style_card = {
        'box-shadow': '0 8px 16px 0 rgba(0,0,0,0.2)',
        'width': '100%',
        'border-radius': '2%',
        'padding': '2% 2%'
    }
    style_container = {'padding': '2%', 'marging': '2%'}
    style_label = {'padding': '1% 1% 1% 1%', 'font-size': '1.3em'}
    style_horGroup = {'textAlign': 'left', 'display': 'flex', 'flex-direction': 'row'}
    app.run_server(debug=True)
