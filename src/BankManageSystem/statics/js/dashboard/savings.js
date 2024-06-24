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
    fetch(`/savings_account_details/?account_number=${account_number}`, {
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