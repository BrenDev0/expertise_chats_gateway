from src.auth.events.setup import initialize_auth_broker
from src.chats.events.setup import initialize_chats_broker
from src.streaming.events.setup import initialize_streaming_broker

def initialize_broker():
    initialize_auth_broker()
    initialize_chats_broker()
    initialize_streaming_broker()
    