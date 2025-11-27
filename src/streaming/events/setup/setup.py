from src.streaming.events.setup.audio_steaming import initialize_audio_streaming_queues
from src.streaming.events.setup.general_streaming import initialize_general_streaming_queues

def initialize_streaming_broker():
    initialize_audio_streaming_queues()
    initialize_general_streaming_queues()
