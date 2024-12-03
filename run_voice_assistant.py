# voice_assistant/main.py

import threading
import random
import logging
import time
import warnings
from colorama import Fore, init
from voice_assistant.audio import record_audio, play_audio, audio_status, audio_quit
from voice_assistant.transcription import transcribe_audio
from voice_assistant.response_generation import *
from voice_assistant.text_to_speech import text_to_speech
from voice_assistant.utils import delete_file
from config import Config
import asyncio
from voice_assistant.api_key_manager import get_transcription_api_key, get_response_api_key, get_tts_api_key

# Configure logging
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')

# Initialize colorama
init(autoreset=True) 
response_list = [
    "Let me just check that information for you, it’ll only take a moment.",
    "I’m just pulling up the details on that product. ",
    "I’m checking the latest updates on that offer for you. ",
    "I’m just taking a moment to gather the best information on this. ",
    "Let me confirm those details for you. ",
    "I’m working on getting the most accurate info for you. ",
    "I need a second to get that exact information for you. ",
    "I’m double-checking the details to ensure you get the right answer. "
]

def response_updater(key, text):
    response_list[key] = text

async def async_text_to_speech(*args):
    await asyncio.to_thread(text_to_speech, *args)

async def main():
    """
    Main function to run the voice assistant.
    """
    warnings.filterwarnings('ignore')  
    # chat_history = [
    #     {"role": "system", "content": """ You are a helpful Assistant.
    #      You are friendly and fun and you will help the users with their requests.
    #      Your answers are short and concise. """}
    # ]

    while True:
        try:
            # Record audio from the microphone and save it as 'test.wav'
            record_audio(Config.INPUT_AUDIO)

            # Get the API key for transcription
            transcription_api_key = get_transcription_api_key()

            # Transcribe the audio file
            user_input = transcribe_audio(
                Config.TRANSCRIPTION_MODEL, transcription_api_key, Config.INPUT_AUDIO, Config.LOCAL_MODEL_PATH)

            # Check if the transcription is empty and restart the recording if it is. This check will avoid empty requests if vad_filter is used in the fastwhisperapi.
            if not user_input:
                logging.info(
                    "No transcription was returned. Starting recording again.")
                continue
            logging.info(Fore.GREEN + "You said: " + user_input + Fore.RESET)

            # Check if the user wants to exit the program
            if "goodbye" in user_input.lower() or "arrivederci" in user_input.lower():
                break

            # Append the user's input to the chat history
            # chat_history.append({"role": "user", "content": user_input})

            if Config.TTS_MODEL == 'openai' or Config.TTS_MODEL == 'elevenlabs' or Config.TTS_MODEL == 'melotts' or Config.TTS_MODEL == 'cartesia':
                output_file = 'output.mp3'
            else:
                output_file = 'output.wav'

#########-----------------------------------------------------------------------------------------############
                 # Generate a response
            response_task = generate_response(
                user_input, Config.LOCAL_MODEL_PATH)
            
#########-----------------------------------------------------------------------------------------############

            # Get the API key for TTS
            tts_api_key = get_tts_api_key()

            # Convert the response text to speech and save it to the appropriate file
        
            tts_task = async_text_to_speech(Config.TTS_MODEL, tts_api_key,
                           random.choice(response_list), output_file, Config.LOCAL_MODEL_PATH)
            
            task_var = await asyncio.gather(tts_task, response_task)

            if Config.TTS_MODEL == "cartesia":
                pass
            else:
                play_audio(output_file)

            # Setting the environment

            # Get the API key for response generation

            response_api_key = get_response_api_key()

           

            # actual_output_received = False

            # first_response = ""
            # while first_response == "":
            #     first_response = dict[1]
            #     if (first_response != ""):
            #         actual_output_received = True
            #         break
            #     first_response = dict[0]

            # print(response_list)

            # Append the assistant's response to the chat history
            # chat_history.append(
            #     {"role": "assistant", "content": response_text})

            # Determine the output file format based on the TTS model
            response_text =  task_var[1]
            text_to_speech(Config.TTS_MODEL, tts_api_key,
                               response_text, "", Config.LOCAL_MODEL_PATH)

            # Play the generated speech audio
            if Config.TTS_MODEL == "cartesia":
                pass
            else:
                play_audio(output_file)

            # Clean up audio files
            # delete_file(Config.INPUT_AUDIO)
            # delete_file(output_file)

        except Exception as e:
            logging.error(Fore.RED + f"An error occurred: {e}" + Fore.RESET)
            delete_file(Config.INPUT_AUDIO)
            if 'output_file' in locals():
                delete_file(output_file)
            time.sleep(1)


if __name__ == "__main__":
   asyncio.run(main())
