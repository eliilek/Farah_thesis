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

function beep() {
    var snd = new Audio("data:audio/wav;base64,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qJrx4KOQjahZxWbcZgztj2c49nKmkId44S71j0c8eV9yDK6uPRzx5X18eDvjvQ6yKo9ZSS6l//8elePK/Lf//IInrOF/FvDoADYAGBMGb7FtErm5MXMlmPAJQVgWta7Zx2go+8xJ0UiCb8LHHdftWyLJE0QIAIsI+UbXu67dZMjmgDGCGl1H+vpF4NSDckSIkk7Vd+sxEhBQMRU8j/12UIRhzSaUdQ+rQU5kGeFxm+hb1oh6pWWmv3uvmReDl0UnvtapVaIzo1jZbf/pD6ElLqSX+rUmOQNpJFa/r+sa4e/pBlAABoAAAAA3CUgShLdGIxsY7AUABPRrgCABdDuQ5GC7DqPQCgbbJUAoRSUj+NIEig0YfyWUho1VBBBA//uQZB4ABZx5zfMakeAAAAmwAAAAF5F3P0w9GtAAACfAAAAAwLhMDmAYWMgVEG1U0FIGCBgXBXAtfMH10000EEEEEECUBYln03TTTdNBDZopopYvrTTdNa325mImNg3TTPV9q3pmY0xoO6bv3r00y+IDGid/9aaaZTGMuj9mpu9Mpio1dXrr5HERTZSmqU36A3CumzN/9Robv/Xx4v9ijkSRSNLQhAWumap82WRSBUqXStV/YcS+XVLnSS+WLDroqArFkMEsAS+eWmrUzrO0oEmE40RlMZ5+ODIkAyKAGUwZ3mVKmcamcJnMW26MRPgUw6j+LkhyHGVGYjSUUKNpuJUQoOIAyDvEyG8S5yfK6dhZc0Tx1KI/gviKL6qvvFs1+bWtaz58uUNnryq6kt5RzOCkPWlVqVX2a/EEBUdU1KrXLf40GoiiFXK///qpoiDXrOgqDR38JB0bw7SoL+ZB9o1RCkQjQ2CBYZKd/+VJxZRRZlqSkKiws0WFxUyCwsKiMy7hUVFhIaCrNQsKkTIsLivwKKigsj8XYlwt/WKi2N4d//uQRCSAAjURNIHpMZBGYiaQPSYyAAABLAAAAAAAACWAAAAApUF/Mg+0aohSIRobBAsMlO//Kk4soosy1JSFRYWaLC4qZBYWFRGZdwqKiwkNBVmoWFSJkWFxX4FFRQWR+LsS4W/rFRb/////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////VEFHAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAU291bmRib3kuZGUAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAMjAwNGh0dHA6Ly93d3cuc291bmRib3kuZGUAAAAAAAAAACU=");
    snd.play();
}

var index = 0;
var str_index = "First";
var player;

var active_timeout;
var timeout_start;
var event_index = 0;
var accepting_keys = true;
var remaining;

var active_interval;
var just_loaded = 0;

var started = false;

var var_opacity = 0;

var playlist = [];

//Load the IFrame Player API
var tag = document.createElement('script');
tag.src = "https://www.youtube.com/iframe_api";
var firstScriptTag = document.getElementsByTagName('script')[0];
firstScriptTag.parentNode.insertBefore(tag, firstScriptTag);

function onYouTubeIframeAPIReady(){
  console.log(videos);
  playlist.push(videos['Second']['video_id']);
  playlist.push(videos['Third']['video_id']);
  playlist.push(videos['Fourth']['video_id']);
  //Create iframes
  player = new YT.Player('player', {
    height: '450',
    width: '800',
    videoId: videos['First']['video_id'],
    playerVars: {
      'autoplay':0,
      'controls':0,
      'disablekb':1,
      'fs':0,
      'modestbranding':1,
      'rel':0,
      'showinfo':0,
      'origin':"http://localhost:8000/",
      'playlist':playlist
    },
    events: {
      'onReady': onPlayerReady,
      'onStateChange': onStateChange
    }

  });

  // Set keyboard hooks
  $(document).keydown(key_input);
  $(document).keyup(key_refresh);
}

function key_refresh(e){
  if (e.keyCode == 32){
    accepting_keys = true;
  }
}

function key_input(e){
  console.log(e.keyCode);
  //Researcher controls
  if (e.shiftKey){
    if (e.keyCode == 49){
      //Pause and unpause
      if (player.getPlayerState() == 1){
        player.pauseVideo();
        if (active_timeout){
          window.clearTimeout(active_timeout);
          remaining = 120000 - (Date.now() - timeout_start)
          accepting_keys = false;
        }
        if (active_interval){
          window.clearInterval(active_interval);
        }
      } else if (player.getPlayerState() == 2){
        player.playVideo();
        accepting_keys = true;
        active_timeout = setTimeout(collection, remaining);
        active_interval = setInterval(fading, 2000);
        }
    } else if (e.keyCode == 50) {
      //Go Forward
      if (active_timeout){
        window.clearTimeout(active_timeout);
      }
      if (active_interval){
        window.clearInterval(active_interval);
      }
      responses[index]['video'] = videos[str_index]['id'];
      next_video();
    }
  } else if (e.keyCode == 32 && accepting_keys) {
    if (started){
      console.log("Response");
      //Record response
      responses[index]['events'][event_index] = Date.now()-timeout_start;
      console.log(Date.now()-timeout_start);
      event_index++;
      //Increase volume, clarity if not full
      var_opacity = Math.max(var_opacity-0.1, 0);
      console.log(var_opacity);
      $(".fading").css("opacity", var_opacity);
      player.setVolume(Math.min(player.getVolume()+10, 100));
      //Reset interval
      if (active_interval) clearInterval(active_interval);
      active_interval = setInterval(fading, 2000);
      accepting_keys = false;
    } else {
      console.log("Start")
      started = true;
      accepting_keys = false;
      player.playVideo();
      active_timeout = setTimeout(function(){
        beep();
        accepting_keys = true;
        active_timeout = setTimeout(collection, 120000);
        timeout_start = Date.now();
        active_interval = setInterval(fading, 2000);
      }, 3000);
    }
  }
}

function collection(){
  clearInterval(active_interval);
  responses[index]['video'] = videos[str_index]['id'];
  responses[index]['play_time'] = 2;
  next_video();
}

function next_video(){
  index++;
  clearInterval(active_interval);
  if (index >= Object.keys(videos).length){
    //AJAX back the data and end
    end_trial();
  }
  if (index == 1){
    str_index = "Second";
    player.loadPlaylist(playlist);
  } else if (index == 2){
    str_index = "Third";
    player.nextVideo();
  } else {
    str_index = "Fourth";
    player.nextVideo();
  }
  accepting_keys = false;
  responses[index] = {'events':{}}
  event_index = 0;
  $(".fading").css("opacity", 0);
  var_opacity = 0;
  player.setVolume(100);
  player.seekTo(videos[str_index]['start_time']);
  just_loaded = 1;
  console.log("Start Time:");
  console.log(videos[str_index]['start_time'])
}

function onPlayerReady(event){
  event.target.seekTo(videos[str_index]['start_time']);
  just_loaded = -1;
}

function onStateChange(event){
  if (event.data == 1 && just_loaded > 0){
    console.log("Begin sample")
    active_timeout = setTimeout(function(){
      beep();
      accepting_keys = true;
      active_timeout = setTimeout(collection, 120000);
      timeout_start = Date.now();
      active_interval = setInterval(fading, 2000);
    }, 3000);
    just_loaded--;
  } else if (event.data == 1 && just_loaded < 0){
    console.log("First load")
    player.pauseVideo();
    player.seekTo(videos[str_index]['start_time']);
    just_loaded++;
  } else if (event.data == 5){
    console.log("Cue visual")
    event.target.playVideo();
    event.target.pauseVideo();
  }
}

function fading(){
  console.log("Fade")
  var_opacity = Math.min(var_opacity+0.1, 1);
  $(".fading").css("opacity", var_opacity);
  player.setVolume(Math.max(player.getVolume()-10, 0));
  console.log(var_opacity)
}
