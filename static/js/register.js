var host = "http://192.168.43.188:8000";
var token = undefined;

function register(){
    $.ajax({
        url: host + "/register/",
        type: "POST",
        data: {
            email: $("#email").val(),
            password: $("#password").val()
        },
        success: function(e){
            token = e;
            document.cookie="token="+token;
            redirectToIndex();
        },
        error: function(e){
            loginFailed();
        }
    });
}
function redirectToIndex(){
    
}
function loginFailed(){
    
}