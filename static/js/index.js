var host = "";
var playlist = undefined;
var token = undefined;
var isAdmin = false;
var isPlaying=false;

function update(){
    $.ajax({
        url: host + "/getplaylist/",
        type: "POST",
        data: {
            token: token   
        },
        success: function(e){
            playlist = JSON.parse(e.playlist);
            display();
        },
        error: function(e){
            loadAuthScreen();
        },
        dataType: "json"
    });
    if(isPlaying == true){
        document.cookie = "curtime=" + player.getCurrentTime() + "";
    }
}
function main(){
    console.log("main");
    update();
    //setInterval(update,5000);
}
function callNext(){
    document.cookie="curtime=0";
    console.log("cur next");
    $.ajax({
        url: host + "/playnext/",
        type: "POST",
        data: {
            token: token
        },
        success: function(e){
            update();
        },
        error: function(e){
            //NOT FOUND
        },
        dataType: "json"
    });
}
function display(){
    //sort();
    var output="<br><br>";
    for(var i=0;i<playlist.songs.length;++i){
        output+='<h5 class="bordered">'+playlist.songs[i].name+' '+playlist.songs[i].rating+'<span style="float:right"><a href="#" onclick="downvote(\''+ playlist.songs[i].name +'\')" style="color:red" class="fa fa-thumbs-down fa-lg"></a> <a href="#" onclick="upvote(\''+ playlist.songs[i].name +'\')" style="color:green" class="fa fa-thumbs-up fa-lg"></a></span></h5>';
    }
    if(isAdmin) {
        $("#player").css("visibility","visible");
    }else {
        $("#player").css("visibility", "hidden");
    }
    if(playlist.songs.length>0 && !isPlaying && isAdmin)
        addPlayer(playlist.songs[0].video_id);
    $("#playlist").html(output);
    $("#songTitle").html(playlist.songs[0].name);
}
function upvote(songname){
    $.ajax({
        url: host + "/vote/",
        type: "POST",
        data: {
            token: token,
            songname: songname,
            vote: 'up'
        },
        success: function(e){
            update();
        },
        error: function(e){
            //NOT FOUND
        },
        dataType: "json"
    });
}
function downvote(songname){
    $.ajax({
        url: host + "/vote/",
        type: "POST",
        data: {
            token: token,
            songname: songname,
            vote: 'down'
        },
        success: function(e){
            update();
        },
        error: function(e){
            //NOT FOUND
        },
        dataType: "json"
    });
}
function fetchToken(){
    var arr = document.cookie.split("token=");
    console.log(arr.length);
    if(arr.length < 2){
        loadAuthScreen();
        return;
    }
    token = arr[1];
}
function addSong(){
     $.ajax({
        url: host + "/addsong/",
        type: "POST",
        data: {
            token: token,
            songname: $("#addSongVal").val()
        },
        success: function(e){
            update();
        },
        error: function(e){
            //NOT FOUND
        },
        dataType: "json"
    });
}
function checkAdmin(){
    fetchToken();
    $.ajax({
        url: host + "/isadmin/",
        type: "POST",
        data: {
            token: token
        },
        success: function(e){
            var isa = e
            console.log(isa.isadmin);
            if(isa.isadmin=="yes"){
                isAdmin=true;
            }else{
                isAdmin=false;
                $("#cover").hide();
            }
            main();
        },
        error: function(e){
            //NOT FOUND
            isAdmin=false;
            main();
        },
        dataType: "json"
    });
}
function loadAuthScreen(){
    console.log("redirecting");
    $(location).attr('href', '/loginForm');
}
checkAdmin();