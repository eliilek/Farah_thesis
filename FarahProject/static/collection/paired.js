function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie != '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) == (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
var csrftoken = getCookie('csrftoken');

function post(path, parameters){
  var xhr = new XMLHttpRequest();
  xhr.open("POST", path, true);
  xhr.setRequestHeader('Content-Type', 'application/json; charset=UTF-8');
  xhr.setRequestHeader('X-CSRFToken', csrftoken);
  complete = true;
  xhr.send(JSON.stringify(parameters));
}

var index = 0;
//Flags to determine when to move from sample to selection
var left_sample = false;
var right_sample = false;
//Flag to determine if we're accepting non-control keys
var accepting_keys = true;
//IFrame Players
var left_player;
var right_player;

var active_timeout;
var timeout_start;
var remaining;

var active = null;
var just_loaded = 0;

var left_keys = [81, 87, 69, 65, 83, 68, 90, 88, 67];
var right_keys = [73, 79, 80, 75, 76, 186, 188, 190, 191];

//Load the IFrame Player API
var tag = document.createElement('script');
tag.src = "https://www.youtube.com/iframe_api";
var firstScriptTag = document.getElementsByTagName('script')[0];
firstScriptTag.parentNode.insertBefore(tag, firstScriptTag);

//Keypress Function
function key_input(e){
  //Researcher controls
  if (e.shiftKey){
    if (e.keyCode == 49){
      //Pause and unpause
      if (active != null){
        if (active.getPlayerState() == 1){
          active.pauseVideo();
          if (active_timeout){
            window.clearTimeout(active_timeout);
            remaining = 30000 - (Date.now() - timeout_start)
          }
        } else if (active.getPlayerState() == 2){
          active.playVideo();
          active_timeout = setTimeout(function(){
            accepting_keys = true;
            active = null;
            left_sample = false;
            right_sample = false;
            next_video();
          }, remaining);
        }
      }
    } else if (e.keyCode == 50) {
      //Go Forward
      if (active_timeout){
        window.clearTimeout(active_timeout);
      }
      responses[index]['video_left'] = pairs[index]['left']['id'];
      responses[index]['video_right'] = pairs[index]['right']['id'];
      next_video();
    }
  } else if (jQuery.inArray(e.keyCode, left_keys) != -1 && accepting_keys){
    //Left is sampling
    if (!left_sample){
      //Disable non-control keys
      accepting_keys = false;
      left_sample = true;
      //Play video for 3 seconds
      left_player.playVideo();
      //In 3 seconds, enable non-control keys
      setTimeout(function(){
        accepting_keys = true;
        console.log("Left");
        left_player.pauseVideo();
        left_player.seekTo(pairs[index]['left']['start_time']);
      }, 3000);
    } else if (right_sample){
      //Select left video, play for 30 sec in fullscreen
      active = left_player;
      accepting_keys = false;
      left_player.playVideo();
      var frame = $("#left_player");
      $(".left").width("100vw");
      $(".right").hide();
      frame.height("100vh");
      frame.width("100vw");
      //var playerElement = $("#left_player");
      //var requestFullScreen = playerElement.requestFullScreen || playerElement.mozRequestFullScreen || playerElement.webkitRequestFullScreen;
      //if (requestFullScreen) {
      //  console.log("FS");
      //  requestFullScreen.bind(playerElement)();
      //}
      //Store selection
      console.log(pairs[index]['left']['id'])
      responses[index]['video_left'] = pairs[index]['left']['id'];
      responses[index]['video_right'] = pairs[index]['right']['id'];
      responses[index]['video_selected'] = false;
      //In 30 seconds, reset flags, switch to next index
      active_timeout = setTimeout(function(){
        //Document.exitFullscreen();
        next_video();
      }, 30000);
      timeout_start = Date.now();
    }
  } else if (jQuery.inArray(e.keyCode, right_keys) != -1 && accepting_keys){
    //Right is sampling
    if (!right_sample){
      //Unhook keypress
      accepting_keys = false;
      right_sample = true;
      //Play video for 3 seconds
      right_player.playVideo();
      //In 3 seconds, rehook keypress
      setTimeout(function(){
        accepting_keys = true;
        console.log("Right")
        right_player.pauseVideo();
        right_player.seekTo(pairs[index]['right']['start_time']);
      }, 3000);
    } else if (left_sample){
      //Select right video, play for 30 sec in fullscreen
      active = right_player;
      accepting_keys = false;
      right_player.playVideo();
      var frame = $("#right_player");
      $(".right").width("100vw");
      $(".left").hide();
      frame.height("100vh");
      frame.width("100vw");
      //var playerElement = $("#right_player");
      //var requestFullScreen = playerElement.requestFullScreen || playerElement.mozRequestFullScreen || playerElement.webkitRequestFullScreen;
      //if (requestFullScreen) {
      //  console.log("FS")
      //  requestFullScreen.bind(playerElement)();
      //}
      //Store selection
      responses[index]['video_left'] = pairs[index]['left']['id'];
      responses[index]['video_right'] = pairs[index]['right']['id'];
      responses[index]['video_selected'] = true;
      //In 30 seconds, reset flags, switch to next index
      active_timeout = setTimeout(function(){
        //Document.exitFullscreen();
        next_video();
      }, 30000);
      timeout_start = Date.now();
    }
  }
};

var left_playlist;
var right_playlist;

//Called when the IFrame API is loaded
function onYouTubeIframeAPIReady(){
  left_playlist = [];
  right_playlist = [];
  console.log(pairs);
  for (var i = 1; i < Object.keys(pairs).length; i++) {
    left_playlist.push(pairs[i]['left']['video_id']);
    right_playlist.push(pairs[i]['right']['video_id']);
  }
  console.log(left_playlist);
  console.log(right_playlist);
  //Create iframes
  left_player = new YT.Player('left_player', {
    height: '315',
    width: '560',
    videoId: pairs[index]['left']['video_id'],
    playerVars: {
      'autoplay':0,
      'controls':0,
      'disablekb':1,
      'fs':0,
      'modestbranding':1,
      'rel':0,
      'showinfo':0,
      'origin':"http://localhost:8000/",
      'playlist':left_playlist
    },
    events: {
      'onReady': onPlayerReady,
      'onStateChange': onStateChange
    }
  });
  right_player = new YT.Player('right_player', {
    height: '315',
    width: '560',
    videoId: pairs[index]['right']['video_id'],
    playerVars: {
      'autoplay':0,
      'controls':0,
      'disablekb':1,
      'fs':0,
      'modestbranding':1,
      'rel':0,
      'showinfo':0,
      'origin':'http://localhost:8000/',
      'playlist':right_playlist
    },
    events: {
      'onReady': onPlayerReady,
      'onStateChange': onStateChange
    }
  });
  // Set keyboard hooks
  $(document).keydown(key_input);

}

function onPlayerReady(event){
  if (event.target == left_player){
    event.target.seekTo(pairs[index]['left']['start_time']);
    just_loaded++;
  } else if (event.target == right_player){
    event.target.seekTo(pairs[index]['right']['start_time']);
    just_loaded++;
  }
  event.target.setShuffle(false);
}

function next_video(){
  index++;
  if (index >= Object.keys(pairs).length){
    //AJAX back the data and end
    end_trial();
  } else if (index == 1) {
    left_player.loadPlaylist(left_playlist);
    right_player.loadPlaylist(right_playlist);
  } else {
    left_player.nextVideo();
    right_player.nextVideo();
  }
  just_loaded = 2;
  $(".right").width("50vw");
  $(".left").show();
  $("#right_player").height("");
  $("#right_player").width("");
  $(".left").width("50vw");
  $(".right").show();
  $("#left_player").height("");
  $("#left_player").width("");
  accepting_keys = true;
  active = null;
  left_sample = false;
  right_sample = false;
  responses[index] = {};
}

function onStateChange(event){
  if (event.data == 1 && just_loaded > 0){
    event.target.pauseVideo();
    if (event.target == left_player){
      left_player.seekTo(pairs[index]['left']['start_time']);
    } else {
      right_player.seekTo(pairs[index]['right']['start_time']);
    }
    just_loaded--;
  }
  else if (event.data == 5){
    event.target.playVideo();
  }
}
