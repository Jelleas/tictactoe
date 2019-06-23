class Board {
    constructor() {
        this._board = [[null, null, null],
                       [null, null, null],
                       [null, null, null]];
        this._turn = true;
    }

    get(x, y) {
        return this._board[x][y];
    }

    *[Symbol.iterator]() {
        for (let x = 0; x < 3; x++) {
            for (let y = 0; y < 3; y++) {
                yield {x: x, y: y, val: this._board[x][y]};
            }
        }
    }
}


function init() {
    socket = io();
    game_id = null;

    let html_tiles = document.getElementsByClassName("tile");
    for (let html_tile of html_tiles) {
        html_tile.addEventListener("click", (event) => {
            if (game_id === null) {
                return;
            }

            let coords = event.target.id.slice(-2);
            socket.emit("place_tile", {"game_id": game_id,
                                       "x": coords[0],
                                       "y": coords[1]});
        });
    }

    socket.on("connect", () => {
        join_game();
    });

    socket.on("game_over", (data) => {
        draw(data["board"])
        update_turn_display("");
        update_status_display(data["reason"]);
    })

    socket.on("placed_tile", (data) => {
        draw(data["board"]);
        update_turn_display(data["is_it_my_turn"] ? "your turn" : "opponent's turn");
    });

    socket.on("joined_game", (data) => {
        game_id = data["game_id"];
        
        draw(data["board"]);

        update_status_display(data["waiting"] ? "Waiting for an opponent" : "Playing!!!");

        if (data["waiting"]) {
            update_turn_display("");
        } else {
            update_turn_display(data["is_it_my_turn"] ? "your turn" : "opponent's turn");
        }
    });
}


function join_game() {
    socket.emit("join_game");
}

function update_turn_display(message) {
    let turn_display = document.getElementById("turn");
    turn_display.innerHTML = message;
}

function update_status_display(message) {
    let status_display = document.getElementById("status");
    status_display.innerHTML = message;
}

function draw(board) {
    for (let x = 0; x < 3; x++) {
        for (let y = 0; y < 3; y++) {
            let html_tile = document.getElementById("tile_" + x + y);

            if (board[x][y] === null) {
                html_tile.innerHTML = "";
            }
            else if (board[x][y] === false) {
                html_tile.innerHTML = "O";
            }
            else {
                html_tile.innerHTML = "X";
            }
        }
    }
}

init();
