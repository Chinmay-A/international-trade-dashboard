from dash import Dash
import dash_bootstrap_components as dbc
from layout import create_layout

# Initialize the Dash app with a black-themed layout
app = Dash(__name__, external_stylesheets=[dbc.themes.DARKLY])
app.title = "International Trade Dashboard"

# Set the layout of the app
app.layout = create_layout(app)

if __name__ == "__main__":
    app.run_server(debug=True)
