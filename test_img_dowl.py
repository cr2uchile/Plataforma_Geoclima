import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
from plotly.io import write_image
from dash_extensions import Download
from dash_extensions.snippets import send_bytes

# Create example figure.
fmt = "png"
fig = {'data': [{'x': [1, 2, 3], 'y': [4, 1, 2], 'type': 'scatter'}], 'layout': {'title': 'So Title'}}
# Create app.
app = dash.Dash(__name__, prevent_initial_callbacks=True)
app.layout = html.Div(children=[
    html.Button("Make Image", id="make-img-btn"), dcc.Graph(id='graph', figure=fig), Download(id='download')
])


@app.callback(Output('download', 'data'), [Input('make-img-btn', 'n_clicks'), Input('graph', 'figure')])
def make_image(n_clicks, figure):
    return send_bytes(lambda x: write_image(figure, x, format=fmt), "figure.{}".format(fmt))


if __name__ == '__main__':
    app.run_server(debug=True)