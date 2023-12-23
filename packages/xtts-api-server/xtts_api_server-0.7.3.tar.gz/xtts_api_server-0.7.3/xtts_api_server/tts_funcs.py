# tts.py

import torch
import torchaudio

from TTS.api import TTS

from TTS.tts.configs.xtts_config import XttsConfig
from TTS.tts.models.xtts import Xtts
from pathlib import Path

from xtts_api_server.modeldownloader import download_model,check_tts_version

from loguru import logger
from datetime import datetime
import os
import time 
import re
import json
import socket

# List of supported language codes
supported_languages = {
    "ar":"Arabic",
    "pt":"Brazilian Portuguese",
    "zh-cn":"Chinese",
    "cs":"Czech",
    "nl":"Dutch",
    "en":"English",
    "fr":"French",
    "de":"German",
    "it":"Italian",
    "pl":"Polish",
    "ru":"Russian",
    "es":"Spanish",
    "tr":"Turkish",
    "ja":"Japanese",
    "ko":"Korean",
    "hu":"Hungarian",
    "hi":"Hindi"
}

official_model_list = ["v2.0.0","v2.0.1","v2.0.2","v2.0.3","main"]
official_model_list_v2 = ["2.0.0","2.0.1","2.0.2","2.0.3"]

reversed_supported_languages = {name: code for code, name in supported_languages.items()}

class TTSWrapper:
    def __init__(self,output_folder = "./output", speaker_folder="./speakers",lowvram = False,model_source = "local",model_version = "2.0.2",device = "cuda",deepspeed = False,enable_cache_results = True):

        self.cuda = device # If the user has chosen what to use, we rewrite the value to the value we want to use
        self.device = 'cpu' if lowvram else (self.cuda if torch.cuda.is_available() else "cpu")
        self.lowvram = lowvram  # Store whether we want to run in low VRAM mode.

        self.latents_cache = {} 

        self.model_source = model_source
        self.model_version = model_version

        self.deepspeed = deepspeed

        self.speaker_folder = speaker_folder
        self.output_folder = output_folder

        self.create_directories()
        check_tts_version()

        self.enable_cache_results = enable_cache_results
        self.cache_file_path = os.path.join(output_folder, "cache.json")

        if self.enable_cache_results:
            # Reset the contents of the cache file at each initialization.
            with open(self.cache_file_path, 'w') as cache_file:
                json.dump({}, cache_file)
    # HELP FUNC
    def check_model_version_old_format(self,model_version):
        if model_version in official_model_list_v2:
            return "v"+model_version
        return model_version

    # CACHE FUNCS
    def check_cache(self, text_params):
        if not self.enable_cache_results:
            return None

        try:
            with open(self.cache_file_path) as cache_file:
                cache_data = json.load(cache_file)

            for entry in cache_data.values():
                if all(entry[key] == value for key, value in text_params.items()):
                    return entry['file_name']

            return None

        except FileNotFoundError:
            return None

    def update_cache(self, text_params, file_name):
        if not self.enable_cache_results:
            return None
        try:
            # Check if the file exists and its contents before downloading.
            if os.path.exists(self.cache_file_path) and os.path.getsize(self.cache_file_path) > 0:
                with open(self.cache_file_path, 'r') as cache_file:
                    cache_data = json.load(cache_file)
            else:
                cache_data = {}  # Initialization of an empty dictionary if the file does not exist or is empty.

            timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
            cache_data[timestamp] = {**text_params, 'file_name': file_name}

            with open(self.cache_file_path, 'w') as cache_file:
                json.dump(cache_data, cache_file)

            logger.info("Cache updated successfully.")
        except IOError as e:
            print("I/O error occurred while updating the cache: ", str(e))
        except json.JSONDecodeError as e:
            print("JSON decode error occurred while updating the cache: ", str(e))
            
    # LOAD FUNCS
    def load_model(self):
        if self.model_source == "api":
            self.model = TTS("tts_models/multilingual/multi-dataset/xtts_v2")

        if self.model_source == "apiManual":
            this_dir = Path(__file__).parent.resolve()
            download_model(this_dir,self.model_version)

            this_dir = Path(__file__).parent.resolve()
            config_path = this_dir / 'models' / f'{self.model_version}' / 'config.json'
            checkpoint_dir = this_dir / 'models' / f'{self.model_version}'

            self.model = TTS(model_path=checkpoint_dir,config_path=config_path).to(self.device)

        if self.model_source != "api" and self.model_source != "apiManual":
          is_official_model = False
        #   Check if the model version is in the official list
          if self.model_version in official_model_list:
            is_official_model = True

          self.load_local_model(load = is_official_model)
          if self.lowvram == False:
            # Due to the fact that we create latents on the cpu and load them from the cuda we get an error
            logger.info("Pre-create latents for all current speakers")
            self.create_latents_for_all() 
          
        logger.info("Model successfully loaded ")
    
    def load_local_model(self,load=True):
        this_dir = Path(__file__).parent.resolve()

        if(load == True):
          download_model(this_dir,self.model_version)

        config = XttsConfig()
        config_path = this_dir / 'models' / f'{self.model_version}' / 'config.json'
        checkpoint_dir = this_dir / 'models' / f'{self.model_version}'

        config.load_json(str(config_path))
        
        self.model = Xtts.init_from_config(config)
        self.model.load_checkpoint(config,use_deepspeed=self.deepspeed, checkpoint_dir=str(checkpoint_dir))
        self.model.to(self.device)

    # LOWVRAM FUNCS
    def switch_model_device(self):
        # We check for lowram and the existence of cuda
        if self.lowvram and torch.cuda.is_available() and self.cuda != "cpu":
            with torch.no_grad():
                if self.device == self.cuda:
                    self.device = "cpu"
                else:
                    self.device = self.cuda

                self.model.to(self.device)

            if self.device == 'cpu':
                # Clearing the cache to free up VRAM
                torch.cuda.empty_cache()

    # SPEAKER FUNCS
    def get_or_create_latents(self, speaker_name, speaker_wav):
        if speaker_name not in self.latents_cache:
            logger.info(f"creating latents for {speaker_name}: {speaker_wav}")
            gpt_cond_latent, speaker_embedding = self.model.get_conditioning_latents(speaker_wav)
            self.latents_cache[speaker_name] = (gpt_cond_latent, speaker_embedding)
        return self.latents_cache[speaker_name]

    def create_latents_for_all(self):
        speakers_list = self._get_speakers()

        for speaker in speakers_list:
            self.get_or_create_latents(speaker['speaker_name'],speaker['speaker_wav'])

        logger.info(f"Latents created for all {len(speakers_list)} speakers.")

    # DIRICTORIES FUNCS
    def create_directories(self):
        directories = [self.output_folder, self.speaker_folder]

        for sanctuary in directories:
            # List of folders to be checked for existence
            absolute_path = os.path.abspath(os.path.normpath(sanctuary))

            if not os.path.exists(absolute_path):
                # If the folder does not exist, create it
                os.makedirs(absolute_path)
                logger.info(f"Folder in the path {absolute_path} has been created")

    def set_speaker_folder(self, folder):
        if os.path.exists(folder) and os.path.isdir(folder):
            self.speaker_folder = folder
            self.create_directories()
            logger.info(f"Speaker folder is set to {folder}")
        else:
            raise ValueError("Provided path is not a valid directory")

    def set_out_folder(self, folder):
        if os.path.exists(folder) and os.path.isdir(folder):
            self.output_folder = folder
            self.create_directories()
            logger.info(f"Output folder is set to {folder}")
        else:
            raise ValueError("Provided path is not a valid directory")

    # GET FUNCS
    def get_wav_files(self, directory):
        """ Finds all the wav files in a directory. """
        wav_files = [f for f in os.listdir(directory) if f.endswith('.wav')]
        return wav_files

    def _get_speakers(self):
        """
        Gets info on all the speakers.

        Returns a list of {speaker_name,speaker_wav,preview} dicts
        """
        speakers = []
        for f in os.listdir(self.speaker_folder):
            full_path = os.path.join(self.speaker_folder,f)
            if os.path.isdir(full_path):
                # multi-sample voice
                subdir_files = self.get_wav_files(full_path) 
                if len(subdir_files) == 0:
                    # no wav files in directory
                    continue

                speaker_name = f
                speaker_wav = [os.path.join(self.speaker_folder,f,s) for s in subdir_files]
                # use the first file found as the preview
                preview = os.path.join(f,subdir_files[0])
                speakers.append({
                        'speaker_name': speaker_name,
                        'speaker_wav': speaker_wav,
                        'preview': preview
                        })

            elif f.endswith('.wav'):
                speaker_name = os.path.splitext(f)[0]
                speaker_wav = full_path 
                preview = f
                speakers.append({
                        'speaker_name': speaker_name,
                        'speaker_wav': speaker_wav,
                        'preview': preview
                        })
        return speakers

    def get_speakers(self):
        """ Gets available speakers """
        speakers = [ s['speaker_name'] for s in self._get_speakers() ] 
        return speakers

    def get_local_ip(self):
      try:
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
            s.connect(('10.255.255.255', 1))
            IP = s.getsockname()[0] 
      except Exception as e:
        print(f"Failed to obtain a local IP: {e}")
        return None
      return IP

    # Special format for SillyTavern
    def get_speakers_special(self):
        BASE_URL = os.getenv('BASE_URL', '127.0.0.1:8020')
        BASE_HOST = os.getenv('BASE_HOST', '127.0.0.1')
        BASE_PORT = os.getenv('BASE_PORT', '8020')
        TUNNEL_URL = os.getenv('TUNNEL_URL', '')

        is_local_host = BASE_HOST == '127.0.0.1' or BASE_HOST == "localhost"

        if TUNNEL_URL == "" and not is_local_host:
            TUNNEL_URL = f"http://{self.get_local_ip()}:{BASE_PORT}"
        speakers_special = []

        speakers = self._get_speakers()

        for speaker in speakers:
            if TUNNEL_URL == "":
                preview_url = f"{BASE_URL}/sample/{speaker['preview']}"
            else:
                preview_url = f"{TUNNEL_URL}/sample/{speaker['preview']}"

            speaker_special = {
                    'name': speaker['speaker_name'],
                    'voice_id': speaker['speaker_name'],
                    'preview_url': preview_url
            }
            speakers_special.append(speaker_special)

        return speakers_special


    def list_languages(self):
        return reversed_supported_languages

    # GENERATION FUNCS
    def clean_text(self,text):
        # Remove asterisks and line breaks
        text = re.sub(r'[\*\r\n]', '', text)
        # Replace double quotes with single quotes and correct punctuation around quotes
        text = re.sub(r'"\s?(.*?)\s?"', r"'\1'", text)
        return text

    def local_generation(self,text,speaker_name,speaker_wav,language,output_file):
        # Log time
        generate_start_time = time.time()  # Record the start time of loading the model

        gpt_cond_latent, speaker_embedding = self.get_or_create_latents(speaker_name, speaker_wav)

        out = self.model.inference(
            text,
            language,
            gpt_cond_latent=gpt_cond_latent,
            speaker_embedding=speaker_embedding,
            temperature=0.75,
            length_penalty=1.0,
            repetition_penalty=5.0,
            top_k=50,
            top_p=0.85,
            enable_text_splitting=True
        )

        torchaudio.save(output_file, torch.tensor(out["wav"]).unsqueeze(0), 24000)

        generate_end_time = time.time()  # Record the time to generate TTS
        generate_elapsed_time = generate_end_time - generate_start_time

        logger.info(f"Processing time: {generate_elapsed_time:.2f} seconds.")

    def api_generation(self,text,speaker_wav,language,output_file):
        self.model.tts_to_file(
                text=text,
                speaker_wav=speaker_wav,
                language=language,
                file_path=output_file,
        )

    def get_speaker_wav(self, speaker_name_or_path):
        """ Gets the speaker_wav(s) for a given speaker name. """
        if speaker_name_or_path.endswith('.wav'):
            # it's a file name
            if os.path.isabs(speaker_name_or_path):
                # absolute path; nothing to do
                speaker_wav = speaker_name_or_path
            else:
                # make it a full path
                speaker_wav = os.path.join(self.speaker_folder, speaker_name_or_path)
        else:
            # it's a speaker name
            full_path = os.path.join(self.speaker_folder, speaker_name_or_path) 
            wav_file = f"{full_path}.wav"
            if os.path.isdir(full_path):
                # multi-sample speaker
                speaker_wav = [ os.path.join(full_path,wav) for wav in self.get_wav_files(full_path) ]
                if len(speaker_wav) == 0:
                    raise ValueError(f"no wav files found in {full_path}")
            elif os.path.isfile(wav_file):
                speaker_wav = wav_file
            else:
                raise ValueError(f"Speaker {speaker_name_or_path} not found.")

        return speaker_wav


    # MAIN FUNC
    def process_tts_to_file(self, text, speaker_name_or_path, language, file_name_or_path="out.wav"):
        try:
            speaker_wav = self.get_speaker_wav(speaker_name_or_path)
            # Determine output path based on whether a full path or a file name was provided
            if os.path.isabs(file_name_or_path):
                # An absolute path was provided by user; use as is.
                output_file = file_name_or_path
            else:
                # Only a filename was provided; prepend with output folder.
                output_file = os.path.join(self.output_folder, file_name_or_path)

            # Check if 'text' is a valid path to a '.txt' file.
            if os.path.isfile(text) and text.lower().endswith('.txt'):
                with open(text, 'r', encoding='utf-8') as f:
                    text = f.read()

            # Generate unic name for cached result
            if self.enable_cache_results:
                timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
                file_name_or_path = timestamp + "_cache_" + file_name_or_path
                output_file = os.path.join(self.output_folder, file_name_or_path)

            # Replace double quotes with single, asterisks, carriage returns, and line feeds
            clear_text = self.clean_text(text)

            # Generate a dictionary of the parameters to use for caching.
            text_params = {
              'text': clear_text,
              'speaker_name_or_path': speaker_name_or_path,
              'language': language
            }

            # Check if results are already cached.
            cached_result = self.check_cache(text_params)

            if cached_result is not None:
                logger.info("Using cached result.")
                return cached_result  # Return the path to the cached result.

            self.switch_model_device() # Load to CUDA if lowram ON

            # Define generation if model via api or locally
            if self.model_source == "local":
                self.local_generation(clear_text,speaker_name_or_path,speaker_wav,language,output_file)
            else:
                self.api_generation(clear_text,speaker_wav,language,output_file)
            
            self.switch_model_device() # Unload to CPU if lowram ON

            # After generation completes successfully...
            self.update_cache(text_params,output_file)
            return output_file

        except Exception as e:
            raise e  # Propagate exceptions for endpoint handling.

        



        
