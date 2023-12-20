#!/home/tushar/miniconda3/bin/python
import sys, os, django

############ PRODUCTION ENV ########################
sys.path.append('/home/tushar/Documents/practices/splittt/demoproject')
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "demoproject.settings")
django.setup()

from demoapp.models import *


badal = Users.objects.get(username__icontains="badal")
# paid_badal = sum(Expenses.objects.filter(paid_by=badal).values_list('amount', flat=True))
# badal_owes = sum(Shares.objects.filter(user=badal).values_list('amount', flat=True))
# actual_amount_badal = paid_badal - badal_owes

gautam = Users.objects.get(username__icontains="gautam")
# paid_gautam = sum(Expenses.objects.filter(paid_by=gautam).values_list('amount', flat=True))
# gautam_owes = sum(Shares.objects.filter(user=gautam).values_list('amount', flat=True))
# actual_amount_gautam = paid_gautam - gautam_owes

kartikey = Users.objects.get(username__icontains="kartikey")
# paid_kartikey = sum(Expenses.objects.filter(paid_by=kartikey).values_list('amount', flat=True))
# kartikey_owes = sum(Shares.objects.filter(user=kartikey).values_list('amount', flat=True))
# actual_amount_kartikey = paid_kartikey - kartikey_owes

tushar = Users.objects.get(username__icontains="tushar")
# paid_tushar = sum(Expenses.objects.filter(paid_by=tushar).values_list('amount', flat=True))
# tushar_owes = sum(Shares.objects.filter(user=tushar).values_list('amount', flat=True))
# actual_amount_tushar = paid_tushar - tushar_owes

# # print all above values in good format seperated
# owes = [
#     (badal.username, badal_owes, actual_amount_badal),
#     (gautam.username, gautam_owes, actual_amount_gautam),
#     (kartikey.username, kartikey_owes, actual_amount_kartikey),
#     (tushar.username, tushar_owes, actual_amount_tushar)
# ]

# owes_dict = {}
# pays_dict = {}

# for i in owes:
#     if i[-1] > 0:
#         owes_dict[i[0]] = i[-1]
#     else:
#         pays_dict[i[0]] = i[-1]

# print(owes_dict)
# print(pays_dict)
result_dict = {}
all_users = (badal, gautam, kartikey, tushar)
for user in all_users:
    if user.username not in result_dict:
        result_dict[user.username] = dict(pay = 0, get = 0)

    filtered_expenses = Expenses.objects.filter(paid_by=user).exclude(settlments__expense__in=Expenses.objects.filter(paid_by=user).values_list('id', flat=True))
    print(filtered_expenses.query)

    for exp in filtered_expenses: # exp must not present in settlement table for this user
        # result_dict[user.username]['get'] += exp.amount
        amount = exp.amount
        share = amount/4
        result_dict[user.username]['get'] = share * 3 

        for share_user in all_users:
            if share_user != user:
                if share_user.username not in result_dict:
                    result_dict[share_user.username] = dict(pay = 0, get = 0)
                result_dict[share_user.username]['pay'] += share

def balance_amounts(transactions):
    balances = {}

    # Calculate net amount for each person
    for person, details in transactions.items():
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

    return transactions

# print(result_dict)
balances = balance_amounts(result_dict)
print(result_dict)
print(balances)%    
