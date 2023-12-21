from django.contrib import admin
from .models import Customer, Group, Expense, Settlement

admin.site.register(Customer)
admin.site.register(Group)
admin.site.register(Expense)
# admin.site.register(Balance)
admin.site.register(Settlement)