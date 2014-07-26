#! /usr/bin/env python
import os, random, sys, termios, tty

gamename="THING!"

class ship:
  """
  XXXXX -> big ship
  X -> small ship
  etc etc etc

  X  X  X
  XX XX XX 
  XXXXXXXXXXX <- This is a ship shipping ship shipping ship, shipping shipping ships shipping ships
  """

  def __init__(self,size,pos,direc,aren):
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
    tsize=self.size
    tsize-=1
    var=0
    while tsize!=0:
      if aren.arenarray[pos[1]][pos[0]]==".":
        try:
          tsize-=1
          var+=1
          if direc: 
            if aren.arenarray[pos[1]+var][pos[0]]=="." and pos[1]+var<10:
              self.coords.append([self.coords[0][0],self.coords[0][1]+var,"O"])
            else: 
              self.coords=[]
              1/0
          else:     
            if aren.arenarray[pos[1]][pos[0]+var]=="." and pos[2]+var<10:
              self.coords.append([self.coords[0][0]+var,self.coords[0][1],"O"])
            else: 
              self.coords=[]
              1/0
        except:
          1/0
        
      else: 
        #Using 1/0 because I'm too lazy to code actual exceptions
        self.coords=[]
        1/0

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

    #Default to 10x10
    if size<10: size=10
    self.size=size

    #Generate your grid
    self.arenarray=[]
    for i in range(size):
      self.arenarray.append([])
      for j in range(size):
        self.arenarray[i].append(".")

    #Generate target grid
    self.targetarray=[]
    for i in range(size):
      self.targetarray.append([])
      for j in range(size):
        self.targetarray[i].append(".")

  def addoil(self,x,y,playa):
    if self.arenarray[y][x]==".": 
      self.arenarray[y][x]="A"
      playa.oil+=1
      return 1,"Oil rig built in (%i,%i)"%(x,y)
    else: return 0,"You can't place it there!"

class player:
  """
  blabla
  """

  def __init__(self,name):
    self.name=name
    self.money=10
    self.ships=[]
    self.oil=0
    self.credits=10

  def aireceivehit(self,x,y,varena):
    for ship in self.ships:
      hit,coords=ship.launch(x,y)
      if hit: 
        varena.targetarray[y][x]="X"
        return "It's a hit!"
    varena.targetarray[y][x]="~"
    return "miss"
    return 0,[-1,-1]

  def humanreceivehit(self,x,y,varena):
    for ship in self.ships:
      hit,coords=ship.launch(x,y)
      if hit: 
        varena.arenarray[y][x]="X"
        return "It's a hit!"
    if varena.arenarray[y][x]!="A": varena.arenarray[y][x]="~"
    return "miss"
    return 0,[-1,-1]

def game(humanplayer):
  """
  Main loop etc etc
  """

  #Generate arena
  varena=arena(-1)
  #Generate """"AI"""" player
  AIplayer=player(random.choice(["Hiei","Musashi","Iku","Hachi"]))
  totalships={"fishing boat (2)":2,"bigger fishing boat (3)":2,"battleboat (4)":1,"carrier (5)":1}
  turnmsg=""
  numbers=[1,2,3,4,5,6,7,8,9,0]
  autoplacevar=0

  #Ship placement screen
  os.system('clear')
  for type in totalships:
    for i in range(totalships[type]):
      while 1:
        os.system('clear')
        print gamename
        print "%s VS %s" %(humanplayer.name,AIplayer.name)
        print "  1234567890"
        for k,j in zip(varena.arenarray,numbers): print str(j)+" "+''.join(map(str,k))

        print "\nPlace your ships with (xcoord,ycoord,vert)"
        print "Type 'autoplace' to randomly distribute your ships"
        print "Now place your %s"%type
        if not autoplacevar: placevar=raw_input(">>>")
        if placevar=="autoplace": autoplacevar=1
        #Player action block
        if autoplacevar:
          try:
            humanplayer.ships.append(ship(int(type.partition('(')[2].partition(')')[0]),[random.randrange(varena.size),random.randrange(varena.size)],random.choice([0,1]),varena))
            for i in humanplayer.ships[-1].coords: varena.arenarray[i[1]][i[0]]="O"
            break
          except ZeroDivisionError:
            pass
        else:
          placevar=placevar.split(',')
          try:
            humanplayer.ships.append(ship(int(type.partition('(')[2].partition(')')[0]),[int(placevar[0])-1,int(placevar[1])-1],int(placevar[2]),varena))
            for i in humanplayer.ships[-1].coords: varena.arenarray[i[1]][i[0]]="O"
            break
          except ZeroDivisionError: 
            print "There is something in the way!"
            getch()
          except:
            print "nope"
            getch()

  #AI ship placing
  for type in totalships:
    for i in range(totalships[type]):
      while 1:
        try:
          AIplayer.ships.append(ship(int(type.partition('(')[2].partition(')')[0]),[random.randrange(varena.size),random.randrange(varena.size)],random.choice([0,1]),varena))
          break
        except ZeroDivisionError:
          pass
        
  #Main game loop
  while 1:
    os.system('clear')
    #Print stuff
    print "%s (%s VS %s)" %(gamename,humanplayer.name,AIplayer.name)
    print "\nTarget screen     Your area"
    print "  1234567890      1234567890"
    for i,j,k,l in zip(varena.targetarray,numbers,varena.arenarray,numbers): 
      print str(j)+" "+''.join(map(str,i))+"    "+str(l)+" "+''.join(map(str,k))
    print "Ships: %i, Credits: %i -- Oil rigs: %i (%ic/turn)"%(len(humanplayer.ships),humanplayer.credits,humanplayer.oil,(humanplayer.oil*1.5)+1)
    print "Enemy ships: %i"%(len(AIplayer.ships))
    print "\n%s"%turnmsg
    print "type the building, action and/or coordinates"
    print "e.g., 'oil,6,3' (cost 10c) or 'bomb,5,0' (cost 5c)"
    print "type F to surrender"

    #wait for action
    turnmsg=""
    loopvar=raw_input(">>>")
    if loopvar=="f": break
    elif len(loopvar.split(','))==3:
      loopvar=loopvar.split(',')
      if loopvar[0]=="oil":
        if humanplayer.credits>=10:
          oilv,turnmsg=varena.addoil(int(loopvar[1])-1,int(loopvar[2])-1,humanplayer)
          if oilv: humanplayer.credits-=10
        else: turnmsg="Not enough credits"
      elif loopvar[0]=="bomb":
        if humanplayer.credits>=5:
          try:
            turnmsg="You dropped a bomb at (%s,%s) \n%s\n"%(loopvar[1],loopvar[2],AIplayer.aireceivehit(int(loopvar[1])-1,int(loopvar[2])-1,varena))
            humanplayer.credits-=5
          except ValueError: pass
        else:turnmsg="Not enough credits"
      else: turnmsg="Not valid, try again"
    else: turnmsg="nope"

    #AI moves
    randx,randy=random.randrange(len(varena.arenarray)),random.randrange(len(varena.arenarray))
    humanplayer.humanreceivehit(randx,randy,varena)
    if varena.arenarray[randy][randx]=="A":
      humanplayer.oil-=1
      varena.arenarray[randy][randx]="X"
      turnmsg="One of your oil rigs has been destroyed!"
    if varena.arenarray[randy][randx]=="O":
      varena.arenarray[randy][randx]="X"
      turnmsg="One of your ships has been hit!"


    #End of turn

    #Add credits
    humanplayer.credits+=(humanplayer.oil*1.5)+1
    AIplayer.credits+=(AIplayer.oil*1.5)+1

    #Delete sunk ship shipping ship shipping ships shipping ship shipping ships shipping ships and the ships and ship shipping ships shipped.
    for i in humanplayer.ships:
      deletevar=1
      for j in i.coords:
        if j[2]=="O":deletevar=0
      if deletevar: del humanplayer.ships[humanplayer.ships.index(i)]
    for i in AIplayer.ships:
      deletevar=1
      for j in i.coords:
        if j[2]=="O":deletevar=0
      if deletevar: del AIplayer.ships[AIplayer.ships.index(i)]

    #End the game if a player has no ships left
    if len(AIplayer.ships)==0 or len(humanplayer.ships)==0: 
      break
      gameover(AIplayer,humanplayer)

def gameover(computer,human):
  """
  Displays the end of game screen
  """

  os.system('clear')
  print "%s (%s VS %s)\n" %(gamename,human.name,computer.name)

  if len(computer.ships)==0 and len(human.ships)!=0:
    print "You won! And you still had %i ships left!"%len(human.ships)
  else:
    print "You lost"
  print "\npress any key to continue"
  getch()

#Does not work in windows because termios but who cares.
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