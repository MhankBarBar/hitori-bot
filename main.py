from wa_automate_socket_client import SocketClient
import message


def Joydazo(msg):
    message.msgHandler(client, msg).handler()


if __name__ == '__main__':
    print(message.lang.ind.BANNER)
    print("Created by: @MhankBarBar")
    print("Source Code: https://github.com/MhankBarBar/hitori-bot")
    print("Found a bug or error ? Report it here: https://github.com/MhankBarBar/hitori-bot/issues")
    client = SocketClient('http://localhost:8085/', 'j0yd4z0')
    client.onMessage(Joydazo)
