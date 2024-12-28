document.addEventListener('DOMContentLoaded', async () => {
    const logout_btn = document.getElementById('logout_btn');

    //Catch the click event on the logout button
    logout_btn.addEventListener('click', function(event){
        event.preventDefault();
        fetch('/logout', {
            method: 'GET'
        }).then((response) => {
            if(response.redirected){
                window.location.href = response.url;
            }
                });
            });
        });