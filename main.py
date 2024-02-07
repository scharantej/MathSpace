
# Import necessary modules
from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy

# Initialize the Flask application
app = Flask(__name__)

# Configure the database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///puzzles.db'
app.config['SECRET_KEY'] = 'supersecretkey'
db = SQLAlchemy(app)

# Define the Puzzle model
class Puzzle(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80), nullable=False)
    body = db.Column(db.Text, nullable=False)
    solution = db.Column(db.Text, nullable=False)

# Define the Comment model
class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    puzzle_id = db.Column(db.Integer, db.ForeignKey('puzzle.id'), nullable=False)
    author = db.Column(db.String(80), nullable=False)
    body = db.Column(db.Text, nullable=False)

# Create the database tables
db.create_all()

# Define the home page route
@app.route('/')
def home():
    return render_template('home.html')

# Define the post puzzle route
@app.route('/post_puzzle', methods=['GET', 'POST'])
def post_puzzle():
    if request.method == 'GET':
        return render_template('post_puzzle.html')
    elif request.method == 'POST':
        title = request.form['title']
        body = request.form['body']
        solution = request.form['solution']
        puzzle = Puzzle(title=title, body=body, solution=solution)
        db.session.add(puzzle)
        db.session.commit()
        flash('Puzzle posted successfully!')
        return redirect(url_for('view_puzzles'))

# Define the view puzzles route
@app.route('/view_puzzles')
def view_puzzles():
    puzzles = Puzzle.query.all()
    return render_template('view_puzzles.html', puzzles=puzzles)

# Define the puzzle detail route
@app.route('/puzzle_detail/<puzzle_id>')
def puzzle_detail(puzzle_id):
    puzzle = Puzzle.query.get(puzzle_id)
    comments = Comment.query.filter_by(puzzle_id=puzzle_id).all()
    return render_template('puzzle_detail.html', puzzle=puzzle, comments=comments)

# Define the solve puzzle route
@app.route('/solve_puzzle/<puzzle_id>')
def solve_puzzle(puzzle_id):
    puzzle = Puzzle.query.get(puzzle_id)
    return render_template('solve_puzzle.html', puzzle=puzzle)

# Define the login route
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    elif request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        # Authenticate the user
        if username == 'admin' and password == 'secret':
            flash('Logged in successfully!')
            return redirect(url_for('home'))
        else:
            flash('Invalid credentials!')
            return render_template('login.html')

# Define the register route
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template('register.html')
    elif request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        # Create a new user
        user = User(username=username, password=password)
        db.session.add(user)
        db.session.commit()
        flash('Registered successfully!')
        return redirect(url_for('login'))

# Run the application
if __name__ == '__main__':
    app.run(debug=True)
