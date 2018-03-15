$(document).ready(function(){
    var bool1 = false,bool2 = false;
    $('#btn-signIn').click(function(){
        if (bool1 == false && bool2 == true) {
            $('#panel-register').slideUp('slow');
            bool2 = false;
        }
        else {
            $('#panel-login').slideDown('slow');
            bool1 = true;
        }
    });
    //close button click up
    $('.close-btn').click(function(){
      $('#panel-login').slideUp('slow')
      $('#panel-register').slideUp('slow')
    });

    $('#btn-signIn2').click(function(){
        bool1 = true, bool2 = false;
        $('#panel-login').slideDown('slow');
        $('#panel-register').slideUp('slow');
    });
    $('#btn-register').click(function(){
        bool2 = true, bool1 = false;
        $('#panel-login').slideUp('slow');
        $('#panel-register').slideDown('slow');
    }).delay(500);
    $("#btn-register-submit").click(function () {
        var password = $("#password").val();
        var confirmPassword = $("#confirm").val();
        if (password != confirmPassword) {
            alert("Passwords do not match.");
            return false;
        }
        document.getElementById("registerForm").submit();
    });
});
