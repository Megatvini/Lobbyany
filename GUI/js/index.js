var host = "http://192.168.43.188:8000";
var playlist = undefined;
var token = undefined;

function addPlayList(song){
    
}
function update(){
    $.ajax({
        url: host + "/getplaylist/",
        type: "POST",
        data: {
            token: token   
        },
        success: function(e){
            playlist = e;
            display();
        },
        error: function(e){
            loadAuthScreen();
        },
        dataType: "json"
    });
}
function main(){
    fetchToken();
    loadPlayList();
    setInterval(update,5000);
}
function sort(){
    var output = [];
    var max = 10000;
    var index = -1;
    while(playlist.songs){
        max = 10000;
        for(var i1=0;i1<playlist.songs.length;++i1){
            if(max>=playlist.songs[i1].rating){
                max = playlist.songs[i1].rating;
            }
        }
        output.push(playlist.songs[index]);
        playlist.songs.splice(index,1);
    }
    playlist.songs=output;
}
function display(){
    sort();
    var output="<br><br>";
    for(var i=0;i<playlist.songs.length;++i){
        output+='<h5 class="bordered">'+playlist.songs[i].name+' '+playlist.songs[i].rating+'<span style="float:right"><a href="#" onclick="upvote(\''+ playlist.songs[i].name +'\')" style="color:red" class="fa fa-thumbs-down fa-lg"></a> <a href="#" onclick="downvote(\''+ playlist.songs[i].name +'\')" style="color:green" class="fa fa-thumbs-up fa-lg"></a></span></h5>';
    }
    $("#playlist").html(output);
    $("#songTitle").html(playlist.lastsong);
}
function upvote(songname){
    
}
function downvote(songname){
       
}
function fetchToken(){
    var arr = document.cookie.split("lobbyAny=");
    if(arr.length > 2){
        loadAuthScreen();
        return;
    }
    token = arr[1];
}
function loadAuthScreen(){
    $.ajax({
        url: host + "/login.html",
        type: "GET",
        data: {},
        success: function(e){
            $(document).html(e);
        },
        error: function(e){
            
        },
        dataType: "html"
    });
}
function loadPlayList(){
    $.ajax({
        url: host + "/getplaylist/",
        type: "POST",
        data: {
            token: token   
        },
        success: function(e){
            playlist = e;
            display();
        },
        error: function(e){
            loadAuthScreen();
        },
        dataType: "json"
    });
}
main();