import dash
from dash import dcc, Input, Output, Dash, html, dash_table
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import numpy as np
import dash_bootstrap_components as dbc

poke_data = pd.read_csv('./pokemons.csv',on_bad_lines='skip')

#poke data
poke_data["Ranks"] = round((poke_data["ATK"] - poke_data["DEF"]) * 0.8 + (poke_data["SP_ATK"] - poke_data["SP_DEF"]) * 0.2)
poke_data = poke_data.sort_values(by='Ranks', ascending=False)
poke_data = poke_data.drop_duplicates(subset=['NAME'],keep='first') 


POKEMON_SKILL = ["HP", "ATK", "SP_ATK" ,"DEF", "SP_DEF" ,"SPD"]
POKEMON_INFO = ["NAME","GENERATION","TYPE1", "ABILITY1","HEIGHT","WEIGHT"]
LABELS_TABLE = ["Pokemon", "Generation", "Type", "Ability", "Height (m)", "Weight (kg)"]
SKILLS = ["ATK","SP_ATK","DEF","SP_DEF","HP"]

pokemon1 = "Pikachu"
pokemon2 = "Raichu"


# creating a list of pokemons

pokemon_options = []
for i in poke_data.index:
    pokemon_options.append({"label": poke_data["NAME"][i], "value": poke_data["NAME"][i]})


# pokemon lists left and right

pokemon_dropdown_left = dcc.Dropdown(id="pokemon1", options=pokemon_options, value="Pikachu")
pokemon_dropdown_right = dcc.Dropdown(id="pokemon2", options=pokemon_options, value="Raichu")

#tables with skills

dashtable_1 = dash_table.DataTable(
    id="table1",
    columns=[{"name": col, "id": POKEMON_INFO[idx]} for (idx, col) in enumerate(LABELS_TABLE)],
    data=poke_data[poke_data["NAME"] == pokemon1].to_dict("records"),
    style_cell={"textAlign": "left", "font_size": "14px"},
    style_data_conditional=[{"if": {"row_index":"odd"}, "backgroundColor": "rgb(248, 248, 248)"}],
    style_header={"backgroundColor": "rgb(230, 230, 230)", "fontWeight": "bold"},
)

dashtable_2 = dash_table.DataTable(
    id="table2",
    columns=[{"name": col, "id": POKEMON_INFO[idx]} for (idx, col) in enumerate(LABELS_TABLE)],
    data=poke_data[poke_data["NAME"] == pokemon2].to_dict("records"),
    style_cell={"textAlign": "right", "font_size": "14px"},
    style_data_conditional=[{"if": {"row_index": "odd"}, "backgroundColor": "rgb(248, 248, 248)"}],
    style_header={"backgroundColor": "rgb(230, 230, 230)", "fontWeight": "bold"},
)

# app layout

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

server = app.server

navbar = dbc.Navbar(
    [
        html.A(
            dbc.Row(
                [
                    dbc.Col(
                        html.Img(src=app.get_asset_url("poke_logo.png"), height="130px", width="200px"),
                        width=4,
                    ),
                    dbc.Col(
                        [
                            html.Label("POKEMONS", id="label1"),
                            html.Br(),
                            html.Label("Explore the differences between all pokemons", className="label2"),
                            html.Br(),
                            html.Label("Poke dash board", className="label2", style={
                                "marginBottom": ".34rem"
                                }),
                        ],
                        width=6,
                        className="header",
                    ),
                ],
                align="between",
            ),),
    ],
    className="navBarclass",
)


controls_player_1 = dbc.Card(
    [
        dbc.Row(
            [
                html.Label("Choose a Pokemon:"),
                html.Br(),
                pokemon_dropdown_left,
            ]
        ),
    ],
    body=True,
    className="pokemons_control",
)

controls_player_2 = dbc.Card(
    [
        dbc.Row(
            [
                html.Label("Choose a Pokemon:"),
                html.Br(),
                pokemon_dropdown_right,
            ]
        ),
    ],
    body=True,
    className="controls_players",
)

cards_3 = dbc.Card(
    [
        dbc.Card(
            dbc.CardBody([html.Div("Rank", className="card-title1"), dcc.Graph(id="graph_example_1")]),
            className="attributes_card",
        ),
        dbc.Card(
            dbc.CardBody([html.Div("Skills", className="card-title1"), dcc.Graph(id="graph_example_3")]),
            className="attributes_card",
        ),
    ], className="card-rank"
)

cards_4 = dbc.Card(
    [
        dbc.Card(
            dbc.CardBody([html.Div("Rank", className="card-title2"), dcc.Graph(id="graph_example_2")]),
            className="attributes_card",
        ),
        dbc.Card(
            dbc.CardBody([html.Div("Skills", className="card-title2"), dcc.Graph(id="graph_example_4")]),
            className="attributes_card",
        ),
    ], className="card-rank"
)

tab1_content = (
    html.Div(
        [
            dbc.Card(
                dbc.CardBody(
                    [
                        html.H1("Pokemon Project"),
                        html.Hr(),
                        dbc.Row(
                            [
                                dbc.Col(
                                    [
                                        dbc.Row(controls_player_1),
                                        dbc.Row(html.Img(src=app.get_asset_url(f"/images/{pokemon1}.png"), id="playerImg1")),
                                    ],
                                    sm=3,
                                ),
                                dbc.Col(
                                    dcc.Graph(id="graph_example"), sm=5, align="center"
                                ),
                                dbc.Col(
                                    [
                                        dbc.Row(controls_player_2),
                                        dbc.Row(html.Img(src=app.get_asset_url(f"/images/{pokemon2}.png"), id="playerImg2")),
                                    ],
                                    sm=3,
                                ),
                            ],
                            justify="between",
                        ),
                        dbc.Row(
                            [
                                dbc.Col(
                                    [dashtable_1],
                                    sm=6,
                                ),
                                dbc.Col(
                                    [dashtable_2],
                                    sm=6,
                                ),
                            ]
                        ),
                        dbc.Row(
                            [
                                dbc.Col(
                                    [cards_3],
                                    sm=6,
                                ),
                                dbc.Col(
                                    [cards_4],
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

app.layout = dbc.Container(
    [
        navbar,
        dbc.Tabs([dbc.Tab(tab1_content, label="Pokemons Comparison")])
    ],
    fluid=True
)

@app.callback(
    [
        Output("playerImg1", "src"),
        Output("playerImg2", "src"),
        Output("graph_example", "figure"),
        Output("table1", "data"),
        Output("graph_example_1", "figure"),
        Output("graph_example_3", "figure"),
        Output("table2", "data"),
        Output("graph_example_2", "figure"),
        Output("graph_example_4", "figure"),
    ],
    [Input("pokemon1", "value"), Input("pokemon2", "value")],
)


def table_pokemons(pokemon1, pokemon2):
    # image route
    poke_url1 = './assets/images/' + pokemon1 + '.png'
    poke_url2 = './assets/images/' + pokemon2 + '.png'

    # scatterpolar
    poke_data1_for_plot = pd.DataFrame(poke_data[poke_data["NAME"] == pokemon1][POKEMON_SKILL].iloc[0])
    poke_data1_for_plot.columns = ["score"]

    poke_data2_for_plot = pd.DataFrame(poke_data[poke_data["NAME"] == pokemon2][POKEMON_SKILL].iloc[0])
    poke_data2_for_plot.columns = ["score"]

    list_scores = [poke_data1_for_plot.index[i].capitalize() + " = " + str(poke_data1_for_plot["score"][i]) for i in range(len(poke_data1_for_plot))]
    text_scores_1 = pokemon1
    for i in list_scores:
        text_scores_1 += "<br>" + i

    list_scores = [poke_data2_for_plot.index[i].capitalize() + " = " + str(poke_data2_for_plot["score"][i]) for i in range(len(poke_data2_for_plot))]
    text_scores_2 = pokemon2
    for i in list_scores:
        text_scores_2 += "<br>" + i

    fig = go.Figure(
        data=go.Scatterpolar(
            r=poke_data1_for_plot["score"],
            theta=poke_data1_for_plot.index,
            fill="toself",
            marker_color="rgb(45,0,198)",
            opacity=1,
            hoverinfo="text",
            name=text_scores_1,
            text=[poke_data1_for_plot.index[i] + " = " + str(poke_data1_for_plot["score"][i]) for i in range(len(poke_data1_for_plot))],
        )
    )
    fig.add_trace(
        go.Scatterpolar(
            r=poke_data2_for_plot["score"],
            theta=poke_data2_for_plot.index,
            fill="toself",
            marker_color="rgb(255,171,0)",
            hoverinfo="text",
            name=text_scores_2,
            text=[poke_data2_for_plot.index[i] + " = " + str(poke_data2_for_plot["score"][i]) for i in range(len(poke_data2_for_plot))],
        )
    )

    fig.update_layout(
        polar=dict(
            hole=0.1,
            bgcolor="white",
            radialaxis=dict(
                visible=True,
                type="linear",
                autotypenumbers="strict",
                autorange=False,
                range=[30, 180],
                angle=90,
                showline=False,
                showticklabels=False,
                ticks="",
                gridcolor="black",
            ),
        ),

        width=450,
        height=450,
        margin=dict(l=80, r=80, t=20, b=20),
        showlegend=False,
        template="plotly_dark",
        plot_bgcolor="rgba(0, 0, 0, 0)",
        paper_bgcolor="rgba(0, 0, 0, 0)",
        font_color="black",
        font_size=15,
    )

    # table 1
    table_updated1 = poke_data[poke_data["NAME"] == pokemon1].to_dict("records")

    # gauge plot 1
    poke_data1_for_plot = pd.DataFrame(poke_data[poke_data["NAME"] == pokemon1]["Ranks"])
    poke_data1_for_plot["name"] = pokemon2

    gauge1 = go.Figure(
            go.Indicator(
                domain={"x": [0, 1], "y": [0, 1]},
                value=poke_data1_for_plot.Ranks.iloc[0],
                mode="gauge+number",
                gauge={"axis": {"range": [None, 100]}, "bar": {"color": "#5000bf"}},
                )
            )

    gauge1.update_layout(
            height=300,
            margin=dict(l=10, r=10, t=40, b=10),
            showlegend=False,
            template="plotly_dark",
            plot_bgcolor="rgba(0, 0, 0, 0)",
            paper_bgcolor="rgba(0, 0, 0, 0)",
            font_color="black",
            font_size=15,
    )


    poke_data1_for_plot = pd.DataFrame(
        poke_data[poke_data["NAME"] == pokemon1][SKILLS].iloc[0].reset_index()
    )
    poke_data1_for_plot.rename(columns={poke_data1_for_plot.columns[1]: "counts"}, inplace=True)
    poke_data1_for_plot.rename(columns={poke_data1_for_plot.columns[0]: "skills"}, inplace=True)
    barplot1 = px.bar(poke_data1_for_plot, x="skills", y="counts")
    barplot1.update_traces(marker_color="#5000bf")
    barplot1.update_layout(
            height=300,
            margin=dict(l=10, r=10, t=20, b=0),
            showlegend=False,
            template="plotly_dark",
            plot_bgcolor="rgba(0, 0, 0, 0)",
            paper_bgcolor="rgba(0, 0, 0, 0)",
            font_color="black",
            font_size=10,
            )

    barplot1.update_yaxes(range=[1, 200])

    table_updated2 = poke_data[poke_data["NAME"] == pokemon2].to_dict("records")

    poke_data2_for_plot = pd.DataFrame(poke_data[poke_data["NAME"] == pokemon2]["Ranks"])
    poke_data2_for_plot["name"] = pokemon2
    gauge2 = go.Figure(
        go.Indicator(
            domain={"x": [0, 1], "y": [0, 1]},
            value=poke_data2_for_plot.Ranks.iloc[0],
            mode="gauge+number",
            gauge={"axis": {"range": [None, 100]}, "bar": {"color": "rgb(255,171,0)"}},
        )
    )

    gauge2.update_layout(
            height=300, 
            margin=dict(l=10, r=10, t=40, b=10), 
            showlegend=False,template="plotly_dark",
            plot_bgcolor="rgba(0, 0, 0, 0)",
            paper_bgcolor="rgba(0, 0, 0, 0)",
            font_color="black",
            font_size=15,
            )

    poke_data2_for_plot = pd.DataFrame(poke_data[poke_data["NAME"] == pokemon2][SKILLS].iloc[0].reset_index())
    poke_data2_for_plot.rename(columns={poke_data2_for_plot.columns[1]: "counts"}, inplace=True)
    poke_data2_for_plot.rename(columns={poke_data2_for_plot.columns[0]: "skills"}, inplace=True)
    barplot2 = px.bar(poke_data2_for_plot, x="skills", y="counts")
    barplot2.update_traces(marker_color="rgb(255,171,0)")
    barplot2.update_layout(
        height=300,
        margin=dict(l=10, r=10, t=20, b=0),
        showlegend=False,
        template="plotly_dark",
        plot_bgcolor="rgba(0, 0, 0, 0)",
        paper_bgcolor="rgba(0, 0, 0, 0)",
        font_color="black",
        font_size=10,
    )
    barplot2.update_yaxes(range=[1, 200])
    
    # cards
    p_pos_1 = poke_data[poke_data["NAME"] == pokemon1]["TYPE1"]
    p_value_1 = poke_data[poke_data["NAME"] == pokemon1]["ABILITY1"]
    p_skill_1 = poke_data[poke_data["NAME"] == pokemon1]["ATK"]
    p_foot_1 = poke_data[poke_data["NAME"] == pokemon1]["DEF"]

    p_pos_2 = poke_data[poke_data["NAME"] == pokemon2]["TYPE1"]
    p_value_2 = poke_data[poke_data["NAME"] == pokemon2]["ABILITY1"]
    p_skill_2 = poke_data[poke_data["NAME"] == pokemon2]["ATK"]
    p_foot_2 = poke_data[poke_data["NAME"] == pokemon2]["DEF"]

    # outputs
    return (
        poke_url1,
        poke_url2,
        fig,
        table_updated1,
        gauge1,
        barplot1,
        table_updated2,
        gauge2,
        barplot2,
    )

if __name__ == "__main__":
    app.run_server(debug=True)
