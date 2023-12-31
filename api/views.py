from .serializers import (CustomerSerializer, 
                          GroupSerializer, 
                          ExpenseSerializer,
                          SettlementSerializer,
                          FriendsSerlializer,
                          ActivitySerializer,
                          SimplifyDebitsInGroupSerializer,
                          FriendsWithBalanceSerializer
                          )
from .models import (Customer, 
                     Group, 
                     Expense, 
                     Settlement)
from rest_framework.views import APIView
from rest_framework.response import Response
from django.http import JsonResponse
from rest_framework import status
from django.contrib.auth import authenticate, login, logout
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.mixins import LoginRequiredMixin
from rest_framework.permissions import IsAuthenticated
from django.db.models import F, Q
from .helper import calculate_overall_balance

class CustomerView(APIView, LoginRequiredMixin):
    permission_classes = [IsAuthenticated]
    def get(self, request, id=None):
        try:
            if id:
                try:
                    customer = Customer.objects.get(id=id)
                except Customer.DoesNotExist:
                    return Response("User not found",status=status.HTTP_404_NOT_FOUND)
                serializer = CustomerSerializer(customer)
            else:
                customers = Customer.objects.all()
                serializer = CustomerSerializer(customers, many=True)
            if not serializer.data:
                return Response("Records Not Found",status=status.HTTP_404_NOT_FOUND)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response("Internal Server Error:: "+str(e),status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    def post(self, request):
        try:
            serializer = CustomerSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            print('err ==>>',e)
            return Response("Internal Server Error:: "+str(e),status=status.HTTP_500_INTERNAL_SERVER_ERROR)    
    
class GroupView(APIView, LoginRequiredMixin):
    permission_classes = [IsAuthenticated]
    def get(self, request, user_id=None):
        try:
            if user_id:
                groups = Group.objects.filter(customers__id=user_id)
                serializer = SimplifyDebitsInGroupSerializer(groups, many=True, context={'user_id': user_id})
            else:
                groups = Group.objects.all()
                serializer = GroupSerializer(groups, many=True)
            if not serializer.data:
                return Response("Records Not Found",status=status.HTTP_404_NOT_FOUND)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            print('group error=>>>',e)
            return Response("Internal Server Error:: "+str(e),status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    
    def post(self, request):
        try:
            serializer = GroupSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response("Internal Server Error:: "+str(e),status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    # update by id
    def put(self, request, id):
        try:
            group = Group.objects.get(id=id)
            serializer = GroupSerializer(group, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response("Internal Server Error:: "+str(e),status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class SettlementView(APIView, LoginRequiredMixin):
    permission_classes = [IsAuthenticated]
    def get(self, request, id=None):
        try:
            if id:
                settlement = Settlement.objects.get(id=id)
                serializer = SettlementSerializer(settlement)
            else:
                settlements = Settlement.objects.all()
                serializer = SettlementSerializer(settlements, many=True)
            if not serializer.data:
                return Response("Records Not Found",status=status.HTTP_404_NOT_FOUND)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response("Internal Server Error:: "+str(e),status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    # add settlement
    def post(self, request):
        try:
            expense_include_list = Expense.objects.filter(Q(paid_by = request.user.customer, split_on = request.data.get('friend_id')) | Q( paid_by=request.data.get('friend_id'), split_on = request.user.customer)).exclude(id__in = Settlement.objects.filter(paid_by = request.user.customer, paid_to = request.data.get('friend_id')).values_list('expense_included__id', flat=True)).values_list('id', flat=True)
            data = {
                'paid_by': request.user.customer.id,
                'paid_to': request.data.get('friend_id'),
                'amount': request.data.get('amount'),
                'expense_included': expense_include_list
            }
            serializer = SettlementSerializer(data=data)
            if serializer.is_valid():
                # after saving settlement entry make a new entry into expense table with paid_by and split_on single person
                settlement = serializer.save()
                # Create a new entry in the Expense table
                # expense_data = {
                #     'paid_by': request.data.paid_by,
                #     'split_on': [request.data.get('friend_id')],
                #     'item': 'Settlement',
                #     'amount': request.data.get('amount')
                # }
                # expense_serializer = ExpenseSerializer(data=expense_data)
                # if expense_serializer.is_valid():
                #     expense_serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            print('ererere ==>', e)
            return Response("Internal Server Error:: "+str(e),status=status.HTTP_500_INTERNAL_SERVER_ERROR)

# add new expense to a group by user
class ExpenseView(APIView, LoginRequiredMixin):
    permission_classes = [IsAuthenticated]
    # get expense by id
    def get(self, request, id=None):
        try:
            if not id:
                return Response("Bad Request expense Id missing",status=status.HTTP_400_BAD_REQUEST)
            expense = Expense.objects.get(id=id)
            serializer = ExpenseSerializer(expense)
            if not serializer.data:
                return Response("Records Not Found",status=status.HTTP_404_NOT_FOUND)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            print('errpr>>>', e)
            return Response("Internal Server Error:: "+str(e),status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    # add expense
    def post(self, request):
        try:
            serializer = ExpenseSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            print('expense creation error ==>',e)
            return Response("Internal Server Error:: "+str(e),status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    # update by id
    def put(self, request, id):
        try:
            expense = Expense.objects.get(id=id)
            serializer = ExpenseSerializer(expense, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            print('e ===>', e)
            return Response("Internal Server Error:: "+str(e),status=status.HTTP_500_INTERNAL_SERVER_ERROR)

# Activity log of expenses by user or specific group
class ActivityView(APIView, LoginRequiredMixin):
    permission_classes = [IsAuthenticated]
    def get(self, request, group_id=None):
        try:
            user_email = request.user
            if not group_id:
                expenses = Expense.objects.filter(Q(paid_by__email = user_email) | Q( split_on__email = user_email)).distinct().order_by('-updatetimestamp')
            else:
                expenses = Expense.objects.filter(Q(paid_by__email = user_email) | Q( split_on__email = user_email), group__id=group_id).distinct().order_by('-updatetimestamp')

            serializer = ActivitySerializer(expenses, many=True, context = {'user_email': user_email.email})
            if not serializer.data:
                return Response("No expenses found for the given user.", status=status.HTTP_404_NOT_FOUND)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            print('activity view error ==>',e)
            return Response(str(e), status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class FriendsView(APIView, LoginRequiredMixin):
    permission_classes = [IsAuthenticated]
    def get(self, request, group_id=None):
        try:
            user_email = request.user
            if not group_id:
                group_id_list = Group.objects.filter(customers__email=user_email).values_list('id', flat=True)
                friends = Customer.objects.filter(groups__id__in=list(group_id_list)).exclude(email=user_email).distinct()
                serializer = FriendsWithBalanceSerializer(friends, many=True, context = {'user_id': user_email.customer.id})
            else:
                group_id_list = Group.objects.filter(id=group_id, customers__email=user_email).values_list('id', flat=True)
                if not group_id_list:
                    return Response("Records Not Found",status=status.HTTP_404_NOT_FOUND)
                friends = Customer.objects.filter(groups__id__in=list(group_id_list)).exclude(email=user_email).distinct()
                serializer = FriendsSerlializer(friends, many=True, context = {'user_email': user_email.email})
            if not serializer.data:
                return Response("Records Not Found",status=status.HTTP_404_NOT_FOUND)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            print('FriendsView=>>>',e)
            return Response("Internal Server Error:: "+str(e),status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
class LoginView(APIView):
    @csrf_exempt
    def post(self, request):
        try:
            email = request.data.get('email')
            password = request.data.get('password')
            user = authenticate(request, username=email, password=password)
            if user is not None:
                request.session.set_expiry(86400*30) # 30 days
                login(request, user)
                user_obj = Customer.objects.get(email=email, password=password)
                return Response({'user_id': user_obj.id}, status=status.HTTP_200_OK)
            else:
                return  Response({'message': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
        except Exception as e:
            print('error login ==>',e)
            return Response("Internal Server Error:: "+str(e),status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class LogoutView(APIView):
    def get(self, request):
        try:
            logout(request)
            # delete cookie
            response = JsonResponse({'message': 'Logout successful'}, status=status.HTTP_200_OK)
            return response
        except Exception as e:
            print('error logout ==>',e)
            return Response("Internal Server Error:: "+str(e),status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
class OverallBalanceView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request, group_id = None):
        try:
            user_email = request.user.email
            if group_id:
                try:
                    Group.objects.get(customers__email=user_email, id=group_id)
                except Group.DoesNotExist:
                    return Response("Bad Request. Group Does Not Exist",status=status.HTTP_400_BAD_REQUEST)
            
            overall_balance = calculate_overall_balance(user_email, group_id)
            return JsonResponse({'overall_balance': overall_balance}, status=status.HTTP_200_OK)
        except ValueError as e:
            return Response(str(e), status=status.HTTP_404_NOT_FOUND)
        
        except Exception as e:
            return Response("Internal Server Error:: "+str(e),status=status.HTTP_500_INTERNAL_SERVER_ERROR)

# class MetricView(APIView):
#     '''
#     API to calculate monthly expense for user
#     '''
#     permission_classes = [IsAuthenticated]
#     def get(self, request):
#         try:
#             user_email = request.user.email
#             month = request.data.month
#             metric = calculate_monthly_expense(user_email, month)
#             return JsonResponse({'metric': metric}, status=status.HTTP_200_OK)
        
#         except ValueError as e:
#             print('ValueError =>>> ',e)
#             return Response(str(e), status=status.HTTP_404_NOT_FOUND)
        
#         except Exception as e:
#             print('MetricView =>>> ',e)
#             return Response("Internal Server Error:: "+str(e),status=status.HTTP_500_INTERNAL_SERVER_ERROR)