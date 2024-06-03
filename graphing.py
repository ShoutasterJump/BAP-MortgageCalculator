import plotly.graph_objs as go
import plotly.io as pio

def newMortgageGraph(mortgage):
    principal = mortgage._initialPrincipal + mortgage._extraCost - mortgage._deposit
    monthly_interest_rate = mortgage._initialInterest / 100 / 12
    monthly_number_of_payments = mortgage._initialTerm * 12
    monthly_repayment = principal * ((monthly_interest_rate * pow(1 + monthly_interest_rate, monthly_number_of_payments)) / (pow(1 + monthly_interest_rate, monthly_number_of_payments) - 1))

    remaining_principal = principal
    total_interest_paid = 0
    equity_owned = []
    interest_paid = []
    periods = []

    for month in range(1, monthly_number_of_payments + 1):
        interest_payment = remaining_principal * monthly_interest_rate
        principal_payment = monthly_repayment - interest_payment
        remaining_principal -= principal_payment
        total_interest_paid += interest_payment
        
        equity_current = round((principal - remaining_principal), 2)
        interest_current = round(total_interest_paid, 2)
        
        equity_owned.append(equity_current)
        interest_paid.append(interest_current)
        periods.append(month)

    # Create the Plot
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=periods, y=equity_owned, mode='lines', name='Equity Owned'))
    fig.add_trace(go.Scatter(x=periods, y=interest_paid, mode='lines', name='Interest Paid'))

    fig.update_layout(
        title='Mortgage Equity and Interest Over Time',
        xaxis_title='Payment Period (Months)',
        yaxis_title='Amount ($)',
        template='plotly_white',
        autosize=False,
        width=1000,
        height=400,
    )

    graph_div = pio.to_html(fig, full_html=False)
    return graph_div
    
