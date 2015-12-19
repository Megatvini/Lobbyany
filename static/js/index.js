var host = "";
var playlist = undefined;
var token = undefined;
var isAdmin = false;
var curVideoURL = 'HQmmM_qwG4k';

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
}
function main(){
    console.log("main");
    update();
    setInterval(update,5000);
}
function sort(){
    var output = [];
    var max = 10000;
    var index = -1;
    while(playlist.songs.length > 0){
        max = 10000;
        for(var i1=0;i1<playlist.songs.length;++i1){
            if(max>=playlist.songs[i1].rating){
                max = playlist.songs[i1].rating;
            }
        }
        output.push(playlist.songs[index]);
        playlist.songs.splice(index+1,1);
    }
    playlist.songs=output;
}
function display(){
    //sort();
    var output="<br><br>";
    for(var i=0;i<playlist.songs.length;++i){
        output+='<h5 class="bordered">'+playlist.songs[i].name+' '+playlist.songs[i].rating+'<span style="float:right"><a href="#" onclick="upvote(\''+ playlist.songs[i].name +'\')" style="color:red" class="fa fa-thumbs-down fa-lg"></a> <a href="#" onclick="downvote(\''+ playlist.songs[i].name +'\')" style="color:green" class="fa fa-thumbs-up fa-lg"></a></span></h5>';
    }
    if(isAdmin) {
        $("#player").css("visibility","visible");
        addPlayer(curVideoURL);
    }else{
        $("#player").css("visibility","hidden");
    }
    $("#playlist").html(output);
    $("#songTitle").html(playlist.lastsong);
}
function upvote(songname){
    
}
function downvote(songname){
       
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
function addSong(name){
     $.ajax({
        url: host + "/addsong/",
        type: "POST",
        data: {
            token: token,
            songname: name
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