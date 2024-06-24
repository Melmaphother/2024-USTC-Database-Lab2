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
    window.location.href = '/'; // 或任何实际的登出处理路径
}

