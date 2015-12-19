var host = "";
var token = undefined;
function auth(){
    $.ajax({
        url: host + "/login/",
        type: "POST",
        data: {
            email: $("#email").val(),
            password: $("#password").val()
        },
        success: function(e){
            token = e.token;
            document.cookie="token="+token + "; path=/";
            redirectToIndex();
        },
        error: function(e){
            loginFailed();
        }
    });
}
function redirectToIndex(){
    $(location).attr('href', '/');
}
function loginFailed(){
    
}