from rest_framework import serializers
from .models import Customer, Group, Expense, Settlement
from .helper import convert_epoch_to_datetime, simplify_debts, calculate_share_on_each, calculate_individual_share

class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = ['id', 'name', 'email','password','avatar', 'mobile','timestamp']
    
    def to_representation(self, instance):
        representation = super(CustomerSerializer, self).to_representation(instance)
        if 'password' in representation:
            del representation['password']
        representation['timestamp'] = convert_epoch_to_datetime(representation['timestamp'])
        return representation

class FriendsSerlializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = ['id','name']
    
class FriendsWithBalanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = ['id','name','avatar']

    def to_representation(self, instance):
        representation = super(FriendsWithBalanceSerializer, self).to_representation(instance)
        group_obj = Group.objects.filter(customers__id=instance.id).values_list('id', flat=True)
        balance = 0
        for group_id in group_obj:
            debts_list = simplify_debts(group_id)
            balance += calculate_individual_share(self.context.get('user_id'),instance.id, debts_list)
        representation['balance'] = round(balance, 2)
        return representation

class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = '__all__'
    
    def to_representation(self, instance):
        representation = super(GroupSerializer, self).to_representation(instance)
        representation['timestamp'] = convert_epoch_to_datetime(representation['timestamp'])
        FriendsData = CustomerSerializer(instance.customers, many=True).data
        
        friends_list = []
        for friend in FriendsData:
            if self.context.get('user_id') != friend['id']: 
                friends_list.append(friend['name']) 
        
        representation['customers'] = friends_list
        return representation

class SimplifyDebitsInGroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ['id', 'name']
    
    def to_representation(self, instance):
        representation = super(SimplifyDebitsInGroupSerializer, self).to_representation(instance)
        debts_list = simplify_debts(instance.id)
        representation['friends_debts'] = debts_list
        overall_amount = 0
        for debt in debts_list:
            if debt[0].get('paid_by').get('id') == self.context.get('user_id'):
                overall_amount -= debt[2]
            elif debt[1].get('paid_to').get('id') == self.context.get('user_id'):
                overall_amount += debt[2]
        representation['user_debts'] = round(overall_amount,2)
        return representation
    
class GroupFriendSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = '__all__'
    
class ExpenseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Expense
        fields = '__all__'
    
    def to_representation(self, instance):
        representation = super(ExpenseSerializer, self).to_representation(instance)
        representation['timestamp'] = convert_epoch_to_datetime(representation['timestamp'])
        representation['updatetimestamp'] = convert_epoch_to_datetime(representation['updatetimestamp'])

        FriendsData = CustomerSerializer(instance.split_on, many=True).data
        representation['paid_by'] = {'id':instance.paid_by.id, 'name':instance.paid_by.name}
        friends_list = []
        for friend in FriendsData:
            if self.context.get('user_id') != friend['id']: 
                friends_list.append({'id':friend['id'],'name':friend['name']}) 
        
        representation['split_on'] = friends_list
        representation['group'] = {'id':instance.group.id, 'name':instance.group.name}
        return representation

class ActivitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Expense
        fields = ['id', 'item', 'amount', 'group','paid_by' ,'split_on','timestamp', 'updatetimestamp']
    
    def to_representation(self, instance):
        representation = super(ActivitySerializer, self).to_representation(instance)
        representation['timestamp'] = convert_epoch_to_datetime(representation['timestamp'])
        representation['updatetimestamp'] = convert_epoch_to_datetime(representation['updatetimestamp'])
        friend_data = CustomerSerializer(instance.split_on, many=True).data
        friends_list = []
        for friend in friend_data:
            if self.context.get('user_email') != friend['email']: 
                friends_list.append({'id':friend['id'],'name':friend['name']}) 
        representation['split_on'] = friends_list
        representation['share'] = calculate_share_on_each(self.context, instance)
        representation['paid_by'] = {'id':instance.paid_by.id, 'name':instance.paid_by.name}
        representation['group'] = {'id':instance.group.id, 'name':instance.group.name}
        return representation

class SettlementSerializer(serializers.ModelSerializer):
    class Meta:
        model = Settlement
        fields = '__all__'
