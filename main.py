from wa_automate_socket_client import SocketClient
import message

HOST = 'http://localhost:8085/'
KEY = 'j0yd4z0'


def Joydazo(msg):
    message.msgHandler(client, msg).handler()


def onIncomingCall(call):
    # Send a message to the caller then block the caller
    client.sendText(call['data']['peerJid'], 'Sorry, unable to answer calls. I am a bot.')
    client.contactBlock(call['data']['peerJid'])


def onParticipantsChanged(participantsChanged):
    # For now, im disabling this feature
    return None
    data = participantsChanged['data']
    me = f"{client.getHostNumber()}@c.us"
    groupInfo = client.getGroupInfo(data['chat'])

    if data['action'] == 'add' and data['who'] != me:
        client.sendTextWithMentions(
            data['chat'],
            message.ind.WELCOME % (data['who'].split('@')[0], groupInfo['title']),
            False,
            [data['who']]
        )
    elif data['action'] == 'remove' and data['who'] != me:
        client.sendTextWithMentions(
            data['chat'],
            message.ind.GOODBYE % (data['who'].split('@')[0]),
            False,
            [data['who']]
        )


if __name__ == '__main__':
    print(message.lang.ind.BANNER)
    print("Created by: @MhankBarBar")
    print("Source Code: https://github.com/MhankBarBar/hitori-bot")
    print("Found a bug or error ? Report it here: https://github.com/MhankBarBar/hitori-bot/issues")
    client = SocketClient(HOST, KEY)
    client.onMessage(Joydazo)
    client.onIncomingCall(onIncomingCall)
    client.onGlobalParticipantsChanged(onParticipantsChanged)
