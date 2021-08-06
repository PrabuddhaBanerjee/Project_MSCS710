$(function(){
  $userId = $('#id');
  $userpwd = $('#pwd');
  $useremail = $('#email');
  $usercheck = $('#usercheck');
  $userpass = $('#pass');
  $userphone = $('#phone');
  $('#login-check').on('click',function(){
    var id = $useremail.val();
    var pass = $userpwd.val();
    var cred = {
       "email" : id,
       "password": pass
    }

    $.ajax({
     type:'POST',
     url:'http://localhost:8080/csumano/AIRservices/1.0.0/login',
     contentType: "application/json",
     data: JSON.stringify(cred),
     success: function(credentialCheck){
       var str = credentialCheck;
       if(str.includes("Success"))
         document.location.href = "/airtrack1.html";
       else alert('Invalid user login or Password');
     },
     error: function(get){
       alert('Invalid user login and Password'+get);
     }
    });
  });

  $('#signup-form').on('click',function(){

    // alert("In Signup");
    var email = $useremail.val();
    var pwd = $userpass.val();
    var u_id = $userphone.val();
    var check = $usercheck.val();
    if(check == true){
      u_id = email;
    }
    var cred = {
       "email" : email,
       "password": pwd,
       "username":u_id
    }
    $.ajax({
     type:'POST',
     url:'http://localhost:8080/csumano/AIRservices/1.0.0/register',
     contentType: "application/json",
     data: JSON.stringify(cred),
     success: function(signup){
      //  alert("Valid "+signup);
       document.location.href = "/index.html";
     },
     error: function(){
       alert('User is already there');
     }
    });
  });
});
