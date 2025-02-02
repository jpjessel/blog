from flask import Flask, render_template, redirect, url_for, session, flash, request
from flask_migrate import Migrate
from .config import Config
from .models import db, Post
from .forms import PostForm, LoginForm
import markdown
from werkzeug.security import generate_password_hash, check_password_hash 


app = Flask(__name__)
app.config.from_object(Config)  # Load config settings
app.config['TEMPLATES_AUTO_RELOAD'] = True

# Initialize the database
db.init_app(app)
migrate = Migrate(app, db)    
    
@app.route('/')
def index():
    return render_template('home.html')


@app.before_request
def create_tables():
    db.create_all()
    
@app.route('/admin_login', methods=['GET', 'POST'])
def admin_login():
    form = LoginForm()
    if form.validate_on_submit():
        hashed_password = generate_password_hash(form.password.data)
        print(hashed_password)
        if (form.username.data == app.config['ADMIN_USERNAME']) and (check_password_hash(app.config['ADMIN_PASSWORD'], form.password.data)):
            session['logged_in'] = True
            flash('Login successful!', 'success')
            return redirect(url_for('admin'))
        else:
            flash('Invalid credentials. Please try again.', 'danger')
    return render_template('login.html', form=form)

@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    flash('You have been logged out.', 'success')
    return redirect(url_for('admin_login'))
    
@app.route('/admin', methods=['GET', 'POST'])
def admin():
    
    if not session.get('logged_in'):
        return redirect(url_for('admin_login'))
    
    form = PostForm()
    posts = Post.query.all()
    
    if request.method == 'POST':
        action = request.form.get('action')
        
        if action == 'create':
            # Create new post logic
            content_type = request.form.get('content_type')
            title = request.form.get('title')
            content = request.form.get('content')
            priority = request.form.get('priority')

            # Ensure content_type is provided
            if not content_type:
                flash('Content type is required.')
                return redirect(url_for('admin'))

            # Create and save the new post
            new_post = Post(content_type=content_type, title=title, content=content, priority=priority)
            db.session.add(new_post)
            db.session.commit()
            flash('Post successfully created.', 'success')

        # Update post logic
        elif action == 'update':
            title = request.form.get('update_title')
            post = Post.query.filter_by(title=title).first()

            if post:
                post.content = request.form.get('content')
                post.priority = request.form.get('priority')
                db.session.commit()
                flash(f"Post '{title}' updated successfully", 'success')
            else:
                flash(f"Post '{title}' not found", 'error')
            return redirect(url_for('admin'))

        # Delete post logic
        elif action == 'delete':
            title = request.form.get('delete_title')
            post = Post.query.filter_by(title=title).first()

            if post:
                db.session.delete(post)
                db.session.commit()
                flash(f"Post '{title}' deleted successfully", 'success')
            else:
                flash(f"Post '{title}' not found", 'error')
            return redirect(url_for('admin'))

    # Handle GET requests (display form and posts)
    return render_template('admin.html', form=form, posts=posts)
    
@app.route('/poetry')
def PoemsPage():
    most_important = Post.query.where(Post.content_type == 'poetry').order_by(Post.priority.asc()).limit(2).all()
    if most_important:
        content_array = [{
            'title': entry.title,
            'content': markdown.markdown(entry.content),
            'created_at': entry.created_at
        } for entry in most_important]
        
        if len(content_array) == 1:
            content_titles = content_array[0]["title"]
        else:
            content_titles = [entry['title'] for entry in content_array]

        other_posts = Post.query.filter(~Post.title.in_(content_titles)) \
                                .where(Post.content_type == 'poetry') \
                                .order_by(Post.title.asc()).all()


        other_posts_array = [{
            'title': entry.title,
            'content': markdown.markdown(entry.content),
            'created_at': entry.created_at
        } for entry in other_posts]
        return render_template('sub_page.html', content_array=content_array, other_posts_array=other_posts_array)
    else:
        return render_template('sub_page.html', content_array=[])
    
@app.route('/shortstories')
def ShortStoryPage():
    most_important = Post.query.where(Post.content_type == 'short story').order_by(Post.priority.asc()).limit(2).all()
    if most_important:
        content_array = [{
            'title': entry.title,
            'content': markdown.markdown(entry.content),
            'created_at': entry.created_at
        } for entry in most_important]
        content_titles = [entry['title'] for entry in content_array]

        other_posts = Post.query.filter(~Post.title.in_(content_titles)) \
                                .where(Post.content_type == 'short story') \
                                .order_by(Post.title.asc()).all()

        other_posts_array = [{
            'title': entry.title,
            'content': markdown.markdown(entry.content),
            'created_at': entry.created_at
        } for entry in other_posts]
        return render_template('sub_page.html', content_array=content_array, other_posts_array=other_posts_array)
    else:
        return render_template('sub_page.html', content_array=[], other_posts_array=[])
    
@app.route('/football')
def FootballPage():
    most_important = Post.query.where(Post.content_type == 'football').order_by(Post.priority.asc()).limit(2).all()
    print(most_important)
    if most_important:
        content_array = [{
            'title': entry.title,
            'content': markdown.markdown(entry.content),
            'created_at': entry.created_at
        } for entry in most_important]
        
        content_titles = [entry['title'] for entry in content_array]

        other_posts = Post.query.filter(~Post.title.in_(content_titles)) \
                                .where(Post.content_type == 'football') \
                                .order_by(Post.title.asc()).all()

        other_posts_array = [{
            'title': entry.title,
            'content': markdown.markdown(entry.content),
            'created_at': entry.created_at
        } for entry in other_posts]
        return render_template('sub_page.html', content_array=content_array, other_posts_array=other_posts_array)
    else: 
        return render_template('sub_page.html', content_array=[], other_posts_array=[])