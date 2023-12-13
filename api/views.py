from .serializers import (CustomerSerializer, 
                          GroupSerializer, 
                          ExpenseSerializer, 
                          BalanceSerializer, 
                          SettlementSerializer)
from .models import (Customer, 
                     Group, 
                     Expense, 
                     Balance, 
                     Settlement)
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import authenticate, login, logout
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.mixins import LoginRequiredMixin
from rest_framework.permissions import IsAuthenticated

class CustomerView(APIView, LoginRequiredMixin):
    permission_classes = [IsAuthenticated]
    def get(self, request, id=None):
        try:
            if id:
                customer = Customer.objects.get(id=id)
                serializer = CustomerSerializer(customer)
            else:
                customers = Customer.objects.all()
                serializer = CustomerSerializer(customers, many=True)
            if not serializer.data:
                return Response("Records Not Found",status=status.HTTP_404_NOT_FOUND)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            print('userview =-==>',e)
            return Response("Internal Server Error",status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    def post(self, request):
        try:
            serializer = CustomerSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response("Internal Server Error",status=status.HTTP_500_INTERNAL_SERVER_ERROR)    
    
class GroupView(APIView, LoginRequiredMixin):
    permission_classes = [IsAuthenticated]
    def get(self, request, id=None):
        try:
            if id:
                group = Group.objects.get(id=id)
                serializer = GroupSerializer(group)
            else:
                groups = Group.objects.all()
                serializer = GroupSerializer(groups, many=True)
            if not serializer.data:
                return Response("Records Not Found",status=status.HTTP_404_NOT_FOUND)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response("Internal Server Error",status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    
    def post(self, request):
        try:
            serializer = GroupSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response("Internal Server Error",status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
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
            return Response("Internal Server Error",status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class BalanceView(APIView, LoginRequiredMixin):
    permission_classes = [IsAuthenticated]
    # get by id
    def get(self, request, id):
        try:
            balance = Balance.objects.get(customer__id=id)
            serializer = BalanceSerializer(balance)
            if not serializer.data:
                return Response("Records Not Found",status=status.HTTP_404_NOT_FOUND)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response("Internal Server Error",status=status.HTTP_500_INTERNAL_SERVER_ERROR)

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
            return Response("Internal Server Error",status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    def post(self, request):
        try:
            serializer = SettlementSerializer(data=request.data)
            if serializer.is_valid():

                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response("Internal Server Error",status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class LoginView(APIView):
    def post(self, request):
        try:
            email = request.data.get('email')
            password = request.data.get('password')
            user = authenticate(request, username=email, password=password)
            if user is not None:
                login(request, user)
                user_obj = Customer.objects.get(email=email, password=password)
                return Response({'user_id': user_obj.id}, status=status.HTTP_200_OK)
            else:
                return  Response({'message': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
        except Exception as e:
            return Response("Internal Server Error",status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class LogoutView(APIView):
    @csrf_exempt
    def post(self, request):
        try:
            logout(request)
            return Response({'message': 'Logout successful'}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response("Internal Server Error",status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
