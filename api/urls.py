from django.urls import path, re_path
from .views import *
from .metadata_views import MetaData

urlpatterns = [
    path('login/',LoginView.as_view(),name='login'),
    path('logout/',LogoutView.as_view(),name='logout'),
    path('users/', CustomerView.as_view(), name="users"),
    path('users/create', CustomerView.as_view(), name="create_users"),
    path('users/<int:id>', CustomerView.as_view(), name="get_by_id_user"),
    path('groups/<int:user_id>', GroupView.as_view(), name="get_group_by_user_id"),
    path('groups/', GroupView.as_view(), name="get_groups"),
    path('groups/create', GroupView.as_view(), name="create_groups"),
    path('settlement/', SettlementView.as_view(), name="get_settlement"),
    path('settlement/<int:id>', SettlementView.as_view(), name="get_settlement_by_id"),
    path('settlement/create', SettlementView.as_view(), name="create_settlement"),
    path('friends/', FriendsView.as_view(), name="get_friends_list_with_balance"),
    path('friends/group/<int:group_id>', FriendsView.as_view(), name="get_friends_list_by_group"),
    path('addexpense/', ExpenseView.as_view(), name="add_expense"),
    path('expense/<int:id>', ExpenseView.as_view(), name="get_expense_by_id"),
    path('activity/', ActivityView.as_view(), name="view activity"),
    path('activity/<int:group_id>', ActivityView.as_view(), name="view activity by group id"),
    path('overallbalance/', OverallBalanceView.as_view(), name="view overall balance w.r.t current user"),
    path('overallbalance/<int:group_id>', OverallBalanceView.as_view(), name="view overall balance w.r.t current user in a group"),
]

metadata_view_urlpatterns = [
    path('metadata/<str:kind>/<int:key_id>/', MetaData.as_view(), name="get_metadata"),
]

urlpatterns += metadata_view_urlpatterns