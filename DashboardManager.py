import dash
from dash import dcc, html, Input, Output
import plotly.graph_objs as go
import dash_bootstrap_components as dbc
import pandas as pd
from FileHandler import FileHandler
from PlotManager import PlotManager


class DashboardManager:
    """
    Class to manage the dashboard using Dash.
    """

    def __init__(self, file_handler, plot_manager):
        self.file_handler = file_handler
        self.plot_manager = plot_manager

        # Load the base files during initialization
        self.sixteen_and_over = self.file_handler.load_file(
            self.file_handler.processed_dir, 'sixteen_and_over.csv')
        self.sixteen_and_sixty_four = self.file_handler.load_file(
            self.file_handler.processed_dir, 'sixteen_and_sixty_four.csv')

        self.app = dash.Dash(
            __name__,
            external_stylesheets=[
                dbc.themes.BOOTSTRAP,
                "https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0-beta3/css/all.min.css"],
            suppress_callback_exceptions=True)
        self.sixteen_and_sixty_four_page = html.Div(
            [
                html.H3("Labour force population Levels and Rates for '16 to 64 age group'"),
                dcc.Graph(
                    id='sixteen-sixty-four-levels-plot'),
                dcc.Graph(
                    id='sixteen-sixty-four-rates-plot'),
                html.Hr(),
            ])

        self.sixteen_and_over_page = html.Div(
            [
                html.H3("Labour force population Levels and Rates for '16 and over age group'"),
                dcc.Graph(
                    id='sixteen-over-levels-plot'),
                dcc.Graph(
                    id='sixteen-over-rates-plot'),
                html.Hr(),
            ])
        self.home_page = html.Div([
            html.P("Forecasting Dashboard of Labour Market Statistics",
                   style={'font-size': '24px', 'font-weight': 'bold'}),
            dbc.Row([
                dbc.Col(html.P('Labour Age Range'), width=4),
                dbc.Col(html.P('Category'), width=4),
                dbc.Col(html.P('Algorithm'), width=4),
            ]),
            dbc.Row([
                dbc.Col(dcc.Dropdown(
                    id='base-file-dropdown',
                    options=[{'label': 'sixteen & over', 
                              'value': 'sixteen_and_over'},
                             {'label': 'sixteen to sixty four', 
                              'value': 'sixteen_and_sixty_four'}],
                    value='sixteen_and_over',  # Set default value
                    placeholder="Select a dataset"
                ), width=4),
                dbc.Col(dcc.Dropdown(
                    id='column-dropdown',
                    options=[{'label': col, 'value': col
                              } for col in self.sixteen_and_over.columns if col not in [
                        'Start Date', 'End Date', 'Dataset identifier code']],
                    value='Total economically active level',  # Set first column as default
                    placeholder="Select a column"
                ), width=4),
                dbc.Col(dcc.Dropdown(
                    id='model-dropdown',
                    options=[{'label': 'Linear Regression', 'value': 'linear_regression'},
                             {'label': 'Prophet', 'value': 'prophet'},
                             {'label': 'XGBoost', 'value': 'xgboost'}],
                    value='linear_regression',  # Set default forecasting model
                    placeholder="Select a forecasting model"
                ), width=4),
            ]),
            dcc.Graph(id='forecast-plot'),
            html.Hr(),


        ])

    def setup_footer(self):
        """
        Set up the footer of the dashboard.
        """
        footer = dbc.NavbarSimple(
            brand="This dashboard is created by: Venky",
            brand_href="#",
            color="secondary",
            dark=True,
            children=[
                # Add GitHub icon
            dbc.NavItem(
                dbc.NavLink(
                    html.I(className="fab fa-github", style={"font-size": "1.5em"}),  # GitHub FaFa icon
                    href="https://github.com/venkatasubramani",  # Replace with your GitHub link
                    target="_blank"
                )
            ),
            
            # Add Kaggle icon (Kaggle doesn't have an official FA icon, so using a work-around with custom style)
            dbc.NavItem(
                dbc.NavLink(
                    html.I("K",className="fab", style={"font-size": "1.5em", "font-weight": "bold"}),  # Kaggle icon using "K"
                    href="https://www.kaggle.com/venkatasubramani",  # Replace with your Kaggle link
                    target="_blank"
                )
            ),

            # Add LinkedIn icon
            dbc.NavItem(
                dbc.NavLink(
                    html.I(className="fab fa-linkedin", style={"font-size": "1.5em"}),  # LinkedIn FaFa icon
                    href="https://www.linkedin.com/in/vsroot5/",  # Replace with your LinkedIn link
                    target="_blank"
                )
            )
            ],
        className="justify-content-left",  # Center the icons horizontally
        style={"padding": "10px 0"},  # Add padding for the footer
        )
        
        return footer

    def setup_layout(self):
        """
        Set up the layout of the dashboard.
        """
        navbar = dbc.NavbarSimple(
            brand="Forecasting analysis on summary of labour market statistics",
            brand_href="#",
            color="primary",
            dark=True,
            className="fixed-top", 
            children=[
                dbc.NavItem(dbc.NavLink("Home", href="/")),
                
                dbc.DropdownMenu(
                label="Data Source",
                children=[
                    dbc.DropdownMenuItem("go to ONS Source page", 
                                         href="https://www.ons.gov.uk/employmentandlabourmarket/peopleinwork/employmentandemployeetypes/datasets/summaryoflabourmarketstatistics",
                                         external_link=True, 
                                         target="_blank"),
                ],
                nav=True,  # Ensures that the dropdown is part of the navigation bar
                in_navbar=True,
            ),
                dbc.NavItem(
                    dbc.NavLink(
                        "16 & over",
                        href="/sixteen_and_over")),
                dbc.NavItem(
                    dbc.NavLink(
                        "16 to 64",
                        href="/sixteen_and_sixty_four")),
        ])

        self.app.layout = html.Div([
            dcc.Location(id='url', refresh=False),
            navbar,
            html.Br(),
            html.Br(),
            html.Br(),
            html.Div(id='page-content'),
            self.setup_footer(), 
        ])

    def setup_callbacks(self):
        """
        Set up the callbacks for interactivity.
        """

        @self.app.callback(Output('page-content', 'children'),
                           [Input('url', 'pathname')])
        def display_page(pathname):
            if pathname == '/sixteen_and_over':
                return self.sixteen_and_over_page
            elif pathname == '/sixteen_and_sixty_four':
                return self.sixteen_and_sixty_four_page
            else:
                return self.home_page

        @self.app.callback(
            Output('column-dropdown', 'options'),
            [Input('base-file-dropdown', 'value')]
        )
        def update_columns(base_file):
            if base_file == 'sixteen_and_over':
                df = self.sixteen_and_over
            else:
                df = self.sixteen_and_sixty_four

            return [{'label': col, 'value': col} for col in df.columns if col not in [
                'Start Date', 'End Date', 'Dataset identifier code']]

        @self.app.callback(
            Output('forecast-plot', 'figure'),
            [Input('base-file-dropdown', 'value'),
             Input('column-dropdown', 'value'),
             Input('model-dropdown', 'value')]
        )
        def update_plot(base_file, column_name, model_name):
            if base_file is None or column_name is None or model_name is None:
                return go.Figure()

            print(
                f"Selected file: {base_file}, column: {column_name}, model: {model_name}")
            forecast_file = self.file_handler.list_model_files(
                base_file, model_name, column_name)
            print(f"Forecast file: {forecast_file}")
            if forecast_file is None:
                print(
                    f"No forecast file found for {base_file}, {model_name}, {column_name}")
                return go.Figure()

            print(f"Forecast file found: {forecast_file}")
            try:
                df = self.file_handler.load_file(
                    self.file_handler.model_results_dir, forecast_file)
                print(f"Loaded forecast file with columns: {df.columns}")
            except Exception as e:
                print(f"Error loading forecast file {forecast_file}: {e}")
                return go.Figure()

            if 'Actual' not in df.columns or (
                    'yhat' not in df.columns and 'Prediction' not in df.columns):
                print(
                    f"Missing required columns in forecast file: {df.columns}")
                return go.Figure()

            return self.plot_manager.create_plot(df, column_name)

        # Display graphs for 'Sixteen and Over'
        @self.app.callback(
            Output('sixteen-over-levels-plot', 'figure'),
            Output('sixteen-over-rates-plot', 'figure'),
            [Input('url', 'pathname')]
        )
        def update_sixteen_over_graphs(base_file):
            fig_levels = go.Figure()
            fig_rates = go.Figure()

            # Population levels for 'Sixteen and Over'
            fig_levels.add_trace(
                go.Scatter(
                    x=self.sixteen_and_over['Start Date'],
                    y=self.sixteen_and_over['All aged 16 & over level'],
                    mode='lines+markers',
                    name='All aged 16 & over level'))
            fig_levels.add_trace(
                go.Scatter(
                    x=self.sixteen_and_over['Start Date'],
                    y=self.sixteen_and_over['Total economically active level'],
                    mode='lines+markers',
                    name='Total economically active level'))
            fig_levels.add_trace(
                go.Scatter(
                    x=self.sixteen_and_over['Start Date'],
                    y=self.sixteen_and_over['Total in employment level'],
                    mode='lines+markers',
                    name='Total in employment level'))
            fig_levels.add_trace(
                go.Scatter(
                    x=self.sixteen_and_over['Start Date'],
                    y=self.sixteen_and_over['Unemployed level'],
                    mode='lines+markers',
                    name='Unemployed level'))
            fig_levels.add_trace(
                go.Scatter(
                    x=self.sixteen_and_over['Start Date'],
                    y=self.sixteen_and_over['Economically inactive level'],
                    mode='lines+markers',
                    name='Economically inactive level'))

            fig_levels.update_layout(
                title="Population Levels Over Time (16 & Over)",
                xaxis_title="Date",
                yaxis_title="Population Levels")

            # Population rates for 'Sixteen and Over'
            fig_rates.add_trace(
                go.Scatter(
                    x=self.sixteen_and_over['Start Date'],
                    y=self.sixteen_and_over['Economic activity rate'],
                    mode='lines+markers',
                    name='Economic activity rate'))
            fig_rates.add_trace(
                go.Scatter(
                    x=self.sixteen_and_over['Start Date'],
                    y=self.sixteen_and_over['Employment rate'],
                    mode='lines+markers',
                    name='Employment rate'))
            fig_rates.add_trace(
                go.Scatter(
                    x=self.sixteen_and_over['Start Date'],
                    y=self.sixteen_and_over['Unemployment rate'],
                    mode='lines+markers',
                    name='Unemployment rate'))
            fig_rates.add_trace(
                go.Scatter(
                    x=self.sixteen_and_over['Start Date'],
                    y=self.sixteen_and_over['Economic inactivity rate'],
                    mode='lines+markers',
                    name='Economic inactivity rate'))

            fig_rates.update_layout(
                title="Population Rates Over Time (16 & Over)",
                xaxis_title="Date",
                yaxis_title="Rates (%)")

            return fig_levels, fig_rates

        # Display graphs for 'Sixteen and Sixty-Four'
        @self.app.callback(
            Output('sixteen-sixty-four-levels-plot', 'figure'),
            Output('sixteen-sixty-four-rates-plot', 'figure'),
            [Input('url', 'pathname')]
        )
        def update_sixteen_sixty_four_graphs(base_file):
            fig_levels = go.Figure()
            fig_rates = go.Figure()

            # Population levels for 'Sixteen and Sixty-Four'
            fig_levels.add_trace(
                go.Scatter(
                    x=self.sixteen_and_sixty_four['Start Date'],
                    y=self.sixteen_and_sixty_four['All aged 16 to 64 level'],
                    mode='lines+markers',
                    name='All aged 16 to 64 level'))
            fig_levels.add_trace(
                go.Scatter(
                    x=self.sixteen_and_sixty_four['Start Date'],
                    y=self.sixteen_and_sixty_four['Total economically active level'],
                    mode='lines+markers',
                    name='Total economically active level'))
            fig_levels.add_trace(
                go.Scatter(
                    x=self.sixteen_and_sixty_four['Start Date'],
                    y=self.sixteen_and_sixty_four['Total in employment level'],
                    mode='lines+markers',
                    name='Total in employment level'))
            fig_levels.add_trace(
                go.Scatter(
                    x=self.sixteen_and_sixty_four['Start Date'],
                    y=self.sixteen_and_sixty_four['Unemployed level'],
                    mode='lines+markers',
                    name='Unemployed level'))
            fig_levels.add_trace(
                go.Scatter(
                    x=self.sixteen_and_sixty_four['Start Date'],
                    y=self.sixteen_and_sixty_four['Economically inactive level'],
                    mode='lines+markers',
                    name='Economically inactive level'))

            fig_levels.update_layout(
                title="Population Levels Over Time (16 to 64)",
                xaxis_title="Date",
                yaxis_title="Population Levels")

            # Population rates for 'Sixteen and Sixty-Four'
            fig_rates.add_trace(
                go.Scatter(
                    x=self.sixteen_and_sixty_four['Start Date'],
                    y=self.sixteen_and_sixty_four['Economic activity rate'],
                    mode='lines+markers',
                    name='Economic activity rate'))
            fig_rates.add_trace(
                go.Scatter(
                    x=self.sixteen_and_sixty_four['Start Date'],
                    y=self.sixteen_and_sixty_four['Employment rate'],
                    mode='lines+markers',
                    name='Employment rate'))
            fig_rates.add_trace(
                go.Scatter(
                    x=self.sixteen_and_sixty_four['Start Date'],
                    y=self.sixteen_and_sixty_four['Unemployment rate'],
                    mode='lines+markers',
                    name='Unemployment rate'))
            fig_rates.add_trace(
                go.Scatter(
                    x=self.sixteen_and_sixty_four['Start Date'],
                    y=self.sixteen_and_sixty_four['Economic inactivity rate'],
                    mode='lines+markers',
                    name='Economic inactivity rate'))

            fig_rates.update_layout(
                title="Population Rates Over Time (16 to 64)",
                xaxis_title="Date",
                yaxis_title="Rates (%)")

            return fig_levels, fig_rates

    def run(self, port=8050):
        """
        Run the Dash app.
        """
        self.setup_layout()
        self.setup_callbacks()
        self.app.run_server(debug=True, port=port)


if __name__ == "__main__":
    # Instantiate handlers
    file_handler = FileHandler(
        processed_dir='processed',
        model_results_dir='model_results')
    plot_manager = PlotManager()

    # Set up and run dashboard
    dashboard_manager = DashboardManager(file_handler, plot_manager)
    dashboard_manager.run()
