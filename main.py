from flask import Flask, request, redirect, render_template, session, flash
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://blogz:allmostth3r3@localhost:8889/blogz'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)
app.secret_key = 'AB2z&ou812?slm0'


class Blog(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120))
    body = db.Column(db.String(300))
    owner_id = db.Column(db.Integer, db.ForeignKey('user.id'))    

    def __init__(self, title, body, owner):
        self.title = title
        self.body = body
        self.owner = owner

class User(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(120), unique=True)
    password = db.Column(db.String(120))
    blogs = db.relationship('Blog', backref='owner')

    def __init__(self, username, password):
        self.username = username
        self.password = password
        
@app.before_request
def require_login():
    allowed_routes = ['login', 'signup']
    if request.endpoint not in allowed_routes and 'username' not in session:
        return redirect('/login')



@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        if user and user.password == password:
            session['username'] = username
            flash("You are here YEAH!")
            return redirect('/')
        else:
            flash("Don't be a GIMBOID...wrong password or you don't exist", 'error')
            

    return render_template('login.html')

@app.route('/signup', methods=['POST', 'GET'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        verify = request.form['verify']

        # TODO - user signup asst 'validate' user's data

        existing_user = User.query.filter_by(username=username).first()
        if not existing_user:
            new_user = User(username, password)
            db.session.add(new_user)
            db.session.commit()
            session['username'] = username
            return redirect('/')
        else:
            # TODO - better response msg
            return "<h1>You GOIT! Are you from duplicate evil verse!</h1>"

    return render_template('signup.html')

@app.route('/logout')
def logout():
    del session['username']
    return redirect('/')

@app.route('/', methods=['POST', 'GET'])
def index():
    users = User.query.all()
    if request.args:
        user_id = request.args.get('id')
        one_user = User.query.filter_by(id=user_id).first()
        return render_template('singleUser.html', title="Single Smeghead,", one_user=one_user)
    return render_template('index.html', title='home', users=users)

@app.route('/singleUser')
def singleUser():
    blogs = Blog.query.all()
    return render_template('singleUser.html', title="Single Smeghead")

@app.route('/blog', methods=['POST', 'GET'])
def list_of_posts():
  
    blogs = Blog.query.all()
    if request.args:
        blog_id = request.args.get('id')
        one_entry = Blog.query.filter_by(id=blog_id).first()
        return render_template('entry.html', title="Posted Smeg,", one_entry=one_entry)
    return render_template('blog.html',title="Build a smegging Blog!", blogs=blogs)

      
@app.route('/newpost', methods=['POST', 'GET'])
def add_new_post():

    title_error = ''
    body_error = ''

    

    if request.method == 'POST':
        title = request.form['title']
        if title == '':
           title_error = "Please add a boody Title"
        
        body = request.form['body']
        if body == '':
            body_error = "Please add some freakin text to the body"

        

        if not title_error and not body_error:   #if it works
            owner = User.query.filter_by(username=session['username']).first()
            new_blog = Blog(title, body, owner)   
            db.session.add(new_blog)
            db.session.commit()
            id = request.args.get('id')
            one_entry = Blog(title, body, owner)
            return render_template('entry.html', title="Posted Smeg,", one_entry=one_entry, owner=owner)   

        else:
            return render_template('newpost.html', title_error=title_error, body_error=body_error)
           
    return render_template('newpost.html')


if __name__ == '__main__':
    app.run()