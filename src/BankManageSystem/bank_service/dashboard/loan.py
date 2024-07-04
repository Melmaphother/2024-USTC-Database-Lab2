from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from bank_service.models import Customer, AccountHoldManage, Account, LoanAccount, LoanGrant, Loan
from collections import defaultdict


@login_required
def loan_dashboard(request):
    c_id = request.user.username
    customer = Customer.objects.get(c_id=c_id)
    loan_dict = defaultdict()
    loan_dict['c_id'] = c_id
    loan_dict['c_name'] = customer.c_name
    loan_dict['c_avatar'] = customer.c_avatar
    loan_dict['LoanAccount'] = []

    # 从 AccountHoldManage 获取用户持有的所有账户号
    account_numbers = AccountHoldManage.objects.filter(
        ahm_c_id=c_id
    ).values('ahm_a_no')

    # 过滤出贷款账户
    loan_accounts = Account.objects.filter(
        a_no__in=account_numbers,
        a_type='Loan'
    ).order_by('-a_open_time').values(
        'a_no', 'a_balance', 'a_currency', 'a_open_time', 'a_open_b_name', 'a_total'
    )

    # 获取每个账户的详细信息
    for account in loan_accounts:
        loan_account_details = LoanAccount.objects.get(
            la_no=account['a_no']
        )
        formatted_balance = f"{account['a_currency']} {account['a_balance']}"
        formatted_time = account['a_open_time'].strftime('%Y-%m-%d %H:%M:%S')
        formatted_rate = f"{loan_account_details.la_rate * 100}%"
        formatted_withdraw_limit = f"{account['a_currency']} {loan_account_details.la_withdraw_limit}"
        formatted_loan_limit = f"{account['a_currency']} {loan_account_details.la_loan_limit}"
        formatted_total = f"{account['a_currency']} {account['a_total']}"

        # 获取该贷款账户所有贷款的信息
        loan_account_loans = []
        # 从 LoanGrant 中获取所有的贷款号
        loan_grant_ids = LoanGrant.objects.filter(
            lg_la_no=account['a_no']
        ).order_by('-lg_l_no').values('lg_l_no')

        status_mapping = {
            'pending': '未发放',
            'disbursed': '已发放',
            'repaying': '还款中',
            'settled': '已结清'
        }

        # 从 Loan 中获取所有的贷款信息
        for loan_grant_id in loan_grant_ids:
            loan = Loan.objects.get(
                l_no=loan_grant_id['lg_l_no']
            )
            formatted_status = status_mapping.get(loan.l_status, loan.l_status)

            loan_info = {
                'l_no': loan.l_no,
                'l_amount': f"{account['a_currency']} {loan.l_amount}",
                'l_grant_time': loan.l_grant_time.strftime('%Y-%m-%d %H:%M:%S'),
                'l_repay_deadline': loan.l_repay_deadline.strftime('%Y-%m-%d'),
                'l_repay_amount_total': f"{account['a_currency']} {loan.l_repay_amount_total}",
                'l_status': formatted_status
            }
            loan_account_loans.append(loan_info)

        account_info = {
            'a_no': account['a_no'],
            'a_balance': formatted_balance,
            'a_open_time': formatted_time,
            'a_open_b_name': account['a_open_b_name'],
            'a_total': formatted_total,
            'la_rate': formatted_rate,
            'la_withdraw_limit': formatted_withdraw_limit,
            'la_loan_limit': formatted_loan_limit,
            'Loans': loan_account_loans
        }
        loan_dict['LoanAccount'].append(account_info)

    return render(
        request,
        'dashboard/loan.html',
        loan_dict
    )
