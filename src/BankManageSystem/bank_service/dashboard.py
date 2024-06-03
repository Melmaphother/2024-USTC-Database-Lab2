from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Customer, AccountHoldManage, Account
from collections import defaultdict


@login_required
def dashboard(request):
    # 使用 Django 自带的用户认证系统，获取用户的用户名
    # 而不是使用 session 中的 id_number，这样更加安全
    # login 的 session 中的 id_number 在重定向后会被清除
    c_id = request.user.username
    customer = Customer.objects.get(c_id=c_id)
    dashboard_dict = defaultdict()
    dashboard_dict['c_id'] = c_id
    dashboard_dict['c_name'] = customer.c_name
    dashboard_dict['c_avatar'] = customer.c_avatar
    account_types = {
        'SavingsAccount': 'Savings',
        'CreditAccount': 'Credit',
        'LoanAccount': 'Loan'
    }

    account_numbers = AccountHoldManage.objects.filter(
        ahm_c_id=c_id
    ).values_list('ahm_a_no', flat=True)

    for key, account_type in account_types.items():
        accounts = Account.objects.filter(
            a_no__in=account_numbers,
            a_type=account_type
        ).order_by('-a_open_time').values(
            'a_no', 'a_balance', 'a_currency', 'a_open_time', 'a_open_b_name'
        )
        formatted_accounts = []
        for account in accounts:
            # 格式化余额和货币单位
            formatted_balance = f"{account['a_currency']} {account['a_balance']}"
            account_info = {
                'a_no': account['a_no'],
                'formatted_balance': formatted_balance,
                'a_open_time': account['a_open_time'],
                'a_open_b_name': account['a_open_b_name'],
            }
            formatted_accounts.append(account_info)

        dashboard_dict[key] = formatted_accounts

    return render(
        request,
        'dashboard/dashboard.html',
        dashboard_dict
    )
