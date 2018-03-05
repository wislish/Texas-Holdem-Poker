var $jq = jQuery.noConflict();

function updateRival(data) {
    var rival = $("#rivalcards");
    rival.html('');

    cardfoldhtml1 = data[0].html;
    cardfoldhtml2 = data[1].html;
    var new_card1 = $jq(cardfoldhtml1);
    var new_card2 = $jq(cardfoldhtml2);
    new_card1.addClass("pcard1");
    new_card2.addClass("pcard2");
    rival.prepend(new_card2);
    rival.prepend(new_card1);
}


function updateRivalFold() {
    var rival = $("#rivalcards");
    rival.html('');
    cardfoldhtml1 = "<img class=\'pcard1\' src=\'/static/images/cardset/red_back.png\' alt=\'\'>";
    cardfoldhtml2 = "<img class=\'pcard2\' src=\'/static/images/cardset/red_back.png\' alt=\'\'>";
    var new_card1 = $jq(cardfoldhtml1);
    var new_card2 = $jq(cardfoldhtml2);
    rival.prepend(new_card2);
    rival.prepend(new_card1);
}

function updateDeskFold() {
    var desk = $("#desk-cards");
    desk.html('');
    cardfoldhtml = "<img class=\'dcard\' src=\'/static/images/cardset/red_back.png\'>";
    for (var i = 0; i < 5; i++) {
        var fold_card = $jq(cardfoldhtml);
        desk.prepend(fold_card);
    }
}

function updateDesk(data) {
    var desk = $("#desk-cards");
    desk.html('');
    for (var i = 0; i < data.length; i++) {
        card = data[i];
        var new_card = $jq(card.html);
        new_card.addClass("dcard");
        desk.prepend(new_card);
    }

    cardfoldhtml = "<img class=\'dcard\' src=\'/static/images/cardset/red_back.png\'>";
    for (var i = data.length; i < 5; i++) {
        var fold_card = $jq(cardfoldhtml);
        desk.prepend(fold_card);
    }
}

function updateMyHands(data) {
    var mydesk = $("#cardslayout");
    mydesk.html('');
    var new_player = $(data.html);
    mydesk.prepend(new_player);

}

function leaveGame() {
    location.href = "/poker/search/"
}

function updateTotalChips(data) {
    var chips = $("#totalchips");
    chips.html('');
    html = "<div><img class=\'chipimg\' alt=\'\' src=\'/static/images/chip.png\'>" + data + "</div>";
    var new_chips = $jq(html);
    chips.prepend(new_chips);
}


function initHoldem() {
    var gid = $("#gid");
    $jq.get("/poker/game/init/" + gid.text())
        .done(function (data) {
            console.log(data.id);
            setPlayerId(data.id);
            updateRivalFold();
            updateDeskFold();
            updateMyHands(data);
            updateTotalChips(data.AccumBet * 2);
            hideWinner();
            updateChoiceButton(true);
        });
}

function updateChoiceButton(is_init) {
    var choice_group = $("#mychoice-group");
    choice_group.html('');
    if (is_init) {
        check = "<button id=\'mychoice-check\' type=\'button\' class=\'snip1434\'>Check<i class=\'ion-cash\'></i></button>";
        bet = "<button id=\'mychoice-bet\' type=\'button\' class=\'snip1434\'>Bet<i class=\'ion-cash\'></i></button>";
        var new_check = $jq(check);
        var new_bet = $jq(bet);
        choice_group.prepend(new_check);
        choice_group.prepend(new_bet);
        $jq("#mychoice-check").click(function () {
            choice = "check";
            updateHoldem(choice)
        });
        $jq("#mychoice-bet").click(function () {
            choice = "bet";
            updateHoldem(choice)
        });
    } else {
        start = "<button id=\'mychoice-start\' type=\'button\' class=\'snip1434\'>Start<i class=\'ion-cash\'></i></button>";
        var new_start = $jq(start);
        choice_group.prepend(new_start);
        $jq("#mychoice-start").click(initHoldem);
    }
}

function updateRivalChips(chip) {
    var chips = $("#rivalchip");
    chips.html('');
    html = "<div><img class=\'chipimg\' alt=\'\' src=\'/static/images/chip.png\'>" + chip + "</div>";
    var new_chips = $jq(html);
    chips.prepend(new_chips);
}

function updateWinner(winner) {
    var windiv = $("#winner");
    windiv.removeClass('hidden');

    var winnername = $("#winnername");
    winnername.html('Winner: ' + winner);
}

function hideWinner() {
    var windiv = $("#winner");
    windiv.addClass('hidden');
}

function updateHoldem(choice) {
    // pId=1;
    console.log(pId);
    cost = 0;
    if (choice == 'bet') {
        cost = 100;
    }
    $jq.post("/poker/game/update", {pid: pId, choice: choice, cost: cost})
        .done(function (data) {
            console.log(data);
            if (typeof(data.players) == "undefined") {
                console.log('finish');
                finishHoldem(data);
                updateChoiceButton(false);
                return;
            }

            var pot_size = data.pot_size;
            var max_bet = data.max_bet;
            var round_status = data.round_status;
            var is_finished = data.is_finished;

            updateMyHands(data.players[0]);
            updateDesk(data.desk);
            updateTotalChips(data.pot_size);
            updateRivalChips(data.players[0].AccumBet);

            console.log(is_finished);
            if (is_finished == 'True') {
                console.log('inside');
                finishHoldem(pId);
            }
        })
}

function finishHoldem(data) {
    console.log('test4');
    // var test = $("#test-p");
    // test.html('');
    var winner = data.winner;
    var chips = data.chips;
    var rival = data.rival;
    var lastBet = data.lastBet;
    updateRival(rival);

    var mychips = $("#mychips");
    mychips.html('$' + chips);

    var myaccumbet = $("#myaccumbet");
    console.log('lastBet:' + lastBet);
    content = "<div><img class=\'chipimg\' alt='' src='/static/images/chip.png\'>$" + lastBet + "</div>";
    myaccumbet.html(content);
    updateWinner(winner);


}


function show_value(x) {
    document.getElementById("slider_value").innerHTML = x;
}

function initial_value() {
    if ($('#slider_value').text() == "") {

        document.getElementById("slider_value").innerHTML = $("#cost").attr("min");
        // $("#cost").attr("min");
    }
}

function newGanme() {
    back = '/static/images/cardset/red_back.png'
    //fold all cards
    for (var i = 0; i < 5; i++) {
        $(".cardslayout" + i + " .pcard1").attr('src', back);
        $(".cardslayout" + i + " .pcard2").attr('src', back);
        $('#dcard' + i).attr('src', back);
        $(".state" + i).show()
    }
    $(".cardslayout" + " .pcard1").attr('src', back);
    $(".cardslayout" + " .pcard2").attr('src', back);
    $(".dealer").remove();
    $("#totalchips").html("<img class='chipimg' alt='' src='/static/images/chip.png'>" + "0");
    // text(0);


}

var pId;

function setPlayerId(playerId) {
    pId = playerId;
}

function updatePlayerCard(userlist) {
    var name = userlist.playername
    var c1 = userlist.card_one
    var c2 = userlist.card_two
    var chip = userlist.begin_chip

    for (var i = 0; i < 5; i++) {
        if ($("#name" + i).text() == name) {
            src1 = '/static/images/cardset/' + c1 + '.png'
            src2 = '/static/images/cardset/' + c2 + '.png'
            $(".cardslayout" + i + " .pcard1").attr('src', src1);
            $(".cardslayout" + i + " .pcard2").attr('src', src2);
            // $("#chips" + i).text(chip);
            $("#chips" + i).html("<span class='label label-default rank-label2'>" + chip + "</span>")
            break;
        }
    }
    if ($("#myname").text() == name) {
        $("#mychips").text(chip);

    }
}

function myInfo(data) {
    $("#myname").html() == data.playername;
    $("#mychips").text(data.chip_remain);
    $("#myaction").html("<span class='label label-default rank-label'>" + data.state + "</span>")
    $("#myaccumbet").html("<img class='chipimg' alt='' src='/static/images/chip.png'>" + data.accum_bet);
    var c1 = $('#mycards .pcard1').attr('src').replace("red_back", data.card0);
    var c2 = $('#mycards .pcard2').attr('src').replace("red_back", data.card1);
    $('#mycards .pcard1').attr('src', c1);
    $('#mycards .pcard2').attr('src', c2);
}

function clock_init(){
    $(".clock-wrapper").removeClass('clock-hidden');
    $("#clock-digit").removeClass('clock-hidden');
    secondDeg = 0 / 60 * 360;
    stylesDeg = [
        "@-webkit-keyframes rotate-second{from{transform:rotate(" + secondDeg + "deg);}to{transform:rotate(" + (secondDeg + 360) + "deg);}}",
        "@-moz-keyframes rotate-second{from{transform:rotate(" + secondDeg + "deg);}to{transform:rotate(" + (secondDeg + 360) + "deg);}}"
    ].join("");

    document.getElementById("clock-animations").innerHTML = stylesDeg;
}

function clock_finish(){
    $(".clock-wrapper").addClass('clock-hidden');
    $("#clock-digit").addClass('clock-hidden');
    document.getElementById("clock-animations").innerHTML = "";
}


$jq(document).ready(function () {
    $(".cardslayout0").hide();
    $(".cardslayout1").hide();
    $(".cardslayout2").hide();
    $(".cardslayout3").hide();
    $(".cardslayout4").hide();
    $("#buttonCombo").hide();
    $("#chatpart").html('');
    var gid = $("#gid").html();
    var ws_path = "ws://" + window.location.host + ":8000/wbconnect/" + gid + "/";

    console.log("Connecting to " + ws_path);

    var webSocketBridge = new channels.WebSocketBridge();
    webSocketBridge.connect(ws_path);

    webSocketBridge.listen(function (data) {
        var pid = data.pid;
        console.log("Got websocket message", data);
        //initial game
        if (data.initial) {
            var num = data.number;
            for (var i = 0; i < num; i++) {
                var player = data.players[i];
                $("#name" + i).text(player.playername);
                if (player.is_online) {
                    var c = $(".state" + i);
                    c.html("<span class='label label-default rank-label'>" + "ready" + "</span>");
                }
                // if(!player.is_online){
                //     var c = $(".state" + i);
                //     c.html("<span class='label label-default rank-label'>" + "not ready" + "</span>");
                // }
                // $("#chips" + i).text(player.begin_chip);
                $("#chips" + i).html("<span class='label label-default rank-label2'>" + player.begin_chip + "</span>")
                $(".cardslayout" + i).show();
            }
        }
        //a new player joins the game
        else if (data.join) {
            for (var i = 0; i < 5; i++) {
                if ($(".cardslayout" + i).is(":visible") == false) {
                    $("#name" + i).text(data.playername);
                    // $("#chips" + i).text(data.begin_chip);
                    $("#chips" + i).html("<span class='label label-default rank-label2'>" + data.begin_chip + "</span>");
                    $(".cardslayout" + i).show();
                    break;
                }
                ;
            }
        }
        //a player leaves game
        else if (data.leave) {
            for (var i = 0; i < 5; i++) {
                if ($("#name" + i).html() == data.playername) {
                    $(".cardslayout" + i).hide();
                }
                ;

            }
        }
        //a player clicks ready
        else if (data.ready) {

            for (var i = 0; i < 5; i++) {
                if ($("#name" + i).html() == data.playername) {
                    $(".state" + i).html("<span class='label label-default rank-label'>" + "ready" + "</span>");
                }
            }
        }
        //start game
        else if (data.start) {
            var c1 = $('#mycards .pcard1').attr('src').replace("red_back", data.card0);
            var c2 = $('#mycards .pcard2').attr('src').replace("red_back", data.card1);


            $('#mycards .pcard1').attr('src', c1);
            $('#mycards .pcard2').attr('src', c2);
            var dealer = "<div class=\"dealer\">D</div>";
            var is_find = false;
            for (var i = 0; i < 5; i++) {
                $(".state" + i).hide()
                if ($("#name" + i).html() == data.dealer) {
                    $(".cardslayout" + i).prepend(dealer)
                    is_find = true;
                }
            }
            if (!is_find) {
                $(".cardslayout").prepend(dealer)
            }

            for (var j = 0; j < data.players.length; j++) {

                var p = data.players[j];

                for (var k = 0; k < 5; k++) {
                    if ($("#name" + k).html() == p.playername) {
                        // $("#chips" + k).text(p.begin_chip);
                        $("#chips" + k).html("<span class='label label-default rank-label2'>" + p.begin_chip + "</span>");
                        $("#action" + k).html("<span class='label label-default rank-label'>" + p.state + "</span>")
                        $("#accum_bet" + k).html("<img class='chipimg' alt='' src='/static/images/chip.png'>" + p.accum_bet);
                    }
                }
            }

            // update self
            $("#mychips").text(data.begin_chip);
            $("#myaction").html("<span class='label label-default rank-label'>" + data.state + "</span>")
            $("#myaccumbet").html("<img class='chipimg' alt='' src='/static/images/chip.png'>" + data.accum_bet);

            // var myname = $(myname).html();
            if (data.playername == data.current_player) {
                $("#buttonCombo").show();
                $("#mychoice-call").hide();
                $("#mychoice-check").show();
                $("#mychoice-bet").show();
                $("#mychoice-fold").show();

                initial_value();
            }

            var is_turn = false;
            for (var i = 0; i < 5; i++) {
                if ($("#name" + i).html() == data.current_player) {
                    $("#clock" + i).addClass("showmyturn");
                    is_turn = true;
                }else{
                    $("#clock" + i).removeClass("showmyturn");
                }
            }
            if (!is_turn) {
                $("#myclock").addClass("showmyturn");
            }else{
                $("#myclock").removeClass("showmyturn");
            }

        }
        //update after a player acts
        else if (data.update) {
            $("#totalchips").html("<img class='chipimg' alt='' src='/static/images/chip.png'>" + data.pot_size);
            // text(data.pot_size);
            var cardlist = data.desk;
            var is_find = false;
            //potsize change
            for (var i = 0; i < cardlist.length; i++) {
                src = '/static/images/cardset/' + cardlist[i] + '.png'
                $('#dcard' + i).attr('src', src);
            }
            //player attributes change
            for (var i = 0; i < 5; i++) {
                var p = data.player[0]
                if ($("#name" + i).html() == p.playername) {
                    // $("#chips" + i).text(p.chip_remain);
                    $("#chips" + i).html("<span class='label label-default rank-label2'>" + p.chip_remain + "</span>")
                    $("#action" + i).html("<span class='label label-default rank-label'>" + p.state + "</span>")

                    // $("#accum_bet" + i).text(p.accum_bet);
                    $("#accum_bet" + i).html("<img class='chipimg' alt='' src='/static/images/chip.png'>" + p.accum_bet);
                    is_find = true;
                }
            }
            if (!is_find) {
                $("#mychips").text(p.chip_remain);
                $("#myaction").html("<span class='label label-default rank-label'>" + p.state + "</span>")
                $("#myaccumbet").html("<img class='chipimg' alt='' src='/static/images/chip.png'>" + p.accum_bet);
                // $("#accum_bet0").html("<img class='chipimg' alt='' src='/static/images/chip.png'>chips")
            }

            var is_turn = false;
            for (var i = 0; i < 5; i++) {
                if ($("#name" + i).html() == data.current_player) {
                    $("#clock" + i).addClass("showmyturn");
                    is_turn = true;
                }else{
                    $("#clock" + i).removeClass("showmyturn");
                }
            }
            if (!is_turn) {
                $("#myclock").addClass("showmyturn");
            }else{
                $("#myclock").removeClass("showmyturn");
            }

            //if it's the turn

            if (data.playername == data.current_player) {
                $("#buttonCombo").show();
                $("#mychoice-bet").show();
                $("#mychoice-fold").show();

                $("#cost").attr('max', $("#mychips").text());
                $("#cost").attr('min', data.player_min_bet);
                document.getElementById("slider_value").innerHTML = $("#cost").attr("min");

                // if chip remain is not enough, only can fold or all in.
                if (data.player_min_bet > data.chip_remain) {
                    $("#mychoice-call").hide();
                    $("#mychoice-check").hide();
                    $("#mychoice-bet").hide();
                }
                // check is feasible.
                else if (data.round_max === 0) {
                    $("#mychoice-call").hide();
                    $("#mychoice-check").show();
                }
                //call is feasible.
                else {
                    $("#mychoice-check").hide();
                    $("#mychoice-call").show();

                }
            }

        }
        else if (data.finish) {
            updateWinner(data.winner)
            for (var i = 0; i < data.players.length; i++) {
                updatePlayerCard(data.players[i])
                $("#accum_bet" + i).html("<img class='chipimg' alt='' src='/static/images/chip.png'>" + "0");
                $(".state" + i).html("<span class='label label-default rank-label'>" + "not ready" + "</span>");

            }
            var cardlist = data.desk;
            for (var i = 0; i < cardlist.length; i++) {
                src = '/static/images/cardset/' + cardlist[i] + '.png'
                $('#dcard' + i).attr('src', src);
            }

            $("#mychoice-start").show()
            $("#totalchips").html("<img class='chipimg' alt='' src='/static/images/chip.png'>" + data.pot_size);

            // $("#myaccumbet").text(0)
            $("#myaccumbet").html("<img class='chipimg' alt='' src='/static/images/chip.png'>" + "0");
            $("#cost").attr('min', "0");
            // $("#mychips").text(data.);

            for (var i = 0; i < 5; i++) {
                $("#clock" + i).removeClass("showmyturn");
            }
            $("#myclock").removeClass("showmyturn");

        }
        else if (data.reconnect) {
            var players = data.players
            var playernm = data.number
            var desk = data.desk
            var dealer = "<div class=\"dealer\">D</div>";

            //distribute players
            var is_find = false;
            for (var i = 0; i < playernm; i++) {
                if (players[i].is_online) {
                    $(".cardslayout" + i).show();

                    $("#name" + i).text(players[i].playername);
                    // $("#chips" + i).text(players[i].chip_remain);
                    $("#chips" + i).html("<span class='label label-default rank-label2'>" + players[i].chip_remain + "</span>")
                    $("#action" + i).html("<span class='label label-default rank-label'>" + players[i].state + "</span>")

                    // $("#accum_bet" + i).text(p.accum_bet);
                    $("#accum_bet" + i).html("<img class='chipimg' alt='' src='/static/images/chip.png'>" + players[i].accum_bet);
                    $(".state" + i).hide();

                    if (data.dealer == players[i].playername) {
                        $(".cardslayout" + i).prepend(dealer)
                        is_find = true;
                    }

                }
            }
            if (!is_find) {
                $(".cardslayout").prepend(dealer)
            }
            for (var i = 0; i < desk.length; i++) {
                src = '/static/images/cardset/' + desk[i] + '.png'
                $('#dcard' + i).attr('src', src);
            }
            //my info
            myInfo(data);
            //desk cards
            // updateDesk(desk)
            //totalchips
            $("#totalchips").html("<img class='chipimg' alt='' src='/static/images/chip.png'>" + data.pot_size);
            $("#mychoice-start").hide();


        }
        else if (data.clockinit) {
            clock_init();
        }
        else if (data.clockfinish) {
            clock_finish();
        }
        else if (data.clock) {
            var list = $('#clock-digit');
            var html = '<p>' + data.countdown + '</p>';
            list.html($(html));
            if (data.countdown < 1) {
                // $("#mychoice-fold").onClick();
                if ($("#buttonCombo").is(':visible')) {
                    webSocketBridge.send({
                        "command": "update",
                        "choice": "fold",
                        "cost": 0
                    });
                    $("#buttonCombo").hide();
                }
                clock_finish();
            }
            // var percent = 100 * (1 - data.countdown / 30);
            // $(".showclock").attr("data-percent",percent);
        }
        else if (data.chat) {
            var name = data.name
            var message = data.ms
            var add_message = '  <li class="right clearfix"><span class="chat-img pull-right">\n' +
                // '{#<div id="username">aa</div>#}\n' +
                // ' <!--<img src="http://placehold.it/50/FA6F57/fff&text=ME" alt="User Avatar" class="img-circle" />-->\n' +
                '</span>\n' +
                '<div class="chat-body clearfix">\n' +
                ' <div class="header">\n' +
                // '{# <small class=" text-muted"><span class="glyphicon glyphicon-time"></span>15 mins ago</small>#}\n' +
                ' <strong class="pull-right primary-font" id="chat_name">' + name + '</strong>\n' + ' </div>\n' +
                ' <p id="chat_message">\n' + message + ' </p>\n' + '</div>\n' + '</li>'
            $('#chatpart').prepend(add_message)
        }
    });

//start click
    $("#mychoice-start").click(function () {
        webSocketBridge.send({
            "command": "start",
        });
        hideWinner();
        newGanme();
        $(this).hide();

    });

//bet click
    $("#mychoice-bet").click(function () {
        // alert("click");
        webSocketBridge.send({
            "command": "update",
            "choice": "bet",
            "cost": $("#cost").val()
        });
        $("#buttonCombo").hide();
    });

//fold click
    $("#mychoice-fold").click(function () {
        webSocketBridge.send({
            "command": "update",
            "choice": "fold",
            "cost": 0
        });
        $("#buttonCombo").hide();
    });

    $("#mychoice-check").click(function () {
        webSocketBridge.send({
            "command": "update",
            "choice": "check",
            "cost": 0
        });
        $("#buttonCombo").hide();
    });

    $("#mychoice-call").click(function () {
        webSocketBridge.send({
            "command": "update",
            "choice": "call",
            "cost": $("#cost").attr("min")
        });
        $("#buttonCombo").hide();
    });

    // all in
    $("#mychoice-allin").click(function () {
        webSocketBridge.send({
            "command": "update",
            "choice": "allin",
            "cost": $("#mychips").text()
        });
        $("#buttonCombo").hide();
    });

//click send message
    $('#btn-chat').click(function () {
        webSocketBridge.send({
            "command": "chat",
            "ms": $('#btn-input').val()

        });
        $("#btn-input").val("").focus();
    });
    $("#btn-input").keypress(function (e) {
        if (e.which == 13) {
            webSocketBridge.send({
                "command": "chat",
                "ms": $('#btn-input').val()

            });
            $("#btn-input").val("").focus();
        }
    });

// userdiv.find("#1").on("click", function () {
//            webSocketBridge.send({
//                "command": "send",
//                "name": data.name,
//                "start":true
//            });
//        });


// Add event-handlers

// $jq("#mychoice-start").click(initHoldem);
// $jq("#mychoice-check").click(function(){choice="check";updateHoldem(choice)});
// $jq("#mychoice-bet").click(function(){choice="bet";updateHoldem(choice)});

// $jq("#finish-button").click(finishHoldem(pId));

// $jq("#desk-button").click(testDeskHoldem);

// // Periodically refresh to-do list
// window.setInterval(getUpdates, 5000);

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
})
;
