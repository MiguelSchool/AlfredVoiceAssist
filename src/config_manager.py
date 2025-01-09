import yaml
from loguru import logger as log


class ConfigManager:

	CONFIG_FILE = "./config.yml"

	def __init__( self ):

		self.config = None

	def load_config( self ):
		try:
			with open( ConfigManager.CONFIG_FILE, 'r', encoding = "utf-8" ) as yml_file:
				self.config = yaml.load( yml_file, Loader = yaml.FullLoader )
				if self.config:
					log.debug( "Config loaded successfully" )
				else:
					log.warning( "Config file is empty." )
		except FileNotFoundError:
			log.error( f"Config file {ConfigManager.CONFIG_FILE} not found." )
		except yaml.YAMLError as e:
			log.error( f"Error parsing the config file: {e}" )
		return self.config

	@classmethod
	def set_config_file( cls, file_path ):

		cls.CONFIG_FILE = file_path
		log.debug( f"Config file path set to: {cls.CONFIG_FILE}" )
