import json
import plotly.graph_objs as go

def load_data():
    # Load JSON data
    with open('stata.json') as f:
        stata = json.load(f)
    with open('statb.json') as f:
        statb = json.load(f)
    with open('statc.json') as f:
        statc = json.load(f)
    with open('statd.json') as f:
        statd = json.load(f)
    
    return stata, statb, statc, statd

def get_static_figures(stata, statb):
    # Cumulative trade by product
    fig_product_trade = go.Figure(
        data=[go.Bar(x=list(stata.keys()), y=list(stata.values()), marker_color='cyan')],
        layout=go.Layout(
            title="Cumulative Trade by Product",
            plot_bgcolor='black',
            paper_bgcolor='black',
            font=dict(color='white'),
            xaxis=dict(showgrid=False),
            yaxis=dict(showgrid=False)
        )
    )

    # World trade by year
    fig_world_trade = go.Figure(
        data=[go.Scatter(x=list(statb.keys()), y=list(statb.values()), mode='lines', line=dict(color='magenta', width=4))],
        layout=go.Layout(
            title="World Trade by Year",
            plot_bgcolor='black',
            paper_bgcolor='black',
            font=dict(color='white'),
            xaxis=dict(showgrid=False),
            yaxis=dict(showgrid=False)
        )
    )

    return fig_product_trade, fig_world_trade

def get_interactive_figures(data, title):
    # Sort the data by year
    sorted_years = sorted(data.keys())
    sorted_values = [data[year] for year in sorted_years]
    
    fig = go.Figure(
        data=[go.Scatter(x=sorted_years, y=sorted_values, mode='lines+markers', line=dict(color='orange', width=4), marker=dict(size=8))],
        layout=go.Layout(
            title=title,
            plot_bgcolor='black',
            paper_bgcolor='black',
            font=dict(color='white'),
            xaxis=dict(showgrid=False),
            yaxis=dict(showgrid=False)
        )
    )
    
    return fig
