import os
import pickle
import shutil
cls =lambda: os.system("cls")


# Grabs and stores the song name and location 
def getSongs(songInfo , path, target):
    for root, dirs, files in os.walk(path):
        for file in files:
            if file.endswith(target):
                songInfo.append([file,root])

    return songInfo  


def getLocation(find): # Find where the file is stored
    found = os.path.dirname(os.path.realpath(find))
    return found

def findMusic(musicPaths, songInfo):
    for i in range(len(musicPaths)):
        # This searches every file path to find the names and locations of the music stored for each of the audio file typed
        #target = "" # The type of audio file the program is going to look for
        #path = "" # The current path to where the songs are being stored 
        path = musicPaths[i]
        target = ".mp3"
        songInfo = getSongs(songInfo, path, target)
        target = ".aac"
        songInfo = getSongs(songInfo, path, target)
        target = ".flac"
        songInfo = getSongs(songInfo, path, target)
        target = ".m4a"
        songInfo = getSongs(songInfo, path, target)
        target = ".wav"
        songInfo = getSongs(songInfo, path, target)
        target = ".wma"
        songInfo = getSongs(songInfo, path, target)
        target = ".ac3"
        songInfo = getSongs(songInfo, path, target)
        target = ".3gp"
        songInfo = getSongs(songInfo, path, target)
        target = ".3g2"
        songInfo = getSongs(songInfo, path, target)
        target = ".amr"

    with open("songInfo.pkl","wb") as s: # Saves the file
        pickle.dump(songInfo ,s)

def addNewLocation(musicPaths):
    # This block of code allows the user to add the paths where their music is located 
    while True:
        cls()
        print("Please type or paste in the path to where your music is located then press enter")
        print("If you have added all of your paths type \"d\" and press enter to move on")
        print("Note: the first location that you enter will store your playlists so don’t delete the folder  ")
        print("(If you have more then one location you will be given the option to add more next)")
        x = input()
        if x == "d": 
            if len(musicPaths) >= 1 : break
            else:
               print("You need to enter at least one place where you store music")
               print(len(musicPaths))
               print("\nPress enter to be taken back")
               input()
        else:
            musicPaths.append(x)
            #print(len(musicPaths))
            cls()
            print("Path added")
            print("\nPress enter to be taken back")
            input()

    with open("musicPaths.pkl","wb") as s: # Saves the file
        pickle.dump(musicPaths ,s)

def getData():
    with open("songInfo.pkl","rb") as s: # Opens the file (songInfo list)
        songInfo  = pickle.load(s)

    with open("musicPaths.pkl","rb") as s: # Opens the file (musicPaths list)
        musicPaths  = pickle.load(s)

    numberOfSongs = len(songInfo) # So the program only has to find the size of songInfo once

    return songInfo, musicPaths, numberOfSongs

def getPlaylistNames(): # This gets the names of past playlists 
    # The reason that I didn’t group this in with getData is because this is called less often or possibly not all depending on the users actions 
        with open("usedPlaylistNames.pkl","rb") as s:
            usedPlaylistNames  = pickle.load(s)
        return usedPlaylistNames

# Creates the folders and also regenerates them if the user deletes them
if os.path.isdir("playlists") == False:
	os.makedirs("playlists")

if os.path.isdir("logs") == False:
	os.makedirs("logs")

songInfo = []  # This will be used to store the name and location of the songs (in a nestled list)
#[0] stores the songs name
#[1] stores the songs location

musicPaths = [] # A list of places that the music is being stored 
numberOfSongs = 0

usedPlaylistNames = []  # This will be used to store the names of all playlists the program has made to make sure that there are no duplicates

if os.path.isfile("musicPaths.pkl") == False: # Since the pickle file containing the list of where the songs are stored is only generated after the program has run
   # we can use it to check if the program has been run before and start setting up  
    addNewLocation(musicPaths)
    findMusic(musicPaths, songInfo)


songInfo, musicPaths, numberOfSongs = getData()


while True:
    
    cls()
    print("--------------------------------------------")
    print("|     Groove playlist converter:  |\n---------------------------------------------")
    print("(Works best in full screen mode)")
    print("Type the number before the action and press enter:\n1) Make a playlist")
    print("2) Export a list of all the songs names\n3) Export a list containing all of the song names and locations")
    print("4) View a list of songs and their locations")
    print("5) Add a new music location (If you moved your music to a new folder) \n6) Have the program refresh its music list (Do this if you added new music to the folders)")
    print("7) Display a list of converted playlists")
    print("8) Exit")
    inp = input()
    cls()
    if inp == "1":
        print("Please make sure that the songs are in txt format\nThen just drag and drop or copy and paste the text file into the playlists folder inside this application")
        print("I recommend the following link to export your playlist’s to text files: https://www.tunemymusic.com/Spotify-to-File.php#step5")
        print("The program can do them all at once, the name on the text file will be the name on the playlist")
        print("Please don’t put a \"\". in the playlist name also please refer to the log folder to make sure that you are not adding a duplicate playlist")
        print("Also the program currently looks for a 100% match in the song name, this may change in future updates")
        print("Press enter once you have at least one text (.txt) file in the playlists folder")
        input()
        cls()

        # Finds all of the playlist files and saves them in a list  
        folder = str(getLocation("Groove_playlist_creator.py"))+"\playlists"
        playlists = []
        print(folder)
        for file in os.listdir(folder):
            if file.endswith(".txt"): playlists.append(file)
        #print(songInfo[0][0]


        # This removes the file extension so it does not interfere with the search for the song   
        songInfoNE = list(songInfo)
        for i in range(numberOfSongs):
            thisFile = songInfoNE[i][0]
            base = os.path.splitext(thisFile)[0]
            songInfoNE[i][0] = base  # songInfoNE Stores the songs without the file extensions  (NE – no extensions)
        #for x in range(len(songInfoNE)): print(songInfoNE[x][0])

        skip = False # This will be used to tell the program what text to display later 

        for i in range(len(playlists)): 

            # This block of code prevents playlist duplicates 
            if os.path.isfile("usedPlaylistNames.pkl") == True:
                usedPlaylistNames = getPlaylistNames() 
                if playlists[i] in usedPlaylistNames:
                    cls()
                    print("This playlist already exists, please remove it from the folder and try again")
                    print("Press enter to be taken back to the main menu")
                    skip = True
                    input()
                    break
            else: 
                usedPlaylistNames.append(playlists[i]) # If the pickle file has not yet been generated the program generates one
                with open("usedPlaylistNames.pkl","wb") as s: 
                   pickle.dump(usedPlaylistNames ,s)

            forLogFile = [] # A log file will be generated for every playlist made
            # This converts the data from the text file into a list  
            playlistName = playlists[i]
            playlistLocation = str(folder+"\\"+playlists[i])
            file = open(playlistLocation,"r")
            listOfSongs= file.readlines()
            file.close()
            cleanedListOfSongs = ([cleanedListOfSongs.replace("\n","") for cleanedListOfSongs in listOfSongs]) # This removes discrepancies in the song names, also removes the empty spaces   

            indexStorage = [] # This will temporally store the indexes of the songs  
            songCount = len(cleanedListOfSongs)
            status  = cleanedListOfSongs.copy() #  This will be used to keep track of what songs did not convert so the user can go in and manually add them


            for x in range(songCount): # This searches the nestled list for a matching song name               
                for sublist in songInfoNE:
                   # for song in sublist: 
                        if cleanedListOfSongs[x] in sublist: 
                            ind = songInfoNE.index(sublist)
                            indexStorage.append(ind)
                            status[x] = "Found"
                           # print("Ran!")
                           # print(songInfo[ind])
                           # print("Found it!",cleanedListOfSongs[x])
                           #print(songInfoNE.index(sublist))
                           
            songInfo, musicPaths, numberOfSongs = getData() # We need to reload the data from the pickle because in the process sometimes the original songInfo file also loose its file extension
            playlistName = playlistName.split(".")
            playlistName = str(playlistName[0])
            #print(playlistName)
            songsFound = len(indexStorage)
            #print(songsFound,songCount)

            temp = "Playlist name: " + playlistName + " Songs converted: "+ str(songsFound) +" Songs that failed to convert: "+ str(songCount-songsFound) + "\n"
            forLogFile.append(temp)
            temp = "List of songs not found: \n"
            forLogFile.append(temp)
            for song in status: # This only adds the songs that the program could not convert
                if song != "Found": forLogFile.append(song+"\n")


            temp = "\nList of songs found: (The songs file path)\n"
            forLogFile.append(temp)
            fileName = playlistName+".wpl" # Makes the Groove playlist have the same name as the text file
            file = open(fileName,"w+") 

            # This is the code that has to be in a .wpl file for Groove to read
            # I have typed it out fully at the bottom of this file
            file.write("<?wpl version=\"1.0\"?>\n")
            file.write("<smil>\n")
            file.write("    <head>\n") 
            file.write("      <author/>\n")
            temp ="       <title>x</title>\n".replace("x",playlistName)
            file.write(temp)
            file.write("    </head>\n")
            file.write("    <body>\n")
            file.write("        <seq>\n")


            # This block of code will add each song into the playlist  
            for x in range(songsFound):
                SL = str(songInfo[indexStorage[x]][1])+"\\"+str(songInfo[indexStorage[x]][0]) # This is the songs exact location on the computer 
                forLogFile.append(SL+"\n")
                temp = "        <media src=\"x\"/>\n".replace("x",SL)
                file.write(temp) 
                
            # Adds the last bit of code and closes the file  
            file.write("        </seq>\n")
            file.write("    </body>\n")
            file.write("</smil>\n")
            file.close()
            
            shutil.move(fileName ,musicPaths[0]) # Move the playlist file into a place where Groove can see it
            forLogFile.append("\nThe playlist location is: "+musicPaths[0]+"\\"+fileName)
            fileName = playlistName+" - log"+".txt" # Makes the Groove playlist have the same name as the text file
            file = open(fileName,"w+")
            file.writelines(forLogFile)
            file.close()
            shutil.move(fileName, getLocation("Groove_playlist_creator.py")+"\logs") # Moves the log to the logs folder
            os.remove(getLocation("Groove_playlist_creator.py")+"\playlists"+"\\"+playlists[i]) # Now that the playlist has been converted it can be removed
            
            cls()
            print("Playlist added, press enter continue")
            print("Print you can view the log here: ",getLocation("Groove_playlist_creator.py")+"\logs")
            input()

        if skip == False:
            cls()
            print("All playlists have successfully been added, press enter to return to the main menu")
            print("Or type o and press enter to launch Groove with your new playlists (please make sure that Groove is your default program to open .wlp files")
            x = input()
            if x == "o": os.startfile(musicPaths[0]+"\\"+playlistName+".wpl")



    elif inp == "2":
        file = open("Song Names.txt","w+", 1,"utf-8") # Will overwrite existing text
        # I used utf-8 because in my testing I was occasionally getting “'charmap' codec can't encode characters in position  x” errors  
        for i in range(numberOfSongs):
            file.write("Song name: "+str(songInfo[i][0]))
            file.write("\n")
        file.close()
        print("Songs successfully written to text file. The text file is called \"Song Names\" and is found in the same folder that this program is being run from")
        print("("+str(getLocation("Song Names.txt"))+")")
        print("\nPress enter to be taken back to the main menu")
        input()


    elif inp == "3":
        file = open("Song Names and locations.txt","w+", 1,"utf-8") # Will overwrite existing text
        for i in range(numberOfSongs):
            file.write("Song name: "+str(songInfo[i][0])+"  Location: "+str(songInfo[i][1]))
            file.write("\n")
        file.close()
        print("Data successfully written to text file. The text file is called \"Song Names and locations\" and is found in the same folder that this program is being run from")
        print("("+str(getLocation("Song Names and locations.txt"))+")")
        print("\nPress enter to be taken back to the main menu")
        input()


    elif inp == "4":
        print(numberOfSongs,"Songs found\n")
        for i in range(len(songInfo)):
            print("Song name:", songInfo[i][0], "Location:", songInfo[i][1])
        print("\nPress enter to be taken back to the main menu")
        input()


    elif inp == "5":
        addNewLocation(musicPaths)
        findMusic(musicPaths, songInfo)
        songInfo, musicPaths, numberOfSongs = getData()
        print("New music added, press enter to be taken back to the main menu")
        input()

    elif inp == "6":
        findMusic(musicPaths, songInfo)
        songInfo, musicPaths, numberOfSongs = getData()
        print("New music added, press enter to be taken back to the main menu")
        input()

    elif inp == "7":
        cls()
        if os.path.exists("usedPlaylistNames.pkl"):
            usedPlaylistNames = getPlaylistNames() 
            for s in usedPlaylistNames: print(s)
        else: print("No converted playlists were detected")
        print("\nPress enter to be taken back to the main menu")
        input()

        

    elif inp == "8":
        exit(0)

    else:
        cls()
        print("That was not a valid option, press enter to be taken back to the main menu")
        input()


#<?wpl version="1.0"?>
#<smil>
#    <head>
#      <author/>
#      <title>playlist name goes here</title>
#    </head>
#    <body>
#        <seq>
#        Song information goes here
#        </seq>
#    </body>
#</smil>
