# Import libraries needed for project

# for youtube connection
from xml.etree import ElementTree

from jinja2 import StrictUndefined

from flask import Flask, render_template, redirect, request, flash, session
from flask_debugtoolbar import DebugToolbarExtension

from model import User, Visit, Topic_visited, Topic, Topic_video, Award_earned, Award, Note, Quiz_completed, connect_to_db, db, Topic_wiki

from sqlalchemy import update

import sqlite3, json


db_connection = sqlite3.connect("learningpage.db", check_same_thread=False)
db_cursor = db_connection.cursor()

app = Flask(__name__)

# Required to use Flask sessions and the debug toolbar
app.secret_key = "ABC"

# Normally, if you use an undefined variable in Jinja2, it fails silently.
# This is horrible. Fix this so that, instead, it raises an error.
app.jinja_env.undefined = StrictUndefined


@app.route('/')
def index():
    """Homepage."""

    return render_template("homepage.html")

# @app.route('/users')
# def user_list():
#     """Show list of users."""

#     users = User.query.all()
#     return render_template("user_list.html", users=users)

@app.route('/login_form')
def login():
    """shows login form"""

    return render_template("login_form.html")

@app.route('/login_submit')
def login_submit():
    """checks whether person has a current logi and if so, logs them in.  If not it creates an account for them"""
    user_name = request.args.get("user_name")
    password = request.args.get("password")

    current_users = db.session.query(User.user_name, User.user_id).filter_by(user_name=user_name, password=password).all()
    
    if len(current_users) >= 1:
        session_id = current_users[0][1]
        
    else:
        if len(db.session.query(User.user_name).filter_by(user_name=user_name).all()) >= 1:
            flash("Incorrect password.  Please try again")
            return redirect('/login_form')

        else:
            
            #SQL Statement entering user info
            user = User(user_name=user_name, 
                    password= password)

            db.session.add(user) 
            db.session.commit()
            
            user_id = db.session.query(User.user_id).filter_by(user_name=user_name, password=password).one()   
            session_id = user_id[0]
               

    if session_id:
        session['user_id'] = session_id
        flash('You are logged in')

    return redirect('/users/' + str(session_id))

@app.route('/logout')
def log_out():

    session.clear()
    flash('You are logged out.')
    return redirect('/')       

@app.route('/view/<int:id>')
def view_topic_selected(id):

    """ Takes the topic id from the URL and uses it to locate correct information to display"""
    # gets all the the youtube keys from the database
    youtube_keys = db.session.query(Topic_video.youtube_video_key).filter(Topic_video.topic_id == id).all()
    # gets the path for the wiki page from the database
    topic_selected_wiki = db.session.query(Topic_wiki.wiki_json).filter(Topic_wiki.topic_id == id).one()
    # prepares the path by stripping off a retrun (will do this before populating the database in the future)
    topic_wiki = str(topic_selected_wiki.wiki_json).strip()


    data = open(topic_wiki).read()
    wiki_data = json.loads(data)
    wiki_data_title = wiki_data['parse']['title']
    wiki_data_parsed = wiki_data['parse']['text']['*']
    
    

    return render_template("view.html", youtube_keys=youtube_keys, wiki_data=wiki_data_parsed, wiki_title=wiki_data_title)

@app.route('/users/<int:id>')
def userinfo(id):

    user_info = User.query.filter_by(user_id = id).one()
    
    topics_visited = db.session.query(Topic_visited.topics_visited_id,
                                    Topic.topic_title,
                                    Visit.visit_date,
                                    Quiz_completed.grade_earned).join(Topic).join(Visit).join(Quiz_completed
                                    ).filter(Topic_visited.user_id == id).all()
    
    return render_template("user_info.html", user=user_info, topics_visited=topics_visited)
    

if __name__ == "__main__":
    # We have to set debug=True here, since it has to be True at the point
    # that we invoke the DebugToolbarExtension
    app.debug = False

    connect_to_db(app)

    # Use the DebugToolbar
    #DebugToolbarExtension(app)

    app.run()