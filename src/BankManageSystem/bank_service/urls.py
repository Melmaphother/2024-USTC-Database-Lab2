from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import (
    login,
    customer_register,
    dashboard,
    profile,
    savings,
    credit,
    loan
)
from .account_utils import savings_account

urlpatterns = ([
                   path('', login.auth_login, name='init_register'),  # 修改默认页面为注册页面
                   path('login/', login.auth_login, name='login'),
                   path('customer_register/', customer_register.customer_register, name='customer_register'),
                   path('edit_profile/', customer_register.edit_profile, name='edit_profile'),
                   path('dashboard/', dashboard.dashboard, name='dashboard'),
                   path('dashboard/profile/', profile.profile, name='profile'),
                   path('dashboard/savings/', savings.savings, name='savings'),
                   path('dashboard/credit/', credit.credit, name='credit'),
                   path('dashboard/loan/', loan.loan, name='loan'),
                   path('savings_account_add/', savings_account.savings_account_add, name='savings_account_add'),
                   path('savings_account_deposit/', savings_account.savings_account_deposit,
                        name='savings_account_deposit'),
                   path('savings_account_withdraw/', savings_account.savings_account_withdraw,
                        name='savings_account_withdraw'),
                   path('savings_account_transfer/', savings_account.savings_account_transfer,
                        name='savings_account_transfer'),
               ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
               )
