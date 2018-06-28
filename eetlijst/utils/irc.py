import socket, string

#some user data, change as per your taste
SERVER = 'irc.freenode.net'
PORT = 6667
NICKNAME = 'iotard_ds4reboot_caller2'
CHANNEL = '#iotard'

IRC = socket.socket(socket.AF_INET, socket.SOCK_STREAM)


def irc_conn():
    # open a connection with the server
    try:
        IRC.connect((SERVER, PORT))
    except:
        pass


def send_data(command):
    # simple function to send data through the socket
    IRC.send(bytes(command + '\n', 'utf-8'))


def join(channel):
    # join the channel
    try:
        send_data("JOIN %s" % channel)
    except:
        pass


def disconnect():
    # join the channel
    send_data("QUIT")


def login(nickname, username='user', password = None, realname='Pythonist', hostname='Helena', servername='Server'):
    # send login data (customizable)
    send_data("USER %s %s %s %s" % (username, hostname, servername, realname))
    send_data("NICK " + nickname)


def send_irc_broad():
    irc_conn()
    login(NICKNAME)
    join(CHANNEL)

    send_data("PRIVMSG " + CHANNEL + " :RING BROADCAST ALL")

    # disconnect()
