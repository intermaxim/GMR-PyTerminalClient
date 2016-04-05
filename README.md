# GMR-PyTerminalClient
Python terminal client for Giant Multiplayer Robot API. http://multiplayerrobot.com/About/Api

GMR is a tool for playing Civilization 5 against other humans.

original forum post
(http://steamcommunity.com/groups/multiplayerrobot/discussions/0/371918937280157414/)

1) Put in your authcode from the GMR website (you find it under download)

2) Edit the path to your civ-saves and save the file.

3) Run the file and enjoy



Oh and maybe I was a little short on words describing how uploads work...

4) When you download a game it will be names as following: gameId-turn
The turn is the total of submitted turns, sadly not the ingame turn number.
When you load the game, it is in first position, because it is the newest file in the folder

5) When you save the game, find the file you just loaded.
This is slightly more tricky as the files are no longer sorted by date.
It helps to have fewer files in the folder.
Select it and then add '-u' to the filename.
Now you can upload through the client. 
