from rasa_sdk import Action
from sqlalchemy import create_engine, Column, String, Float, JSON, Integer
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import json

# Define the base and table structure
Base = declarative_base()

class CleanConversation(Base):
    __tablename__ = 'clean_conversations'
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_message = Column(String)
    predicted_intent = Column(String)
    confidence = Column(Float)
    entities = Column(JSON)
    bot_response = Column(String)

# Database setup
DATABASE_URL = "postgresql://rpostgres:postgres@localhost:5432/rasa_db"
engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)
session = Session()

class ActionStoreCleanConversations(Action):
    def name(self):
        return "action_store_clean_conversations"

    def run(self, dispatcher, tracker, domain):
        # Fetch relevant data from the conversation
        user_message = tracker.latest_message.get('text')
        intent = tracker.latest_message.get('intent', {}).get('name')
        confidence = tracker.latest_message.get('intent', {}).get('confidence')
        entities = tracker.latest_message.get('entities')
        bot_response = tracker.latest_action_name

        
        clean_conversation = CleanConversation(
            user_message=user_message,
            predicted_intent=intent,
            confidence=confidence,
            entities=json.dumps(entities),
            bot_response=bot_response
        )

        # Add and commit the conversation to the database
        session.add(clean_conversation)
        session.commit()

        return []
