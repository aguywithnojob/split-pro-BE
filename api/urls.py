from django.urls import path
from .views import *

urlpatterns = [
    path('login/',LoginView.as_view(),name='login'),
    path('logout/',LogoutView.as_view(),name='logout'),
    path('users/', CustomerView.as_view(), name="users"),
    path('users/create', CustomerView.as_view(), name="create_users"),
    path('users/<int:id>', CustomerView.as_view(), name="get_by_id_user"),
    path('groups/<int:user_id>', GroupView.as_view(), name="get_group_by_id"),
    path('groups/', GroupView.as_view(), name="get_groups"),
    path('groups/create', GroupView.as_view(), name="create_groups"),
    path('settlement/', SettlementView.as_view(), name="get_settlement"),
    path('settlement/<int:id>', SettlementView.as_view(), name="get_settlement_by_id"),
    path('settlement/create', SettlementView.as_view(), name="create_settlement"),
    path('balance/<int:id>', BalanceView.as_view(), name="get_balance_by_id"),
    path('friends/', FriendsView.as_view(), name="get_friends_list"),
    path('friends/group/<int:group_id>', FriendsView.as_view(), name="get_friends_list_by_group"),
    path('friends/group/', FriendsView.as_view(), name="get_all_friends_list"),
    path('addexpense/', ExpenseView.as_view(), name="add_expense"),
    path('activity/', ActivityView.as_view(), name="view activity"),
    path('activity/<int:group_id>', ActivityView.as_view(), name="view activity by group id"),
]
