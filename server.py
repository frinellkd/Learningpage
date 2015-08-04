# Import libraries needed for project

# for youtube connection
from xml.etree import ElementTree

from jinja2 import StrictUndefined

from flask import Flask, render_template, redirect, request, flash, session
from flask_debugtoolbar import DebugToolbarExtension

from model import User, Visit, Topic_visited, Topic, Topic_video, Award_earned, Award, Note, Quiz_completed, connect_to_db, db

from sqlalchemy import update

import sqlite3

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

@app.route('/view')
def view_topic_selected():


    return render_template("view.html")

@app.route('/users/<int:id>')
def userinfo(id):

    user_info = User.query.filter_by(user_id = id).one()
    
    topics_visited = db.session.query(Topic_visited.topics_visited_id,
                                    Topic.topic_title,
                                    Visit.visit_date,
                                    Quiz_completed.grade_earned).join(Topic).join(Visit).join(Quiz_completed
                                    ).filter(Topic_visited.user_id == id).all()
    
    return render_template("user_info.html", user=user_info, topics_visited=topics_visited)

# @app.route('/movies')
# def movies_list():
#     """Show list of movies."""

#     movies = Movie.query.order_by(Movie.movie_title).all()
#     return render_template("movies_list.html", movies=movies)

# @app.route('/movies/<int:id>')
# def movieinfo(id):

#     movie_info = Movie.query.filter_by(movie_id = id).one()
    
#     rating_list = db.session.query(Rating.score,
#                                    Rating.user_id).filter(Rating.movie_id == id).order_by(Rating.score).all()
#     print rating_list


#     return render_template('movie_info.html', movie=movie_info, movies_rated=rating_list)

# @app.route('/test/<int:movie_id>', methods=["Post"])
# def userrating(movie_id):
#     userrating = int(request.form['user_rating'])
    
#     email = session.get('user_id')
#     try:
#         user_id = db.session.query(User.user_id).filter_by(email=email).one()[0]
    
#     except:
#         flash("you must be logged in to rate a movie")
#         return redirect('/movies/' + str(movie_id))


#     current_ratings = db.session.query(Rating).filter_by(user_id=user_id).filter_by(movie_id=movie_id).all()
    
    
#     if len(current_ratings) >= 1:

#         current_ratings[0].score=userrating
#         db.session.add(current_ratings[0])
               

#     else:
#         user_rating = Rating(movie_id=movie_id,
#                             score= userrating, 
#                             user_id=user_id)

#         db.session.add(user_rating) 
#     db.session.commit()

#     flash('Thanks for rating this movie')
#     return redirect('/movies/' + str(movie_id))
    

if __name__ == "__main__":
    # We have to set debug=True here, since it has to be True at the point
    # that we invoke the DebugToolbarExtension
    app.debug = True

    connect_to_db(app)

    # Use the DebugToolbar
    DebugToolbarExtension(app)

    app.run()