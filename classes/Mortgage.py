import datetime

class Mortgage:
    def __init__(self, mortgageName, estabDate, initialInterest, initialTerm, initialPrincipal, extraCost, deposit):
        self.mortgageName = mortgageName
        self.estabDate = estabDate
        self.initialInterest = initialInterest
        self.initialTerm = initialTerm
        self.initialPrincipal = initialPrincipal
        self.extraCost = extraCost
        self.deposit = deposit
    
    @property
    def mortgageName(self):
        return self._mortgageName
    
    @mortgageName.setter
    def mortgageName(self, value):
        mortgageName = str(value)
        if len(mortgageName) <= 0 or len(mortgageName) > 40:
            raise ValueError("Mortgage name must be between 1 and 40 characters long")
        self._mortgageName = mortgageName
    
    @property
    def estabDate(self):
        return self._estabDate

    @estabDate.setter
    def estabDate(self, value):
        if not value:
            self._estabDate = datetime.datetime.today()
        elif isinstance(value, datetime.datetime):
            self._estabDate = value
        elif isinstance(value, str):
            try:
                self._estabDate = datetime.datetime.strptime(value, '%Y-%m-%d')
            except ValueError:
                raise ValueError("Established date must be in YYYY-MM-DD format")
        else:
            raise TypeError("Established date must be a string or datetime.datetime")

    @property
    def initialInterest(self):
        return self._initialInterest
    
    @initialInterest.setter
    def initialInterest(self, value):
        if not value:
            raise ValueError("Initial interest cannot be empty")
        try:
            initialInterest = float(value)
        except ValueError:
            raise ValueError("Initial interest must be a number")
        if initialInterest <= 0 or initialInterest > 100:
            raise ValueError("Initial interest must be between 1 and 100")
        self._initialInterest = initialInterest
    
    @property
    def initialTerm(self):
        return self._initialTerm

    @initialTerm.setter
    def initialTerm(self, value):
        if not value:
            raise ValueError("Initial term cannot be empty")
        try:
            initialTerm = int(value)
        except ValueError:
            raise ValueError("Initial term must be an integer")
        if initialTerm <= 0 or initialTerm > 100:
            raise ValueError("Initial term must be between 1 and 100")
        self._initialTerm = initialTerm
        
    @property
    def initialPrincipal(self):
        return self._initialPrincipal

    @initialPrincipal.setter
    def initialPrincipal(self, value):
        if not value:
            raise ValueError("Initial principal cannot be empty")
        try:
            initialPrincipal = float(value)
        except ValueError:
            raise ValueError("Initial principal must be a number")
        if initialPrincipal <= 0:
            raise ValueError("Initial principal must be greater than 0")
        self._initialPrincipal = initialPrincipal
    
    @property
    def extraCost(self):
        return self._extraCost

    @extraCost.setter
    def extraCost(self, value):
        if not value:
            self._extraCost = 0
        else:
            try:
                extraCost = float(value)
            except ValueError:
                raise ValueError("Extra cost must be a number")
            self._extraCost = extraCost

    @property
    def deposit(self):
        return self._deposit

    @deposit.setter
    def deposit(self, value):
        if not value:
            self._deposit = 0
        else:
            try:
                deposit = float(value)
            except ValueError:
                raise ValueError("Deposit must be a number")
            if deposit <= 0:
                raise ValueError("Deposit must be greater than 0")
            self._deposit = deposit
