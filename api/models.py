from django.db import models
from datetime import datetime
from django.contrib.auth.models import User
# Create your models here.
class Customer(models.Model):
    name = models.CharField(max_length=50)
    email = models.EmailField(max_length=50, unique=True)
    password = models.CharField(max_length=255)
    mobile = models.CharField(max_length=10, unique=True)
    avatar = models.URLField(null=True, blank=True)
    django_user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
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
    group = models.ForeignKey(Group, on_delete=models.CASCADE, related_name="groups")
    item = models.CharField(max_length=100)
    amount = models.FloatField()
    timestamp = models.IntegerField(blank=True, null=True)
    updatetimestamp = models.IntegerField(blank=True, null=True)
    class Meta:
        db_table = "expenses"
    def __str__(self):
        return self.paid_by__name+" paid for "+self.item
    def save(self, *args, **kwargs):
        # Convert epoch timestamp to datetime before saving
        if not self.timestamp:
            self.timestamp = int(datetime.now().timestamp())
        if not self.updatetimestamp:
            self.updatetimestamp = int(datetime.now().timestamp())
        super().save(*args, **kwargs)

# customer outstanding balance (need to pay or need to recieve)
class Balance(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name="balances")
    amount = models.FloatField(default=0.00)
    timestamp = models.IntegerField(blank=True, null=True)
    class Meta:
        db_table = "balances"
    def __str__(self):
        return self.customer__name+" : "+self.amount
    def save(self, *args, **kwargs):
        # Convert epoch timestamp to datetime before saving
        if not self.timestamp:
            self.timestamp = int(datetime.now().timestamp())
        super().save(*args, **kwargs)

class Settlement(models.Model):
    paid_by = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name="settlements_paid_by")
    paid_to = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name="settlements_paid_to")
    amount = models.FloatField()
    mode = models.CharField(max_length=50, default="cash")
    timestamp = models.IntegerField(blank=True, null=True)
    class Meta:
        db_table = "settlements"
    def __str__(self):
        return self.paid_by__name+" paid to  "+self.paid_to__name
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
        #     "django_user":1
        # }
        # {
        #     "name":"kpa-406",
        #     "customers":2
        # }

        # {
        #     "paid_by":1,
        #     "split_on":[1,2,3,4],
        #     "group":2,
        #     "item":"milk",
        #     "amount":90
        # }