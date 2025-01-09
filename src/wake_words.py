import sys

import pvporcupine
import pyaudio
from loguru import logger

from src.config_manager import ConfigManager

CONFIG_FILE = "./config.yml"

class WakeWords:
	def __init__(self):
		config_manager = ConfigManager()
		self.config = config_manager.load_config( )

		if self.config is None:
			sys.exit( "Error loading config file" )

		self.wake_words = self.config[ "assistant" ][ "wakewords" ]

		if not self.wake_words:
			sys.exit( "Error loading wake words" )

		self.porcupine = pvporcupine.create( keywords = self.wake_words, sensitivities= [0.6, 0.35] )  # sensitivities= [0.6, 0.35]
		self.py_audio = pyaudio.PyAudio()

		logger.info( "Wake words loaded" )