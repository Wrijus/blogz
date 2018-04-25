from flask import Flask, request, redirect, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://blogz:allmostth3r3@localhost:8889/blogz'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)


class Blog(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120))
    body = db.Column(db.String(300))

    def __init__(self, title, body):
        self.title = title
        self.body = body


class User(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(120), unique=True)
    password = db.Column(db.String(120))

    def __init__(self, username, password):
        self.username = username
        self.password = password



@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/signup')
def signup():
    return render_template('signup.html')


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
            new_blog = Blog(title, body)   
            db.session.add(new_blog)
            db.session.commit()
            id = request.args.get('id')
            one_entry = Blog(title, body)
            return render_template('entry.html', title="Posted Smeg,", one_entry=one_entry)   

        else:
            return render_template('newpost.html', title_error=title_error, body_error=body_error)
           
    return render_template('newpost.html')


if __name__ == '__main__':
    app.run()