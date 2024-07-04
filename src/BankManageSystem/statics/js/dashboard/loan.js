function openAddAccountModal() {
    document.getElementById('addAccountModal').style.display = 'block';
    document.getElementById('pageContent').style.filter = 'blur(5px)';
}

function closeAddAccountModal() {
    document.getElementById('addAccountModal').style.display = 'none';
    document.getElementById('pageContent').style.filter = 'none';
}

function openDepositModal(button) {
    document.getElementById('hiddenDepositAccountNumber').value = button.getAttribute('data-deposit-account-number');
    document.getElementById('depositModal').style.display = 'block';
    document.getElementById('pageContent').style.filter = 'blur(5px)';
}

function closeDepositModal() {
    document.getElementById('depositModal').style.display = 'none';
    document.getElementById('pageContent').style.filter = 'none';
}

function openWithdrawModal(button) {
    document.getElementById('hiddenWithdrawAccountNumber').value = button.getAttribute('data-withdraw-account-number');
    document.getElementById('hiddenWithdrawBalance').value = button.getAttribute('data-withdraw-balance');
    document.getElementById('hiddenWithdrawLimit').value = button.getAttribute('data-withdraw-limit');
    document.getElementById('withdrawModal').style.display = 'block';
    document.getElementById('pageContent').style.filter = 'blur(5px)';
}

function closeWithdrawModal() {
    document.getElementById('withdrawModal').style.display = 'none';
    document.getElementById('pageContent').style.filter = 'none';
}

function openTransferModal(button) {
    document.getElementById('hiddenTransferAccountNumber').value = button.getAttribute('data-transfer-account-number');
    document.getElementById('hiddenTransferBalance').value = button.getAttribute('data-transfer-balance');
    document.getElementById('hiddenTransferLimit').value = button.getAttribute('data-transfer-limit');
    document.getElementById('transferModal').style.display = 'block';
    document.getElementById('pageContent').style.filter = 'blur(5px)';
}

function closeTransferModal() {
    document.getElementById('transferModal').style.display = 'none';
    document.getElementById('pageContent').style.filter = 'none';
}

function openDetailModal(button) {
    let account_number = button.getAttribute('data-detail-account-number')
    document.getElementById('hiddenDetailAccountNumber').textContent = account_number;
    document.getElementById('detailModal').style.display = 'block';
    document.getElementById('pageContent').style.filter = 'blur(5px)';

    let csrfToken = document.getElementById('csrfToken').value;

    // AJAX 请求获取交易明细
    fetch(`/loan_account_details/?account_number=${account_number}`, {
        method: 'GET',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrfToken
        }
    })
        .then(response => response.json())
        .then(data => {
            updateDetailTable(data.details);
        })
        .catch(error =>
            console.error('Error fetching account details:', error)
        );
}

function updateDetailTable(details) {
    let tableBody = document.querySelector('.detail-table table tbody');
    tableBody.innerHTML = '';  // 清空表格内容
    if (details.length > 0) {
        details.forEach(detail => {
            let row = `<tr>
                <td>${detail.d_time}</td>
                <td>${detail.d_type}</td>
                <td>${detail.d_amount}</td>
                <td>${detail.d_balance}</td>
                <td>${detail.d_other_a_no}</td>
            </tr>`;
            tableBody.innerHTML += row;
        });
    } else {
        tableBody.innerHTML = '<tr><td colspan="5" class="empty-row">没有交易信息</td></tr>';
    }
}

function closeDetailModal() {
    document.getElementById('detailModal').style.display = 'none';
    document.getElementById('pageContent').style.filter = 'none';
}

function openLoanGrantModal(button) {
    document.getElementById('hiddenLoanGrantAccountNumber').value = button.getAttribute('data-loan-grant-account-number');
    document.getElementById('hiddenLoanLimit').value = button.getAttribute('data-loan-limit');
    document.getElementById('loanGrantModal').style.display = 'block';
    document.getElementById('pageContent').style.filter = 'blur(5px)';
}

document.addEventListener('DOMContentLoaded', function () {
    flatpickr("#repay-deadline", {
        minDate: "today",
        dateFormat: "Y-m-d",
        altInput: true,
        altFormat: "Y年 Fj日",
        locale: "zh"
    });
});

function closeLoanGrantModal() {
    document.getElementById('loanGrantModal').style.display = 'none';
    document.getElementById('pageContent').style.filter = 'none';
}

function openLoanRepayModal(button) {
    document.getElementById('hiddenLoanRepayAccountNumber').value = button.getAttribute('data-loan-repay-account-number');
    let loan_number = button.getAttribute('data-loan-repay-loan-number');
    document.getElementById('hiddenLoanRepayLoanNumber').textContent = loan_number;
    document.getElementById('hiddenInFormLoanRepayLoanNumber').value = loan_number;
    document.getElementById('hiddenLoanAmount').value = button.getAttribute('data-loan-amount');
    document.getElementById('hiddenRepayAmountTotal').value = button.getAttribute('data-repay-amount-total');
    document.getElementById('loanRepayModal').style.display = 'block';
    document.getElementById('pageContent').style.filter = 'blur(5px)';
}

function closeLoanRepayModal() {
    document.getElementById('loanRepayModal').style.display = 'none';
    document.getElementById('pageContent').style.filter = 'none';
}

function openLoanDetailModal(button) {
    let loan_number = button.getAttribute('data-loan-detail-loan-number')
    document.getElementById('hiddenLoanDetailLoanNumber').textContent = loan_number;
    document.getElementById('loanDetailModal').style.display = 'block';
    document.getElementById('pageContent').style.filter = 'blur(5px)';

    let csrfToken = document.getElementById('csrfToken').value;

    // AJAX 请求获取贷款明细
    fetch(`/loan_details/?loan_number=${loan_number}`, {
        method: 'GET',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrfToken
        }
    })
        .then(response => response.json())
        .then(data => {
            updateLoanDetailTable(data.details);
        })
        .catch(error =>
            console.error('Error fetching loan details:', error)
        );
}

function updateLoanDetailTable(details) {
    let tableBody = document.querySelector('.loan-detail-table table tbody');
    tableBody.innerHTML = '';  // 清空表格内容
    if (details.length > 0) {
        details.forEach(detail => {
            let row = `<tr>
                <td>${detail.lr_repay_period}</td>
                <td>${detail.lr_time}</td>
                <td>${detail.lr_amount}</td>
                <td>${detail.lr_after_repay_amount_total}</td>
            </tr>`;
            tableBody.innerHTML += row;
        });
    } else {
        tableBody.innerHTML = '<tr><td colspan="4" class="empty-row">没有贷款信息</td></tr>';
    }
}

function closeLoanDetailModal() {
    document.getElementById('loanDetailModal').style.display = 'none';
    document.getElementById('pageContent').style.filter = 'none';
}