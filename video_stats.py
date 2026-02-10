import requests
import json

import os

from dotenv import load_dotenv

load_dotenv(dotenv_path="C:/Courses/YT_ELT/venv/.env")

API_KEY = os.getenv("API_KEY")
#print(API_KEY)
CHANNEL_HANDLE = "MrBeast"
maxResults = 50


def get_playlist_id():
    try:
        url = f"https://youtube.googleapis.com/youtube/v3/channels?part=contentDetails&forHandle={CHANNEL_HANDLE}&key={API_KEY}"
        #url = "https://youtube.googleapis.com/youtube/v3/channels?part=contentDetails&forHandle=MrBeast&key=..."
        response = requests.get(url)
        #print(response)
        response.raise_for_status()

        data = response.json()
        #print(json.dumps(data, indent=4))

        # data["items"][0]["contentDetails"]["relatedPlaylists"]["uploads"]

        channel_items = data["items"][0]
        channel_playlist_id = channel_items["contentDetails"]["relatedPlaylists"]["uploads"]
        print(channel_playlist_id)
        return(channel_playlist_id)
    except requests.exceptions.RequestException as e:
        raise e
    


def get_video_ids(playlist_id):
    video_ids = []
    pageToken = None
    
    #base_url = f"https://youtube.googleapis.com/youtube/v3/channels?part=contentDetails&id={playlist_id}&maxResults={maxResults}&key={API_KEY}"
    base_url = f"https://youtube.googleapis.com/youtube/v3/playlistItems?part=contentDetails&maxResults={maxResults}&playlistId={playlist_id}&key={API_KEY}"

    print("get_video_ids is running")
    
    try:
        while True:
            url = base_url
            if pageToken:
                url+=f"&pageToken={pageToken}"
            response = requests.get(url)
            response.raise_for_status()
            data = response.json()
            
            for item in data.get("items", []):
                video_id = item["contentDetails"]["videoId"]
                video_ids.append(video_id)
                
            pageToken = data.get("nextPageToken")
            
            if not pageToken:
                break        

        return video_ids
    except requests.exceptions.RequestException as e:
        raise e
    

if __name__ == "__main__":
    print("get_playlist_id will be executed")
    playlist_id = get_playlist_id()     
    print("playlist_id will be executed")
    get_video_ids(playlist_id)
else:    
    print("get_playlist_id won't be executed")          
