import datetime


class Mortgage:
    def __init__(self, mortgageID, mortgageName, estabDate, initialInterest, initialTerm, initialPrincipal, extraCost, desposit):
        self._mortgageID = mortgageID
        self._mortgageName = mortgageName
        self._estabDate = estabDate
        self._initialInterest = initialInterest
        self._initialTerm = initialTerm
        self._initialPrincipal = initialPrincipal
        self._extraCost = extraCost
        self._desposit = desposit

    @property
    def mortgageID(self):
        return int(self._mortgageID)
    
    @mortgageID.setter
    def mortgageID(self, value):
        if not value:
            raise ValueError("Mortgage ID cannot be empty")
        try:
            mortgage_ID = int(value)
        except ValueError:
            raise ValueError("Mortgage ID must be an integer")
        if mortgage_ID <= 0:
            raise ValueError("Mortgage ID must be between 1 and 8")
        self._mortgageID = mortgage_ID
    
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
            self._estabDate = datetime.today()
        try:
            estabDate = datetime.strptime(value, '%Y-%m-%d')
        except ValueError:
            raise ValueError("Established date must be in YYYY-MM-DD format")
        self._estabDate = estabDate

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
            initialPrincipal = int(value)
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
        try:
            extraCost = float(value)
        except ValueError:
            raise ValueError("Extra cost must be a number")
        self._extraCost = extraCost

    @property
    def desposit(self):
        return self._desposit

    @desposit.setter
    def desposit(self, value):
        if not value:
            self._desposit = 0
        try:
            desposit = float(value)
        except ValueError:
            raise ValueError("Desposit must be a number")
        if desposit <= 0:
            raise ValueError("Desposit must be greater than 0")
        self._desposit = desposit
    
    '''
    @property
    def userID(self):
        return self._userID
    
    @userID.setter
    def userID(self, value):
        if not value:
            raise ValueError("User ID cannot be empty")
        try:
            userID = int(value)
        except ValueError:
            raise ValueError("User ID must be an integer")
        if userID <= 0:
            raise ValueError("User ID must be greater than 0")
        self._userID = userID
    '''