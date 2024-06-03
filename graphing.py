from analysis import *
import plotly.graph_objs as go
import plotly.io as pio
import json

def mortgage_graph(mortgage, transactions, keyword):
    try:
        analysis_data = mortgage_analysis(mortgage, transactions, 'graph')
        periods = analysis_data['monthly_periods']
        equity_owned = analysis_data['monthly_equity_owned']
        interest_paid = analysis_data['monthly_interest_paid']

        fig = go.Figure()
        fig.add_trace(go.Scatter(x=periods, y=equity_owned, mode='lines', name='Equity Owned'))
        fig.add_trace(go.Scatter(x=periods, y=interest_paid, mode='lines', name='Interest Paid'))

        fig.update_layout(
            title='Mortgage Equity and Interest Over Time',
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
