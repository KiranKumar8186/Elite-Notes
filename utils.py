import os
import re
import requests
##--------------------------------------------------------------------------------------------------------------------------------------------------------------------
from pytube import YouTube
import streamlit as st
import whisper

from transformers import pipeline

MAX_VIDEO_LENGTH = 30*60

##----------------------------------{Youtube Part}----------------------------------------------------------------------------------------------------------------------------------

@st.cache(show_spinner=False)
def load_whisper_model():
    model = whisper.load_model('tiny', device='cpu')
    return model

##--------------------------------------------------------------------------------------------------------------------------------------------------------------------

def valid_url(url):
 return re.search(r'((http(s)?:\/\/)?)(www\.)?((youtube\.com\/)|(youtu.be\/))[\S]+', url)

##--------------------------------------------------------------------------------------------------------------------------------------------------------------------

def get_video_duration_from_youtube_url(url):
    
    _get_audio_from_youtube_url(url)
    st.audio('downloads','audio.mp3')
    
    yt = YouTube(url)
    return yt.length
    
##--------------------------------------------------------------------------------------------------------------------------------------------------------------------

def _get_audio_from_youtube_url(url):
    yt = YouTube(url)
    if not os.path.exists('downloads'):
        os.makedirs('downloads')
    yt.streams.filter(only_audio=True).first().download(filename=os.path.join('downloads','audio.mp3'))

##--------------------------------------------------------------------------------------------------------------------------------------------------------------------

def _whisper_result_to_srt(result):
    text = []
    for i,s in enumerate(result['segments']):
        time_start = s['start']
        hours, minutes, seconds = int(time_start/3600), (time_start/60) % 60, (time_start) % 60
        timestamp_start = "%02d:%02d:%06.3f" % (hours, minutes, seconds)
        timestamp_start = timestamp_start.replace('.',',')     
        time_end = s['end']
        hours, minutes, seconds = int(time_end/3600), (time_end/60) % 60, (time_end) % 60
        timestamp_end = "%02d:%02d:%06.3f" % (hours, minutes, seconds)
        timestamp_end = timestamp_end.replace('.',',')        
        text.append(timestamp_start + "➡" + timestamp_end)
        text.append(s['text'].strip() + "\n")            
    return "\n".join(text)

##--------------------------------------------------------------------------------------------------------------------------------------------------------------------

@st.experimental_memo(show_spinner=False, max_entries=1)
def transcribe_URL(_model, url):
    
    url_type = verify_url(url)
    
    if url_type == "youtube":
        _get_audio_from_youtube_url(url)
        options = whisper.DecodingOptions(language='en', fp16=False)
        result = _model.transcribe(os.path.join('downloads','audio.mp3'), **options.__dict__)
        result['srt'] = _whisper_result_to_srt(result)
        return result
    ##--------------------------------------------------------------------------------------------------------------------------------------------------------------------
    elif url_type == "drive":
        get_audio_from_GDrive_url(url)
        options = whisper.DecodingOptions(language='en', fp16=False)
        result = _model.transcribe(os.path.join('downloads', "audio1.mp3"), **options.__dict__)
        result['srt'] = _whisper_result_to_srt(result)
        return result

##--------------------------------------------------------------------------------------------------------------------------------------------------------------------

@st.cache(persist=True,allow_output_mutation=False,show_spinner=True,suppress_st_warning=True)

def verify_url(url):
    youtube_pattern = re.compile(r'^(https?://)?(www\.)?(youtube\.com|youtu\.?be)/.+$')
    drive_pattern = re.compile(r'^(https?://)?(drive\.google\.com)/.+$')

    if re.match(youtube_pattern, url):
        return "youtube"
    elif re.match(drive_pattern, url):
        return "drive"
    else:
        return "invalid"
    
##----------------------------------{Google Drive Part}----------------------------------------------------------------------------------------------------------------------------------

file_name = None

def get_audio_from_GDrive_url(url):
    global file_name
    parts = url.split("/")
    if len(parts) < 3:
        st.error("❎ Invalid URL")
        return
    file_id = parts[-2]
    file_name = "downloads/audio1.mp3"
    # destination = "audio.mp4"
    download_file_from_google_drive(file_id, file_name)

##--------------------------------------------------------------------------------------------------------------------------------------------------------------------

def download_file_from_google_drive(id, destination):
        URL = "https://drive.google.com/uc?id=" + id
        response = requests.get(URL)
        open((destination), "wb").write(response.content)
        
##--------------------------------------------------------------------------------------------------------------------------------------------------------------------

def Load_Video():
    global file_name
    st.success("File downloaded!")
    st.sidebar.header("Your 🎵 Audio or 🎥 Video...")
    st.sidebar.video(file_name)

##-------------------------------------------------{Upload File Part}-------------------------------------------------------------------------------------------------------------------

def get_audio_from_Upload(uploaded_file): 
    if uploaded_file is not None:
        upload_path = "downloads/"
        with open(os.path.join(upload_path, uploaded_file.name),"wb") as f:
            f.write((uploaded_file).getbuffer())
    
@st.experimental_memo(show_spinner=False, max_entries=1)
def transcribe_audio(_model, uploaded_file):
    get_audio_from_Upload(uploaded_file)
    options = whisper.DecodingOptions(language='en', fp16=False)
    result = _model.transcribe(os.path.join("downloads", uploaded_file.name), **options.__dict__)
    result['srt'] = _whisper_result_to_srt(result)
    return result

#--------------------------------------------------------------------------------------------------------------------------------------------#        
#                                                         Summarization                                                                      #
#--------------------------------------------------------------------------------------------------------------------------------------------#

def point_wise_summary(data):
    summarizer = pipeline("summarization")
    summary = summarizer(data, max_length=1050, min_length=30)
    summary_text = summary[0]["summary_text"]
    points = summary_text.split(".")
    return [point for point in points]
