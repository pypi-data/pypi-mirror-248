"""Tools for the subtitling pipeline"""

import logging
import os
from typing import Optional
from typing import Union

from .language_identification import extract_subclip
from .language_identification import identify_language
from .save_subtitles import generate_txt_path
from .save_subtitles import save_to_srt_file
from .save_subtitles import save_to_txt_file
from .utils import convert_video_to_audio_ffmpeg
from .utils import download_from_youtube
from .whisperx_transcribe import get_phrase_level_timestamps
from .whisperx_transcribe import get_word_level_timestamps


def generate_subtitles_for_youtube(
    youtube_url: str, language: Optional[str] = None, output_dir: Optional[Union[str, os.PathLike]] = None
) -> dict:
    """A quick implementation for youtube videos of the universal subtitler.

    Parameters
    ----------
    youtube_url : str
        Youtube video URL
    language : Optional[str], optional
        language ISO code of the video. If unspecified, use automatic language detection, by default None
    output_dir : Optional[Union[str, os.PathLike]], optional
        Directory for saving the video and subtitles. If unspecified, use the current working directory, by default None

    Returns
    -------
    dict
        A dictionary containing the locations of the downloaded video, subtitles, and text file
    """

    # Configure logging settings
    logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

    logging.info("Downloading youtube Video")
    video_filepath = download_from_youtube(youtube_url)

    logging.info("Extracting audio from video")
    audio_filepath = convert_video_to_audio_ffmpeg(video_filepath=video_filepath, output_ext="wav")

    if language is None:
        logging.info("Detecting video language with Speechbrain AI")

        audio_subclip_filepath = extract_subclip(audio_filepath=audio_filepath)
        detected_language = identify_language(audio_filepath=audio_subclip_filepath)

        logging.info(f"{detected_language} - Detected language")
        language = detected_language

    logging.info("Captioning at the phrase level with Whisper")
    phrase_level_transcription = get_phrase_level_timestamps(audio_filename=audio_filepath, language=language, batch_size=16)
    phrase_level_transcription["language"] = language

    logging.info("Captioning at the word level with WhisperX")
    word_level_transcription = get_word_level_timestamps(
        audio_filename=audio_filepath, phrase_level_transcription=phrase_level_transcription, language=language
    )
    word_level_transcription["language"] = language

    logging.info("Saving subtitles")
    text_filepath = generate_txt_path(input_file_path=video_filepath)
    subtitles_filepath = generate_txt_path(input_file_path=video_filepath, extension="srt")

    save_to_srt_file(subtitles_path=subtitles_filepath, annotated_transcription_result=word_level_transcription)
    save_to_txt_file(txt_path=text_filepath, annotated_transcription_result=word_level_transcription)

    logging.info("Finished subtitling!")

    subtitling_result = {"video": video_filepath, "subtitles": subtitles_filepath, "text": text_filepath, "language": language}
    return subtitling_result
