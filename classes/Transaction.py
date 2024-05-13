import datetime


class Transaction:
    def __init__(self, transactionID, currentPrincipal, currentInterest, startDate, extraPayment, extraPaymentType, ballonPayment, comment):
        self._transactionID = transactionID
        self._currentPrincipal = currentPrincipal
        self._currentInterest = currentInterest
        self._startDate = startDate
        self._extraPayment = extraPayment
        self._extraPaymentType = extraPaymentType
        self._ballonPayment = ballonPayment
        self._comment = comment
    
    @property
    def transactionID(self):
        return self._transactionID
    
    @transactionID.setter
    def transactionID(self, value):
        if not value:
            raise ValueError("Transaction ID must be provided.")
        try:
            transaction_ID = int(value)
        except ValueError:
            raise ValueError("Mortgage ID must be an integer")
        if transaction_ID <= 0:
            raise ValueError("Mortgage ID must be between 1 and 8")
        self._trasnactionID = transaction_ID
    
    @property
    def currentPrincipal(self):
        return self._currentPrincipal
    
    @currentPrincipal.setter
    def currentPrincipal(self, value):
        if not value:
            raise ValueError("Current Principal must be provided.")
        try:
            current_principal = float(value)
        except ValueError:
            raise ValueError("Current Principal must be a number")
        if current_principal < 0:
            raise ValueError("Current Principal cannot be negative")
        self._currentPrincipal = current_principal
        
    @property
    def currentInterest(self):
        return self._currentInterest
    
    @currentInterest.setter
    def currentInterest(self, value):
        if not value:
            raise ValueError("Current Interest must be provided.")
        try:
            current_interest = float(value)
        except ValueError:
            raise ValueError("Current Interest must be a number")
        if current_interest < 0:
            raise ValueError("Current Interest cannot be negative")
        self._currentInterest = current_interest
    
    @property
    def startDate(self):
        return self._startDate
    
    @startDate.setter
    def startDate(self, value):
        if not value:
            self._startDate = datetime.today()
        try:
            startDate = datetime.strptime(value, '%Y-%m-%d')
        except ValueError:
            raise ValueError("Start date must be in YYYY-MM-DD format")
        self._estabDate = startDate
    
    @property
    def extraPayment(self):
        return self._extraPayment
    
    @extraPayment.setter
    def extraPayment(self, value):
        if not value:
            self._extraPayment = 0
        try:
            extra_payment = float(value)
        except ValueError:
            raise ValueError("Extra Payment must be a number")
        if extra_payment < 0:
            raise ValueError("Extra Payment cannot be negative")
        self._extraPayment = extra_payment
    
    @property
    def extraPaymentType(self):
        return self._extraPaymentType
    
    @extraPaymentType.setter
    def extraPaymentType(self, value):
        if not value:
            self._extraPaymentType = "None"
        if value not in ["Monthly", "Fortnightly", "None"]:
            raise ValueError("Extra Payment Type must be 'Monthly', 'Fortnightly', or 'None'")
        self._extraPaymentType = value
    
    @property
    def ballonPayment(self):
        return self._ballonPayment
    
    @ballonPayment.setter
    def ballonPayment(self, value):
        if not value:
            self._ballonPayment = 0
        try:
            ballon_payment = int(value)
        except ValueError:
            raise ValueError("Ballon Payment must be a number")
        if ballon_payment < 0:
            raise ValueError("Ballon Payment cannot be negative")
        self._ballonPayment = ballon_payment
    
    @property
    def comment(self):
        return self._comment
    
    @comment.setter
    def comment(self, value):
        if not value:
            self._comment = ""
        self._comment = str(value)