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