from django.db import models
from datetime import datetime
from django.contrib.auth.models import User

def validate_decimals(value):
    try:
        return round(float(value), 2)
    except:
        raise Exception(
            ('%(value)s is not an integer or a float  number'),
            params={'value': value},
        )

# Create your models here.
class Customer(models.Model):
    name = models.CharField(max_length=50)
    email = models.EmailField(max_length=50, unique=True)
    password = models.CharField(max_length=255)
    mobile = models.CharField(max_length=10, unique=True)
    avatar = models.URLField(null=True, blank=True)
    django_user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True, related_name="customer")
    # timestamp epoch time
    timestamp = models.IntegerField(blank=True, null=True)
    class Meta:
        db_table = "customers"
    def __str__(self):
        return self.name
    def save(self, *args, **kwargs):
        # Convert epoch timestamp to datetime before saving
        if not self.timestamp:
            self.timestamp = int(datetime.now().timestamp())
        if not self.avatar:
            # generate random number between 1 to 53
            import random
            self.avatar = f"https://xsgames.co/randomusers/assets/avatars/pixel/{random.randint(1,53)}.jpg"
        try:
            user_obj = User.objects.create(
                username=self.email,
                email=self.email,
            )
            user_obj.set_password(self.password)
            user_obj.save()
        except Exception as e:
            print('user_pbj created error ===>',e)
        self.django_user = user_obj
        super().save(*args, **kwargs)

class Group(models.Model):
    name = models.CharField(max_length=50, unique=True)
    customers = models.ManyToManyField(Customer, related_name="groups")
    timestamp = models.IntegerField(blank=True, null=True)
    class Meta:
        db_table = "groups"
    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        # Convert epoch timestamp to datetime before saving
        if not self.timestamp:
            self.timestamp = int(datetime.now().timestamp())
        super().save(*args, **kwargs)

class Expense(models.Model):
    paid_by = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name="paid_bi")
    split_on = models.ManyToManyField(Customer,related_name="splits_on")
    group = models.ForeignKey(Group, on_delete=models.CASCADE, related_name="groups", blank=True, null=True)
    item = models.CharField(max_length=100)
    amount = models.FloatField(validators=[validate_decimals])
    timestamp = models.IntegerField(blank=True, null=True)
    updatetimestamp = models.IntegerField(blank=True, null=True)
    class Meta:
        db_table = "expenses"
    def __str__(self):
        return self.paid_by.name+" paid for "+self.item
    def save(self, *args, **kwargs):
        # Convert epoch timestamp to datetime before saving
        if not self.timestamp:
            self.timestamp = int(datetime.now().timestamp())
        if not self.updatetimestamp:
            self.updatetimestamp = int(datetime.now().timestamp())
        super().save(*args, **kwargs)


class Settlement(models.Model):
    paid_by = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name="settlements_paid_by")
    paid_to = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name="settlements_paid_to")
    amount = models.FloatField(validators=[validate_decimals])
    mode = models.CharField(max_length=50, default="cash")
    expense_included = models.ManyToManyField(Expense, related_name="expenses")
    timestamp = models.IntegerField(blank=True, null=True)
    class Meta:
        db_table = "settlements"
    def __str__(self):
        return self.paid_by.name+" paid to  "+self.paid_to.name
    def save(self, *args, **kwargs):
        # Convert epoch timestamp to datetime before saving
        if not self.timestamp:
            self.timestamp = int(datetime.now().timestamp())
        super().save(*args, **kwargs)


class Balance(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name="balances")
    amount = models.FloatField(validators=[validate_decimals], default=0.00)
    expense_included = models.ManyToManyField(Expense, related_name="balances")
    timestamp = models.IntegerField(blank=True, null=True)
    class Meta:
        db_table = "balances"
    def __str__(self):
        return self.customer.name
    def save(self, *args, **kwargs):
        # Convert epoch timestamp to datetime before saving
        if not self.timestamp:
            self.timestamp = int(datetime.now().timestamp())
        super().save(*args, **kwargs)

        # {
        #     "email":"gautam@gmail.com",
        #     "name":"gautam",
        #     "mobile":1234234,
        #     "password":"gautam1234",
        # }
        # {
        #     "name":"test-1",
        #     "customers":[2,3,4,5]
        # }

        # {
        #     "paid_by":1,
        #     "split_on":[1,2,3,4],
        #     "group":2,
        #     "item":"milk",
        #     "amount":90
        # }



    