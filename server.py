from flask import *
from flask_login import LoginManager, UserMixin, login_user, logout_user, current_user
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
import os

# from Models import db, User, Game, Object

import random
import time

from Hunt import Hunt
from SavedHunt import SavedHunt
from ObjectGenerated import ObjectGenerated
from ObjectProvided import ObjectProvided
from Player import Player
from ScoreEntry import ScoreEntry

app = Flask(__name__)

# Login code is taken from https://www.geeksforgeeks.org/how-to-add-authentication-to-your-app-with-flask-login/
# Configuration
load_dotenv()

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///db.sqlite"   
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config["SECRET_KEY"] = os.environ['DB_KEY']

login_manager = LoginManager()
login_manager.init_app(app)

db = SQLAlchemy()

# User Model
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(250), unique=True, nullable=False)
    password = db.Column(db.String(250), nullable=False)
    games = db.relationship('Game', backref='user')

class Game(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    save_id = db.Column(db.Integer)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

db.init_app(app)
with app.app_context():
    db.drop_all()
    db.create_all()

# User Loader
@login_manager.user_loader
def loaded_user(user_id):
    return User.query.get(user_id)

# Registration
@app.route('/register', methods=["GET", "POST"])
def register():
    if request.method == 'POST':
        if (db.session.query(User).filter_by(username=request.form.get("username")).count() < 1):
            user = User(username=request.form.get("username"), password=request.form.get("password"))
            db.session.add(user)
            db.session.commit()
            return redirect(url_for("login"))
        return render_template("error.html", error="User Already Exists")
    
    return render_template("sign-up.html")

# Login
@app.route('/login', methods = ["GET", "POST"])
def login():
    if request.method == 'POST':
        user = User.query.filter_by(username=request.form.get("username")).first()

        if (user.password == request.form.get("password")):
            login_user(user)
            return redirect(url_for("home"))
        
    return render_template("login.html")

# Logout
@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("home"))

# Home
@app.route("/")
def home():
    # Render home.html on "/" route
    return render_template("home.html")

# Game Functions
# Game Creation
@app.route("/create-game")
def create_game():
    return render_template("create-game.html")

# Join Game
@app.route("/join-game")
def join_game():
    return render_template("join-game.html")


hunts = {}

# Route for organizers to start a hunt
@app.route("/start-hunt", methods=['POST'])
def start_hunt():
    # Cleaning out inactive hunts that have been open for 3 hours
    INACTIVITY_LIMIT = 60*60*3
    for id in hunts:
        if time.time() - hunts[id].get_start_time() > INACTIVITY_LIMIT:
            hunts.pop(id)

    # Creating new hunt
    hunt_name = request.form['roomName']
    organizer = request.form['org']
    
    objectNumber = 1
    objects = []
    players = []

    while f"riddle{objectNumber}" in request.form:
        obj = None
        if (request.form[f'riddle-type-{objectNumber}'] == 'AI'):
            obj = ObjectGenerated("", request.form[f'room{objectNumber}'], request.form[f'code{objectNumber}'])
        else: 
            obj = ObjectProvided("", request.form[f'room{objectNumber}'], request.form[f'code{objectNumber}'])
        objects.append(obj)
        objectNumber += 1

    hunt_id = random.randint(1000, 9999)    
    while hunt_id in hunts:
        hunt_id = random.randint(1000, 9999)

    for cnt, object in enumerate(objects):
        object.set_riddle(request.form[f'riddle{cnt+1}'])

    hunts[hunt_id] = Hunt(hunt_name, organizer, objects, players, time.time())
    return render_template("hunt-code.html", hunt_name=hunt_name, hunt_id=hunt_id)

# Saving Hunts
saved_hunts = {}
current_save = [0] #Counter to Set IDs for saved hunts

@app.route("/save-hunt", methods=["POST"])
def save_hunt():
    # Creating new hunt
    hunt_name = request.form['roomName']
    organizer = request.form['org']
    
    objectNumber = 1
    objects = []

    while f"riddle{objectNumber}" in request.form:
        obj = None
        if (request.form[f'riddle-type-{objectNumber}'] == 'AI'):
            obj = ObjectGenerated("", request.form[f'room{objectNumber}'], request.form[f'code{objectNumber}'])
        else: 
            obj = ObjectProvided("", request.form[f'room{objectNumber}'], request.form[f'code{objectNumber}'])
        objects.append(obj)
        objectNumber += 1

    current_cnt = current_save[0]
    hunt_id = current_cnt
    current_save[0] += 1

    for cnt, object in enumerate(objects):
        object.set_riddle(request.form[f'riddle{cnt+1}'])

    saved_hunts[hunt_id] = SavedHunt(hunt_id, hunt_name, organizer, objects)

    curr_user = User.query.filter_by(username=current_user.username).first()
    save = Game(save_id=hunt_id, user=curr_user)
    db.session.add(save)
    db.session.commit()
    return redirect(url_for("dashboard"))

# Dashboard for Saved Games
@app.route("/dashboard", methods=["GET"])
def dashboard():
    if not current_user.is_authenticated:
        return render_template("error.html", error="Not Logged In")

    user_games = []
    for hunt in current_user.games:
        if hunt.save_id in saved_hunts:
            user_games.append(saved_hunts[hunt.save_id])

    return render_template("dashboard.html", user_games=user_games)

@app.route("/start-saved-hunt", methods=["POST"])
def start_saved_hunt():
    # Cleaning out inactive hunts that have been open for 3 hours
    INACTIVITY_LIMIT = 60*60*3
    for id in hunts:
        if time.time() - hunts[id].get_start_time() > INACTIVITY_LIMIT:
            hunts.pop(id)

    # Creating new hunt
    game_id = int(request.form.get("game_id"))
    saved_hunt = saved_hunts[game_id]
    
    objects = saved_hunt.objects
    players = []

    hunt_id = random.randint(1000, 9999)    
    while hunt_id in hunts:
        hunt_id = random.randint(1000, 9999)

    hunts[hunt_id] = Hunt(saved_hunt.get_name(), saved_hunt.get_organizer(), objects, players, time.time())
    return render_template("hunt-code.html", hunt_name=saved_hunt.get_name(), hunt_id=hunt_id)

@app.route("/delete-saved-hunt", methods=["POST"])
def delete_saved_hunt():
    id = int(request.form.get("game_id"))
    game = Game.query.filter_by(save_id=id).first()
    db.session.delete(game)
    db.session.commit()
    return redirect(url_for("dashboard"))

@app.route("/join-hunt", methods=["POST"])
def join_hunt():
    hunt_id = int(request.form["id"])
    player_name = str(request.form["name"])

    if hunt_id in hunts:
        player = Player(len(hunts[hunt_id].players), player_name, 0, time.time(), time.time(), False)
        hunts[hunt_id].players.append(player)
        return render_template("enter-hunt.html", hunt_id=hunt_id, player_id=player.get_id(), player_name=player_name, hunt_name=hunts[hunt_id].get_name())
    else:
        return render_template("error.html", error="Hunt Not Found")

@app.route("/current-riddle", methods=["POST"])
def current_riddle():
    hunt_id = int(request.form["hunt_id"])
    player_id = int(request.form["player_id"])

    for player in hunts[hunt_id].players:
        if player_id == player.get_id():
            player.set_start_time(time.time())
            next_hint = hunts[hunt_id].objects[player.get_current_object()].get_riddle()
            next_room = hunts[hunt_id].objects[player.get_current_object()].get_room()
            return render_template("player-dashboard.html", riddle=next_hint, room=next_room, obj=player.get_current_object(), player_id=player_id, hunt_id=hunt_id)
    
    return render_template("error.html", error="Player Not Found")

@app.route("/current-riddle/<player>/<hunt>", methods=["GET"])
def current_riddle_get(player, hunt):
    hunt_id = int(hunt)
    player_id = int(player)

    for player in hunts[hunt_id].players:
        if player_id == player.get_id():
            next_hint = hunts[hunt_id].objects[player.get_current_object()].get_riddle()
            next_room = hunts[hunt_id].objects[player.get_current_object()].get_room()
            return render_template("player-dashboard.html", riddle=next_hint, room=next_room, obj=player.get_current_object(), player_id=player_id, hunt_id=hunt_id)
    
    return render_template("error.html", error="Player Not Found")

@app.route("/submit-item", methods=['POST'])
def submit_item():
    hunt_id = int(request.form["hunt_id"])
    player_id = int(request.form["player_id"])
    code = str(request.form["code"])

    if hunt_id not in hunts:
        return render_template("error.html", error="Hunt Not Found")
    
    for player in hunts[hunt_id].players:
        if player_id == player.get_id():
            current_object_idx = player.get_current_object()
            correct_code = str(hunts[hunt_id].objects[current_object_idx].get_code())

            if player.get_finished():
                return render_template("error.html", error="You have already finished the hunt.")
            
            if code == correct_code:
                player.set_current_object(player.get_current_object() + 1)
                player.set_current_time(time.time())
                if player.get_current_object() < len(hunts[hunt_id].objects):
                    return redirect(f"/current-riddle/{player_id}/{hunt_id}")
                else:
                    player.set_finished(True)
                    return redirect(f"/finish/{player_id}/{hunt_id}")
            else:
                return render_template("error.html", error="Your code is incorrect. Please go back and try again")

    return render_template("error.html", error="Player Not Found")

# Route for finishing
@app.route("/finish/<player>/<hunt>", methods=["GET"])
def finish_game(player, hunt):
    player_id = int(player)
    hunt_id = int(hunt)
    for player in hunts[hunt_id].players:
        if player_id == player.get_id():
            if player and player.get_finished():
                player_time = player.get_current_time()
                rank = 1
                for pl in hunts[hunt_id].players:
                    if pl and pl.get_finished() and pl.get_current_time() < player_time:
                        rank += 1

                total_seconds = round(player.get_current_time() - player.get_start_time())
                hours = total_seconds // 3600
                total_seconds %= 3600
                minutes = total_seconds // 60
                total_seconds %= 60
                seconds = total_seconds
                return render_template("finish.html", name=player.get_name(), rk=rank, hrs=hours, mins=minutes, secs=seconds)
            else:
                return render_template("error.html", error="Hunt is Unfinished")

    return render_template("error.html", error="Player Not Found")
    
@app.route("/leaderboard/<int:hunt_id>", methods=['GET'])
def leaderboard(hunt_id):
    print("LEADERBOARD")
    if hunt_id not in hunts:
        return render_template("error.html", error="Hunt Not Found")

    scores = []
    for player in hunts[hunt_id].players:
        current_time = time.time()
        if (player.get_finished()):
            current_time = player.get_current_time()
        else:
            current_time = time.time()
        score = ScoreEntry(player.get_name(), player.get_current_object(), current_time-player.get_start_time())
        scores.append(score)
        print(player.get_start_time())

    sorted_scores = sorted(scores, key=lambda x: (x.get_score(), -x.get_time()), reverse=True)
    
    return render_template("leaderboard.html", sorted_scores=enumerate(sorted_scores))

@app.route("/guessr")
def guessr():
    return render_template("guessr.html")

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
        app.run(debug=True)
