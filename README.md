# Pytron
Programmed by:
Jared Rodgers and Charles Shinaver

Pytron is our implementation of the classic tron game using the
basic pyton libraries along with pygame and twisted. Our game works
for two players and starts immediately upon connection between the
host and the client. To create the host server simply type:

python main.py --host [port]

To connect to that host simply type:

python main.py --client [hostname]:[port]

Any confusion can be cleared up by accessing our terminal help menu
by typing:

python main.py -h

Upon connection the game will start and you will be given control
of 1 of 2 bikes that create a trail behind them. The bikes begin
initially moving upward and the direction can be changed with the
arrow keys. Collision into the outer boarder of the grid, your
trail, or your opponents trail will result in the death of your bike
and will proceed to quit the game. Note that moving backwards onto
your own trail will kill your bike (trying to move down while 
moving up).


Some helpful debugging messages can be printed by changing line 23
of main.py where is says WARNING to DEBUG.
