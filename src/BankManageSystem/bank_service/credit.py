from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Customer, AccountHoldManage, Account, CreditAccount
from collections import defaultdict


@login_required
def credit(request):
    c_id = request.user.username
    customer = Customer.objects.get(c_id=c_id)
    credit_dict = defaultdict()
    credit_dict['c_id'] = c_id
    credit_dict['c_name'] = customer.c_name
    credit_dict['c_avatar'] = customer.c_avatar
    credit_dict['CreditAccount'] = []

    # 从 AccountHoldManage 获取用户持有的所有账户号
    account_numbers = AccountHoldManage.objects.filter(
        ahm_c_id=c_id
    ).values('ahm_a_no')

    # 过滤出信用账户
    credit_accounts = Account.objects.filter(
        a_no__in=account_numbers,
        a_type='Credit'
    ).order_by('-a_open_time').values(
        'a_no', 'a_balance', 'a_currency', 'a_open_time', 'a_open_b_name', 'a_total'
    )

    # 获取每个账户的详细信息
    for account in credit_accounts:
        credit_account_details = CreditAccount.objects.get(
            ca_no=account['a_no']
        )
        formatted_balance = f"{account['a_currency']} {account['a_balance']}"
        formatted_time = account['a_open_time'].strftime('%Y-%m-%d %H:%M:%S')
        formatted_rate = f"{credit_account_details.ca_rate * 100}%"
        formatted_overdraft_limit = f"{account['a_currency']} {credit_account_details.ca_overdraft_limit}"
        formatted_current_overdraft_amount = f"{account['a_currency']} {credit_account_details.ca_current_overdraft_amount}"
        formatted_total = f"{account['a_currency']} {account['a_total']}"
        account_info = {
            'a_no': account['a_no'],
            'a_balance': formatted_balance,
            'a_open_time': formatted_time,
            'a_open_b_name': account['a_open_b_name'],
            'a_total': formatted_total,
            'ca_rate': formatted_rate,
            'ca_overdraft_limit': formatted_overdraft_limit,
            'ca_current_overdraft_amount': formatted_current_overdraft_amount
        }
        credit_dict['CreditAccount'].append(account_info)

    return render(
        request,
        'dashboard/credit.html',
        credit_dict
    )
