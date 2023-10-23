import os
import secrets
from PIL import Image
from flask import render_template, url_for, flash, redirect, request, abort
from flask_blog import app, db, bcrypt
from flask_blog.forms import RegistrationForm, LoginForm, UpdateAccountForm, PostForm
from flask_blog.models import User, Post
from flask_login import login_user, current_user, logout_user, login_required

# dummy data
#    posts = [
#       {
#            "author": "Corey",
#            "title": "Blog Post 1",
#            "content": "first post content",
#            "date_posted": "April, 2018"
#        },
#        {
#            "author": "Jane doe",
#            "title": "Blog Post 2",
#            "content": "Second post content",
#            "date_posted": "April 21, 2018"
#       }
#    ]

@app.route("/home")
def home():
    posts = Post.query.all()
    return render_template("home.html", posts = posts)

@app.route("/about")
def about():
    return render_template("about.html", title = "About")

@app.route("/register", methods = ["GET", "POST"])
def register():
    if current_user.is_authenticated:
        return redirect(url_for("home"))

    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_pw = bcrypt.generate_password_hash(form.password.data).decode("utf-8")
        user = User(username = form.username.data, email = form.email.data, password = hashed_pw)
        
        db.session.add(user)
        db.session.commit()
        
        flash(f"Account created for {form.username.data}", "success")
        return redirect(url_for("login"))

    return render_template("register.html", title = "Register", form = form)

@app.route("/login", methods = ["POST", "GET"])
def login():
    form = LoginForm()
    #if form.validate_on_submit():
    #   if form.email.data == "admin@blog.com" and form.password.data   == "password":
    #           flash(f"Logged in!", "success")
    #           return redirect(url_for("home"))
    #   else:
    #        flash("Login unseccessful. Check username and password", "danger")
    if current_user.is_authenticated:
        return redirect(url_for("home"))

    if form.validate_on_submit():
        user = User.query.filter_by(email = form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember = form.remember.data)
            next_page = request.args.get("next")
            flash(f"Logged in as {current_user.username}", "success")
            return redirect(next_page) if next_page else redirect(url_for("home"))
        else:
            flash(f"Login Unsuccessful, check email and password", "danger")
    return render_template("login.html", title = "Login", form = form)

@app.route("/logout")
def logout():
    logout_user()
    return redirect (url_for("home"))

#save picture update
def save_picture(form_picture):
    #randomize the name of the picture to a random hex
    random_hex = secrets.token_hex(8)
    #get the file extentsion eg jpg pg
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    
    #saving picture to static/
    picture_path = os.path.join(app.root_path, "static/profile_pics", picture_fn)
    
    #resizing image to 125x125px using pillow
    output_size = (125, 125)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)

    return picture_fn


# user account route
@app.route("/account", methods = ["GET", "POST"])
@login_required
def account():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            current_user.image_file = picture_file

        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()

        flash("Account Updated", "success")
        return redirect(url_for('account'))

    elif request.method == "GET":
        form.username.data = current_user.username
        form.email.data = current_user.email

    image_file = url_for("static", filename="profile_pics/" + current_user.image_file)
    return render_template("account.html", title = "account", image_file = image_file, form = form)

# users to create new posts
@app.route("/post/new", methods = ["GET", "POST"])
@login_required
def new_post():
    form = PostForm()
    if form.validate_on_submit():
        post = Post(title = form.title.data, content = form.content.data, author = current_user)
        db.session.add(post)
        db.session.commit()

        flash("Your Post Has Been Created!", "success")
        return redirect(url_for("home"))

    return render_template("create_post.html", title = "New Post", form = form, legend = "New Post")

# individual post page
@app.route("/post/<int:post_id>")
def post(post_id):
    post = Post.query.get_or_404(post_id)
    return render_template("post.html", title = post.title, post = post)

# update post
@app.route("/post/<int:post_id>/update", methods = ["GET", "POST"])
@login_required
def update_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    form = PostForm()
    if form.validate_on_submit():
        post.title = form.title.data
        post.content = form.content.data
        db.session.commit()
        flash("Post Has Been Updated", "success")
        return redirect(url_for("post", post_id = post.id))

    elif request.method == "GET":
        form.title.data = post.title
        form.content.data = post.content

    return render_template("create_post.html", title = "Update Post", form = form, legend = "Update Post")


# delete post
@app.route("/post/<int:post_id>/delete", methods = ["POST"])
@login_required
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    db.session.delete(post)
    db.session.commit()
    flash("Post Has Been Deleted", "success")
    return redirect(url_for("home"))
