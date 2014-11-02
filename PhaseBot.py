import socket, time, random

HOST = "irc.freenode.net"
PORT = 6667
CHANNEL = "#OREServerChat"
NICK = "PhaseBot"
IDENT = "PhaseBot"
REALNAME = "Phase's Bot"
OWNERIRC = "Phasesaber"
COMMAND = "~"

#-Minecraft connection exclusive variables-#
OWNER = "Phasesaber"
SERVER1 = "OREBuild"
SERVER2 = "ORESchool"

#Connecting to IRC
sock = socket.socket( )
sock.connect((HOST, PORT))
sock.send(("NICK "+NICK+"\r\n").encode())
sock.send(("USER "+IDENT+" "+HOST+" bla :"+REALNAME+"\r\n").encode())
sock.send(("JOIN "+CHANNEL+"\r\n").encode())

#Get the args
def args(x):
    args=line.split(x)
    return args[1]

#Print line
def printLine():
    try:print(ident+" :"+message)
    except:print(line)

#Most recent user to send a message
def recentUser():
    if(ident!=SERVER1 and ident!=SERVER2): return ident
    user = line.split(":")
    return user[2]

def user():
    if(ident!=SERVER1 and ident!=SERVER2): return ident
    user = line.split(":")
    return user[2]

#Pings & Pongs
def ping():
    if(line.find("PING")!= -1):
        sock.send(("PONG"+args("PING")).encode())

#Send message to channel
def send(message, channel):
    print(channel+"<"+message)
    sock.send(("PRIVMSG "+channel+" :"+message+"\r\n").encode())

#Check for string is a command
def command(cmd):
    if(line.find(COMMAND+cmd)!= -1): return True

#Check if owner issued a command
def ownerCommand(cmd):
    if(command(cmd) and (user()==OWNER or user()==OWNERIRC)): return True

#Sends a message to a user
def message(message, user):
    if(ident==SERVER1 or ident==SERVER2):
          send("@"+user+" "+message+"\r\n", SERVER1)
          send("@"+user+" "+message+"\r\n", SERVER2)
    if(ident!=SERVER1 and ident!=SERVER2):
        sock.send(("PRIVMSG "+user+" :"+message+"\r\n").encode())

def random_line(file):
    return random.choice(open(file).readlines())

""" COMMANDS """
def eecho():
    if command("echo "):
        send(args("echo "), CHANNEL);

def eeval():
    if(command("eval")):
        try:
            send(str(eval(args("eval "))), CHANNEL);
        except:send("ERROR!", CHANNEL)

def suck():
    #Being a meanie :P
    if(command("suck")):
        send(args("suck ") + " sucks! What a loser!", CHANNEL)

def add():
    if(command("add")):
        try:
            aargs = args("add ")
            aargs = aargs.split(" ")
            send(str(sum([int(a) for a in aargs])), CHANNEL)
        except:
            send("All args must be ints!", CHANNEL)


def repeat():
    if ownerCommand("repeat"):
        try:
            a = args("repeat ")
            a = a.split(" ")
            b = args("repeat ")
            b = b.split(a[0])
            b = b[1]
            for x in range(0, int(a[0])):
                send(b, CHANNEL)
        except:
            send("Error!", CHANNEL)

def ttime():
    if(command("time")):
        send(time.strftime("%m/%d/%Y %H:%M:%S"), CHANNEL)

def quote():
    if command("quote") or command("q"):
        send(random_line("quotes.txt"), CHANNEL)

#Runs all commands
def runCommands():
    printLine()
    ping()
    eecho()
    eeval()
    suck()
    add()
    repeat()
    ttime()
    quote()

while True:
    #Receive text and check if it's empty
    try: text = sock.recv(2048).decode()
    except: pass
    for line in text.split("\r\n"):
        #Parse
        try:
            message = line.split(" :")
            message = message[1]
            ident = line.split("!")
            ident = ident[0].split(":")
            ident = ident[1]
        except: pass
        #Run commands
        runCommands()
