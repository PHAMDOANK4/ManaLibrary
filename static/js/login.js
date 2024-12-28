const form = document.getElementById('loginForm');
const responseMessage = document.getElementById('responseMessage');
form.addEventListener('submit', async (e) => {
    e.preventDefault();
    const username = document.getElementById('username').value;
    const password = document.getElementById('password').value;

    const response = await fetch('/login', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ username, password }),
    });
    const result = await response.json();
    // if (result.success) {
    //     alert('Login successful');
    //     window.location.href = 'home';
    // } else {
    //     responseMessage.textContent = result.message;
    //     responseMessage.style.display = 'block';
    // }
    if (response.ok) { // Kiểm tra xem phản hồi có thành công không
        if (result.redirect) {
            window.location.href = result.redirect; // Redirect đến URL mới
        } else {
            responseMessage.textContent = result.message; // Hiển thị thông báo nếu không có redirect
            responseMessage.style.display = 'block';
        }
    } else {
        // Xử lý lỗi nếu có
        responseMessage.textContent = 'Login failed: ' + result.message;
        responseMessage.style.display = 'block';
    }
});