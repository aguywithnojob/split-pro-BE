from rest_framework import serializers
from .models import Customer, Group, Expense, Balance,  Settlement
from .helper import convert_epoch_to_datetime
class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = '__all__'
    
    def to_representation(self, instance):
        representation = super(CustomerSerializer, self).to_representation(instance)
        representation['password'] = '*'*len(representation['password'])
        representation['timestamp'] = convert_epoch_to_datetime(representation['timestamp'])
        return representation


class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = '__all__'
    
    def to_representation(self, instance):
        representation = super(GroupSerializer, self).to_representation(instance)
        representation['timestamp'] = convert_epoch_to_datetime(representation['timestamp'])
        return representation

class ExpenseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Expense
        fields = '__all__'
    
    def to_representation(self, instance):
        representation = super(ExpenseSerializer, self).to_representation(instance)
        representation['timestamp'] = convert_epoch_to_datetime(representation['timestamp'])
        representation['updatetimestamp'] = convert_epoch_to_datetime(representation['updatetimestamp'])
        return representation

class BalanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Balance
        fields = '__all__'
    
    def to_representation(self, instance):
        representation = super(BalanceSerializer, self).to_representation(instance)
        representation['timestamp'] = convert_epoch_to_datetime(representation['timestamp'])
        return representation

class SettlementSerializer(serializers.ModelSerializer):
    class Meta:
        model = Settlement
        fields = '__all__'
    
    def to_representation(self, instance):
        representation = super(SettlementSerializer, self).to_representation(instance)
        representation['timestamp'] = convert_epoch_to_datetime(representation['timestamp'])
        return representation
