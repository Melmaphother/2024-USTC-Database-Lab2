from django.urls import path
from . import views, login, customer_register, dashboard

urlpatterns = [
    path('', login.auth_login, name='init_register'),  # 修改默认页面为注册页面
    path('login/', login.auth_login, name='login'),
    path('customer_register/', customer_register.customer_register, name='customer_register'),
    path('edit_profile/', customer_register.edit_profile, name='edit_profile'),
    path('dashboard/', dashboard.dashboard, name='dashboard'),
    path('dashboard/profile/', dashboard.profile, name='profile'),
    path('dashboard/savings/', dashboard.savings, name='savings'),
    path('dashboard/credit/', dashboard.credit, name='credit'),
    path('dashboard/loan/', dashboard.loan, name='loan'),
    path('dashboard/logout/', dashboard.logout, name='logout'),
]