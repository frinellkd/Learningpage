"""Utility file to seed database from data in wiki_search_urls.txt and topic_youtube.txt"""

# makes data tables and ancilary programs avaialable.
from model import Topic_videos, Topic_wiki, Topic, connect_to_db, db
from server import app

from datetime import datetime

def load_Topics():
    """Load topics and topic_wiki info from wiki_search_urls into database."""
    User_file = open('seed_data/wiki_search_urls')
    
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
    Movie_file = open('seed_data/topic_youtube')
    
    for line in Movie_file:
        line.strip()
        row = line.split('|')
        topic_id = row[0]
        video_title = row[2]
        youtube_video_key = row[3]
        video_description = row[4]

        video = Topic_video(topic_id=topic_id, video_title=video_title, 
            youtube_video_key=youtube_video_key, video_description=video_description)

        db.session.add(video) 
    db.session.commit()

if __name__ == "__main__":
    connect_to_db(app)
    db.create_all()


    load_topics()
    load_topic_wiki()
    load_topic_videos()