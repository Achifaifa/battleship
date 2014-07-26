#! /usr/bin/env python
import os, random, sys, termios, tty

gamename="THING!"

class ship:
  """
  XXXXX -> big ship
  X -> small ship
  etc etc etc

  XX XX XX 
  XXXXXXXXXXX <- This is a ship shipping ship, shipping shipping ships
  """

  def __init__(self,size,pos,direc):
    """
    size:lenght of the ship
    pos: Initial position (array [x,y])
    dir: 0 is horizontal, 1 is vertical

    e.g.: size 2, pos 1,1; dir 0

    XX~
    ~~~
    ~~~

    """

    self.size=size
    #Structure of the coords array: [X position, Y position, Status (O OK, X hit)]
    tpos=pos
    tpos.append("O")
    self.coords=[]
    self.coords.append(tpos)
    tsize=size
    tsize-=1
    while tsize!=0:
      tsize-=1
      if direc:
        self.coords.append([self.coords[0][0],self.coords[0][1]+1],"O")
      else:
        self.coords.append([self.coords[0][0]+1,self.coords[0][1],"O"])

  def launch(self,targetx,targety):
    """
    Receives coordinates and changes status accordingly

    Returns 1 if the ship has been hit
    """

    for part in self.coords:
      if part[0]==targetx and part[1]==targety: 
        part[2]="X"
        return 1,[targetx,targety]
    return 0,[-1,-1]

class arena:
  """
  Like the gladiator thing, but with ships
  """

  def __init__(self,size):
    """
    creates a square arena of sizexsize squares. Minimum and default 10x10

    I wanted to make a circular one but meh. Just imagine it and don't place anything in the corners.
    """

    if size<10: size=10
    self.arenarray=[]
    for i in range(size):
      self.arenarray.append([])
      for j in range(size):
        self.arenarray[i].append("~")

class player:
  """
  blabla
  """

  def __init__(self,name):
    self.name=name
    self.money=10
    self.ships=[]

  def receivehit(self,x,y):
    for ship in self.ships:
      if ship.launch(x,y):

def game(humanplayer):
  """
  Main loop etc etc
  """

  #Generate arena
  varena=arena(-1)
  #Generate """"AI"""" player
  AIplayer=player(random.choice(["Hiei","Musashi","Iku","Hachi"]))
  totalships={"fishing boat (2)":3,"bigger fishing boat (3)":2,"battleboat (4)":1,"carrier (5)":1}
  turnmsg=""
  numbers=[1,2,3,4,5,6,7,8,9,0]

  #Ship placement!
  os.system('clear')
  for type in totalships:
    for i in range(totalships[type]):
      while 1:
        os.system('clear')
        print gamename
        print "%s VS %s" %(humanplayer.name,AIplayer.name)
        print "  1234567890"
        for i,j in zip(varena.arenarray,numbers): print str(j)+" "+''.join(map(str,i))

        print "\nPlace your ships with (xcoord,ycoord,vert)"
        print "Now place your %s"%type
        placevar=raw_input(">>>")
        placevar=placevar.split(',')



  while 1:
    os.system('clear')
    #Print stuff
    print gamename
    print "%s VS %s" %(humanplayer.name,AIplayer.name)
    print "  1234567890"
    for i,j in zip(varena.arenarray,numbers): print str(j)+" "+''.join(map(str,i))

    print "\n%s"%turnmsg
    print "\ntype the building, action and/or coordinates"
    print "e.g., 'oil,6,3' or 'bomb,5,0'"
    print "type F to surrender"

    #wait for action
    loopvar=raw_input(">>>")
    if loopvar=="f": break
    else:
      loopvar=loopvar.split(',')
      if loopvar[0]=="oil":
        turnmsg="You built an oil rig in (%s,%s)"%(loopvar[1],loopvar[2])
      elif loopvar[0]=="bomb":
        turnmsg="You dropped a bomb at (%s,%s) \n%s"%(loopvar[1],loopvar[2],"more info")
      else: turnmsg="Not valid, try again"


def getch():
  """
  Reads a single key from the console input*. Code by Joeyespo:
  https://github.com/joeyespo/py-getch

  *I can't fucking believe this is not in the os library
  """

  fd=sys.stdin.fileno()
  old=termios.tcgetattr(fd)
  try:
    tty.setraw(fd)
    return sys.stdin.read(1)
  finally:
    termios.tcsetattr(fd, termios.TCSADRAIN, old) 


if __name__=="__main__":
  while 1:
    os.system('clear')
    print gamename
    print "1.- play"
    print "2.- help"
    print "0.- exit"
    mmenu=getch()
    if mmenu=="1":
      playername=raw_input("Player name?> ")
      if len(playername)<1: playername="Anon"
      dude=player(playername)
      game(dude)
    elif mmenu=="2":
      os.system('clear')
      print gamename+" (TL;DR)\n"
      print "Oiling rigs generate money"
      print "Shooting stuff costs money"
      print "You can do both"
      print "???"
      print "Profit!!\n"
      print "(You can also press any key to continue)"
      getch()
    elif mmenu=="0": 
      os.system('clear')
      break
    else: 
      print "NOPE"
      getch()