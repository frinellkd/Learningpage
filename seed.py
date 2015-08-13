"""Utility file to seed database from data in wiki_search_urls.txt and topic_youtube.txt"""

# makes data tables and ancilary programs avaialable.
from model import Topic_video, Topic_wiki, Topic, Event_data, connect_to_db, db
from server import app

from datetime import datetime

def load_topics():
    """Load topics and topic_wiki info from wiki_search_urls into database."""
    User_file = open('seed_data/wiki_search_urls.txt')
    
    for line in User_file:
        # prepare line for reading data
        line.strip()
        row = line.split('|')
        #sets variables to correct data
        topic_title = row[0]
        topic_id = row[1]
        wiki_json = row[3]
        wiki_json_url = row[2]
        
        topic = Topic(topic_title=topic_title)
        wiki = Topic_wiki(topic_id=topic_id, wiki_json=wiki_json)

        db.session.add(topic)
        db.session.add(wiki) 
    db.session.commit()  
  

def load_topic_video():
    """Load Topic_videos info from topic_youtube into database."""
    Movie_file = open('seed_data/topic_youtube.txt')
    
    for line in Movie_file:
        line = line.strip()
        row = line.split('|')
        topic_id = row[0]
        video_title = row[2]
        youtube_video_key = row[3]
        video_description = row[4]

        video = Topic_video(topic_id=topic_id, video_title=video_title, 
            youtube_video_key=youtube_video_key, video_description=video_description)

        db.session.add(video) 
    db.session.commit()

def load_event_data():
    """Load data about the topics from the data file"""
    Data_file = open('seed_data/topic_data.txt')

    

    for line in Data_file:
        line = line.strip()
        row = line.split('|')
        topic_id=row[0]
        lat=row[1]
        lng=row[2]
        info=row[3]
        event_date=row[4]
        date = datetime.strptime(event_date, '%Y,%m,%d')
        event_title=row[5]
        image=row[6]

        topic_data=Event_data(topic_id=topic_id, lat=lat, lng=lng, description=info, event_date=date, event_title=event_title, image=image)

        
        db.session.add(topic_data)
    db.session.commit()   

if __name__ == "__main__":
    connect_to_db(app)
    db.create_all()

    load_topics()
    load_topic_video()
    load_event_data()
    
    