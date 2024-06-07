import datetime
import math
from dateutil.relativedelta import relativedelta
from itertools import zip_longest
from collections import defaultdict

def calculate_remaining_periods(principal, payment, interest_rate_per_period):
    if interest_rate_per_period > 0:
        return math.ceil(math.log(payment / (payment - principal * interest_rate_per_period)) / math.log(1 + interest_rate_per_period))
    else:
        return math.ceil(principal / payment)

def mortgage_analysis(mortgages, transactions, response, date, keyword="Monthly"):
    def format_currency(value):
        if isinstance(value, (int, float)):
            return f"${value:,.2f}"
        return value

    def calculate_repayment_amount(principal, interest_rate, repayment_periods):
        if interest_rate > 0:
            return principal * (interest_rate / (1 - (1 + interest_rate) ** -repayment_periods))
        else:
            return principal / repayment_periods

    def calculate_repayment_plan(mortgage, transactions, frequency, date_increment):
        principal = mortgage.initialPrincipal + mortgage.extraCost - mortgage.deposit
        interest_rate = mortgage.initialInterest / 100 / (12 if frequency == "Monthly" else 26)
        repayment_periods = mortgage.initialTerm * (12 if frequency == "Monthly" else 26)
        
        total_interest_paid = 0
        remaining_principal = principal
        remaining_principal_list = []
        interest_paid = []
        principal_paid = []
        periods = []
        amortization_table = []

        current_date = date if isinstance(date, datetime.datetime) else datetime.datetime.strptime(date, "%Y-%m-%d")
        accumulated_interest = 0
        accumulated_principal_payments = 0

        repayment_amount = calculate_repayment_amount(principal, interest_rate, repayment_periods)
        print(f"Initial repayment amount: {repayment_amount}")

        transaction_index = 0
        for period in range(1, repayment_periods + 1):
            # Check and apply transaction if it exists
            if transaction_index < len(transactions):
                transaction = transactions[transaction_index]
                transaction_date = transaction.startDate if isinstance(transaction.startDate, datetime.datetime) else datetime.datetime.strptime(transaction.startDate, "%Y-%m-%d")
                if transaction_date <= current_date:
                    remaining_principal -= transaction.balloonPayment
                    print(f"Remaining principal: {remaining_principal}")
                    interest_rate = transaction.currentInterest / 100 / (12 if frequency == "Monthly" else 26)
                    print(f"Interest Rate: {interest_rate}")
                    
                    # Calculate the new repayment periods
                    calculated_remaining_periods = transaction.remainingYears * (12 if frequency == "Monthly" else 26) + transaction.remainingMonths
                    if calculated_remaining_periods != repayment_periods:
                        repayment_periods = calculated_remaining_periods
                        print(f"Repayment Periods updated: {repayment_periods}")

                    repayment_amount = calculate_repayment_amount(remaining_principal, interest_rate, repayment_periods)
                    if transaction.extraPayment:
                        repayment_amount = transaction.extraPayment
                        repayment_periods = calculate_remaining_periods(remaining_principal, repayment_amount, interest_rate)
                    print(f"Repayment Amount: {repayment_amount}")
                    transaction_index += 1
                    print(f"Transaction applied on {current_date}: New repayment amount: {repayment_amount}, New balance: {remaining_principal}")

            interest_payment = remaining_principal * interest_rate
            principal_payment = min(repayment_amount - interest_payment, remaining_principal)
            new_balance = remaining_principal - principal_payment

            total_interest_paid += interest_payment
            accumulated_interest += interest_payment
            accumulated_principal_payments += principal_payment

            remaining_principal_list.append(round(new_balance, 2))
            interest_paid.append(round(interest_payment, 2))
            principal_paid.append(round(principal_payment, 2))
            periods.append(current_date.strftime("%Y-%m-%d"))

            amortization_table.append({
                "Date": current_date.strftime("%Y-%m-%d"),
                "Balance": format_currency(round(remaining_principal, 2)),
                "Interest": format_currency(round(interest_payment, 2)),
                "Principal": format_currency(round(principal_payment, 2)),
                "Repayment": format_currency(round(repayment_amount, 2)),
                "New Balance": format_currency(round(new_balance, 2)),
                "Accumulated Interest": format_currency(round(accumulated_interest, 2)),
                "Accumulated Principal Payments": format_currency(round(accumulated_principal_payments, 2)),
                "Extra": format_currency(0)
            })

            print(f"Date: {current_date.strftime('%Y-%m-%d')}, Balance: {remaining_principal}, Interest: {interest_payment}, Principal: {principal_payment}, New Balance: {new_balance}")

            remaining_principal = new_balance
            current_date += date_increment

            if remaining_principal <= 0:
                remaining_principal_list[-1] = 0
                break

        return {
            "repayment_amount": round(repayment_amount, 2),
            "total_repayment": round(repayment_periods * repayment_amount, 2),
            "remaining_principal_list": remaining_principal_list,
            "interest_paid": interest_paid,
            "principal_paid": principal_paid,
            "periods": periods,
            "amortization_table": amortization_table,
            "total_interest_paid": round(total_interest_paid, 2),
            "remaining_periods": repayment_periods
        }

    def format_periods(periods, frequency="Monthly"):
        if frequency == "Monthly":
            years = periods // 12
            months = periods % 12
        else:
            years = periods // 26
            months = (periods % 26) * 2 // 1  # Convert fortnightly periods to months
        return f"{int(years)} years, {int(months)} months"

    monthly_data = []
    fortnightly_data = []

    for mortgage in mortgages:
        initial_principal = mortgage.initialPrincipal + mortgage.extraCost - mortgage.deposit
        monthly_interest_rate = mortgage.initialInterest / 100 / 12
        monthly_repayment_periods = mortgage.initialTerm * 12
        monthly_data.append(calculate_repayment_plan(mortgage, transactions, "Monthly", relativedelta(months=1)))

        fortnightly_interest_rate = mortgage.initialInterest / 100 / 26
        fortnightly_repayment_periods = mortgage.initialTerm * 26
        fortnightly_data.append(calculate_repayment_plan(mortgage, transactions, "Fortnightly", relativedelta(weeks=2)))
    
    def parse_currency(value):
        return float(value.replace("$", "").replace(",", ""))
    
    def combine_amortization_tables(data):
        combined_data = defaultdict(lambda: {
            "Balance": 0.0,
            "Interest": 0.0,
            "Principal": 0.0,
            "Repayment": 0.0,
            "New Balance": 0.0,
            "Accumulated Interest": 0.0,
            "Accumulated Principal Payments": 0.0,
            "Extra": 0.0
        })
        
        for entry in data:
            for record in entry["amortization_tables"]:
                date = record["Date"]
                combined_data[date]["Balance"] += parse_currency(record["Balance"])
                combined_data[date]["Interest"] += parse_currency(record["Interest"])
                combined_data[date]["Principal"] += parse_currency(record["Principal"])
                combined_data[date]["Repayment"] += parse_currency(record["Repayment"])
                combined_data[date]["New Balance"] += parse_currency(record["New Balance"])
                combined_data[date]["Accumulated Interest"] += parse_currency(record["Accumulated Interest"])
                combined_data[date]["Accumulated Principal Payments"] += parse_currency(record["Accumulated Principal Payments"])
                combined_data[date]["Extra"] += parse_currency(record["Extra"])
        
        combined_table = []
        for date in sorted(combined_data.keys(), key=lambda d: datetime.datetime.strptime(d, "%Y-%m-%d")):
            combined_table.append({
                "Date": date,
                "Balance": format_currency(combined_data[date]["Balance"]),
                "Interest": format_currency(combined_data[date]["Interest"]),
                "Principal": format_currency(combined_data[date]["Principal"]),
                "Repayment": format_currency(combined_data[date]["Repayment"]),
                "New Balance": format_currency(combined_data[date]["New Balance"]),
                "Accumulated Interest": format_currency(combined_data[date]["Accumulated Interest"]),
                "Accumulated Principal Payments": format_currency(combined_data[date]["Accumulated Principal Payments"]),
                "Extra": format_currency(combined_data[date]["Extra"])
            })
        
        return combined_table
    
    def combine_remaining_periods(data):
        remaining_periods = []
        highest_value = float("-inf")
        
        for entry in data:
            periods = entry["remaining_periods"]
            max_value = max(periods)
            if max_value > highest_value:
                highest_value = max_value
                remaining_periods = periods
            
        return remaining_periods
    
    def combine_data(data):
        combined_periods_set = set()
        for entry in data:
            combined_periods_set.update(entry["periods"])
        combined_periods = sorted(combined_periods_set)
        combined_amortization_table = combine_amortization_tables(data)
        remaining_periods = combine_remaining_periods(data)
        combined = {
            "repayment_amount": [sum(x) for x in zip_longest(*[d["repayment_amount"] for d in data], fillvalue=0)],
            "total_repayment": [sum(x) for x in zip_longest(*[d["total_repayment"] for d in data], fillvalue=0)],
            "remaining_principal_list": [sum(x) for x in zip_longest(*[d["remaining_principal_list"] for d in data], fillvalue=0)],
            "interest_paid": [sum(x) for x in zip_longest(*[d["interest_paid"] for d in data], fillvalue=0)],
            "principal_paid": [sum(x) for x in zip_longest(*[d["principal_paid"] for d in data], fillvalue=0)],
            "periods": combined_periods,
            "amortization_table": combined_amortization_table,
            "total_interest_paid": [sum(x) for x in zip_longest(*[d["total_interest_paid"] for d in data], fillvalue=0)],
            "remaining_periods": remaining_periods
        }
        return combined

    monthly_combined = combine_data(monthly_data)
    fortnightly_combined = combine_data(fortnightly_data)

    # Save original values for comparison
    original_monthly_repayment = monthly_combined["repayment_amount"]
    original_total_monthly_repayment = monthly_combined["total_repayment"]
    original_fortnightly_repayment = fortnightly_combined["repayment_amount"]
    original_total_fortnightly_repayment = fortnightly_combined["total_repayment"]

    if response == "new_summary":
        return {
            "monthly_repayment": format_currency(monthly_combined["repayment_amount"]),
            "monthly_periods": format_periods(monthly_combined["remaining_periods"], "Monthly"),
            "monthly_total_repayment": format_currency(monthly_combined["total_repayment"]),
            "fortnightly_repayment": format_currency(fortnightly_combined["repayment_amount"]),
            "fortnightly_periods": format_periods(fortnightly_combined["remaining_periods"], "Fortnightly"),
            "fortnightly_total_repayment": format_currency(fortnightly_combined["total_repayment"]),
        }
    elif response == "summary":
        return {
            "monthly_repayment": format_currency(monthly_combined["repayment_amount"]),
            "monthly_total_repayment": format_currency(monthly_combined["total_repayment"]),
            "fortnightly_repayment": format_currency(fortnightly_combined["repayment_amount"]),
            "fortnightly_total_repayment": format_currency(fortnightly_combined["total_repayment"]),
            "monthly_total_interest_paid": format_currency(monthly_combined["total_interest_paid"]),
            "fortnightly_total_interest_paid": format_currency(fortnightly_combined["total_interest_paid"])
        }
    elif response == "change_summary":
        new_monthly_repayment = monthly_combined["repayment_amount"]
        change_in_monthly_repayment = new_monthly_repayment - original_monthly_repayment
        new_monthly_total_repayment = original_total_monthly_repayment + monthly_combined["total_repayment"]
        change_in_monthly_total_repayment = new_monthly_total_repayment - original_total_monthly_repayment

        new_fortnightly_repayment = fortnightly_combined["repayment_amount"]
        change_in_fortnightly_repayment = new_fortnightly_repayment - original_fortnightly_repayment
        new_fortnightly_total_repayment = original_total_fortnightly_repayment + fortnightly_combined["total_repayment"]
        change_in_fortnightly_total_repayment = new_fortnightly_total_repayment - original_total_fortnightly_repayment

        return {
            "new_monthly_repayment": format_currency(new_monthly_repayment),
            "change_in_monthly_repayment": format_currency(change_in_monthly_repayment),
            "new_monthly_total_repayment": format_currency(new_monthly_total_repayment),
            "change_in_monthly_total_repayment": format_currency(change_in_monthly_total_repayment),
            "new_fortnightly_repayment": format_currency(new_fortnightly_repayment),
            "change_in_fortnightly_repayment": format_currency(change_in_fortnightly_repayment),
            "new_fortnightly_total_repayment": format_currency(new_fortnightly_total_repayment),
            "change_in_fortnightly_total_repayment": format_currency(change_in_fortnightly_total_repayment)
        }
    elif response == "graph":
        return {
            "monthly_periods": monthly_combined["periods"],
            "monthly_remaining_principal": monthly_combined["remaining_principal_list"],
            "monthly_interest_paid": monthly_combined["interest_paid"],
            "fortnightly_periods": fortnightly_combined["periods"],
            "fortnightly_remaining_principal": fortnightly_combined["remaining_principal_list"],
            "fortnightly_interest_paid": fortnightly_combined["interest_paid"]
        }
    elif response == "amortization":
        return {
            "monthly_amortization": monthly_combined["amortization_table"],
            "fortnightly_amortization": fortnightly_combined["amortization_table"]
        }
    elif response == "detailed_summary":
        return {
            "estimated_repayments": format_currency(monthly_combined["repayment_amount"]),
            "full_term_to_amortize": format_periods(monthly_combined["remaining_periods"], "Monthly"),
            "interest": format_currency(monthly_combined["interest_paid"][0]),
            "principal": format_currency(monthly_combined["principal_paid"][0]),
            "extra": "$0.00",
            "repayment": format_currency(monthly_combined["repayment_amount"]),
            "payments_over_term": monthly_combined["remaining_periods"],
            "payments_over_reduced_term": 0,
            "total_principal_interest": format_currency(monthly_combined["total_repayment"]),
            "interest_over_term": format_currency(sum(monthly_combined["interest_paid"])),
            "interest_over_reduced_term": "$0.00",
            "interest_saved_over_reduced_term": "$0.00",
            "total_principal_interest_over_reduced_term": "$0.00"
        }
    else:
        raise ValueError("Invalid response type. Expected 'new_summary', 'summary', 'change_summary', 'graph', 'amortization', or 'detailed_summary'.")

'''
def format_periods(periods, frequency="Monthly"):
    if frequency == "Monthly":
        years = periods // 12
        months = periods % 12
    else:
        years = periods // 26
        months = (periods % 26) * 2 // 1  # Convert fortnightly periods to months
    return f"{int(years)} years, {int(months)} months"
'''