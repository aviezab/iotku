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
        bool1 = false, bool2 = false;
        $('#panel-login').slideUp('slow');
        $('#panel-register').slideUp('slow');
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
    $("#register-form").submit(function (event) {
        event.preventDefault();
        var password = $("#register-password").val();
        var confirmPassword = $("#register-password-confirm").val();
        if (password != confirmPassword) {
           $('#register-error').text("Passwords do not match.");
        }
        else {
            $.ajax({
                type: "POST",
                url: register_url,
                contentType: "application/json",
                dataType: "json",
                data: JSON.stringify({
                    "email": $("#register-email").val(),
                    "password": $("#register-password").val()
                }),
                success: function(result){
                    if (result.result == true) {
                        window.location.reload(true);
                    }
                    else {
                        $('#register-error').text(result.reason);
                    }
                }
            });
        }
    });
    $("#login-form").submit(function (event) {
        event.preventDefault();
        $.ajax({
            type: "POST",
            url: connect_url,
            contentType: "application/json",
            dataType: "json",
            data: JSON.stringify({
                "email": $("#login-email").val(),
                "password": $("#login-password").val()
            }),
            success: function(result){
                if (result.result == true) {
                    window.location.reload(true);
                }
                else {
                    $('#login-error').text(result.reason);
                }
            }
        });
    });
});
