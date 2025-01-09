from loguru import logger
import time
import pyttsx3
import multiprocessing


def __speak__( text, voiceId ):
	engine = pyttsx3.init( )
	engine.setProperty( 'voice', voiceId )
	engine.say( text )
	engine.runAndWait( )


class Voice:

	def __init__( self ):
		self.name = "Alfred"
		self.process = None
		self.voiceId = "HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\Tokens\TTS_MS_DE-DE_HEDDA_11.0"

	def say( self, text ):
		if self.process:
			self.stop()

		process = multiprocessing.Process( target=__speak__, args=( text, self.voiceId ) )
		process.start( )
		self.process = process


	def set_voice( self, voiceId ):
		self.voiceId = voiceId

	def stop( self ):
		if self.process:
			self.process.terminate( )

	def get_voice_keys_by_language( self, language= "" ):
		result = []
		engine = pyttsx3.init( )
		voices = engine.getProperty( 'voices' )

		for voice in voices:
			if language == '':
				result.append( voice.id )
			elif language.lower() in voice.name.lower( ):
				result.append( voice.id )

		return result