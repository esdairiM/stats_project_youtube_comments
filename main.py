import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
from flask import Flask, request

from src.controller import Controller

server = Flask(__name__)
app = dash.Dash(__name__, server=server)
app.config.suppress_callback_exceptions = True
app.scripts.config.serve_locally = True
app.css.append_css({'external_url': 'https://codepen.io/chriddyp/pen/bWLwgP.css'})

app.layout = html.Div([
    ################################  HIDEN INPUT  #####################################
    html.Div(children=[], id='intermediate-data', style={'display': 'none'}),
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
            {'label': 'Gender Data', 'value': 4},
            {'label': 'Search for Expression', 'value': 5}
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

        if value == 4:
            return gender_data_tab(children)
        if value == 5:
            return expression_search_tab(children)


@app.callback(Output('expression-proba', 'children'),
              [Input('submit-expre', 'n_clicks'),
               Input('intermediate-data', 'children')],
              [State('input-expre-one', 'value'),
               State('input-expre-two', 'value')])
def expression_stats(n_clicks, videoId, expression1, expression2):
    if videoId != 'failed' and expression1 != '':
        if expression2 == '':
            res = controller.get_expression_frequency(videoId, expression1)
            return html.Div([
                html.H4('Results', style={'textAlign': 'center'}),
                html.Div([
                    html.Label('Expression          :', style=style_label),
                    html.P(expression1, style=style_label)
                ], style=style_horGroup),
                html.Div([
                    html.Label('Frequency           :', style=style_label),
                    html.P(str(round(res['frequency'],4)), style=style_label)
                ], style=style_horGroup),
                html.Div([
                    html.Label('Mention per comment :', style=style_label),
                    html.P(str(round(res['mpc'],4)), style=style_label)
                ], style=style_horGroup),
                html.Div([
                    html.Div([
                        html.Div([
                            html.Label('Note* :', style={'color': 'green'}),
                            html.P('Frequency is calculated over the entire data set ', style={'color': 'green'})
                        ], style=style_horGroup),
                        html.Div([
                            html.Label('Note* :', style={'color': 'green'}),
                            html.P('Mention per comment is calculated only over the comments where the expression is '
                                   'mentioned ', style={'color': 'green'})
                        ], style=style_horGroup)
                    ], id='general-data', style=style_card)
                ], id='tab-container', className='container')
            ])
        else:
            res = controller.get_expressions_proba(videoId, expression1, expression2)
            return html.Div([
                html.H4('Results', style={'textAlign': 'center'}),
                html.Div([
                    html.Label('Expression one occurrences           :', style=style_label),
                    html.P(str(round(res['ex1_occurence'],4)), style=style_label)
                ], style=style_horGroup),
                html.Div([
                    html.Label('Expression two occurrences           :', style=style_label),
                    html.P(str(round(res['ex2_occurence'],4)), style=style_label)
                ], style=style_horGroup),
                html.Div([
                    html.Label('Expression one Existence probability :', style=style_label),
                    html.P(str(round(res['proba'])), style=style_label)
                ], style=style_horGroup),
                html.Div([
                    html.Div([
                        html.Div([
                            html.Label('Note* :', style={'color': 'green'}),
                            html.P('The probability is that of the existence of the expression one knowing that '
                                   'expression two exists', style={'color': 'green'})
                        ], style=style_horGroup)
                    ], id='general-data', style=style_card)
                ], id='tab-container', className='container')
            ])


def expression_search_tab(videoId):
    ex_card = dict(style_card)
    del ex_card['width']
    # ex_card['padding']='2% 2%'
    return html.Div([
        # row
        html.Div([
            # 1st col
            html.Div([
                html.Label('First expression', style=style_label),
                dcc.Textarea(
                    placeholder='Enter a value...',
                    value='',
                    style={'width': '103%', 'resize': 'none'},
                    id='input-expre-one'
                ),
                html.Label('Second expression', style=style_label),
                dcc.Textarea(
                    placeholder='Enter a value...',
                    value='',
                    style={'width': '103%', 'resize': 'none'},
                    id='input-expre-two'
                ),
                html.Hr(),
                html.Button(children='Search', id='submit-expre', style=style_container)
            ], className="four columns", style=ex_card),
            # 2nd col
            html.Div([
            ], className="eight columns", id='expression-proba', style=ex_card)

            # end row
        ], className='row')
    ], style=style_container)


def gender_data_tab(children):
    resdict = controller.get_gender_percentage(children)
    labels = list(resdict.keys())
    values = list(resdict.values())
    print(labels)
    print(values)
    data = [
        {
            'values': values,
            'labels': labels,
            'type': 'pie',
        },
    ]
    return html.Div([
        html.H3('Gender frequency in comments of video with ID ({})'.format(children),
                style={'textAlign': 'center'}),
        dcc.Graph(
            id='graph',
            figure={
                'data': data,
                'layout': {
                    'margin': {
                        'l': 30,
                        'r': 0,
                        'b': 30,
                        't': 0
                    },
                    'legend': {'x': 0, 'y': 1},
                    'font': {'size': 20}
                }
            }
        )
    ])


def frequent_words_tab(children):
    top_words = controller.get_frequent_words(children)
    words = list(top_words.keys())
    count = list(top_words.values())
    return html.Div([
        html.H3('Top 10 frequent words video with ID ({})'.format(children),
                style={'textAlign': 'center'}),
        dcc.Graph(
            id='frequent-words-graph',
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
                    html.Label('Note* :', style={'color': 'green'}),
                    html.P('Top ten frequent words in comments for a video', style={'color': 'green'})
                ], style=style_horGroup),
                html.Div([
                    html.Label('Note* :', style={'color': 'green'}),
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
    data = controller.get_video_data(children)
    return html.Div([
        html.H4('Video Information', style={'textAlign': 'center'}),
        html.Div([
            # general data card
            html.Div([
                html.Div([
                    html.Label('Video :', style=style_label),
                    html.A(data['title'], href=data['videoUrl'], style=style_label)
                ], style=style_horGroup),
                html.Div([
                    html.Label('View count :', style=style_label),
                    html.P(data['viewCount'], style=style_label)
                ], style=style_horGroup),
                html.Div([
                    html.Label('Likes count :', style=style_label),
                    html.P(data['likeCount'], style=style_label)
                ], style=style_horGroup),
                html.Div([
                    html.Label('Dislike Count :', style=style_label),
                    html.P(data['dislikeCount'], style=style_label)
                ], style=style_horGroup),
                html.Div([
                    html.Label('Channel :', style=style_label),
                    html.A('youtube channel',href=data['channelUrl'], style=style_label)
                ], style=style_horGroup),
                html.Div([
                    html.Label('Comments count :', style=style_label),
                    html.P(str(count), style=style_label)
                ], style=style_horGroup)
            ], id='general-data', style=style_card)
        ], id='cards', style={'textAlign': 'center'})
    ], id='tab-container', className='container')


def first_quarter_tab(children):
    quarter = controller.get_first_quarter(children)
    return html.Div([
        html.Div([
            html.H4('First Quarter Comments'),
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
        card = []
        if index == 0: card.append(html.H4('Most Popular Comment'))
        card.extend([
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
        ])
        cards.append(
            html.Div(card, id=str(index) + id, style=style_card)
        )
    return cards


msg = ""


#
# message when getting gender data is loaded
@server.route('/youtubestats/api/v1/gender', methods=['POST'])
def genderdata_resuls():
    global msg
    if request is None or not request.json or not 'status' in request.json:
        msg = request.json['status']
    # request with json
    return 'ok', 200


if __name__ == '__main__':
    controller = Controller()
    style_card = {
        'box-shadow': '0 8px 16px 0 rgba(0,0,0,0.2)',
        'width': '100%',
        'border-radius': '2%',
        'padding': '2% 2%'
    }
    style_container = {'marging': '2% 2% 2% 2%'}
    style_label = {'padding': '1% 1% 1% 1%', 'font-size': '1.3em'}
    style_horGroup = {'textAlign': 'left', 'display': 'flex', 'flex-direction': 'row'}
    app.run_server(debug=True, port=8000)
