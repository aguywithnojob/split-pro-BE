import datetime
from .models import Expense, Customer
from django.db.models import Q
# function convert epoch to datetime format "6 Nov, 12:14 AM"
def convert_epoch_to_datetime(epoch):
    dt = datetime.datetime.fromtimestamp(epoch)
    formatted_dt = dt.strftime("%d %b, %I:%M %p")
    return formatted_dt

def calculate_overall_balance(user_email):
    paid_amount = 0
    split_amount = 0
    user_obj = Customer.objects.get(email=user_email)
    if not user_obj:
        # throw error user not found
        raise ValueError('User not found')
    # in which you paid
    paid_by_obj = Expense.objects.filter(Q(paid_by=user_obj)|Q(split_on__in=[user_obj])).distinct()
    
    # cash flow would be sum(paid_amount) - sum(split_amount)
    for expense_obj in paid_by_obj:
        if user_obj == expense_obj.paid_by:
            paid_amount += expense_obj.amount 
        elif (user_obj in expense_obj.split_on.all()) :
            split_amount += expense_obj.amount

    return paid_amount - split_amount