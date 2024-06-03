import datetime

class Transaction:
    def __init__(self, currentPrincipal, currentInterest, startDate, extraPayment, extraPaymentType, balloonPayment, comment):
        self.currentPrincipal = currentPrincipal
        self.currentInterest = currentInterest
        self.startDate = startDate
        self.extraPayment = extraPayment
        self.extraPaymentType = extraPaymentType
        self.balloonPayment = balloonPayment
        self.comment = comment
    
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
            self._startDate = datetime.datetime.today().strftime("%Y-%m-%d")
        elif isinstance(value, datetime.date):
            self._startDate = value.strftime("%Y-%m-%d")
        elif isinstance(value, str):
            try:
                self._startDate = datetime.datetime.strptime(value, '%Y-%m-%d').strftime("%Y-%m-%d")
            except ValueError:
                raise ValueError("Start date must be in YYYY-MM-DD format")
        else:
            raise TypeError("Start date must be a string or datetime.date")
    
    @property
    def extraPayment(self):
        return self._extraPayment
    
    @extraPayment.setter
    def extraPayment(self, value):
        if not value:
            self._extraPayment = 0
        else:
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
        else:
            if value not in ["Monthly", "Fortnightly", "None"]:
                raise ValueError("Extra Payment Type must be 'Monthly', 'Fortnightly', or 'None'")
            self._extraPaymentType = value
    
    @property
    def balloonPayment(self):
        return self._balloonPayment
    
    @balloonPayment.setter
    def balloonPayment(self, value):
        if not value:
            self._balloonPayment = 0
        else:
            try:
                balloon_payment = int(value)
            except ValueError:
                raise ValueError("Balloon Payment must be a number")
            if balloon_payment < 0:
                raise ValueError("Balloon Payment cannot be negative")
            self._balloonPayment = balloon_payment
    
    @property
    def comment(self):
        return self._comment
    
    @comment.setter
    def comment(self, value):
        if not value:
            self._comment = ""
        else:
            self._comment = str(value)
