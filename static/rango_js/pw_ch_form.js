var passwordvalidate = function() {
    if (document.getElementById('id_new_password1').value == document.getElementById('id_new_password2').value) {
           document.getElementById('validationmessage').style.color = 'green';
           document.getElementById('validationmessage').innerHTML = 'Password Matched';
   } else {
           document.getElementById('validationmessage').style.color = 'red';
           document.getElementById('validationmessage').innerHTML = 'Password not match';
           }
}