from dash import dcc, html, Input, Output
import plotly.graph_objs as go
import dash_bootstrap_components as dbc
from data import load_data, get_static_figures, get_interactive_figures

# Load the data
stata, statb, statc, statd = load_data()

def create_layout(app):
    # Static Figures
    fig_product_trade, fig_world_trade = get_static_figures(stata, statb)
    
    # Layout of the dashboard
    layout = dbc.Container([
        dbc.Tabs([
            dbc.Tab(label="Cummulative Data", tab_id="tab1", children=[
                dbc.Row([
                    dbc.Col(dcc.Graph(figure=fig_product_trade, config={'displayModeBar': False}), width=6),
                    dbc.Col(dcc.Graph(figure=fig_world_trade, config={'displayModeBar': False}), width=6),
                ], className="mt-4")
            ]),
            dbc.Tab(label="Data in Categories", tab_id="tab2", children=[
                dbc.Row([
                    dbc.Col(dcc.Dropdown(
                        id='country-dropdown',
                        options=[{'label': country[:15], 'value': country} for country in statc.keys()],
                        value=list(statc.keys())[0],
                        clearable=False,
                        style={'color': 'black', 'backgroundColor': 'white', 'font-size': '16px', 'font-weight': 'bold'}
                    ), width=6),
                    dbc.Col(dcc.Dropdown(
                        id='product-dropdown',
                        options=[{'label': prod[:15], 'value': prod} for prod in statd.keys()],
                        value=list(statd.keys())[0],
                        clearable=False,
                        style={'color': 'black', 'backgroundColor': 'white', 'font-size': '16px', 'font-weight': 'bold'}
                    ), width=6),
                ], className="mt-4"),
                dbc.Row([
                    dbc.Col(dcc.Graph(id='country-trade'), width=6),
                    dbc.Col(dcc.Graph(id='product-trade'), width=6),
                ], className="mt-4")
            ]),
            dbc.Tab(label="Yearly Data", tab_id="tab3", children=[
                dbc.Row([
                    dbc.Col(dcc.Slider(
                        id='year-slider',
                        min=min(int(year) for year in statc[list(statc.keys())[0]].keys()),
                        max=max(int(year) for year in statc[list(statc.keys())[0]].keys()),
                        step=1,
                        marks={year: str(year) for year in range(min(int(year) for year in statc[list(statc.keys())[0]].keys()), max(int(year) for year in statc[list(statc.keys())[0]].keys()) + 1)},
                        value=min(int(year) for year in statc[list(statc.keys())[0]].keys()),
                        tooltip={"placement": "bottom", "always_visible": True}
                    ), width=12)
                ], className="mt-4"),
                dbc.Row([
                    dbc.Col(dcc.Graph(id='yearly-trade-bar'), width=12),
                ], className="mt-4")
            ]),
        ], id="tabs", active_tab="tab1")
    ], fluid=True, style={'height': '100vh', 'overflow': 'hidden', 'backgroundColor': 'black'})

    # Callbacks for interactivity
    @app.callback(
        Output('country-trade', 'figure'),
        Input('country-dropdown', 'value')
    )
    def update_country_trade(selected_country):
        return get_interactive_figures(statc[selected_country], title=f"Trade by Year - {selected_country[:15]}")

    @app.callback(
        Output('product-trade', 'figure'),
        Input('product-dropdown', 'value')
    )
    def update_product_trade(selected_product):
        return get_interactive_figures(statd[selected_product], title=f"Trade by Year - {selected_product[:15]}")

    @app.callback(
        Output('yearly-trade-bar', 'figure'),
        Input('year-slider', 'value')
    )
    def update_yearly_trade_bar(selected_year):
        bar_data = {country: statc[country].get(str(selected_year), 0) for country in statc.keys()}
        fig = go.Figure()

        # Add bars for all countries
        fig.add_trace(go.Bar(
            x=list(bar_data.keys()),
            y=list(bar_data.values()),
            marker_color='lightblue',
            name='Trade Value',
            width=0.8
        ))

        fig.update_layout(
            title=f"Trade Comparison by Country for Year {selected_year}",
            plot_bgcolor='black',
            paper_bgcolor='black',
            font=dict(color='white'),
            xaxis=dict(showgrid=False, tickangle=45),
            yaxis=dict(showgrid=False, title='Trade Value'),
            barmode='group',
            margin=dict(t=50, b=50)  # Pull the chart down
        )
        
        return fig

    return layout
