import sys

from loguru import logger as log
from src.TTS import Voice
import yaml

CONFIG_FILE = "./config.yml"

class VoiceAssistant:

	def __init__(self):

		self.config = None
		self.load_voice_assistant_config( )

		if self.config is None:
			sys.exit( "Error loading config file" )

		language = self.config["assistant"]["language"]
		if not language:
			language = "de"

		self.name = "Voice Assistant"
		self.tts = Voice()
		voices = self.tts.get_voice_keys_by_language(language)

		if len(voices) > 0:
			self.tts.set_voice( voices[0] )
			log.info(voices[0])


	def run( self ):
		log.info( "Starting Voice Assistant" )
		message = "Hello, I am your voice assistant. How can I help you?"
		self.talk_to_user( message )

	def talk_to_user( self, text ):
		speaker = self.tts
		speaker.say( text )

	def load_voice_assistant_config( self ):
		global CONFIG_FILE
		with open( CONFIG_FILE, 'r', encoding = "utf-8" ) as ymlFile:
			self.config = yaml.load( ymlFile, Loader = yaml.FullLoader )
			if self.config:
				log.debug( "Config loaded" )

