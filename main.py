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

    status variable
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
        return 1
    return 0

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

def game(humanplayer):
  """
  Main loop etc etc
  """

  #Generate arena
  varena=arena(-1)
  #Generate """"AI"""" player
  AIplayer=player(random.choice(["Hiei","Musashi","Iku","Hachi"]))
  totalships={"fishing boat (2)":3,"Bigger fishing boat (3)":2,"battleboat (4)":1,"Carrier (5)":1}

  #Ship placement!
  os.system('clear')
  # for key,value in totalships:
  #   print 


  while 1:
    os.system('clear')
    #Print stuff
    print gamename
    print "%s VS %s" %(humanplayer.name,AIplayer.name)
    print "  1234567890"
    for i in varena.arenarray: print str(varena.arenarray.index(i)+1)+" "+''.join(map(str,i))
    print "\npress F to surrender"

    #wait for action
    loopvar=getch()
    if loopvar=="f": break

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
      dude=player(raw_input("Player name?> "))
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