document.addEventListener('DOMContentLoaded', function () {
    const lastMessage = document.querySelector('.error-message');
    if (lastMessage) {
        alert(lastMessage.textContent); // 显示最后一条消息
    }
});