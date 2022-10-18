//global variables
var N = 8;
var BLACK = 'black';
var WHITE = 'white';
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
//var coordinateswhite = { 1 : "a", 2:"b", 3:"c", 4:"d", 5:"e", 6:"f", 7:"g", 8:"h"}
var coordinatesblack = { 8 : "a", 7:"b", 6:"c", 5:"d", 4:"e", 3:"f", 2:"g", 1:"h"}
var coordinates = coordinatesblack
var pressed = 0;
var turn = 0;
//var moves -> all moves done
var possible_moves=null;
var move_from = '';
var game_over = '';

/*if(color_player === WHITE){
    coordinates = coordinateswhite;
    position = reverseString(position);
}*/

drawboard(player_color);

function reverseString(str) {
    return str.split("").reverse().join("");
}

//draw the chessboard
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
            img.src = path + '/' + pieces[position[i*N+j]];
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
            img.src = path + '/' + pieces[position[i*N+j]];
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
        if(game_over == '1-0'){
            text = 'White wins';
        }
        else if(game_over == '0-1'){
            text = 'Black wins';
        }
        else if(game_over == '1/2-1/2'){
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
                img.src = path + '/' + pieces[position[i*N+j]];
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

function resign(){
	if(game_over === ''){
        p = document.createElement('p');
	p.innerHTML = 'You resigned. Stockfish wins';
	document.getElementById('panel').appendChild(p);
    game_over = 1;
    }
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
    if(game_over===1){
        return
    }
    if(document.getElementById(id).style.backgroundColor === 'rgb(230, 194, 41)'){
        move_piece(id);
    }
        refresh();
    
}

function select(id){
    if(game_over===1){
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
        xhttp.open("GET", "getmoves/?moves=" + moves + "&from=" + move_from);
        xhttp.send();

        document.getElementById(id).style.backgroundColor = 'red';
        movefrom = id
        pressed = 1;
    }
    else if(pressed == 1){
        if(document.getElementById(id).style.backgroundColor === 'rgb(230, 194, 41)'){
            move_piece(id);
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

function move_piece(id){
    xhttp = new XMLHttpRequest();
    xhttp.onload = function(){
        jsonresponse = JSON.parse(this.responseText);
        position = jsonresponse['board'];
        moves = jsonresponse['allmoves'];
        game_over = jsonresponse['gameover'];
        update_board();
    };
    xhttp.open("GET", "makemove/?move="+move_from+id+'&position='+moves);
    xhttp.send();
}



