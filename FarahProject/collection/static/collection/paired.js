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

var active = null;

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
    if (e.which == 49){
      //Pause and unpause
      if (active != null){
        if (active.getPlayerState() == 1) active.pauseVideo();
        else if (active.getPlayerState() == 2) active.playVideo();
      }
    } else if (e.which == 48) {
      //Go Forward
      responses[index]['video_left'] = pairs[index]['left']['id'];
      responses[index]['video_right'] = pairs[index]['right']['id'];
      next_video();
    }
  } else if (jQuery.inArray(e.which, left_keys) && accepting_keys){
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
        left_player.pauseVideo();
        left_player.seekTo(pairs[index]['left']['start_time']);
      }, 3000);
    } else if (right_sample){
      //Select left video, play for 30 sec in fullscreen
      active = left_player;
      accepting_keys = false;
      left_player.playVideo();
      var playerElement = $(".left");
      var requestFullScreen = playerElement.requestFullScreen || playerElement.mozRequestFullScreen || playerElement.webkitRequestFullScreen;
      if (requestFullScreen) {
        requestFullScreen.bind(playerElement)();
      }
      //Store selection
      responses[index]['video_left'] = pairs[index]['left']['id'];
      responses[index]['video_right'] = pairs[index]['right']['id'];
      responses[index]['video_selected'] = false;
      //In 30 seconds, reset flags, switch to next index
      setTimeout(function(){
        accepting_keys = true;
        active = null;
        left_sample = false;
        right_sample = false;
        Document.exitFullscreen();
        next_video();
      }, 30000);
    }
  } else if (jQuery.inArray(e.which, right_keys) && accepting_keys){
    //Right is sampling
    if (!right_sample){
      //Unhook keypress
      accepting_keys = false;
      right_sample = true;
      //Play video for 3 seconds
      //In 3 seconds, rehook keypress
      setTimeout(function(){
        accepting_keys = true;
      }, 3000);
    } else if (left_sample){
      //Select right video, play for 30 sec in fullscreen
      active = left_player;
      accepting_keys = false;
      left_player.playVideo();
      var playerElement = $(".right");
      var requestFullScreen = playerElement.requestFullScreen || playerElement.mozRequestFullScreen || playerElement.webkitRequestFullScreen;
      if (requestFullScreen) {
        requestFullScreen.bind(playerElement)();
      }
      //Store selection
      responses[index]['video_left'] = pairs[index]['left']['id'];
      responses[index]['video_right'] = pairs[index]['right']['id'];
      responses[index]['video_selected'] = true;
      //In 30 seconds, reset flags, switch to next index
      setTimeout(function(){
        accepting_keys = true;
        active = null;
        left_sample = false;
        right_sample = false;
        Document.exitFullscreen();
        next_video();
      }, 30000);
    }
  }
};

//Called when the IFrame API is loaded
function onYouTubeIframeAPIReady(){
  //Create iframes
  left_player = new YT.Player('player', {
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
      'showinfo':0
    },
    events: {
      'onReady': onPlayerReady,
      'onStateChange': onPlayerStateChange
    }
  });
  right_player = new YT.Player('player', {
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
      'showinfo':0
    },
    events: {
      'onReady': onPlayerReady
    }
  });
  $("iframe").setAttribute('allowFullScreen', '');

  // Set keyboard hooks
  $(document).keypress(key_input);

}

function onPlayerReady(event){
  if (event.target == left_player){
    event.target.seekTo(pairs[index]['left']['start_time']);
  } else if (event.target == right_player){
    event.target.seekTo(pairs[index]['right']['start_time']);
  }
  event.target.pauseVideo();
}

function next_video(){
  index++;
  if (index >= Object.keys(stimuli).length){
    //AJAX back the data and end
    end_trial();
  }
  left_player.cueVideoByID({'video_id':pairs[index]['left']['video_id'], 'startSeconds':pairs[index]['left']['start_time']});
  right_player.cueVideoByID({'video_id':pairs[index]['right']['video_id'], 'startSeconds':pairs[index]['right']['start_time']});
}
