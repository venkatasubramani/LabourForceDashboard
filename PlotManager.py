import plotly.graph_objs as go

class PlotManager:
    """
    Class to manage plotting of data using Plotly.
    """
    def __init__(self):
        pass

    def create_plot(self, df, column_name):
        """
        Create a plot with original and forecasted values.

        Parameters:
        -----------
        df : pd.DataFrame
            The DataFrame containing the data.
        column_name : str
            The name of the column to plot.

        Returns:
        --------
        go.Figure
            The Plotly figure containing the plot.
        """
        fig = go.Figure()

        # Add original values
        fig.add_trace(go.Scatter(
            x=df['Start Date'],
            y=df['Actual'],
            mode='lines',
            name='Actual'
        ))
        
        fig.add_shape(
            type="line",
            x0="2024-04-01", x1="2024-04-01",  # X-axis at April 1, 2024
            y0=0, y1=1,  # The y-axis will span the full range from 0 to 1 (scaled later)
            xref="x", yref="paper",  # xref is the x-axis, yref is the entire plot area
            line=dict(color="Red", width=2, dash="dash")  # Customize the appearance of the line
        )
        # Add forecasted values
        if 'yhat' in df.columns:
            fig.add_trace(go.Scatter(
                x=df['Start Date'],
                y=df['yhat'],
                mode='lines',
                name='Forecast'
            ))
        else:
            fig.add_trace(go.Scatter(
                x=df['Start Date'],
                y=df['Prediction'],
                mode='lines',
                name='Forecast'
            ))

        fig.update_layout(
            title=f'Original and Forecasted Values for {column_name}',
            xaxis_title='Date',
            yaxis_title=column_name
        )

        return fig
