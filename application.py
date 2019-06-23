from flask import Flask, render_template, request
from flask_socketio import SocketIO
from game import Game

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
app.config["DEBUG"] = True
socketio = SocketIO(app, ping_interval=4, ping_timeout=10)


@app.route("/")
def index():
    return render_template("index.html")


@socketio.on("disconnect")
def disconnect():
    game = Game.player_to_game.get(request.sid, None)

    if not game:
        return

    for player in game.players:
        if player == request.sid:
            reason = "disconnected"
        else:
            reason = "other player left"
        socketio.emit("game_over",
                      {"game_id": game.id,
                       "board": game.to_list(),
                       "reason": reason},
                      room=player)


@socketio.on("join_game")
def join_game():
    # Join a new game
    game = Game.join_game(request.sid)

    print("hi!", request.sid)

    for player in game.players:
        # Let client know which game he is in
        socketio.emit("joined_game",
                      {"game_id": game.id,
                       "board": game.to_list(),
                       "waiting": len(game.players) < 2,
                       "is_it_my_turn": len(game.players) < 2 or game.whose_turn() == player},
                      room=player)


@socketio.on("place_tile")
def place(data):
    game = Game.get_game(data["game_id"])

    if not game:
        socketio.send("game_does_not_exist", room=request.sid)
        return

    if request.sid != game.whose_turn():
        socketio.send("not_your_turn", room=request.sid)
        return

    game.place(int(data["x"]), int(data["y"]))

    if game.is_won():
        winning_player = game.who_won()

        for player in game.players:
            if winning_player == player:
                reason = "congratulations, you won!"
            else:
                reason = "you lost, better luck next time!"
            socketio.emit("game_over",
                          {"game_id": game.id,
                           "board": game.to_list(),
                           "reason": reason},
                          room=player)
        return

    for player in game.players:
        socketio.emit("placed_tile",
                      {"game_id": game.id,
                       "board": game.to_list(),
                       "is_it_my_turn": game.whose_turn() == player},
                      room=player)


if __name__ == '__main__':
    socketio.run(app)
