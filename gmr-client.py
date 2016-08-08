import requests, json, datetime, urllib2, httplib, os

authKey = "your key" #find it on gmr-site
savepath = "your path" #like '/home/maxe/.local/share/Aspyr/Sid Meier's Civilization 5/Saves/hotseat/'
backup = "your path/backup/"  # to move file in this backup folder after upload

playerID = ""
mygames = []

def start():  
    print "...checking authKey and getting playerID..."
    r = requests.get('http://multiplayerrobot.com/api/' +
                     'Diplomacy/AuthenticateUser?authKey=' + authKey)
    global playerID
    playerID = r.text
    #TODO validate playerID --> should be 64bit integer
    update(False);       

def update(raw):
    global mygames
    print "...updating game overview..."
    print '------------start of list----------'
    r = requests.get('http://multiplayerrobot.com/api/Diplomacy/' +
                     'GetGamesAndPlayers?playerIDText=' + playerID +
                     '&authKey=' + authKey)
    
    if raw == True:
        print r.text
        return

    mygames = []
    answer = json.loads(r.text)
    #list my current turns
    counter = 1
    for game in answer["Games"]:
        if int(game["CurrentTurn"]["UserId"]) == int(playerID):
            turn = str(game["CurrentTurn"]["Number"])
            
            #calculate remaining turntimer - crashes on some games
	#
        #    expires = game["CurrentTurn"]["Expires"]
        #    if expires != None:
        #        expires = datetime.datetime.strptime(expires,"%Y-%m-%dT%H:%M:%S.%f")
        #        expires = expires - datetime.datetime.utcnow()
            print str(counter) + ") " + game["Name"] # + " _time remaining: " + str(expires)
            mygames.append({"GameId" : game["GameId"],"Name" : game["Name"],
                            "Counter" : counter, # "Remaining" : expires,
                            "Turn" : turn, "TurnID" : game["CurrentTurn"]["TurnId"]})
            counter += 1
    print '------------end of list----------'
    #TODO sort by remaining time
    menu()

def upload():
    #find uploadable save files
    print "-------------------------------------"
    print "Saves must be named: [GameID]-[Turn]-u.Civ5Save"
    print "You basically just need to add '-u' when you save in Civ after you played your turn..."
    print "... finding uploadable saves now ..."
    print "----------Start of list--------------"
    counter = 1
    choices = []
    for root, dirs, files in os.walk(savepath, topdown=True):
        for name in files:
            if name[-11:] == "-u.Civ5Save":
                try:
                    gameID, turn, rest = name.split("-")
                    canBeUploaded = False
                    selectedgame = None
                    for game in mygames:
                        if int(game["GameId"]) == int(gameID):
                            canBeUploaded = True
                            selectedgame = game
                    if canBeUploaded:
                        print "["+str(counter)+"] "+selectedgame["Name"]+" --> TURN "+turn
                        choices.append({"TurnID" : selectedgame["TurnID"], "counter" : counter, "fileName" : name})
                        counter += 1
                    else:
                        print '--> not in your current list of games' + name
                except:
                    print '--> not named after upload convention: ' + name
                    pass
            else:
                print '--> not named after upload convention: ' + name
                pass
        break
    print '-----------------End of list----------------------'
    print 'Which file do you want to upload? [c] to cancel...'

    response = raw_input()
    if response == "c":
        menu()
    else:
        turnID = str(choices[int(response)-1]["TurnID"])
        file = savepath + choices[int(response)-1]["fileName"]
        url = "/api/Diplomacy/SubmitTurn?authKey="+authKey+"&turnId="+turnID
        #TODO needs a progress bar! https://github.com/niltonvolpato/python-progressbar
        print "sending file now.... this might take a while..."
        h = httplib.HTTPConnection('multiplayerrobot.com:80')
        headers = {"Content-type": "application/x-www-form-urlen coded", "Accept": "text/plain"}
        with open(file, "rb") as f:
            h.request('POST', url, f, headers)
            r = h.getresponse()
        print r.read()

        # move files to backup folder
        import shutil 
        shutil.move(file, backup)
        file2 = file.replace('-u', '') #original file
        shutil.move(file2, backup)
        
        menu()
        
def download():
    print '---------download list ------------'
    counter = 1
    for game in mygames:
        print "[" + str(counter) + "] " + game["Name"]
        counter += 1
    print '---------end of list ------------'
    print 'please choose your game - [c]ancel'

    response = raw_input()
    if response == "c":
        menu()

    game = mygames[int(response)-1]
    url = "http://multiplayerrobot.com/api/Diplomacy/" + \
                     "GetLatestSaveFileBytes?authKey=" + authKey + \
                     "&gameId=" + str(game["GameId"])
    file_name = savepath + str(game["GameId"]) + "-" + \
                str(game["Turn"]) + ".Civ5Save"
    download_file(url, file_name)
    menu()

def download_file(url, file_name):
    u = urllib2.urlopen(url)
    f = open(file_name, 'wb')
    meta = u.info()
    file_size = int(meta.getheaders("Content-Length")[0])
    print "Downloading: %s Bytes: %s" % (file_name, file_size)

    file_size_dl = 0
    block_sz = 8192
    while True:
        buffer = u.read(block_sz)
        if not buffer:
            break

        file_size_dl += len(buffer)
        f.write(buffer)
        status = r"%10d  [%3.2f%%]" % (file_size_dl, file_size_dl * 100. / file_size)
        status = status + chr(8)*(len(status)+1)
        print status,

    f.close()

def menu():
    print "----------- What do you want do to next? ------------"
    print "[r]efresh - [u]pload - [d]ownload - [j]son-dump - e[x]it"
    response = raw_input()
    if response == "r":
        update(False)
    elif response == "u":
        upload()
    elif response == "d":
        download()
    elif response == "j":
        update(True)
    elif response == "x":
        return
    else:
        print "What? Try again!"
        menu()
        
start()
