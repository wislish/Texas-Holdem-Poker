var $jq = jQuery.noConflict();

var socket;

function initWebsocket() {
    socket = new WebSocket("ws://" + window.location.host + "/chat/");
    socket.onmessage = function (e) {
        var list = $('#clock-digit');
        var html = '<p>' + e.data + '</p>';
        list.html($(html));
        if (e.data<1){
            clock_stop();
        }

    };
    socket.onopen = function () {
        socket.send(30);
    };
    // Call onopen directly if socket is already open
    if (socket.readyState == WebSocket.OPEN) socket.onopen();
}


function clock_start() {
    initWebsocket();
    var count_down = 30;
    $jq.get("/poker/game/clock/"+ count_down)
    $(".clock-wrapper").removeClass('clock-hidden');
    $("#clock-digit").removeClass('clock-hidden');

    secondDeg = 0 / 60 * 360;
    stylesDeg = [
        "@-webkit-keyframes rotate-second{from{transform:rotate(" + secondDeg + "deg);}to{transform:rotate(" + (secondDeg + 360) + "deg);}}",
        "@-moz-keyframes rotate-second{from{transform:rotate(" + secondDeg + "deg);}to{transform:rotate(" + (secondDeg + 360) + "deg);}}"
    ].join("");

    document.getElementById("clock-animations").innerHTML = stylesDeg;
}

function clock_stop(){
    document.getElementById("clock-animations").innerHTML = "";
    $(".clock-wrapper").addClass('clock-hidden');
    $("#clock-digit").addClass('clock-hidden');
}


$jq(document).ready(function () {
    // Add event-handlers
    $jq("#clock_start").click(clock_start);
    $jq("#clock_stop").click(clock_stop);


    // CSRF set-up copied from Django docs
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
    $jq.ajaxSetup({
        beforeSend: function (xhr, settings) {
            xhr.setRequestHeader("X-CSRFToken", csrftoken);
        }
    });
});
