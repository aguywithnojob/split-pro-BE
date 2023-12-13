from django.urls import path
from .views import *

urlpatterns = [
    path('login/',LoginView.as_view(),name='login'),
    path('logout/',LogoutView.as_view(),name='logout'),
    path('users/', CustomerView.as_view(), name="users"),
    path('users/create', CustomerView.as_view(), name="create_users"),
    path('users/<int:id>', CustomerView.as_view(), name="get_by_id_user"),
    path('groups/<int:id>', GroupView.as_view(), name="get_group_by_id"),
    path('groups/', GroupView.as_view(), name="get_groups"),
    path('groups/create', GroupView.as_view(), name="create_groups"),
    path('settlement/', SettlementView.as_view(), name="get_settlement"),
    path('settlement/<int:id>', SettlementView.as_view(), name="get_settlement_by_id"),
    path('settlement/create', SettlementView.as_view(), name="create_settlement"),
    path('balance/<int:id>', BalanceView.as_view(), name="get_balance_by_id"),
    # path('friends/', FriendsView.as_view(), name="get_friends_list"),
]
