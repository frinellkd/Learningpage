"""Models and database functions for LearningPage project."""



# This is the connection to the SQLite database; we're getting this through
# the Flask-SQLAlchemy helper library. On this, we can find the `session`
# object, where we do most of our interactions (like committing, etc.)

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Integer, String, ForeignKey, or_, create_engine, DateTime
from sqlalchemy.orm import sessionmaker


db = SQLAlchemy()


##############################################################################
# Model definitions

class User(db.Model):

    __tablename__ = "users"

    user_id = db.Column(Integer, autoincrement=True, primary_key=True)
    user_name = db.Column(String(50), nullable=False)
    password = db.Column(String(50), nullable=False)
    age = db.Column(Integer, nullable=True)
    

    def __repr__(self):
        """Provide helpful representation when printed."""

        return "<User user_id=%s email=%s>" % (self.user_id, self.email)

    

class Visit(db.Model):

    __tablename__ = "visits"

    visit_id = db.Column(Integer, autoincrement=True, primary_key=True)
    user_id = db.Column(String(200), db.ForeignKey('users.user_id'), nullable=False)
    visit_date = db.Column(DateTime, nullable=False)
   
    # define relationship with user table

    user = db.relationship("User",
                           backref=db.backref("visit"))

    def __repr__(self):
        """Provide helpful representation when printed."""

        return "<Visit visit_id=%s user_id=%s visit_date=%s>" % (
            self.visit_id, self.user_id, self.visit_date)



class Topic_visited(db.Model):

    __tablename__ = "topics_visited"

    topics_visited_id = db.Column(Integer, autoincrement=True, primary_key=True)
    visit_id = db.Column(Integer, ForeignKey('visits.visit_id'), nullable=False)
    user_id = db.Column(Integer, ForeignKey('users.user_id'), nullable=False)
    quiz_completed_id = db.Column(Integer, ForeignKey('quizes_completed.quiz_completed_id'), nullable=False)
    topic_id = db.Column(Integer, ForeignKey('topics.topic_id'), nullable=False)

    # Define relationship to User
    user = db.relationship("User",
                           backref=db.backref("topic_visited"))
    
    # Define relationship with Quiz_completed
    quiz = db.relationship("Quiz_completed",
                           backref=db.backref("topic_visited"))
    
    # Define relationship with Topic
    topic = db.relationship("Topic",
                           backref=db.backref("topic_visited"))

    visit = db.relationship("Visit",
                           backref=db.backref("topic_visited"))

    
    # def __repr__(self):
    #     """Provide helpful representation when printed."""

    #     return "<Rating rating_id=%s movie_id=%s user_id=%s score=%s>" % (
    #         self.rating_id, self.movie_id, self.user_id, self.score)

class Topic(db.Model):

    __tablename__ = "topics"

    topic_id = db.Column(Integer, autoincrement=True, primary_key=True)
    topic_title = db.Column(String(100), nullable=False)
    wiki_url = db.Column(String(200), nullable=False)
    wiki_data = db.Column(String(1000), nullable=False)

    # def __repr__(self):
    #     """Provide helpful representation when printed."""

    #     return "<Rating rating_id=%s movie_id=%s user_id=%s score=%s>" % (
    #         self.rating_id, self.movie_id, self.user_id, self.score)

class Topic_video(db.Model):

    __tablename__ = "topic_videos"

    topic_video_id = db.Column(Integer, autoincrement=True, primary_key=True)
    video_key = db.Column(Integer, nullable=False)
    topic_id = db.Column(Integer, ForeignKey('topics.topic_id'), nullable=False)
    topic_thumbnail = db.Column(String(50), nullable=True)
        
    # Define relationship with Topic
    topic = db.relationship("Topic",
                           backref=db.backref("topics_visited"))

    # def __repr__(self):
    #     """Provide helpful representation when printed."""

    #     return "<Rating rating_id=%s movie_id=%s user_id=%s score=%s>" % (
    #         self.rating_id, self.movie_id, self.user_id, self.score)

class Quiz_completed(db.Model):

    __tablename__ = "quizes_completed"

    quiz_completed_id = db.Column(Integer, autoincrement=True, primary_key=True)
    grade_earned = db.Column(Integer, nullable=False)

    # def __repr__(self):
    #     """Provide helpful representation when printed."""

    #     return "<Rating rating_id=%s movie_id=%s user_id=%s score=%s>" % (
    #         self.rating_id, self.movie_id, self.user_id, self.score)

class Award_earned(db.Model):

    __tablename__ = "awards_earned"

    award_earned_id = db.Column(Integer, autoincrement=True, primary_key=True)
    award_id = db.Column(Integer, ForeignKey('awards.award_id'), nullable=False)
    visit_id = db.Column(Integer, ForeignKey('visits.visit_id'), nullable=False)

    # Define relationship to Award
    award = db.relationship("Award",
                           backref=db.backref("award_earned"))
    
    # Define relationship with Visit
    visit = db.relationship("Visit",
                           backref=db.backref("award_earned"))

    # def __repr__(self):
    #     """Provide helpful representation when printed."""

    #     return "<Rating rating_id=%s movie_id=%s user_id=%s score=%s>" % (
    #         self.rating_id, self.movie_id, self.user_id, self.score)

class Award(db.Model):

    __tablename__ = "awards"

    award_id = db.Column(Integer, autoincrement=True, primary_key=True)
    award_name = db.Column(String(50), nullable=False)
    award_gif_url = db.Column(String(100), nullable=False)

    def __repr__(self):
        """Provide helpful representation when printed."""

        return "<Award award_id=%s award_name=%s award_gif_url=%s>" % (
            self.award_id, self.award_name, self.award_gif_url)

class Note(db.Model):

    __tablename__ = "notes"

    note_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    topics_visit_id = db.Column(Integer, ForeignKey('topics_visited.topics_visited_id'), nullable=False)
    

    # Define relationship to Topic_visited
    topics_visited = db.relationship("Topic_visited",
                           backref=db.backref("note"))

    def __repr__(self):
        """Provide helpful representation when printed."""

        return "<Note note_id=%s topics_visited_id=%s>" % (
            self.note_id, self.topis_visited_id)
        
                    


def connect_to_db(app):
    """Connect the database to our Flask app."""

    # Configure to use our SQLite database
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///learningpage.db'
    engine = create_engine(app.config['SQLALCHEMY_DATABASE_URI'])
    Session = sessionmaker(bind=engine)
    session = Session()
    app.config['SQLALCHEMY_ECHO'] = False
    db.app = app
    db.init_app(app)
    db.create_all()

if __name__ == "__main__":
    # If this module is run interactively, it will be left 
    # in a state of being making it possible able to work with the database directly.
    
    from server import app
    from flask import Flask
    app = Flask(__name__)

    connect_to_db(app)
    print "Connected to DB."

    