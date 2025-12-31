# Bingo Game
**Video Demo: https://youtu.be/I6oPhlRx0zg**

A web‑based Bingo game runner built with Flask

https://cs50.harvard.edu/certificates/db23d22b-9868-4d44-acf4-9470fe6b60e9

#### Overview
This project is a fully interactive **Bingo game runner** built using **Flask**, designed to simulate the experience of hosting and playing a live Bingo game through the browser. The application handles number generation, game state management, and player interaction, providing a clean and responsive interface for both hosts and participants.

The goal of this project is to demonstrate practical web development skills using Python, Flask, HTML/CSS/JavaScript, and CS50 SQL library — all while creating a fun, functional game environment.

#### Features
- **Randomized Bingo number calling** with no repeats
- **Live game state tracking** (called numbers, remaining numbers, game progress)
- **Host controls** for starting, resetting, and advancing the game
- **Player view** for following along in real time
- **Fun sound effects**
- **Lightweight, modular design** that’s easy to extend

#### Motivation
I wanted to build something that blends logic, UI design, and real‑time interaction. A Bingo runner is simple enough to implement cleanly, but flexible enough to expand with features like multiple bingo game modes or text to speech number calling.

#### How It Works
First, the user can choose to start a new game or join a running game. A new game is created and added to the games table in bingo.db. The game host gains control of a ball and can press a button to roll new bingo numbers. Bingo numbers are updated in the called_numbers table of the bingo database and on the side of the screen labeled "Previous Numbers". After the player joins a running game, a board is generated for them and stored within the boards table in bingo.db. The player clicks numbers on their board to score and can press a button that shows their game details when they have bingo. After, the game host can enter the player's game details which will verify that they won bingo.

#### How to Run
1. Clone the repository.
2. Install the dependencies.
   `pip install -r bingo/requirements.txt`
3. Set bingo.py to the FLASK_APP
   `export FLASK_APP=bingo.py`
4. Run the flask app.
   `flask run`
5. Visit the URL that Flask outputs.

#### File Structure
README.md<br>
bingo/<br>
├── requirements.txt<br>
├── bingo.py (This is where all of the main Flask functionality lies.)<br>
├── bingo.db (This database stores information about running games, numbers, and boards.)<br>
├── static/<br>
│   ├── styles.css (This holds all of the styling for the web pages/templates.)<br>
│   ├── script.js (This handles functions like sound playing.)<br>
│   ├── pictures/ (Holds themed bingo pictures and image credits)<br>
│   │   ├── bingo-pic1.jpg<br>
│   │   ├── bingo-pic2.jpg<br>
│   │   └── picture-credits.txt (Credits for images)<br>
│   └── sounds/ (Holds sound effects and sound credits)<br>
│       ├── ball-roll-sound.mp3<br>
│       ├── tap-sound.mp3<br>
│       ├── winner.mp3<br>
│       └── sound-credits.txt (Credits for sounds)<br>
├── templates/<br>
│   ├── layout.html (This is a template that other templates build off of.)<br>
│   ├── index.html (This page is for when a user first visits the website.)<br>
│   ├── join.html (This page is for a user entering a session ID to join a bingo game.)<br>
│   ├── invalidjoin.hmtl (This page shows a message for an invalid game id that was entered.)<br>
│   ├── baller.html (This page is for a user running a bingo game and rolling numbers.)<br>
│   ├── board.html (This page is for a someone playing bingo.)<br>
│   └── status.html (This page reveals whether the entered user has a winning bingo board or not.)<br>
└── tests/<br>
    ├── Test Pic<br>
    └── Test Pic...<br>

#### Development Process
##### Brainstorming
My brainstorming process was typing project ideas in my notes app.

##### Planning
For planning, I created a project note within my Obsidian vault. First, I decided on project features, then I typed out bullet points for each page of the website describing functionality. I also described the database layout.

##### Development 
First, I formatted the project files within folders. Inside my bingo folder, I created a static folder (where my CSS, JavaScript, sound, and picture files reside) and a templates folder (for my Jinja templates). I created bingo.db for storing game information. Then I set up requirements.txt and started bingo.py. After that, I created a layout.html file for the other Jinja templates to build off of. Then, I added more Jinja templates for each page of my web app. As I set up my templates, I styled them in styles.css. Eventually, I added some interactive functions within script.js.

##### Testing & Debugging
As I was coding each page in bingo.py, I tested the functionality and styling. If I ran into a bug, I would fix the issue before continuing my work. Eventually, all features were completed and the web app was bug free.

#### Challenges
- Filling in knowledge gaps
	- Designing a game board
	- Storing board data with JSON
	- Generating only unique numbers
	- Connecting game_ids to games
	- Jinja Templating
- Bug Fixes
	- Jinja If Statement for Navigation Bar Not Working
	- Mobile Screens Needed Styling Corrections
	- 500 Internal Server Error After Creating New Board

#### Timeline
- 12/22/25: Draft a plan for bingo game and set up codespace
- 12/23/25: Create website and templates
- 12/24/25-12/28/25: Handle bingo game logic and SQL database for tracking
- 12/29/25: Add finishing touches, write video script, record video, write README file, and publish to YouTube and GitHub

#### Limitations
- No permanent users
- Only traditional bingo games
- One number roll at a time
- Join current game defaults to games that the user is running

#### Future Improvements
- Text to speech bingo numbers
- More bingo game modes
- Online hosting 
- User accounts
- Bingo win record
- Improved CSS styling

#### Acknowledgements
- [Harvard CS50](https://cs50.harvard.edu/x/)
- [W3Schools (HTML, CSS, Javascript)](https://www.w3schools.com/)
- [Pixabay (for sounds and images)](https://pixabay.com/)
