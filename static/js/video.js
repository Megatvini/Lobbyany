
var player;
var timeIsSet=false;

function onYouTubeIframeAPIReady() {

}
function addPlayer(video){
     player = new YT.Player('player', {
        height: '390',
        width: '100%',
        videoId: video,
        events: {
          'onReady': onPlayerReady,
          'onStateChange': onPlayerStateChange
        }
    });
}
// 4. The API will call this function when the video player is ready.
function onPlayerReady(event) {
    event.target.playVideo();
}

// 5. The API calls this function when the player's state changes.
//    The function indicates that when playing a video (state=1),
//    the player should play for six seconds and then stop.
var done = false;
function getTimeFromCookies(){
    var k = document.cookie.split("curtime=");
    if(k.length < 2)
        return 0;
    var k1= k[1].split(";");
    return parseFloat(k1[0]);
}
function onPlayerStateChange(event) {
    if (event.data == YT.PlayerState.PLAYING && !done) {
        done = true;
    }
    if(event.data == 0){
        isPlaying = false;
        callNext();
    }
    if(event.data == 1){
        if(!timeIsSet){
            player.seekTo(getTimeFromCookies());
            timeIsSet=true;
        }
        isPlaying = true;
    }
    setTimeout(function(){$("#player").css("visibility","visible");},3000);
}
function stopVideo() {
    player.stopVideo();
}