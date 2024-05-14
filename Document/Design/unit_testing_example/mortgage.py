class Mortgage:
    def __init__(self, mortgageID, mortgageName, estabDate, initialInterest, 
                 initialTerm, initialPrincipal, extraCost, deposit, UserID):
        self.mortgageID = mortgageID
        self.mortgageName = mortgageName
        self.estabDate = estabDate
        self.initialInterest = initialInterest
        self.initialTerm = initialTerm
        self.initialPrincipal = initialPrincipal
        self.extraCost = extraCost
        self.deposit = deposit
        self.UserID = UserID

    @property
    def principal(self):
        return self.initialPrincipal

    @principal.setter
    def principal(self, value):
        if not isinstance(value, int):
            raise ValueError("Principal must be an integer")
        self.initialPrincipal = value
        return

