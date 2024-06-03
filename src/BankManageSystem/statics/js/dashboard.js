function goToPage(page) {
    window.location.href = page;
}

function openLogoutModal() {
    document.getElementById('logoutModal').style.display = 'block';
    document.getElementById('pageContent').style.filter = 'blur(5px)';  // 添加模糊效果到主内容
}

function closeLogoutModal() {
    document.getElementById('logoutModal').style.display = 'none';
    document.getElementById('pageContent').style.filter = 'none';  // 移除模糊效果
}

function logout() {
    // 执行登出操作，例如清除session、重定向等
    // 这里只是示例，可能需要实际的服务器请求
    window.location.href = '/login'; // 或任何实际的登出处理路径
}

function openAddAccountModal() {
    document.getElementById('addAccountModal').style.display = 'block';
    document.getElementById('pageContent').style.filter = 'blur(5px)';
}

function closeAddAccountModal() {
    document.getElementById('addAccountModal').style.display = 'none';
    document.getElementById('pageContent').style.filter = 'none';
}

function openDepositModal(button) {
    let accountNumber = button.getAttribute('data-account-number');
    document.getElementById('depositAccountNumber').textContent = accountNumber;
    document.getElementById('hiddenAccountNumber').value = accountNumber;
    document.getElementById('depositModal').style.display = 'block';
    document.getElementById('pageContent').style.filter = 'blur(5px)';
}

function closeDepositModal() {
    document.getElementById('depositModal').style.display = 'none';
    document.getElementById('pageContent').style.filter = 'none';
}

function openWithdrawModal() {
    document.getElementById('withdrawModal').style.display = 'block';
    document.getElementById('pageContent').style.filter = 'blur(5px)';
}

function closeWithdrawModal() {
    document.getElementById('withdrawModal').style.display = 'none';
    document.getElementById('pageContent').style.filter = 'none';
}

function openTransferModal() {
    document.getElementById('transferModal').style.display = 'block';
    document.getElementById('pageContent').style.filter = 'blur(5px)';
}

function closeTransferModal() {
    document.getElementById('transferModal').style.display = 'none';
    document.getElementById('pageContent').style.filter = 'none';
}