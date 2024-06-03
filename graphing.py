import plotly.graph_objs as go
import plotly.io as pio
import json
from analysis import *

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

        fig = go.Figure()
        fig.add_trace(go.Scatter(x=periods, y=remaining_principal, mode='lines', name='Remaining Principal'))
        fig.add_trace(go.Scatter(x=periods, y=interest_paid, mode='lines', name='Interest Paid'))

        fig.update_layout(
            title='Mortgage Remaining Principal and Interest Over Time',
            xaxis_title='Payment Period (Months)' if keyword == 'Monthly' else 'Payment Period (Fortnights)',
            yaxis_title='Amount ($)',
            template='plotly_white',
            autosize=False,
            width=1000,
            height=400,
        )

        graph_json = pio.to_json(fig)
        return graph_json
    except Exception as e:
        return json.dumps({"error": "Error creating graph: {}".format(str(e))})