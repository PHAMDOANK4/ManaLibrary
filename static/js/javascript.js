document.getElementById('loginForm').addEventListener('submit', function(event) {
    event.preventDefault(); // Prevent the form from submitting the traditional way

    const email = document.getElementById('email').value;
    const password = document.getElementById('password').value;

    fetch('../data/authen.json')
        .then(response => response.json())
        .then(data => {
            const user = data.find(user => user.username === email && user.password === password);
            if (user) {
                alert('Login successful!');
            } else {
                alert('Invalid email or password.');
            }
        })
        .catch(error => {
            console.error('Error fetching authentication data:', error);
        });
});
