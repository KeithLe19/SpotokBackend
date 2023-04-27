import openai
import json
import os
from dotenv import load_dotenv

from app.managers.MessageManager import MessageManager


class OpenAIManager:
    def __init__(self) -> None:
        self.openAIManager = openai
        self.openAIManager.api_key = os.getenv("OPENAI_KEY")
        
        self.RECOMMENDATIONPROMPT = ". Give me 1 song sung by the first recommended artist. Provide the information in the form of a JSON with a genre as a key and the value is the recommended artist. Add the recommended song at the end of the JSON with the key as 'song' and the value as the recommended song."
        
        self.TIMESTAMPPROMPT = " is a JSON where the key is a song and the value are the artists who sang that song. Add a second key-value pair to each song where the key is 'catch' and the value is the time in the song that is the catchiest, memorable, or most replayed. If you don't know the song, set the value to -1. Only return the JSON."
    
        
    def getInitialRecommendation(self, genres) :
        # Set up prompt
        prompt = "Give me 1 artist recommendation for the following genres: " + genres[0][1] + " and " + genres[1][1] + self.RECOMMENDATIONPROMPT
        try:
            response = self.openAIManager.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                        {"role": "user", "content": prompt}
                    ]
                )
            response_json = json.loads(response.choices[0].message.content)
            return response_json
        except:
            return None
        
    def getSongDictGptJson(self, spotifyRecommendations):
        songDict = {}
        gptDict = {}

        for i, track in enumerate(spotifyRecommendations['tracks']):
            song_entry = {
                'songName': track['name'],
                'songID': track['id'],
                'artists': '',
                'artistIDs': '',
                'genres': '', #get genres of artists
                'catchyTimestamp': -1
            }

            for j, artist in enumerate(track['artists']):
                if j == 0:
                    song_entry['artists'] += artist['name']
                    song_entry['artistIDs'] += artist['id']
                    gptDict[track['name']] = artist['name']
                else:
                    song_entry['artists'] += ','
                    song_entry['artists'] += artist['name']
                    song_entry['artistIDs'] += ','
                    song_entry['artistIDs'] += artist['id']
                    gptDict[track['name']] += ", " + artist['name']

            songDict[i] = song_entry
        gptJSON = json.dumps(gptDict)
        return songDict, gptJSON
        
    def getTimeStamps(self, spotifyRecommendations):
        
        # Split up spotify recommendation into a dict and json
        songDict, gptJSON = self.getSongDictGptJson(spotifyRecommendations=spotifyRecommendations)
        
        # Set up ChatGPT prompt
        prompt = gptJSON + self.TIMESTAMPPROMPT
        try:
            final_response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                    {"role": "user", "content": prompt}
                ]
            )
            finJSON = json.loads(final_response.choices[0].message.content)
            for ct, song in enumerate(finJSON):
                songDict[ct]['catchyTimestamp'] = finJSON[song]['catch']
            return songDict
        except:
            return None
