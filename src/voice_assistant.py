import struct
import sys
import pyaudio as py_audio
import vosk

from loguru import logger as log
from src.TTS import Voice
from src.config_manager import ConfigManager
from src.wake_words import WakeWords
from vosk import Model, SpkModel, KaldiRecognizer
import json
import text2numde


class VoiceAssistant:

	def __init__( self ):
		self.name = "Alfred Voice Assistant"

		config_manager = ConfigManager( )

		self.config = config_manager.load_config( )
		self.wake_words = WakeWords( )

		if self.config is None or self.wake_words is None:
			sys.exit( "Error loading config file" )

		language = self.config[ "assistant" ][ "language" ]
		if not language:
			language = "de"

		self.print_device_channels( )

		self.audio_stream = self.wake_words.py_audio.open(
			format = py_audio.paInt16,
			frames_per_buffer = self.wake_words.porcupine.frame_length,
			rate = self.wake_words.porcupine.sample_rate,
			channels = 1,
			input = True,
			input_device_index = self.config[ "assistant" ][ "inputdeviceindex" ]
		)

		log.info( "Audio stream started" )

		self.tts = Voice( )
		voices = self.tts.get_voice_keys_by_language( language )

		if len( voices ) > 0:
			self.tts.set_voice( voices[ 0 ] )
			log.info( voices[ 0 ] )

		log.info( "Voice assistant initialize..." )

		peak2text_model = Model( "./vosk-model-de-0.21" )
		speaker_model = SpkModel( "./vosk-model-spk-0.4" )
		self.recognizer = vosk.KaldiRecognizer( peak2text_model, speaker_model, 16000 )

		self.is_listening = False
		log.debug( "Voice assistant initialized" )



	def print_device_channels( self ):
		for i in range( self.wake_words.py_audio.get_device_count( ) ):
			value = self.wake_words.py_audio.get_device_info_by_index( i )
			log.debug( "id: {}, name: {}", value[ "index" ], value[ "name" ] )

	def run( self ):
		log.info( "Starting Voice Assistant" )
		try:
			while True:
				pcm = self.audio_stream.read( self.wake_words.porcupine.frame_length )
				pcm_unpacked = struct.unpack_from( "h" * self.wake_words.porcupine.frame_length, pcm )
				keyword_index = self.wake_words.porcupine.process( pcm_unpacked )
				if keyword_index >= 0:
					log.info( "Wake word detected" )
					self.is_listening = True
				if self.is_listening and self.recognizer.AcceptWaveform( pcm ):
					result = json.loads( self.recognizer.Result( ) )
					sentence = result[ "text" ]
					log.debug( "Recognized text: {}", sentence )
					self.is_listening = False

		except KeyboardInterrupt:
			log.info( "Stopping Voice Assistant" )

		finally:
			log.info( "Stopping Voice Assistant" )

			if self.wake_words.porcupine is not None:
				self.wake_words.porcupine.delete( )

			if self.audio_stream is not None:
				self.audio_stream.stop_stream( )
				self.audio_stream.close( )

			if self.wake_words.py_audio is not None:
				self.wake_words.py_audio.terminate( )

	def talk_to_user( self, text ):
		speaker = self.tts
		speaker.say( text )
