from typing import Any, Dict, List
from urllib.parse import parse_qs
import plotly.graph_objs as go

import dash_bootstrap_components as dbc
import dash_leaflet as dl
from dash import Dash, dcc, html
from dash.dependencies import Input, Output

from services.weather import (
    get_five_day_weather_by_city,
    get_five_day_weather_by_location,
    get_one_day_weather_by_city,
    get_one_day_weather_by_coordinates,
    get_ten_day_weather_by_city,
    get_ten_day_weather_by_location,
)


def prepare_weather_info(location: str, details: Dict[str, Any]) -> str:
    info = details.get("data", [{}])[0] if "data" in details else {}
    return (
        f"{location}\n"
        f"Temperature: {info.get('temperature', 'N/A')}°C\n"
        f"Humidity: {info.get('humidity', 'N/A')}%\n"
        f"Wind Speed: {info.get('wind_speed', 'N/A')} km/h\n"
        f"Rain Probability: {info.get('rain_probability', 'N/A')}%\n"
        f"Conditions: {info.get('weather_conditions', 'N/A')}\n"
    )


def create_dash_app(server: Any) -> Dash:
    app = Dash(__name__, server=server, external_stylesheets=[dbc.themes.BOOTSTRAP])

    app.layout = html.Div(
        style={
            "backgroundColor": "#000",  # Чёрный фон
            "color": "#0f0",  # Зелёный текст
            "fontFamily": "monospace",  # Моноширинный шрифт
        },
        children=[
            dcc.Location(id="url", refresh=False),
            html.H1(
                "Weather Route Planner",
                className="text-center my-4",
                style={"color": "#0f0"},
            ),
            dcc.Store(id="weather-store"),
            html.Div(
                id="cards-wrapper",
                className="d-flex flex-wrap justify-content-center",
                style={"padding": "20px"},
            ),
            html.Div(
                [
                    html.Label(
                        "Parameters:",
                        style={"color": "#0f0", "marginBottom": "10px"},
                    ),
                    dcc.Dropdown(
                        id="params-select",
                        options=[
                            {"label": "Temperature", "value": "temperature"},
                            {"label": "Humidity", "value": "humidity"},
                            {"label": "Wind Speed", "value": "wind_speed"},
                            {"label": "Rain Probability", "value": "rain_probability"},
                        ],
                        value=["temperature"],
                        multi=True,
                        className="mb-4",
                        style={
                            "backgroundColor": "#000",
                            "color": "#0f0",
                            "border": "1px solid #0f0",
                        },
                    ),
                    dcc.Graph(
                        id="weather-chart",
                        style={"backgroundColor": "#000", "border": "1px solid #0f0"},
                    ),
                ],
                style={"padding": "20px"},
            ),
            dl.Map(
                center=[55, 55],
                zoom=5,
                id="map-wrapper",
                style={
                    "height": "600px",
                    "width": "90%",
                    "border": "2px solid #0f0",
                    "margin": "20px auto",
                },
                children=[dl.TileLayer(), dl.LayerGroup(id="map-layer")],
            ),
        ],
    )

    @app.callback(
        Output("weather-store", "data"),
        [Input("url", "search")],
    )
    def retrieve_weather(query: str) -> Dict[str, Any]:
        if not query:
            return {}

        params = parse_qs(query.lstrip("?"))
        locations = params.get("data", [])
        period = int(params.get("days", [1])[0])

        weather_info = []
        for loc in locations:
            if "," in loc:
                lat, lon = map(float, loc.split(","))
                weather = {
                    1: get_one_day_weather_by_coordinates,
                    5: get_five_day_weather_by_location,
                    10: get_ten_day_weather_by_location,
                }.get(period, lambda *_: {})(lat, lon)
            else:
                weather = {
                    1: get_one_day_weather_by_city,
                    5: get_five_day_weather_by_city,
                    10: get_ten_day_weather_by_city,
                }.get(period, lambda _: {})(loc)

            if period == 1:
                weather = {
                    "data": [weather] if "error" not in weather else [],
                    **weather
                }

            weather_info.append({"point": loc, "data": weather})

        return {"days": period, "weather_info": weather_info}

    @app.callback(
        Output("cards-wrapper", "children"),
        [Input("weather-store", "data")],
    )
    def render_weather_cards(data: Dict[str, Any]) -> List[Any]:
        if not data:
            return [
                html.Div(
                    "No data available",
                    style={"color": "#0f0", "textAlign": "center", "marginTop": "20px"},
                )
            ]

        cards = []
        for entry in data.get("weather_info", []):
            point = entry.get("point", "Unknown")
            weather_data = entry.get("data", {})
            error_message = weather_data.get("error")

            if error_message:
                card = dbc.Card(
                    dbc.CardBody(
                        [
                            html.H5(f"{point} - Error", style={"color": "#0f0"}),
                            html.P(error_message, style={"color": "#f00"}),
                        ]
                    ),
                    style={
                        "backgroundColor": "#000",
                        "border": "1px solid #0f0",
                        "margin": "10px",
                        "width": "18rem",
                    },
                )
            else:
                card = dbc.Card(
                    dbc.CardBody(
                        [
                            html.H5(
                                f"{point} - {data['days']} Day{'s' if data['days'] > 1 else ''}",
                                style={"color": "#0f0"},
                            ),
                            html.Pre(
                                prepare_weather_info(point, weather_data),
                                style={"color": "#0f0", "whiteSpace": "pre-wrap"},
                            ),
                        ]
                    ),
                    style={
                        "backgroundColor": "#000",
                        "border": "1px solid #0f0",
                        "margin": "10px",
                        "width": "18rem",
                    },
                )
            cards.append(card)

        return cards

    @app.callback(
        Output("weather-chart", "figure"),
        [Input("params-select", "value"), Input("weather-store", "data")],
    )
    def generate_chart(params: List[str], data: Dict[str, Any]) -> go.Figure:
        if not data or not params:
            return go.Figure()

        fig = go.Figure()
        days = data.get("days", 0)
        for entry in data["weather_info"]:
            if "error" in entry["data"]:
                continue
            loc = entry["point"]
            weather_data = entry["data"].get("data", [])

            if days == 1:
                for param in params:
                    value = weather_data[0].get(param, 0) if weather_data else 0
                    fig.add_trace(
                        go.Bar(
                            x=[loc],
                            y=[value],
                            name=f"{loc} - {param}",
                            marker_color="#0f0",
                        )
                    )
            else:
                for param in params:
                    values = [day.get(param, 0) for day in weather_data]
                    dates = [day.get("date", "") for day in weather_data]
                    fig.add_trace(
                        go.Scatter(
                            x=dates,
                            y=values,
                            mode="lines+markers",
                            name=f"{loc} - {param}",
                            line=dict(color="#0f0"),
                        )
                    )

        fig.update_layout(
            paper_bgcolor="#000",
            plot_bgcolor="#000",
            font=dict(color="#0f0"),
            title=dict(
                text="Weather Data" if days != 1 else "One Day Weather Data",
                x=0.5,
            ),
            xaxis_title="Date" if days != 1 else "Location",
            yaxis_title="Values",
        )

        return fig

    @app.callback(
        Output("map-layer", "children"),
        [Input("weather-store", "data")],
    )
    def update_map_markers(data: Dict[str, Any]) -> List:
        if not data:
            return []

        markers = []
        route_points = []

        for entry in data.get("weather_info", []):
            weather_data = entry.get("data", {})
            if "error" in weather_data:
                continue

            latitude = weather_data.get("latitude")
            longitude = weather_data.get("longitude")

            if latitude is not None and longitude is not None:
                route_points.append((latitude, longitude))
                markers.append(
                    dl.Marker(
                        position=(latitude, longitude),
                        children=dl.Tooltip(prepare_weather_info(entry["point"], weather_data)),
                    )
                )

        if len(route_points) > 1:
            route_line = dl.Polyline(
                positions=route_points,
                color="#0f0",
                weight=3,
            )
            return markers + [route_line]

        return markers

    return app
