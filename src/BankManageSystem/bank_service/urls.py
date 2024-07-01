from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from .system import (
    customer_register,
    terms,
    login,
    home
)
from .dashboard import (
    dashboard,
    profile,
    savings,
    credit,
    loan
)
from .account_utils import (
    savings_account,
    credit_account,
    loan_account
)

# System URLs
system_patterns = [
    path('', home.home, name='home'),
    path('login/', login.auth_login, name='login'),
    path('terms/', terms.terms, name='terms'),
    path('privacy/', terms.privacy, name='privacy'),
    path('customer_register/', customer_register.customer_register, name='customer_register'),
    path('edit_profile/', customer_register.edit_profile, name='edit_profile'),
]

# Dashboard URLs
dashboard_patterns = [
    path('dashboard/', dashboard.dashboard, name='dashboard'),
    path('dashboard/profile/', profile.profile, name='profile'),
    path('dashboard/savings/', savings.savings, name='savings'),
    path('dashboard/credit/', credit.credit, name='credit'),
    path('dashboard/loan/', loan.loan, name='loan'),
]

# Savings Account URLs
savings_account_patterns = [
    path('savings_account_add/', savings_account.savings_account_add, name='savings_account_add'),
    path('savings_account_deposit/', savings_account.savings_account_deposit, name='savings_account_deposit'),
    path('savings_account_withdraw/', savings_account.savings_account_withdraw, name='savings_account_withdraw'),
    path('savings_account_transfer/', savings_account.savings_account_transfer, name='savings_account_transfer'),
    path('savings_account_details/', savings_account.savings_account_details, name='savings_account_details'),
]

# Credit Account URLs
credit_account_patterns = [
    path('credit_account_add/', credit_account.credit_account_add, name='credit_account_add'),
    path('credit_account_deposit/', credit_account.credit_account_deposit, name='credit_account_deposit'),
    path('credit_account_withdraw/', credit_account.credit_account_withdraw, name='credit_account_withdraw'),
    path('credit_account_transfer/', credit_account.credit_account_transfer, name='credit_account_transfer'),
    path('credit_account_details/', credit_account.credit_account_details, name='credit_account_details'),
]

# Loan Account URLs
loan_account_patterns = [
    path('loan_account_add/', loan_account.loan_account_add, name='loan_account_add'),
    path('loan_account_deposit/', loan_account.loan_account_deposit, name='loan_account_deposit'),
    path('loan_account_withdraw/', loan_account.loan_account_withdraw, name='loan_account_withdraw'),
    path('loan_account_transfer/', loan_account.loan_account_transfer, name='loan_account_transfer'),
    path('loan_account_details/', loan_account.loan_account_details, name='loan_account_details'),
]

# Main urlpatterns
urlpatterns = (
        system_patterns +
        dashboard_patterns +
        savings_account_patterns +
        credit_account_patterns +
        loan_account_patterns +
        static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
)
