import plotly.graph_objs as go
import plotly.io as pio
import json
from analysis import *
import datetime

def mortgage_graph(mortgage, transactions, keyword):
    try:
        analysis_data = mortgage_analysis(mortgage, transactions, 'graph')
        if keyword == 'Monthly':
            periods = analysis_data['monthly_periods']
            remaining_principal = analysis_data['monthly_remaining_principal']
            interest_paid = analysis_data['monthly_interest_paid']
        else:
            periods = analysis_data['fortnightly_periods']
            remaining_principal = analysis_data['fortnightly_remaining_principal']
            interest_paid = analysis_data['fortnightly_interest_paid']
        
        # Debugging statements to ensure correct data
        print("Periods:", periods)
        print("Remaining Principal:", remaining_principal)
        print("Interest Paid:", interest_paid)

        # Convert periods to datetime objects for better plotting
        periods = [datetime.datetime.strptime(date, "%Y-%m-%d") for date in periods]

        # Ensure x-axis shows all periods correctly
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=periods, y=remaining_principal, mode='lines', name='Remaining Principal'))
        fig.add_trace(go.Scatter(x=periods, y=interest_paid, mode='lines', name='Interest Paid'))

        fig.update_layout(
            title='Mortgage Remaining Principal and Interest Over Time',
            xaxis_title='Year',
            yaxis_title='Amount ($)',
            xaxis=dict(
                tickmode='array',
                tickvals=[periods[i] for i in range(0, len(periods), 12)],  # Show ticks every year
                ticktext=[period.strftime('%Y') for period in periods[::12]],
                tickangle=-45
            ),
            template='plotly_white',
            autosize=False,
            width=1000,
            height=400,
        )

        graph_json = pio.to_json(fig)
        return graph_json
    except Exception as e:
        print("Error creating graph:", str(e))  # Debugging statement for errors
        return json.dumps({"error": "Error creating graph: {}".format(str(e))})