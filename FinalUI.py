import os
import streamlit as st
##--------------------------------------------------------------------------------------------------------------------------------------------------------------------
st.set_page_config(
    page_title="Elite Notes",
    page_icon="📖",
    layout="wide",
)
#-------------------------------------------------------------------------------------------------------------------------------------------------------------------------
                                    ## Drive Libraries
import requests
import whisper
import time
from pydub import AudioSegment
#--------------------------------------------------------------------------------------------
                                    ## Youtube Libraries
import time
from utils import *
##----------------------------------------------------------------## Saving Files Path--------------------------------------------------------------------------------
upload_path = "uploads/"
download_path = "downloads/"
transcript_path = "transcripts/"

##--------------------------------------------------------------------------------------------------------------------------------------------------------------------

st.markdown("<h1 style='text-align: center; color: red; font-size: 55px;'>Elite Notes</h1>", unsafe_allow_html=True)
st.markdown("<h2 style='padding: 10px; text-align: center; color: lightblack; font-size: 15px; margin : 15px auto;'>At EliteNotes, we believe everyone is a note-taker because every conversation matters</h1>", unsafe_allow_html=True)
st.markdown("---")
st.markdown("<h3 style= 'color: red;'>Audio Transcribe</h3>", unsafe_allow_html=True)

col1, col2 = st.columns(2)

uploaded_file = col1.file_uploader("Upload Audio File :", type=["wav","mp3","ogg","wma","aac","flac","mp4","flv","m4a"])
# uploaded_file = st.file_uploader("Upload audio file", type=["wav","mp3","ogg","wma","aac","flac","mp4","flv","m4a"])
# # st.audio(uploaded_file)  
st.markdown("---")
##--------------------------------------------------------------------------------------------------------------------------------------------------------------------

def main():
    model =  load_whisper_model() 
    if uploaded_file:
        getting_audio = get_audio_from_Upload(uploaded_file)        
        st.sidebar.header("Your 🎵 Audio or 🎥 Video...") 
        st.sidebar.write("`File downloaded!`")     
        st.sidebar.audio(uploaded_file)
#         st.sidebar.markdown("<h1 style='text-align: left; color: red; font-size: 15px;'>Generate_Transcript</h1>", unsafe_allow_html=True)
        transcribe_button = st.sidebar.checkbox("`Generate Transcript`")
        st.sidebar.markdown("---")
        #-----------------------------------------------------------------## Transcribing the audio file (refer utils.py) ##------------------------------------              
        if transcribe_button:
            ##---------------------------------------------------------------------
            start_time = time.time()
            ##---------------------------------------------------------------------
            with st.spinner("Transcribing audio..."):
                result = None
                try:
                    result = transcribe_audio(model, uploaded_file)
                except RuntimeError:
                    result = None
                    st.warning("Oops! Someone else is using the model right now to transcribe another video. Please try again in a few seconds.")
            ##---------------------------------------------------------------------                    
            end_time = time.time()
            time_elapsed = end_time - start_time
            st.sidebar.write("Time elapsed:", round(time_elapsed,2), "seconds")
            ##---------------------------------------------------------------------
            #------------------------------## getting transcript Text and Downlaoding Text file into .txt or .srt (process refer to utils.py) ##----------------                                                       
                
            if result:
                st.sidebar.header("Select Option To Download The Transcript :")
                file_extension_1 = st.sidebar.selectbox("Select Here...", ["TXT (.txt)", "SubRip (.srt)"], key='selectbox_1')
                st.sidebar.write("You selected: ", file_extension_1)
                st.markdown("---")                        
                # file_extension = st.selectbox("Select File Type To Download Transcript :", options=["TXT (.txt)", "SubRip (.srt)"])
                if file_extension_1 == "TXT (.txt)":
                    file_extension_1 = "txt"
                    data = result['text'].strip()
                elif file_extension_1 == "SubRip (.srt)":
                    file_extension_1 = "srt"
                    data = result['srt']    
                
                
                #---------------------------------------## Printing the Transcript and dtecting the language (process refer to utils.py)------------------------                             
                
                det_L = st.success("Detected language: {}".format(result['language']))
                data = st.text_area("Transcription of `" + uploaded_file.name + "` :-", value= data, height=350)
    
                #-------------------------------------------## Downloading transcripts into .txt or .srt------------------------------------------------------------    
                                                            
                st.download_button("Download", data=data, file_name="Transcript.{}".format(file_extension_1))
                st.markdown("---")
if __name__ == "__main__":
        main()
#---------------------------------------------------------------------------------------------------------------------------------------------------------------#        
#                                                                                                                                                               #   
#                                   Uploading URL and Verifying whether it is a Youtube's URL or GDrive's URL##                                                 #
#                                                                                                                                                               #
#---------------------------------------------------------------------------------------------------------------------------------------------------------------#

# col2.markdown("<h1 style='text-align: center; color: red; font-size: 10px;'>[or]</h1>", unsafe_allow_html=True)

#---------------------------------------------------------------------------------------------------------------------------------------------------------------#
url = col2.text_input("Enter the URL: ")
col2.warning("Make sure that URL can access anyone...")
col2.button("Submit")
url_type = verify_url(url)

#------------------------------------------------------------## if it is a Youtube URL ##----------------------------------------------------------------------------
if url_type == "youtube":
    def main():       
##-----------------------------------------------------## Load Whisper model ##------------------------------------------------------------------------------
        model =  load_whisper_model()    
#---------------------------------------------------- # Check if the input url is a valid YouTube url (refer utils.py) ##------------------------------------
        if url:          
            right_url = valid_url(url)
            if right_url:  
                st.sidebar.header("Your 🎦 Youtube Video...")
                if get_video_duration_from_youtube_url(url) <= MAX_VIDEO_LENGTH: 
                    st.sidebar.markdown("---")
                    st.sidebar.video(url)
#----------------------------------------------------------# Transcribe checkbox-----------------------------------------------------------------
                    st.sidebar.markdown("---")
#                     st.sidebar.markdown("<h1 style='text-align: left; color: red; font-size: 15px;'></h1>", unsafe_allow_html=True)
                    transcribe_cb = st.sidebar.checkbox("`Generate YouTube Transcript`")                    
#-----------------------------------------------------------------## Transcribing the audio file (refer utils.py) ##-----------------------------
                    if transcribe_cb:
                        ##---------------------------------------------------------------------
                        start_time = time.time()
                        ##---------------------------------------------------------------------
            
                        with st.spinner("Transcribing audio..."):
                            result = None
                            try:
                                result = transcribe_URL(model, url)
                            except RuntimeError:
                                result = None
                                st.warning("Oops! Someone else is using the model right now to transcribe another video. Please try again in a few seconds.")

                        ##---------------------------------------------------------------------                    
                        end_time = time.time()
                        time_elapsed = end_time - start_time
                        st.sidebar.write("Time elapsed:", round(time_elapsed,2), "seconds")        
                        #------------------------------## Result Text and Downlaoding Text file into .txt or .srt (process refer to utils.py) ##---------------------                                                                               
                        if result:
                            st.sidebar.header("Select Option To Download The Transcript :")
                            file_extension_2 = st.sidebar.selectbox("Select Here...", ["TXT (.txt)", "SubRip (.srt)"], key='selectbox_2')
                            st.sidebar.write("You selected: ", file_extension_2)
                            if file_extension_2 == "TXT (.txt)":
                                file_extension_2 = "txt"
                                data = result['text'].strip()
                            elif file_extension_2 == "SubRip (.srt)":
                                file_extension_2 = "srt"
                                data = result['srt']                           
#---------------------------------------## Printing the Transcript and dtecting the language (process refer to utils.py)-----------------                                                        
                            det_L = st.success("Detected language: {}".format(result['language']))
                            data = st.text_area("Transcript :", value= data, height=350)
#--------------------------------------------------------------## Downloading transcripts into .txt or .srt----------------------------------                                                                          
                            st.download_button("Download", data=data, file_name="Transcript.{}".format(file_extension_2))
#------------------------------------------------------------Drive URL----------------------------------------------------------------------------------------------
                else:
                    st.warning("Sorry, the video has to be shorter than or equal to eight minutes.")
            else:
                st.warning("❎ Invalid YouTube URL.")
    if __name__ == "__main__":
        main()
#------------------------------------------------------------Drive URL----------------------------------------------------------------------------------------------
elif url_type == "drive":
    def main():
        with st.spinner("Loading Whisper model..."):
            model =  load_whisper_model()
        #----------------------------------- ## input url, downloading and display the video or audio (refer utils.py) ##-------------------------------------------
        if url:
            get_GDrive_file = get_audio_from_GDrive_url(url)
            load_gdrive_file = Load_Video()
            st.markdown("<h1 style='text-align: left; color: red; font-size: 15px;'>Transcribe</h1>", unsafe_allow_html=True)
            transcribe_cb = st.checkbox("🎤")
            #-----------------------------------------------------------------## Transcribing the audio file (refer utils.py) ##------------------------------------           
            if transcribe_cb:
                ##---------------------------------------------------------------------
                start_time = time.time()
                ##---------------------------------------------------------------------
            
                with st.spinner("Transcribing audio..."):
                    result = None
                    try:
                        result = transcribe_URL(model, url)
                    except RuntimeError:
                        result = None
                        st.warning("Oops! Someone else is using the model right now to transcribe another video. Please try again in a few seconds.")
                
                ##---------------------------------------------------------------------                    
                end_time = time.time()
                time_elapsed = end_time - start_time
                st.write("Time elapsed:", round(time_elapsed,2), "seconds")
                ##---------------------------------------------------------------------        
                #------------------------------## getting transcript Text and Downlaoding Text file into .txt or .srt (process refer to utils.py) ##----------------                                                       
                
                if result:
                    st.sidebar.header("Select Option To Download The Transcript :")
                    file_extension_3 = st.sidebar.selectbox("Select Here...", ["TXT (.txt)", "SubRip (.srt)"], key='selectbox_3')
                    st.sidebar.write("You selected: ", file_extension_3)
                                            
                    # file_extension = st.selectbox("Select File Type To Download Transcript :", options=["TXT (.txt)", "SubRip (.srt)"])
                    if file_extension_3 == "TXT (.txt)":
                        file_extension_3 = "txt"
                        data = result['text'].strip()
                    elif file_extension_3 == "SubRip (.srt)":
                        file_extension_3 = "srt"
                        data = result['srt']                           
                   
                    #---------------------------------------## Printing the Transcript and dtecting the language (process refer to utils.py)--------------------------                             
                  
                    det_L = st.success("Detected language: {}".format(result['language']))
                    data = st.text_area("Transcript :", value= data, height=350)
               
                #-------------------------------------------## Downloading transcripts into .txt or .srt--------------------------------------------------------------    
                                                             
                    st.download_button("Download", data=data, file_name="Transcript.{}".format(file_extension_3))
               
##--------------------------------------------------------------------------------------------------------------------------------------------------------------------
        else:
            st.warning("Sorry, the video has to be shorter than or equal to eight minutes.")

    if __name__ == "__main__":
        main()
else:
    print("Invalid URL.")
