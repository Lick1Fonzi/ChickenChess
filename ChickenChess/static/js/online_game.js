//VARIABLES -----------------------------------------------------------------------------------------
connect_ok = 0;
var position = 'RNBKQBNRPPPPPPPP................................pppppppprnbkqbnr'; //starting position
//var your_color, img_path, time, increment defined in game.html
var draw = '1/2-1/2', win,lose;
if(your_color === 'white'){
    var your_turn = true;
    var win = '1-0';
    var lose = '0-1';
    var white_player = username;
    var black_player = '';
    console.log(your_color)
}
else{
    var your_turn = false;
    var win = '0-1';
    var lose = '1-0';
    var white_player = '';
    var black_player = username;
}

var your_time = time;
var opponent_time = time;
var white_time = time;
var black_time = time;

var allmoves = '';
var turn = 0;

var N = 8;
var BLACK = 'black';
var WHITE = 'white';
var player = {[WHITE] : 0, [BLACK] : 1}; //per valutare variabile WHITE e BLACK necessita di parentesi quadre

var board = document.getElementById("chessboard");
board.style.border = '1px solid black';
var pieces = {
    'K' : 'WKing.png',
    'Q' : 'WQueen.png',
    'B' : 'WBishop.png',
    'N' : 'WKnight.png',
    'R' : 'WRook.png',
    'P' : 'Wpawn.png',

    'k' : 'BKing.png',
    'q' : 'BQueen.png',
    'b' : 'BBishop.png',
    'n' : 'BKnight.png',
    'r' : 'BRook.png',
    'p' : 'Bpawn.png',
}

var coordinates = { 8 : "a", 7:"b", 6:"c", 5:"d", 4:"e", 3:"f", 2:"g", 1:"h"};
var pressed = 0;
var turn = 0;
var possible_moves=null;
var move_from = '';
var game_over = '';

var location_path_ws = window.location.pathname.replace('/game/','');
var socket = new WebSocket('ws://127.0.0.1:8000/ws/gamews/'+ location_path_ws);

socket.addEventListener('open', (event) => {
    socket.send("connected_"+ username);
  });

//websocket -------------------------------------------------------------------

socket.onclose = function(){
    if(game_over !== '')
        return
    window.alert("Connection error, please leave game and create a new one")
}



socket.onmessage = function(event){
    console.log(String(event.data));
    if( String(event.data) === "connected"){
            connect_ok = 1;
            drawboard(your_color);
        return;
    }

    console.log("on receive ->vars of"+ your_color + " "+ event.data["white_player"]+ event.data["black_player"])
    var data = JSON.parse(event.data);
    for(let i in data)
        console.log(i+": "+data[i]);
    position = data['position'];
    
    allmoves = data['allmoves'];
    outcome = data['outcome'];
    //console.log("outcome+gameover: ",outcome,game_over)
    if(outcome !== ''){
        stop(outcome);
        //console.log(outcome,game_over)
        update_board();
        return 
    }
    
    turn = data['turn'];
    var white_time = data['white_time'];
    var black_time = data['black_time'];

    if(data['black_player'] !== '' || data['black_player'] !== undefined)
        {black_player = data['black_player'];}
    if(data['white_player'] !== '' || data['white_player'] !== undefined) 
        {white_player = data['white_player'];}

    //console.log(white_player,black_player)

    if(!player[your_color]){
        your_time = white_time;
        opponent_time = black_time;
    }
    else{
        your_time = black_time;
        opponent_time = white_time;
    }

    if(turn % 2 === player[your_color]){
        your_turn = true;
    }
    //console.log(turn,your_color,your_turn,player[your_color]);
    update_board();
}


function sendmove(last_move){
    console.log("on send -> vars of "+your_color +" " + white_player + black_player)
    var outcome = '';
    var data = JSON.stringify(
        {   
            'outcome' : outcome,
            'position' : position,
            'allmoves' : allmoves,
            'last_move' : last_move,
            'turn' : turn,
            'white_time' : white_time,
            'black_time' : black_time,
            'white_player' : white_player,
            'black_player' : black_player,
            'time' : time,
            'increment' : increment,
        }
    );
    your_turn = false;
    
    console.log("creazione jsonfile: ");
    for(let i in JSON.parse(data)){
        console.log(i+ ": ", JSON.parse(data)[i]);
    }
    //console.log(white_player,black_player)

    socket.send(data);
}

function send_game_end(result){
    game_over = result;
    var data = JSON.stringify(
        {
            'allmoves' : allmoves,
            'outcome' : result,
            'position' : position
        }
    );
    socket.send(data);
}

//FUNCTIONS --------------------------------------------------------------------------------------

function resign(){
    if(game_over===''){
    send_game_end(lose);
    }
}

function stop(result){
    game_over = result;
}

function drawboard(player_color){
    if(player_color === 'white'){
        for(var i=N-1;i>=0;i--){
        let tr = document.createElement("tr");
        tr.id = "tr_" + i+1;
    for(var j=N-1;j>=0;j--){
        let td = document.createElement("td");
        td.id = coordinates[j+1] + (i+1);
        td.style.height='50px';
        td.style.width='50px';
        if((i+j)%2==0){
            td.style.backgroundColor = "#B6EA9A";}
        else{
            td.style.backgroundColor = "#68B684";}
        td.innerHTML = " ";
        tr.appendChild(td);
        td.onclick = function(){nopiece(td.id)};
        if(position[i*N+j] != '.'){
            img = document.createElement('img');
            img.src = img_path + '/' + pieces[position[i*N+j]];
            img.id = position.charAt(i*N+j);
            img.style.width = td.style.width;
            img.style.height= td.style.height;
            td.appendChild(img);
            if(td.hasChildNodes())
                td.onclick = function(){select(td.id);};
        }
    }
    board.appendChild(tr);
} 
}
else{
    for(var i=0;i<N;i++){
        let tr = document.createElement("tr");
        tr.id = "tr_" + i+1;
    for(var j=0;j<N;j++){
        let td = document.createElement("td");
        td.id = coordinates[j+1] + (i+1);
        td.style.height='50px';
        td.style.width='50px';
        if((i+j)%2==0){
            td.style.backgroundColor = "#B6EA9A";}
        else{
            td.style.backgroundColor = "#68B684";}
        td.innerHTML = " ";
        tr.appendChild(td);
        td.onclick = function(){nopiece(td.id)};
        if(position[i*N+j] != '.'){
            img = document.createElement('img');
            img.src = img_path + '/' + pieces[position[i*N+j]];
            img.id = position.charAt(i*N+j);
            img.style.width = td.style.width;
            img.style.height= td.style.height;
            td.appendChild(img);
            if(td.hasChildNodes())
                td.onclick = function(){select(td.id);};
        }
    }
    board.appendChild(tr);
}
}   
 
}

function update_board(){
    if(game_over !== ''){
        var text = '';
        if(game_over === '1-0'){
            text = 'White wins';
        }
        else if(game_over === '0-1'){
            text = 'Black wins';
        }
        else if(game_over === '1/2-1/2'){
            text = 'Draw';
        }
        p = document.createElement('p');
	    p.innerHTML = text;
	    document.getElementById('panel').appendChild(p);
    }
    for(i=0;i<N;i++){
        for(j=0;j<N;j++){
            let td = document.getElementById(get_square_id(i,j));
            if(td.hasChildNodes()){
                while (td.firstChild) { td.removeChild(td.firstChild); } 
            }
            td.onclick = function(){nopiece(td.id)};
            if(position[i*N+j] != '.'){
                img = document.createElement('img');
                img.src = img_path + '/' + pieces[position[i*N+j]];
                img.id = position.charAt(i*N+j);
                img.style.width = td.style.width;
                img.style.height= td.style.height;
                td.appendChild(img);
                td.onclick = function(){select(td.id)};
            }
        }
    }
    
    

}

function checkid(){
    console.log('checking id');
    for(i=0;i<N;i++){
        for(j=0;j<N;j++){
            td = document.getElementById(get_square_id(i,j));
            console.log(td.id);
        }}
}



//chess logic

function clean_vars(){
    move_from = null;
    possible_moves = null;
}

function refresh(){
    for(let i = 0;i<N;i++){
        for(let j=0;j<N;j++){
            if((i+j)%2==0)
                var col = "#B6EA9A";
            else 
                var col = "#68B684";
            var td = document.getElementById(String(coordinates[j+1]+(i+1))).style.backgroundColor = col;
        }
    }
    if(pressed == 1)
    pressed = 0;
    clean_vars();
}

function nopiece(id){
    if(game_over!=='' || !your_turn){
        return
    }
    if(document.getElementById(id).style.backgroundColor === 'rgb(230, 194, 41)'){
        sendmove(move_from+id);
    }
        refresh();
    
}

function select(id){
    if(game_over!=='' || !your_turn){
        return
    }
    console.log('this tdid:'+id);
    if(pressed==0){
        refresh();
        move_from = id;
        xhttp = new XMLHttpRequest();
        xhttp.onload = function(){
            if(xhttp.status==200){
                possible_moves = JSON.parse(this.responseText);
                color_possible_moves(possible_moves)
                document.getElementById(id).style.backgroundColor = 'red';
            }
        }
        xhttp.open("GET", "/getmoves/?moves=" + allmoves + "&from=" + move_from);
        xhttp.send();

        document.getElementById(id).style.backgroundColor = 'red';
        movefrom = id
        pressed = 1;
    }
    else if(pressed == 1){
        if(document.getElementById(id).style.backgroundColor === 'rgb(230, 194, 41)'){
            sendmove(move_from+id);
        }
        refresh();
        pressed = 0;
        movefrom = null;
    }
} 

function color_possible_moves(possible_moves){
    var values = Object.keys(possible_moves).map(function(key){return possible_moves[key]});
    console.log('possible moves: ' +values);
    // anche se costruito con codice esadecimale il colore viene salvato come tripletta rgb
    var col = "#e6c229";
    for(let i = 0;i<N;i++){
        for(let j=0;j<N;j++){
            values.forEach(function(val){
                if(val.includes(get_square_id(i,j)) && (get_square_id !== move_from)){
                    document.getElementById(get_square_id(i,j)).style.backgroundColor = col;
                }
            });
                
        }
    }
}


function get_square_id(i,j){
    return String(coordinates[j+1]+(i+1));
}


//Orologi
var x = setInterval(function() {
    if(turn === 0)
        return
    if(game_over === ''){
    if(your_turn){
        var id = "your";
        if(your_time === 0){
            send_game_end(lose);
        }
        your_time -= 1;
        var time = your_time;
        if(your_color === WHITE){
            white_time = your_time;
        }
        else{
            black_time = your_time;
        }
    }
    else{
        var id = "opponent";
        opponent_time -= 1;
        var time = opponent_time;
    }
    
    
  
    // Display the result in the element with id="demo"
    document.getElementById("Timer_"+id).innerHTML = time;

    let opp_name = ''
    if(your_color === BLACK){
        opp_name = white_player;
    }
    else{
        opp_name = black_player;
    }
    document.getElementById("opp_name").innerHTML = opp_name;
    
}
  }, 1000);
  
  
// main -------------------------------------------------------------------------------------

//drawboard(your_color);