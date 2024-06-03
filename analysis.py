from classes.Mortgage import Mortgage

def newMortgageSummary(mortgage):
    principal = mortgage._initialPrincipal + mortgage._extraCost - mortgage._deposit
    
    monthlyInterest = mortgage._initialInterest / 100 / 12
    monthlyNumberofPayments = mortgage._initialTerm * 12
    
    monthlyRepayment = principal * ((monthlyInterest * pow(1 + monthlyInterest, monthlyNumberofPayments))/(pow(1 + monthlyInterest, monthlyNumberofPayments) - 1))
    monthlyRepaymentPeriods = mortgage._initialTerm * 12
    monthlyTotalRepayment = monthlyRepaymentPeriods * monthlyRepayment
    
    fortnightlyInterest = mortgage._initialInterest / 100 / 26
    fortnightlyNumberofPayments = mortgage._initialTerm * 26
    
    fortnightlyRepayment = principal * ((fortnightlyInterest * pow(1 + fortnightlyInterest, fortnightlyNumberofPayments))/(pow(1 + fortnightlyInterest, fortnightlyNumberofPayments) - 1))
    fortnightlyRepaymentPeriods = mortgage._initialTerm * 26
    fortnightlyTotalRepayment = fortnightlyRepaymentPeriods * fortnightlyRepayment
    print(fortnightlyTotalRepayment)
    
    return {
        'monthly_repayment': '$' + str(round(monthlyRepayment,2)),
        'monthly_repayment_periods': monthlyRepaymentPeriods,
        'monthly_total_repayment': '$' + str(round(monthlyTotalRepayment,2)),
        'fortnightly_repayment': '$' + str(round(fortnightlyRepayment,2)),
        'fortnightly_repayment_periods': fortnightlyRepaymentPeriods,
        'fortnightly_total_repayment': '$' + str(round(fortnightlyTotalRepayment,2)),
    }
    
def newMortgageGraph(mortgage):
    pass