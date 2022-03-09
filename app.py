import dash
from dash import dcc, Input, Output, Dash, html, dash_table
import dash_bootstrap_components as dbc

import plotly.graph_objects as go
import plotly.express as px

import pandas as pd
import numpy as np


poke_data = pd.read_csv('pokemons.csv')

poke_data["Ranking"] = ((poke_data["ATK"] - poke_data["DEF"]) * 0.8 + (poke_data["SP_ATK"] - poke_data["SP_DEF"]) * 0.2)
poke_data = poke_data.sort_values(by="Ranking", ascending=False)
poke_data = poke_data.drop_duplicates(subset=['NAME'], keep='first')


POKEMON_SKILL = ['HP', 'ATK', 'SP_ATK', 'DEF', 'SP_DEF', 'SPD']
POKEMON_INFO = ['NAME', 'GENERATION', 'TYPE1', 'ABILITY1', 'ABILITY2', 'HEIGHT', 'WEIGHT']
LABELS_TABLE = ['Pokemon', 'Generation', 'Type', 'Ability', 'Height (m)', 'Weight (kg)']
SKILLS = ['ATK', 'SP_ATK', 'DEF', 'SP_DEF', 'HP']
poke_options = [{'label': poke_data['NAME'][x], 'value': poke_data['NAME'][x]} for x in poke_data.index]


left_dropdown = dcc.Dropdown(id="pokemon1", options=poke_options, value="")
right_dropdown = dcc.Dropdown(id="pokemon2", options=poke_options, value="")

dash_table1 = dash_table.DataTable(
        id="table1",
        columns = [{"name": col, "id": POKEMON_INFO[idx]} for idx, col in enumerate(LABELS_TABLE)],
        data = poke_data[poke_data['NAME'] == "" ],
        )


dash_table2 = dash_table.DataTable(
        id="table2",
        columns = [{"name": col, "id": POKEMON_INFO[::-1][idx]} for idx, col in enumerate(LABELS_TABLE)],
        data = poke_data[poke_data['NAME'] == "" ],
        )


app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

server = app.server

navbar = dbc.Navbar([
        html.A(
            dbc.Row(
                [
                    dbc.Col(
                        html.Img(
                            src=app.get_asset_url("poke_logo.png"), height="130px", width="200px"
                            ),
                        width=3,
                        ),
                    dbc.Col([
                        html.Label("Pokemon generations", id="label1"),
                        html.Label("Compare your pokemons base of their skills", 
                            className="label2",
                            ),
                        html.Br(),
                        html.Label(
                            "Pokemon challenge scandiweb",
                            className="label2",
                            style={"margin-bottom": ".34rem"},
                            ),
                        ],
                        width=8,
                        ),
                    ],
                align="between",
                ),
            )
        ])

controls_player1 = dbc.Card(
        [
            dbc.Row(
                [
                    html.Label("Choose a pokemon:"),
                    html.Br(),
                    left_dropdown,
                ]
            ),
            ],
        body=True,
        className="pokemon_control",
    )

controls_player2 = dbc.Card(
        [
            dbc.Row(
                [
                    html.Label("Choose a pokemon:"),
                    html.Br(),
                    left_dropdown,
                ]
            ),
            ],
        body=True,
        className="pokemon_control",
    )

cards1 = dbc.Container(
        [
            dbc.Card(
                dbc.CardBody(
                    [
                        html.Div("Type", className="card-title1"),
                        html.Div(id="P_position1", className="card_info1"),
                        ]
                    ),
                    className="attributes_card",
                ),

            dbc.Card(
                dbc.CardBody(
                    [
                        html.Div("Type", className="card-title1"),
                        html.Div(id="P_value1", className="card_info1"),
                        ]
                    ),
                    className="attributes_card",
                ),

            dbc.Card(
                dbc.CardBody(
                    [
                        html.Div("Type", className="card-title1"),
                        html.Div(id="P_skill1", className="card_info1"),
                        ]
                    ),
                    className="attributes_card",
                ),
            
            dbc.Card(
                dbc.CardBody(
                    [
                        html.Div("Type", className="card-title1"),
                        html.Div(id="P_foot1", className="card_info1"),
                        ]
                    ),
                    className="attributes_card",
                ),
            ]

        )

cards2 = dbc.Container(
        [
            dbc.Card(
                dbc.CardBody(
                    [
                        html.Div("Deffence", className="card-title2"),
                        html.Div(id="P_foot2", className="card_info2"),
                        ]
                    ),
                    className="attributes_card",
                ),

            dbc.Card(
                dbc.CardBody(
                    [
                        html.Div("Attack", className="card-title2"),
                        html.Div(id="P_skill2", className="card_info2"),
                        ]
                    ),
                    className="attributes_card",
                ),

            dbc.Card(
                dbc.CardBody(
                    [
                        html.Div("Type", className="card-title2"),
                        html.Div(id="P_value2", className="card_info2"),
                        ]
                    ),
                    className="attributes_card",
                ),
            
            dbc.Card(
                dbc.CardBody(
                    [
                        html.Div("Type", className="card-title1"),
                        html.Div(id="P_position2", className="card_info2"),
                        ]
                    ),
                    className="attributes_card",
                ),
            ]

        )


cards3 = dbc.Container(
        [
            dbc.Card(
                dbc.CardBody(
                    [
                        html.Div("Ranking", className="card-title1"),
                        dcc.Graph(id="graph1"),
                        ]
                    ),
                    className="attributes_card",
                ),

            dbc.Card(
                dbc.CardBody(
                    [
                        html.Div("Attack", className="card-title1"),
                        dcc.Graph(id="graph3"),
                        ]
                    ),
                    className="attributes_card",
                ),
            ]
        )

cards4 = dbc.Container(
        [
            dbc.Card(
                dbc.CardBody(
                    [
                        html.Div("Ranking", className="card-title2"),
                        dcc.Graph(id="graph4"),
                        ]
                    ),
                    className="attributes_card",
                ),

            dbc.Card(
                dbc.CardBody(
                    [
                        html.Div("Attack", className="card-title2"),
                        dcc.Graph(id="graph2"),
                        ]
                    ),
                    className="attributes_card",
                ),
            ]
        )

table_content1 = (
        html.Div(
            [
                dbc.Card(
                    dbc.CardBody(
                        [
                            html.H1("Comparison between Pokemons"),
                            html.Hr(),
                            dbc.Row(
                                [
                                    dbc.Col([
                                        dbc.Row(controls_player1),
                                        dbc.Row((
                                            html.Img(
                                                src=app.get_asset_url('pokeball.png'),
                                                className="playerImg",
                                                )
                                            ),
                                        ),
                                    ],
                                    sm=3,
                                ),
                                    dbc.Col(
                                        dcc.Graph(id="graph"), sm=5, align="center"
                                        ),
                                    dbc.Col(
                                        [
                                            dbc.Row(controls_player2),
                                            dbc.Row(
                                                html.Img(
                                                    src=app.get_asset_url('pokeball.png'),
                                                    className="playerImg",
                                                    )
                                                ),
                                            ],
                                        sm=3,
                                        ),
                                    ],
                                justify="between",
                                ),
                            dbc.Row(
                                [
                                    dbc.Col(
                                        [
                                            dash_table1,
                                            html.Br(),
                                            cards1,
                                            html.Br(),
                                            cards3,
                                            ],
                                        sm=6,
                                        ),
                                    dbc.Col(
                                        [
                                            dash_table2,
                                            html.Br(),
                                            cards2,
                                            html.Br(),
                                            cards4,
                                            ],
                                        sm=6,
                                        ),
                                    ]
                                ),
                            ]
                        )
                    )
                ]
            ),
        )



app.layout = dbc.Container([
    navbar,
    dbc.Tabs(
        [
            dbc.Tab(table_content1, label="Comparison"),
            ],
        ),
    ],
    fluid=True,
    )


if __name__ == "__main__":
    app.run_server(debug=True)
