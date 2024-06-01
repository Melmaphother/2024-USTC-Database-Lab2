function openLoanRepayModal() {
    document.getElementById('loanRepayModal').style.display = 'block';
    document.getElementById('pageContent').style.filter = 'blur(5px)';  // 添加模糊效果到主内容
}

function closeLoanRepayModal() {
    document.getElementById('loanRepayModal').style.display = 'none';
    document.getElementById('pageContent').style.filter = 'none';  // 移除模糊效果
}

function openLoanApplyModal() {
    document.getElementById('loanApplyModal').style.display = 'block';
    document.getElementById('pageContent').style.filter = 'blur(5px)';
}

function closeLoanApplyModal() {
    document.getElementById('loanApplyModal').style.display = 'none';
    document.getElementById('pageContent').style.filter = 'none';
}

function openLoanDetailModal() {
    document.getElementById('loanDetailModal').style.display = 'block';
    document.getElementById('pageContent').style.filter = 'blur(5px)';
}

function closeLoanDetailModal() {
    document.getElementById('loanDetailModal').style.display = 'none';
    document.getElementById('pageContent').style.filter = 'none';
}