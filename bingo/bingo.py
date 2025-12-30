from cs50 import SQL
from flask import Flask, flash, redirect, render_template
from flask_session import Session

from cs50 import SQL
from flask import Flask, session, request, render_template
from flask_session import Session
import random
import string
import json

app = Flask(__name__)

# Server-side sessions
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Database
db = SQL("sqlite:///bingo.db")


def generate_player_id():
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=10))


@app.route("/")
def index():
    # Check if player exists
    if "player_id" not in session:
        session["player_id"] = generate_player_id()

    # Show the home screen
    return render_template("index.html", page="index")


@app.route("/join", methods=["GET", "POST"])
def join():
    if request.method == "GET":
        # Type game ID and join game
        return render_template("join.html", page="join")
    elif request.method == "POST":
        game_id = request.form.get("game_id")

        # Look up the game
        query = db.execute("SELECT * FROM games WHERE game_id = ? AND winner_found = 0;", game_id)

        if len(query) == 0:
            # Game does not exist
            return render_template("invalidjoin.html", page="join")

        # If game exists, join it
        session["game_id"] = game_id

        # Ensure player_id exists in session
        if "player_id" not in session:
            session["player_id"] = generate_player_id()

        return redirect("/board")


def generate_game_id():
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))


def format_ball(n):
    if 1 <= n <= 15:
        return f"B{n}"
    elif 16 <= n <= 30:
        return f"I{n}"
    elif 31 <= n <= 45:
        return f"N{n}"
    elif 46 <= n <= 60:
        return f"G{n}"
    else:
        return f"O{n}"


@app.route("/baller")
def baller():
    game_id = session.get("game_id")

    # Check if game_id exists
    if not game_id:
        game_id = generate_game_id()
        session["game_id"] = game_id

        player_id = session.get("player_id")

        db.execute(
            "INSERT INTO games (game_id, runner_id) VALUES (?, ?)",
            game_id,
            player_id
        )

    # Get called numbers
    called_rows = db.execute(
        "SELECT number FROM called_numbers WHERE game_id = ? ORDER BY called_at ASC",
        game_id
    )

    previous_numbers = [row["number"] for row in called_rows]
    ball_count = len(previous_numbers)
    current_ball = previous_numbers[-1] if previous_numbers else None

    formatted_numbers = [format_ball(n) for n in previous_numbers]
    formatted_csv = ", ".join(formatted_numbers)
    formatted_current = format_ball(current_ball) if current_ball else None

    # Set up page with previous numbers
    return render_template(
        "baller.html",
        page="baller",
        game_id=game_id,
        ball_count=ball_count,
        current_ball=formatted_current,
        previous_numbers=previous_numbers,
        numbers_csv=formatted_csv
    )


@app.route("/roll")
def roll():
    game_id = session.get("game_id")

    if not game_id:
        return redirect("/baller")

    # Get all previously called numbers
    rows = db.execute(
        "SELECT number FROM called_numbers WHERE game_id = ?",
        game_id
    )
    previous_numbers = [row["number"] for row in rows]

    # Determine remaining numbers (1–75)
    all_numbers = set(range(1, 76))
    remaining = list(all_numbers - set(previous_numbers))

    if not remaining:
        # All balls rolled
        return redirect("/baller")

    # Pick a new unique number
    new_number = random.choice(remaining)

    # Insert into called_numbers
    db.execute(
        "INSERT INTO called_numbers (game_id, number) VALUES (?, ?)",
        game_id,
        new_number
    )

    return redirect("/baller")


def generate_new_board(game_id, player_id):
    B = random.sample(range(1, 16), 5)
    I = random.sample(range(16, 31), 5)
    N = random.sample(range(31, 46), 5)
    G = random.sample(range(46, 61), 5)
    O = random.sample(range(61, 76), 5)

    N[2] = "FREE"

    bingo = {
        "B": B,
        "I": I,
        "N": N,
        "G": G,
        "O": O
    }

    board_json = json.dumps(bingo)

    # Insert board into database
    db.execute(
        "INSERT INTO boards (game_id, player_id, board_json) VALUES (?, ?, ?)",
        game_id,
        player_id,
        board_json
    )

    result = db.execute("SELECT last_insert_rowid() AS id")
    board_id = result[0]["id"]

    return board_id, bingo


@app.route("/board")
def show_board():
    # Get player and game details
    game_id = session.get("game_id")
    player_id = session.get("player_id")

    if not game_id:
        return redirect("/")

    # Look for an existing board
    rows = db.execute(
        "SELECT * FROM boards WHERE game_id=? AND player_id=?",
        game_id,
        player_id
    )

    if len(rows) == 0:
        # Create a new board
        board_id, bingo_board = generate_new_board(game_id, player_id)
    else:
        # Load existing board
        row = rows[0]
        board_id = row["board_id"]
        bingo_board = json.loads(row["board_json"])

    return render_template(
        "board.html",
        page="board",
        player_id=player_id,
        board_id=board_id,
        bingo=bingo_board
    )


def normalize_board(board_json):
    columns = ["B", "I", "N", "G", "O"]

    # Convert column-major → row-major
    board = []
    for row in range(5):
        board.append([board_json[col][row] for col in columns])

    # Force FREE space
    board[2][2] = "FREE"

    return board


def load_board(game_id, player_id):
    rows = db.execute(
        "SELECT board_json FROM boards WHERE game_id = ? AND player_id = ?",
        game_id, player_id
    )

    if len(rows) == 0:
        return None

    raw = json.loads(rows[0]["board_json"])
    return normalize_board(raw)


def get_called_numbers(game_id):
    rows = db.execute(
        "SELECT number FROM called_numbers WHERE game_id = ?",
        game_id
    )

    return {row["number"] for row in rows}


def check_bingo(board, called):
    size = 5

    # FREE is always considered called
    called = set(called)
    called.add("FREE")

    # Rows
    for row in board:
        if all(num in called for num in row):
            return True

    # Columns
    for col in range(size):
        if all(board[row][col] in called for row in range(size)):
            return True

    # Main diagonal
    if all(board[i][i] in called for i in range(size)):
        return True

    # Anti-diagonal
    if all(board[i][size - 1 - i] in called for i in range(size)):
        return True

    return False


def update_winner(game_id):
    db.execute(
        "UPDATE games SET winner_found = 1 WHERE game_id = ?",
        game_id
    )


@app.route("/check")
def check():
    game_id = session.get("game_id")
    player_id = request.args.get("player_id")
    board_id = request.args.get("board_id")

    # Validate inputs
    if not game_id or not player_id or not board_id:
        return "Missing game_id, player_id, or board_id", 400

    # Load the board
    rows = db.execute(
        "SELECT board_json FROM boards WHERE board_id = ? AND player_id = ? AND game_id = ?",
        board_id, player_id, game_id
    )

    if len(rows) == 0:
        return "Board not found", 404

    raw_board = json.loads(rows[0]["board_json"])
    board = normalize_board(raw_board)

    # Load called numbers
    called_rows = db.execute(
        "SELECT number FROM called_numbers WHERE game_id = ?",
        game_id
    )
    called_numbers = {row["number"] for row in called_rows}

    # Check bingo
    winner = check_bingo(board, called_numbers)

    # If winner, update game
    if winner:
        update_winner(game_id)

        return render_template(
            "status.html",
            message=f"BINGO! {player_id} won!",
            redirect_url="/baller",
            delay=5,
            play_sound=True
        )

    # No winner
    return render_template(
        "status.html",
        message="No bingo yet!",
        redirect_url="/baller",
        delay=5,
        play_sound=False
    )


@app.route("/rejoin")
def rejoin():
    game_id = session["game_id"]
    player_id = session["player_id"]
    query = db.execute("SELECT * FROM games WHERE game_id=? AND winner_found=0;", game_id)

    if len(query) == 0:
        return redirect("/")
    else:
        result = query[0]
        print(result)

        if player_id == result["runner_id"]:
            return redirect("/baller")  # If player is the runner
        else:
            return redirect("/board")  # If the player has a board


@app.route("/reset")
def reset():
    game_id = session.get("game_id")
    player_id = session.get("player_id")

    # If no game in session, just go home
    if not game_id:
        return redirect("/")

    # Mark game as abandoned ONLY if no winner yet
    db.execute(
        "UPDATE games SET winner_found = 2 WHERE game_id = ? AND runner_id = ? AND winner_found = 0",
        game_id,
        player_id
    )

    # Remove game_id from session
    session.pop("game_id", None)

    return redirect("/")
