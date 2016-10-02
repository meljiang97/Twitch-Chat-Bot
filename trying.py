import socket               # Used to connect to the server using a socket
from time import sleep      # Used to timeout the recieved messasges
import re                   # Used for regular expressions
import threading

HOST = "irc.twitch.tv"          #TWITCH HOST
NICK = "testingforbot"     #username (make sure its all lower case)
PORT = 6667                     #Port connecting to
PASS = "oauth:3g4urmaropl7j9ltoabjsg33161zog"   #OAuth Key (acts as a password)
JOIN = "sir_williamwallace"

# A regular expression used to find the response (I think... took it off of the code online)
#CHAT_MSG = re.compile(r"^:\w+!\w+@\w+\.tmi\.twitch\.tv PRIVMSG #\w+ :")

question_list = ["How many taste buds does an average human tongue have(3000)?",
                 "What percentage of your brain is water?(80%)"]

def listening_thread():
    #Connects to a server as a certain user into a certain chat stream whatnot thing
    print("Connecting to server...")
    s = socket.socket()
    s.connect((HOST, PORT))
    s.send(bytes("PASS " + PASS + "\r\n", "UTF-8"))
    s.send(bytes("NICK " + NICK + "\r\n", "UTF-8"))
    s.send(bytes("JOIN #" + JOIN + " \r\n", "UTF-8"))
    print("Connected!")
    readbuffer = ""
    MODT = False
    while True:
        print("Waiting for messages...")
        readbuffer = readbuffer + str(s.recv(1024),"UTF-8")
        temp = readbuffer.split("\n")
        readbuffer = temp.pop()
        for line in temp:
            if (line[0] == "PING"):
                s.send("PONG %s\r\n" % line[1])
            else:
                parts = line.split(":")
                if ("QUIT" not in parts[1] and "JOIN" not in parts[1] and "PART" not in parts[1]):
                    try:
                        message = parts[2][:len(parts[2]) - 1]
                    except:
                        message = ""
                    usernamesplit = parts[1].split("!")
                    username = usernamesplit[0]
                    if (MODT):
                        print(username + ": " + message)
                        message.lower()
                        if (message == "hey"):
                            send_message("Welcome to the stream, " + username)
                        if message.lower() == "stars":
                            send_message("   * \n" +
                                         "  ***\n" +
                                         " *****\n" +
                                         "  ***\n" +
                                         " *   *\n")
                        if message.lower() == "smile":
                            send_message(":)")
                        if message.lower() == "shrug":
                            send_message("¯\_(ツ)_/¯")
                    for l in parts:
                        if "End of /NAMES list" in l:
                            MODT = True

        sleep(1.5)
        k = take_input(s)
        if k:
            break

class myThread(threading.Thread):
    def __init__(self, threadID, name, threadfunc):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.threadfunc = threadfunc
    def run(self):
        print("Starting " + self.name)
        self.threadfunc()
        print ("Existing " + self.name)


def take_input(s):
    while True:
        command = input()
        if command == "quit":
            s.close()
            print('closing')
            return True
        elif command[:3] == "ban":
            print(command)
        elif command == "join":
            print('joining different')
        else:
            print("not a valid command")

# Create new threads
thread1 = myThread(1, "Thread-1", take_input)
thread2 = myThread(2, "Thread-2", listening_thread)

#Start new threads
'''thread1.start()
thread2.start()

thread1.join()'''

listening_thread()


# try:
#     _thread.start_new_thread(listening_thread)
# except:
#     print("Unable to start thread")

#sends a given message to a chatbox
def send_message(message):
    #sends a given message to a chatbox
    if (len(message) > 0):
        s.send(bytes("PRIVMSG #" + JOIN + " :" + message + "\r\n", "UTF-8"))

#closes the socket
#s.close()
