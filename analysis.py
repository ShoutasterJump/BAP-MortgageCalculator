import datetime

def mortgage_analysis(mortgage, transactions, response):
    def calculate_repayment(principal, interest_rate, repayment_periods, frequency, date_increment, is_initial=False):
        total_interest_paid = 0
        remaining_principal = principal
        remaining_principal_list = []
        interest_paid = []
        periods = []
        amortization_table = []

        current_date = mortgage.estabDate if isinstance(mortgage.estabDate, datetime.datetime) else datetime.datetime.strptime(mortgage.estabDate, "%Y-%m-%d")
        accumulated_interest = 0
        accumulated_principal_payments = 0

        # Use precise calculation for repayment amount
        if interest_rate > 0:
            repayment_amount = principal * (interest_rate / (1 - (1 + interest_rate) ** -repayment_periods))
        else:
            repayment_amount = principal / repayment_periods

        if not is_initial:
            transactions.sort(key=lambda x: x.startDate if isinstance(x.startDate, datetime.datetime) else datetime.datetime.strptime(x.startDate, "%Y-%m-%d"))
            last_transaction_index = 0

            for period in range(1, repayment_periods + 1):
                extra_payment = 0
                if last_transaction_index < len(transactions):
                    transaction = transactions[last_transaction_index]
                    transaction_date = transaction.startDate if isinstance(transaction.startDate, datetime.datetime) else datetime.datetime.strptime(transaction.startDate, "%Y-%m-%d")
                    if transaction_date <= current_date:
                        remaining_principal = transaction.currentPrincipal - transaction.balloonPayment
                        interest_rate = transaction.currentInterest / 100 / (12 if frequency == "Monthly" else 26)
                        extra_payment = transaction.extraPayment
                        if interest_rate > 0:
                            repayment_amount = remaining_principal * (interest_rate / (1 - (1 + interest_rate) ** -repayment_periods))
                        else:
                            repayment_amount = remaining_principal / repayment_periods
                        last_transaction_index += 1

                interest_payment = remaining_principal * interest_rate
                principal_payment = repayment_amount - interest_payment
                total_repayment = principal_payment + interest_payment + extra_payment

                new_balance = remaining_principal - principal_payment - extra_payment
                total_interest_paid += interest_payment
                accumulated_interest += interest_payment
                accumulated_principal_payments += principal_payment

                remaining_principal_list.append(round(new_balance, 2))
                interest_paid.append(round(total_interest_paid, 2))
                periods.append(period)

                amortization_table.append({
                    "Date": current_date.strftime("%Y-%m-%d"),
                    "Balance": round(remaining_principal, 2),
                    "Interest": round(interest_payment, 2),
                    "Principal": round(principal_payment, 2),
                    "Extra": round(extra_payment, 2),
                    "Repayment": round(repayment_amount, 2),
                    "Amount of Principal": round(principal_payment + extra_payment, 2),
                    "New Balance": round(new_balance, 2),
                    "Accumulated Interest": round(accumulated_interest, 2),
                    "Accumulated Principal Payments": round(accumulated_principal_payments, 2)
                })

                remaining_principal = new_balance
                current_date += date_increment

                if remaining_principal <= 0:
                    break

        return {
            "repayment_amount": round(repayment_amount, 2),
            "total_repayment": round(repayment_periods * repayment_amount, 2),
            "remaining_principal_list": remaining_principal_list,
            "interest_paid": interest_paid,
            "periods": periods,
            "amortization_table": amortization_table,
            "total_interest_paid": round(total_interest_paid, 2)
        }

    # Initial calculations
    principal = mortgage.initialPrincipal + mortgage.extraCost - mortgage.deposit

    # Monthly calculations
    monthly_interest_rate = mortgage.initialInterest / 100 / 12
    monthly_repayment_periods = mortgage.initialTerm * 12
    initial_monthly_data = calculate_repayment(principal, monthly_interest_rate, monthly_repayment_periods, "Monthly", datetime.timedelta(days=30), is_initial=True)

    # Fortnightly calculations
    fortnightly_interest_rate = mortgage.initialInterest / 100 / 26
    fortnightly_repayment_periods = mortgage.initialTerm * 26
    initial_fortnightly_data = calculate_repayment(principal, fortnightly_interest_rate, fortnightly_repayment_periods, "Fortnightly", datetime.timedelta(days=14), is_initial=True)

    # Recalculate with transactions
    monthly_data = calculate_repayment(principal, monthly_interest_rate, monthly_repayment_periods, "Monthly", datetime.timedelta(days=30))
    fortnightly_data = calculate_repayment(principal, fortnightly_interest_rate, fortnightly_repayment_periods, "Fortnightly", datetime.timedelta(days=14))

    if response == "new_summary":
        return {
            "monthly_repayment": initial_monthly_data["repayment_amount"],
            "monthly_periods": monthly_repayment_periods,
            "monthly_total_repayment": initial_monthly_data["total_repayment"],
            "fortnightly_repayment": initial_fortnightly_data["repayment_amount"],
            "fortnightly_periods": fortnightly_repayment_periods,
            "fortnightly_total_repayment": initial_fortnightly_data["total_repayment"],
        }
    elif response == "summary":
        return {
            "monthly_repayment": initial_monthly_data["repayment_amount"],
            "monthly_total_repayment": initial_monthly_data["total_repayment"],
            "fortnightly_repayment": initial_fortnightly_data["repayment_amount"],
            "fortnightly_total_repayment": initial_fortnightly_data["total_repayment"],
            "monthly_total_interest_paid": monthly_data["total_interest_paid"],
            "fortnightly_total_interest_paid": fortnightly_data["total_interest_paid"]
        }
    elif response == "change_summary":
        new_monthly_repayment = monthly_data["repayment_amount"]
        change_in_monthly_repayment = new_monthly_repayment - initial_monthly_data["repayment_amount"]
        change_in_monthly_repayment = round(change_in_monthly_repayment, 2)
        new_monthly_total_repayment = monthly_data["total_repayment"]
        change_in_monthly_total_repayment = new_monthly_total_repayment - initial_monthly_data["total_repayment"]
        change_in_monthly_total_repayment = round(change_in_monthly_total_repayment, 2)

        new_fortnightly_repayment = fortnightly_data["repayment_amount"]
        change_in_fortnightly_repayment = new_fortnightly_repayment - initial_fortnightly_data["repayment_amount"]
        change_in_fortnightly_repayment = round(change_in_fortnightly_repayment, 2)
        new_fortnightly_total_repayment = fortnightly_data["total_repayment"]
        change_in_fortnightly_total_repayment = new_fortnightly_total_repayment - initial_fortnightly_data["total_repayment"]
        change_in_fortnightly_total_repayment = round(change_in_fortnightly_total_repayment, 2)

        return {
            "new_monthly_repayment": new_monthly_repayment,
            "change_in_monthly_repayment": change_in_monthly_repayment,
            "new_monthly_total_repayment": new_monthly_total_repayment,
            "change_in_monthly_total_repayment": change_in_monthly_total_repayment,
            "new_fortnightly_repayment": new_fortnightly_repayment,
            "change_in_fortnightly_repayment": change_in_fortnightly_repayment,
            "new_fortnightly_total_repayment": new_fortnightly_total_repayment,
            "change_in_fortnightly_total_repayment": change_in_fortnightly_total_repayment
        }
    elif response == "graph":
        return {
            "monthly_periods": monthly_data["periods"],
            "monthly_remaining_principal": monthly_data["remaining_principal_list"],
            "monthly_interest_paid": monthly_data["interest_paid"],
            "fortnightly_periods": fortnightly_data["periods"],
            "fortnightly_remaining_principal": fortnightly_data["remaining_principal_list"],
            "fortnightly_interest_paid": fortnightly_data["interest_paid"]
        }
    elif response == "amortization":
        return {
            "monthly_amortization": monthly_data["amortization_table"],
            "fortnightly_amortization": fortnightly_data["amortization_table"]
        }
    else:
        raise ValueError("Invalid response type. Expected 'new_summary', 'summary', 'change_summary', 'graph', or 'amortization'.")
