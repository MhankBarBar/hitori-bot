from wa_automate_socket_client import SocketClient
import message


def Joydazo(msg):
    message.msgHandler(client, msg).handler


if __name__ == '__main__':
    client = SocketClient('http://localhost:8085/', 'j0yd4z0')
    client.onMessage(Joydazo)
