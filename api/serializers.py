from rest_framework import serializers
from .models import Customer, Group, Expense, Settlement
from .helper import convert_epoch_to_datetime, simplify_debts, calculate_share_on_each

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
        # call smplify_debts function with group_id
        representation['friends_debts'] = simplify_debts(instance.id)
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
    
    def to_representation(self, instance):
        representation = super(SettlementSerializer, self).to_representation(instance)
        representation['timestamp'] = convert_epoch_to_datetime(representation['timestamp'])
        representation['paid_by'] = {'id':instance.paid_by.id, 'name':instance.paid_by.name}
        representation['paid_to'] = {'id':instance.paid_to.id, 'name':instance.paid_to.name}
        return representation
