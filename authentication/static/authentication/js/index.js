/**
 * Created by bazinga on 05.06.17.
 */

var register = document.getElementById("register");
var login = document.getElementById("login");
document.getElementById('show-registration-form').onclick = function(){
    register.style.display = 'block';
    login.style.display = 'none';
};
document.getElementById('show-login-form').onclick = function(){
    login.style.display = 'block';
    register.style.display = 'none';
};