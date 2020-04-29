import os
import sys
import json
import tkinter as tk
from tkinter import ttk
from tkinter import *
import PIL
from PIL import Image
from PIL import ImageTk
from collections import Counter 
import math, copy, random, decimal
import spotipy
import spotipy.util as util
import requests
from json.decoder import JSONDecodeError

#from https://www.cs.cmu.edu/~112/notes/notes-variables-and-functions.html#RecommendedFunctions
def roundHalfUp(d):
    # Round to nearest with ties going away from zero.
    rounding = decimal.ROUND_HALF_UP
    # See other rounding options here:
    # https://docs.python.org/3/library/decimal.html#rounding-modes
    return int(decimal.Decimal(d).to_integral_value(rounding=rounding))

##FONTS##
largeFont = ("Verdana", 18)
smallFont = ("Verdana", 14)


class Main(tk.Tk):

    def __init__(self, *args, **kwargs):

        tk.Tk.__init__(self, *args, **kwargs)

        container = tk.Frame(self)
        style = ttk.Style()
        style.configure('TButton', font = smallFont, bg = 'blue', foreground = "black")

        self.title("Spotify Plus")
        container.pack(side="top", fill="both", expand = True)

        self.frames = {}

        for page in (StartPage, PlaylistPage, RecommendPage, QueuePage):
            frame = page(container, self)
            self.frames[page] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        #from Object Oriented Programming Crash course with Python 3 - Tkinter tutorial Python 3.4 p. 2
        #https://www.youtube.com/watch?v=A0gaXfM1UN0 

        self.show_frame(StartPage)

    def show_frame(self, cont):
        
        frame = self.frames[cont]
        frame.tkraise()

class StartPage(tk.Frame):

    def __init__(self, parent, controller):
        
        tk.Frame.__init__(self, parent)
        tk.Frame.config(self, background="black")
        
        label = tk.Label(self, text = "Welcome to Spotify Plus!", font=largeFont, background="black", foreground="white")
        label.grid(row=1, column=0, pady=20, padx=250)

        self.img = Image.open("spotify.jpg").resize((70,70))
        self.img = ImageTk.PhotoImage(self.img)
        panel = Label(self, image = self.img,  background="black")
        panel.grid(row=0, column=0, pady=10)
        
        button = ttk.Button(self, text="Create A New Playlist Mood", command=lambda: controller.show_frame(PlaylistPage))
        button.grid(row=2, column=0, pady=10)

        button2 = ttk.Button(self, text="Add Recommended Songs", command=lambda: controller.show_frame(RecommendPage))
        button2.grid(row=3, column=0, pady=10)

        button3 = ttk.Button(self, text="Add To Queue", command=lambda: controller.show_frame(QueuePage))
        button3.grid(row=4, column=0, pady=10)

    
class PlaylistPage(tk.Frame):

    def __init__(self, parent, controller):
        
        #MY ACCOUNT
        scope = 'playlist-modify-public user-top-read user-modify-playback-state'
        self.userID = "22rr3gzk75qrvzazocbv3x23q"
        self.client_id = 'e697b9036e434b4da4593d1d76181ccb'
        self.client_secret = '1dcdd21d3ddb4128ba30652370859c91'  
        self.token = util.prompt_for_user_token(self.userID, scope, client_id = self.client_id, client_secret=self.client_secret, redirect_uri='https://google.com/')

        ########### TEST ACCOUNT #############
        '''
        scope = 'playlist-modify-public user-top-read'
        self.userID = "toppingdj"
        self.client_id = 'b509698e53ff4e0f9a25b977be11d843'
        self.client_secret = '204ba9c196d943368771756878909b4f'  
        self.token = util.prompt_for_user_token(self.userID, scope, client_id = self.client_id, client_secret=self.client_secret, redirect_uri='https://google.com/')
        '''
        #######################################

        ########### INIT BUTTONS ##############
        
        tk.Frame.__init__(self, parent)
        tk.Frame.config(self, background = "black") 
        
        label = tk.Label(self, text = "Create New Playlist", font=largeFont, background="black", foreground="white")
        label.grid(row=0, column=1, pady=20)

        label = tk.Label(self, text = "Pick a genre", font=smallFont, background="black", foreground="white")
        label.grid(row=1, column=1, pady=20)

        ### SET IMAGES ###
        self.workout = Image.open("workout.jpg").resize((75,75))
        self.workoutImg = ImageTk.PhotoImage(self.workout)

        self.sad = Image.open("sad.jpg").resize((75,75))
        self.sadImg = ImageTk.PhotoImage(self.sad)

        self.happy = Image.open("happy.jpg").resize((75,75))
        self.happyImg = ImageTk.PhotoImage(self.happy)
        
        self.chill = Image.open("chill.jpg").resize((75,75))
        self.chillImg = ImageTk.PhotoImage(self.chill)

        self.artists = Image.open("artists.jpg").resize((75,75))
        self.artistsImg = ImageTk.PhotoImage(self.artists)

        self.songs = Image.open("songs.jpg").resize((75,75))
        self.songsImg = ImageTk.PhotoImage(self.songs)

        button2 = ttk.Button(self, text="Workout", image = self.workoutImg, compound = TOP, command=lambda: self.makeWorkoutPlaylist())
        button2.grid(row=2, column=0, pady=10, padx = (130, 10))

        button3 = ttk.Button(self, text="Sad", image = self.sadImg, compound = TOP, command=lambda: self.makeSadPlaylist())
        button3.grid(row=2, column=1, pady=10, padx = 10)

        button4 = ttk.Button(self, text="Happy", image = self.happyImg, compound = TOP, command=lambda: self.makeHappyPlaylist())
        button4.grid(row=2, column=2, pady=10, padx = 10)

        button5 = ttk.Button(self, text="Chill", image = self.chillImg, compound = TOP, command=lambda: self.makeChillPlaylist())
        button5.grid(row=3, column=0, pady=10, padx = (130, 10))

        button6 = ttk.Button(self, text="Top Artists Tracks", image = self.artistsImg, compound = TOP, command=lambda: self.getTopArtists())
        button6.grid(row=3, column=1, pady=10, padx = 10)

        button7 = ttk.Button(self, text="Your Top Tracks", image = self.songsImg, compound = TOP, command=lambda: self.getTopTracks())
        button7.grid(row=3, column=2, pady=10, padx = 10)

        button8 = ttk.Button(self, text="Back to Home", command=lambda: controller.show_frame(StartPage))
        button8.grid(row=4, column=1, pady=(10, 30))
        

    def createNewPlaylist(self, request_body):
        query = "https://api.spotify.com/v1/users/{}/playlists".format(self.userID)
        response = requests.post(
            query,
            data=request_body,
            headers={
                "Content-Type":"application/json",
                "Authorization":"Bearer {}".format(self.token)
            }     
        )
        response_json = response.json()
        #playlist ID
        return response_json["id"]


    def addToPlaylist(self, playlistID, uris):
        request_data = json.dumps(uris)
        query = "https://api.spotify.com/v1/playlists/{}/tracks".format(playlistID)
        repsonse = requests.post(
            query,
            data=request_data,
            headers={
                "Content-Type":"application/json",
                "Authorization":"Bearer {}".format(self.token)
            }
        )
        
    def makeWorkoutPlaylist(self):
        request_body = json.dumps({
            "name":"Workout Playlist",
            "description": "Workout jams!!!",
            "public": True
        })
    
        #POST request to create new playlist, format on base url using 
        #user's ID
        
        workoutID = self.createNewPlaylist(request_body) 

        #search top songs using keyword "workout music"
        query = "https://api.spotify.com/v1/search?q=workout%20music&type=track&market=US&limit=30"
        response = requests.get(
            query,
            headers={
                "Content-Type":"application/json",
                "Authorization":"Bearer {}".format(self.token)
            }     
        )
        response_json = response.json()
        songs = response_json["tracks"]["items"]
        workoutUris = []
        for songNum in range(len(songs)):
            workoutUris.append(songs[songNum]["uri"])
    
        self.addToPlaylist(workoutID, workoutUris)
        print("Success!")

    def makeSadPlaylist(self):
        request_body = json.dumps({
            "name":"Sad Playlist",
            "description": "Im sad boo hoo",
            "public": True
        })
        
        sadID = self.createNewPlaylist(request_body)
        query = "https://api.spotify.com/v1/search?q=sad%20music&type=track&market=US&limit=30"
        response = requests.get(
            query,
            headers={
                "Content-Type":"application/json",
                "Authorization":"Bearer {}".format(self.token)
            }     
        )
        response_json = response.json()
        songs = response_json["tracks"]["items"]
        sadUris = []
        for songNum in range(len(songs)):
            sadUris.append(songs[songNum]["uri"])
        
        self.addToPlaylist(sadID, sadUris)
        print("Success!")

    def makeHappyPlaylist(self):
        request_body = json.dumps({
            "name":"Happy Vibes",
            "description": "im happy yay!",
            "public": True
        })
    
        happyID = self.createNewPlaylist(request_body)
        
        query = "https://api.spotify.com/v1/search?q=happy&type=track&market=US&limit=30"
        response = requests.get(
            query,
            headers={
                "Content-Type":"application/json",
                "Authorization":"Bearer {}".format(self.token)
            }     
        )
        response_json = response.json()
        songs = response_json["tracks"]["items"]
        happyUris = []
        for songNum in range(len(songs)):
            happyUris.append(songs[songNum]["uri"])
            
        self.addToPlaylist(happyID, happyUris)
        print("Success!")

    def makeChillPlaylist(self):
        request_body = json.dumps({
            "name":"Chill",
            "description": "relax",
            "public": True
        })
    
        happyID = self.createNewPlaylist(request_body)
        
        query = "https://api.spotify.com/v1/search?q=relax&type=track&market=US&limit=30"
        response = requests.get(
            query,
            headers={
                "Content-Type":"application/json",
                "Authorization":"Bearer {}".format(self.token)
            }     
        )
        response_json = response.json()
        songs = response_json["tracks"]["items"]
        happyUris = []
        for songNum in range(len(songs)):
            happyUris.append(songs[songNum]["uri"])
            
        self.addToPlaylist(happyID, happyUris)
        print("Success!")

    def getTopArtists(self):
        query =  "https://api.spotify.com/v1/me/top/artists?limit=30"
        response = requests.get(
            query,
            headers={
                "Content-Type":"application/json",
                "Authorization":"Bearer {}".format(self.token)
            }     
        )
        response_json = response.json()

        topArtists = []
        topArtistsNames = []

        for artist in response_json["items"]:
            topArtists.append(artist["id"])

        for artist in response_json["items"]:
            topArtistsNames.append(artist["name"])

        print("Your top artists are: ",topArtistsNames)

        #get those artists top tracks and put them into a playlist
        #make a combined list of ALL track uris from each top artist

        allTracks = []
        for artistID in topArtists:
            query =  "https://api.spotify.com/v1/artists/{}/top-tracks?country=US".format(artistID)
            response = requests.get(
                query,
                headers={
                    "Content-Type":"application/json",
                    "Authorization":"Bearer {}".format(self.token)
                }     
            )
            response_json = response.json()
            #add each track to combined list
            for track in response_json["tracks"]:
                if track["popularity"] > 75:
                    allTracks.append(track["uri"])

        #create new playlist
        request_body = json.dumps({
            "name":"Top Artist Tracks",
            "description": "My Top Artists Songs",
            "public": True
        })
        
        #top tracks ID
        topArtistID = self.createNewPlaylist(request_body)

        #add all the top tracks to the playlist
        self.addToPlaylist(topArtistID, allTracks)
        

    def getTopTracks(self):
        query =  "https://api.spotify.com/v1/me/top/tracks?limit=30"
        response = requests.get(
            query,
            headers={
                "Content-Type":"application/json",
                "Authorization":"Bearer {}".format(self.token)
            }     
        )
        response_json = response.json()
        topTracks = []

        for track in response_json["items"]:
            topTracks.append(track["uri"])

        print(topTracks)

        request_body = json.dumps({
            "name":"Top Tracks",
            "description": "My Top Songs",
            "public": True
        })
        
        #top tracks ID
        topID = self.createNewPlaylist(request_body)

        #add all the top tracks to the playlist
        self.addToPlaylist(topID, topTracks)

   
class RecommendPage(tk.Frame):

    def __init__(self, parent, controller):
        
        #MY ACCOUNT

        scope = 'playlist-modify-public user-top-read user-modify-playback-state'
        self.userID = "22rr3gzk75qrvzazocbv3x23q"
        self.client_id = 'e697b9036e434b4da4593d1d76181ccb'
        self.client_secret = '1dcdd21d3ddb4128ba30652370859c91'  
        self.token = util.prompt_for_user_token(self.userID, scope, client_id = self.client_id, client_secret=self.client_secret, redirect_uri='https://google.com/')

        ##################TEST#################
        '''
        scope = 'playlist-modify-public user-top-read'
        self.userID = "toppingdj"
        self.client_id = 'b509698e53ff4e0f9a25b977be11d843'
        self.client_secret = '204ba9c196d943368771756878909b4f'  
        self.token = util.prompt_for_user_token(self.userID, scope, client_id = self.client_id, client_secret=self.client_secret, redirect_uri='https://google.com/')
        '''
        #######################################
        self.userPlaylists = None
        
        tk.Frame.__init__(self, parent)
        tk.Frame.config(self,background="black")
        
        label = tk.Label(self, text = "Add New Songs to Current Playlist!", font=largeFont, background="black", foreground="white")
        label.grid(row=0, column=0, pady=20, padx = 200)

        label2 = tk.Label(self, text="Choose a Playlist", font=smallFont)
        label2.grid(row=1, column=0)

        #From https://pythonspot.com/tk-dropdown-example/
        tkvar = tk.StringVar(self)

        # Dictionary with options
        playlists = self.getPlaylists()
        tkvar.set(playlists[0]) # set the default option

        popupMenu = OptionMenu(self, tkvar, *playlists)
        popupMenu.grid(row=2, column =0, pady=10)
        
        button = ttk.Button(self, text="Generate Recommended Songs", command=lambda: self.getRecommendedSongs(tkvar.get()))
        button.grid(row=3, column=0, pady=10)

        button2 = ttk.Button(self, text="Back to Home", command=lambda: controller.show_frame(StartPage))
        button2.grid(row=4, column=0, pady=10)

    def getPlaylists(self):
        query = "https://api.spotify.com/v1/me/playlists?limit=10"
        response = requests.get(
                query,
                headers={
                    "Content-Type":"application/json",
                    "Authorization":"Bearer {}".format(self.token)
                }     
            )
        response_json = response.json()
        self.userPlaylists = response_json
        
        playlistNames = []
        for playlist in response_json["items"]:
            playlistNames.append(playlist["name"])
        #get list of playlist names for view
        return playlistNames

    def createNewPlaylist(self, request_body):
        query = "https://api.spotify.com/v1/users/{}/playlists".format(self.userID)
        response = requests.post(
            query,
            data=request_body,
            headers={
                "Content-Type":"application/json",
                "Authorization":"Bearer {}".format(self.token)
            }     
        )
        response_json = response.json()
        #return the new playlist ID
        return response_json["id"]


    def addToPlaylist(self, playlistID, uris):
        request_data = json.dumps(uris)
        query = "https://api.spotify.com/v1/playlists/{}/tracks".format(playlistID)
        repsonse = requests.post(
            query,
            data=request_data,
            headers={
                "Content-Type":"application/json",
                "Authorization":"Bearer {}".format(self.token)
            }
        )
        
    def getRecommedationQuery(self, audioFeatures, topArtists):
        #returns recommendation query link given audio features
        topArtistsStr = ""
        for artist in topArtists[0:3]:
            topArtistsStr+= artist+"%2C"
        topArtistsStr+topArtists[4]

        audioFeaturesStr = "https://api.spotify.com/v1/recommendations?&market=US&seed_artists={}".format(topArtistsStr)
        for feature in audioFeatures:
            val = audioFeatures[feature]
            minVal = val-(val*0.9)
            maxVal = val+(val*0.9)
            if feature in ["duration_ms","mode","time_signature"]:
                minVal = roundHalfUp(minVal)
                maxVal = roundHalfUp(maxVal)
            elif feature == "loudness":
                minVal, maxVal = maxVal, minVal
            
            minAdd = "&min_"+feature+"="+str(minVal)
            maxAdd = "&max_"+feature+"="+str(maxVal)
    
            audioFeaturesStr+=(minAdd+maxAdd)

        return audioFeaturesStr

    def getAverageAudioFeatureVals(self, trackIDs):
        audioFeatures = dict()
        for trackId in trackIDs:
            query = "https://api.spotify.com/v1/audio-features/{}".format(trackId)
            response = requests.get(
                query,
                headers={
                    "Content-Type":"application/json",
                    "Authorization":"Bearer {}".format(self.token)
                }     
            )
            response_json = response.json()
            for feature in response_json:
                if isinstance(response_json[feature], (int, float)) and (feature not in ["key", "speechiness", "loudness"]):
                    if feature not in audioFeatures:
                        audioFeatures[feature] = [response_json[feature]]
                    else:
                        audioFeatures[feature].append(response_json[feature])

        #get average of audio feature values
        for feature in audioFeatures:
            total = 0
            count = 0
            for val in audioFeatures[feature]:
                total+=val
                count+=1
            audioFeatures[feature] = total/count

        return audioFeatures

    def getTopArtists(self, trackIDs):
        topArtists = dict()
        for trackId in trackIDs:
            query = "https://api.spotify.com/v1/tracks/{}".format(trackId)
            response = requests.get(
                query,
                headers={
                    "Content-Type":"application/json",
                    "Authorization":"Bearer {}".format(self.token)
                }     
            )
            response_json = response.json()
            for artist in response_json["artists"]:
                artistID = artist["id"]
                if artistID not in topArtists:
                    topArtists[artistID]= 1
                else:
                    topArtists[artistID]+= 1
        c = Counter(topArtists) 
        # Finding 5 most common artists in the dictionary
        mostCommon = c.most_common(5)
        topArtistIDs = []
        for artist in mostCommon:
            topArtistIDs.append(artist[0])
        return (topArtistIDs)


    def getRecommendedSongs(self, playlistName):
        playlistID = None
        for playlist in self.userPlaylists["items"]:
            if playlist["name"] == playlistName:
                playlistID = playlist["id"]
                
        query = "https://api.spotify.com/v1/playlists/{}/tracks?market=US&limit=20".format(playlistID)
        response = requests.get(
            query,
            headers={
                "Content-Type":"application/json",
                "Authorization":"Bearer {}".format(self.token)
            }     
        )
        response_json = response.json()
        trackIDs = []
        for track in response_json["items"]:
            trackIDs.append(track["track"]["id"])

        #create Dictionary of audio feature values
        audioFeatures = self.getAverageAudioFeatureVals(trackIDs)
        topArtists = self.getTopArtists(trackIDs)
        

        query = self.getRecommedationQuery(audioFeatures, topArtists)
        response = requests.get(
                query,
                headers={
                    "Content-Type":"application/json",
                    "Authorization":"Bearer {}".format(self.token)
                }     
            )
        
        response_json = response.json()
        uris = []
        for track in response_json["tracks"]:
            uris.append(track["uri"])
        self.addToPlaylist(playlistID, uris)
        print("Success!")

class QueuePage(tk.Frame):

    def __init__(self, parent, controller):
        
        #MY ACCOUNT
        scope = 'playlist-modify-public user-top-read user-modify-playback-state'
        self.userID = "22rr3gzk75qrvzazocbv3x23q"
        self.client_id = 'e697b9036e434b4da4593d1d76181ccb'
        self.client_secret = '1dcdd21d3ddb4128ba30652370859c91'  
        self.token = util.prompt_for_user_token(self.userID, scope, client_id = self.client_id, client_secret=self.client_secret, redirect_uri='https://google.com/')

        ##################TEST#################
        '''
        scope = 'playlist-modify-public user-top-read'
        self.userID = "toppingdj"
        self.client_id = 'b509698e53ff4e0f9a25b977be11d843'
        self.client_secret = '204ba9c196d943368771756878909b4f'  
        self.token = util.prompt_for_user_token(self.userID, scope, client_id = self.client_id, client_secret=self.client_secret, redirect_uri='https://google.com/')
        '''
        #######################################
        
        tk.Frame.__init__(self, parent)
        tk.Frame.config(self,background="black")

        label = tk.Label(self, text = "Add Songs to Queue", font=largeFont, background="black", foreground="white")
        label.grid(row=0, column=0, pady=20, padx = 270)

        label = tk.Label(self, text = "Choose the number of songs you want to add", font=smallFont, background="black", foreground="white")
        label.grid(row=1, column=0, pady=10)

        numSongs = tk.Scale(self, from_=1, to=50, orient=HORIZONTAL)
        numSongs.grid(row=2, column=0, pady=10)

        button = ttk.Button(self, text="Add", command=lambda: self.getSongs(numSongs.get()))
        button.grid(row=3, column=0, pady=10)

        button2 = ttk.Button(self, text="Back to Home", command=lambda: controller.show_frame(StartPage))
        button2.grid(row=4, column=0, pady=10)


    def getSongs(self, numSongs):
        query = "https://api.spotify.com/v1/me/top/tracks?time_range=medium_term&limit={}".format(numSongs)
        response = requests.get(
            query,
            headers={
                "Content-Type":"application/json",
                "Authorization":"Bearer {}".format(self.token)
            }     
        )
        response_json = response.json()
        songUris = []
        for song in response_json["items"]:
            songUris.append(song["uri"])

        self.addToQueue(songUris)
        print("Added ",numSongs," songs!")


    def addToQueue(self, songUris):
        for uri in songUris:
            request_data = json.dumps(uri)
            query = "https://api.spotify.com/v1/me/player/queue?uri={}".format(uri)
            repsonse = requests.post(
                query,
                data=request_data,
                headers={
                    "Content-Type":"application/json",
                    "Authorization":"Bearer {}".format(self.token)
                }
            )
        

#Run whole app
def run():
    
    app = Main()
    app.mainloop()

run()
