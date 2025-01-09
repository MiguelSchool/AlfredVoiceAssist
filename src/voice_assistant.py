from loguru import logger as log
from TTS import Voice

class VoiceAssistant:

	def __init__(self):
		self.name = "Voice Assistant"
		self.tts = Voice()
		voices = self.tts.get_voice_keys_by_language('German')

		if len(voices) > 0:
			self.tts.set_voice( voices[0] )

	def run( self ):
		log.info( "Starting Voice Assistant" )
		message = "Hello, I am your voice assistant. How can I help you?"
		self.talk_to_user( message )

	def talk_to_user( self, text ):
		speaker = self.tts
		speaker.say( text )

