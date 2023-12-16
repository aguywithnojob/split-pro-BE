import datetime
from .models import Expense, Customer
from django.db.models import Q
# function convert epoch to datetime format "6 Nov, 12:14 AM"
def convert_epoch_to_datetime(epoch):
    dt = datetime.datetime.fromtimestamp(epoch)
    formatted_dt = dt.strftime("%d %b, %I:%M %p")
    return formatted_dt

def calculate_overall_balance(user_email):
    overall_balance = 0
    user_obj = Customer.objects.get(email=user_email)
    if not user_obj:
        # throw error user not found
        raise ValueError('User not found')
    
    # in which you paid
    paid_by_obj = Expense.objects.filter(Q(paid_by=user_obj)|Q(split_on__in=[user_obj])).distinct()

    for expense_obj in paid_by_obj:
        print('=>>>>',expense_obj.split_on.all())
        if user_obj == expense_obj.paid_by:
            individual_share = (expense_obj.amount - (expense_obj.amount / expense_obj.split_on.count()))
            print('paid by you ==>', individual_share)
            overall_balance += individual_share
        elif (user_obj in expense_obj.split_on.all()) :
            individual_share = expense_obj.amount / expense_obj.split_on.count()
            print('split on you ===>', individual_share)
            overall_balance -= individual_share
        
    print('overall balance ==>',overall_balance)

    # split_on_obj = Expense.objects.filter(split_on__in=user_obj)
    # print('split on obj ==>',split_on_obj.query)
    # for expense_obj in split_on_obj:
    #     individual_share = expense_obj.amount / expense_obj.paid_by.count()
    #     overall_balance -= individual_share
    return overall_balance