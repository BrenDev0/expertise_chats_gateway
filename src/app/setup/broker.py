from src.streaming.events.setup.setup import initialize_streaming_broker
from src.auth.events.setup.setup import initialize_auth_broker

def initialize_broker():
    initialize_streaming_broker()
    initialize_auth_broker()