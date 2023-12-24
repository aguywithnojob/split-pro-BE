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

def calculate_overall_balance(user_email, group_id = None):
    paid_amount = 0
    split_amount = 0
    user_obj = Customer.objects.get(email=user_email)

    if not user_obj:
        # throw error user not found
        raise ValueError('User not found')
    
    if group_id:
        # group in which you paid or you are part of split_on
        paid_by_obj = Expense.objects.filter(Q(Q(paid_by=user_obj)| Q(split_on__in=[user_obj])) & Q(group__id=group_id)).distinct()
    else:
        # in which you paid or you are part of split_on
        paid_by_obj = Expense.objects.filter(Q(paid_by=user_obj)|Q(split_on__in=[user_obj])).distinct()
    
    for expense_obj in paid_by_obj:
        if user_obj == expense_obj.paid_by:
            if (user_obj not in expense_obj.split_on.all()):
                paid_amount += expense_obj.amount
            else:
                # calculate paid amount which is ((totalamount/number of people) * number of people - 1)
                paid_amount += ((expense_obj.amount/expense_obj.split_on.count()) * (expense_obj.split_on.count() - 1))
        elif (user_obj in expense_obj.split_on.all()) :
            if (user_obj in expense_obj.split_on.all()):
                split_amount += (expense_obj.amount/expense_obj.split_on.count())

    return round(paid_amount - split_amount, 2)


# method to calculate share on each person w.r.t to current_user
def calculate_share_on_each(context, instance):
    # if current_user didn't pay and he is part of split_on
    if (context.get('user_email') != instance.paid_by.email) and (context.get('user_email') in instance.split_on.values_list('email', flat=True)):
        share = -(instance.amount/instance.split_on.all().count())
    elif (context.get('user_email') != instance.paid_by.email) and (context.get('user_email') not in instance.split_on.values_list('email', flat=True)):
        share = 0
    # if current_user paid and he is part of split_on
    elif (context.get('user_email') == instance.paid_by.email) and (context.get('user_email') in instance.split_on.values_list('email', flat=True)):
        share = (instance.amount/instance.split_on.all().count()) * (instance.split_on.all().count() - 1)
    else: 
        share = instance.amount
    
    return round(share, 2)

# method to simplidy debts for a group
def simplify_debts(group_id):
    result_dict = {}
    user_list = Customer.objects.filter(groups__id=group_id)
    for user_tuple in user_list:
        if user_tuple not in result_dict:
            result_dict[user_tuple] = dict(pay = 0.00, get = 0.00)

        filtered_expenses = Expense.objects.filter(paid_by=user_tuple, group_id=group_id).exclude(expenses__expense_included__in = Expense.objects.filter(paid_by=user_tuple, group_id=group_id).values_list('id', flat=True))

        for exp in filtered_expenses: # exp must not present in settlement table for this user
            amount = exp.amount
            if (user_tuple.id in exp.split_on.all().values_list('id', flat=True)):    
                #if payer is also part of the split
                share = (amount/exp.split_on.count()) * (exp.split_on.count() - 1)
            else:       
                #if payer is not part of the split
                share = amount
            result_dict[user_tuple]['get'] += share
            
            # for current expense dividing amount among users who have to pay
            for share_user in user_list:
                if share_user != user_tuple:
                    if share_user not in result_dict:
                        result_dict[share_user] = dict(pay = 0.00, get = 0.00)
                    
                    # share_user is involved in transaction then he has to pay the expense amount
                    if (share_user.id in exp.split_on.all().values_list('id', flat=True)):
                        result_dict[share_user]['pay'] += exp.amount/exp.split_on.count()

    balances = {}
    
    # Calculate net amount for each person
    for person, details in result_dict.items():
        pay = details['pay']
        get = details['get']
        balances[person] = (get - pay)

    # Identify people who owe and people who are owed
    creditors = {person: amount for person, amount in balances.items() if amount > 0.00}
    debtors = {person: -amount for person, amount in balances.items() if amount < 0.00}

    # Build a list of transactions using the Debt Graph algorithm
    transactions = []
    for debtor, debtor_amount in debtors.items():
        while debtor_amount > 0.00:
            # Find the creditor with the maximum amount
            creditor, creditor_amount = max(creditors.items(), key=lambda x: x[1])

            # Determine the amount to be transferred
            transfer_amount = min(debtor_amount, creditor_amount)

            # Update balances
            debtor_amount = (debtor_amount - transfer_amount)
            creditor_amount = (creditor_amount - transfer_amount)

            # Add the transaction to the list
            transactions.append(({"paid_by":{"id":debtor.id, "name":debtor.name}}, {"paid_to":{"id":creditor.id, "name":creditor.name}}, round(transfer_amount, 2)))

            # Update balances and remove creditors with a balance of 0
            creditors[creditor] = creditor_amount
            if creditor_amount == 0.00:
                del creditors[creditor]

    return transactions


def calculate_individual_share(current_user_id, friend_id, debt_list ):
    overall_amount = 0
    for debt in debt_list:
        # paid_by is current_user and paid_to is my friend or vice versa then calculate share amount
        if (debt[0].get('paid_by').get('id') == current_user_id) and (debt[1].get('paid_to').get('id') == friend_id):
            overall_amount -= debt[2]
        
        if (debt[0].get('paid_by').get('id') == friend_id) and (debt[1].get('paid_to').get('id') == current_user_id):
            overall_amount += debt[2]
    return round(overall_amount,2)