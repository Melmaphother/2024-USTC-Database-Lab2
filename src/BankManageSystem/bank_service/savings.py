from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Customer, AccountHoldManage, Account, SavingsAccount
from collections import defaultdict


@login_required
def savings(request):
    c_id = request.user.username
    customer = Customer.objects.get(c_id=c_id)
    savings_dict = defaultdict()
    savings_dict['c_id'] = c_id
    savings_dict['c_name'] = customer.c_name
    savings_dict['c_avatar'] = customer.c_avatar
    savings_dict['SavingsAccount'] = []

    # 从 AccountHoldManage 获取用户持有的所有账户号
    account_numbers = AccountHoldManage.objects.filter(
        ahm_c_id=c_id
    ).values('ahm_a_no')

    # 过滤出储蓄账户
    savings_accounts = Account.objects.filter(
        a_no__in=account_numbers,
        a_type='Savings'
    ).order_by('-a_open_time').values(
        'a_no', 'a_balance', 'a_currency', 'a_open_time', 'a_open_b_name'
    )

    # 获取每个账户的详细信息
    for account in savings_accounts:
        savings_account_details = SavingsAccount.objects.get(
            sa_no=account['a_no']
        )
        formatted_balance = f"{account['a_currency']} {account['a_balance']}"
        account_info = {
            'a_no': account['a_no'],
            'formatted_balance': formatted_balance,
            'a_open_time': account['a_open_time'],
            'a_open_b_name': account['a_open_b_name'],
            'sa_rate': savings_account_details.sa_rate,
            'sa_withdraw_limit': savings_account_details.sa_withdraw_limit
        }
        savings_dict['SavingsAccount'].append(account_info)

    return render(
        request,
        'dashboard/savings.html',
        savings_dict
    )
