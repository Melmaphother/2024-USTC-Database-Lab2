document.addEventListener('DOMContentLoaded', function () {
    const fileUploadButton = document.getElementById('file-upload-button');
    const fileUpload = document.getElementById('file-upload');
    const fileNameDisplay = document.getElementById('file-name-display');

    // 设置点击自定义上传按钮时触发隐藏的 file input
    fileUploadButton.addEventListener('click', function () {
        fileUpload.click(); // 触发 file input 的点击事件
    });

    // 监听 file-upload 的变化，当文件被选中时
    fileUpload.addEventListener('change', function () {
        // 检查是否有文件被选择
        if (fileUpload.files.length > 0) {
            // 获取第一个文件的名字
            console.log(fileUpload.files[0].name);
            fileNameDisplay.textContent = fileUpload.files[0].name;
        }
    });
});
