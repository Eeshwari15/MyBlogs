from flask import Flask, render_template, request,session
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail
import json
from datetime import datetime



with open('config.json', 'r') as c:
    param= json.load(c)["param"]

local_server = True
app = Flask(__name__)
app.secret_key='super-secret-key'
app.config.update(
    MAIL_SERVER = 'smtp.gmail.com',
    MAIL_PORT = '465',
    MAIL_USE_SSL = True,
    MAIL_USERNAME = param['user'],
    MAIL_PASSWORD=  param['password']
)
mail = Mail(app)
if(local_server):
    app.config['SQLALCHEMY_DATABASE_URI'] = param['local_uri']
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = param['prod_uri']

db = SQLAlchemy(app)


class Contacts(db.Model):
    sno = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    phone= db.Column(db.String(12), nullable=False)
    message = db.Column(db.String(120), nullable=False)
    date = db.Column(db.String(12), nullable=True)
    email = db.Column(db.String(20), nullable=False)


class Posts(db.Model):
    sno = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80), nullable=False)
    slug = db.Column(db.String(21), nullable=False)
    content = db.Column(db.String(120), nullable=False)
    date = db.Column(db.String(12), nullable=True)
    def p(self):
       print(self.title)
@app.route("/")
def home():
    posts=Posts.query.filter_by().all()[0:param['no_of_posts']]
    return render_template('index.html', param=param,posts=posts)
@app.route("/post2")
def post2():
    posts=Posts.query.filter_by().all()[0:param['no_of_posts']]
    return render_template('post2.html', param=param,posts=posts)
p=[]

@app.route("/post/<post_slug>", methods=['GET'])
def post_route(post_slug):
    post = Posts.query.filter_by(slug=post_slug).first()
    return render_template('post.html', param=param, post=post)

@app.route("/about")
def about():
    return render_template('about.html', param=param)
@app.route("/dashboard",methods=['GET','POST'])
def dashboard():
    if 'user' in session and session['user']==param['admin_user']:
        posts = Posts.query.all()
        return render_template('dashboard.html',param=param,posts=posts)

    if request.method=='POST':
        username=request.form.get('uname')
        password=request.form.get('pass')
        if username==param['admin_user'] and password==param['admin_pass']:
            session['user']=username
            posts=Posts.query.all()
            return render_template('dashboard.html',param=param,posts=posts)

    return render_template('login.html', param=param)

@app.route("/edit/<sno>",methods = ['GET', 'POST'])
def edit(sno):
    if 'user' in session and session['user'] == param['admin_user']:
     if request.method=='POST':
         req_title=request.form.get("title")
         req_slug=request.form.get("slug")
         req_content=request.form.get("content")





@app.route("/contact", methods = ['GET', 'POST'])
def contact():
    if(request.method=='POST'):
        name = request.form.get('name')
        email = request.form.get('email')
        phone = request.form.get('phone')
        message = request.form.get('message')
        entry = Contacts(name=name, phone = phone, message = message, date= datetime.now(),email = email )
        db.session.add(entry)
        db.session.commit()
        mail.send_message('New message from ' + name,
                          sender=email,
                          recipients = [param['user']],
                          body = message + "\n" + phone
                          )
    return render_template('contact.html', param=param)


app.run(debug=True)

