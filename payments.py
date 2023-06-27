

class Payment:
    def __init__(self,payment_id,payment_due=None,amount=0,has_been_paid='Yes'):
        self.payment_id = payment_id
        self.payment_due = payment_due
        self.amount = amount
        self.has_been_paid = has_been_paid

    def get_payment_id(self):
        return self.payment_id

    def set_payment_id(self, payment_id):
        self.payment_id = payment_id

    def get_payment_due(self):
        return self.payment_due

    def set_payment_due(self, payment_due_):
        self.payment_due = payment_due_

    def get_amount(self):
        return self.amount

    def set_amount(self, amount):
        self.amount = amount
        if amount > 0:
            self.has_been_paid = "No"
        else:
            self.has_been_paid = 'Yes'

    def get_has_been_paid(self):
        return self.has_been_paid

    def set_has_been_paid(self, has_been_paid):
        self.has_been_paid = has_been_paid

    def print_payment_details(self,name_):
        print(f"payment of user {name_}")
        print("Payment ID:", self.get_payment_id())
        print("Payment Due Date:", self.get_payment_due())
        print("Amount:", self.get_amount())
        print("Has Been Paid?:", self.get_has_been_paid(),end='')
        return ''

