from src.voice_assistant import VoiceAssistant
import multiprocessing

if __name__ == "__main__":
	multiprocessing.set_start_method('spawn')

	voice_assistant = VoiceAssistant( )
	voice_assistant.run( )