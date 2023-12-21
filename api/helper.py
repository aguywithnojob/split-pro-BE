import datetime
from .models import Expense, Customer
from django.db.models import Q, F
# function convert epoch to datetime format "6 Nov, 12:14 AM"
def convert_epoch_to_datetime(epoch):
    dt = datetime.datetime.fromtimestamp(epoch)
    if dt.date() == datetime.date.today():
        formatted_dt = f"Today, {dt.strftime('%I:%M %p')}"
    else:
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


# method to calculate share on each person w.r.t to current_user
def calculate_share_on_each(context, instance):
    # if current_user didn't pay and he is part of split_on
    if (context.get('user_email') != instance.paid_by.email) and (context.get('user_email') in instance.split_on.values_list('email', flat=True)):
        share = -(instance.amount/instance.split_on.all().count())
    elif (context.get('user_email') != instance.paid_by.email) and (context.get('user_email') not in instance.split_on.values_list('email', flat=True)):
        share = 0
    # if current_user paid and he is part of split_on
    elif (context.get('user_email') == instance.paid_by.email) and (context.get('user_email') in instance.split_on.values_list('email', flat=True)):
        share = round((instance.amount/instance.split_on.all().count()),2) * (instance.split_on.all().count() - 1)
    else: 
        share = instance.amount
    
    return share

    # result_dict = {}
    # all_users = (badal, gautam, kartikey, tushar)
    # for user in all_users:
    #     if user.username not in result_dict:
    #         result_dict[user.username] = dict(pay = 0, get = 0)

    #     filtered_expenses = Expenses.objects.filter(paid_by=user).exclude(settlments__expense__in=Expenses.objects.filter(paid_by=user).values_list('id', flat=True))
    #     print(filtered_expenses.query)

    #     for exp in filtered_expenses: # exp must not present in settlement table for this user
    #         # result_dict[user.username]['get'] += exp.amount
    #         amount = exp.amount
    #         share = amount/4
    #         result_dict[user.username]['get'] = share * 3 

    #         for share_user in all_users:
    #             if share_user != user:
    #                 if share_user.username not in result_dict:
    #                     result_dict[share_user.username] = dict(pay = 0, get = 0)
    #                 result_dict[share_user.username]['pay'] += share

# method simplify debts in a group
def simplify_debts(group_id):
    result_dict = {}
    user_list = Customer.objects.filter(groups__id=group_id).values_list('id','name')
    
    for user_tuple in user_list:
        if user_tuple not in result_dict:
            result_dict[user_tuple] = dict(pay = 0, get = 0)

        filtered_expenses = Expense.objects.filter(paid_by=user_tuple[0]).exclude(id__in = Expense.objects.filter(paid_by=user_tuple[0]).values_list('id', flat=True))
        print(filtered_expenses.query)

        for exp in filtered_expenses: # exp must not present in settlement table for this user
            # result_dict[user.username]['get'] += exp.amount
            amount = exp.amount
            if (user_tuple[0] in exp.split_on.all()):    
                #if payer is also part of the split
                share = (amount/exp.split_on.count()) * (exp.split_on.count() - 1)
            else:       
                #if payer is not part of the split
                share = amount
            result_dict[user_tuple]['get'] = share

            for share_user in user_list:
                if share_user != user_tuple:
                    if share_user not in result_dict:
                        result_dict[share_user] = dict(pay = 0, get = 0)
                    result_dict[share_user]['pay'] += share

    balances = {}

    # Calculate net amount for each person
    for person, details in result_dict.items():
        pay = details['pay']
        get = details['get']
        balances[person] = get - pay

    # Identify people who owe and people who are owed
    creditors = {person: amount for person, amount in balances.items() if amount > 0}
    debtors = {person: -amount for person, amount in balances.items() if amount < 0}

    # Build a list of transactions using the Debt Graph algorithm
    transactions = []
    for debtor, debtor_amount in debtors.items():
        while debtor_amount > 0:
            # Find the creditor with the maximum amount
            creditor, creditor_amount = max(creditors.items(), key=lambda x: x[1])

            # Determine the amount to be transferred
            transfer_amount = min(debtor_amount, creditor_amount)

            # Update balances
            debtor_amount -= transfer_amount
            creditor_amount -= transfer_amount

            # Add the transaction to the list
            transactions.append((debtor, creditor, transfer_amount))

            # Update balances and remove creditors with a balance of 0
            creditors[creditor] = creditor_amount
            if creditor_amount == 0:
                del creditors[creditor]

    print(transactions)  
    return transactions
