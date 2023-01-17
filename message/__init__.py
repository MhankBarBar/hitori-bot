from src.utils import Dict2Obj, colorize
from lib.genshin_achievement import genshin_achievement
from io import BytesIO
from base64 import b64encode
from json import loads


class msgHandler:
    def __init__(self, client, message) -> None:
        self.client = client
        self.message = Dict2Obj(message["data"]) if isinstance(message, dict) else None
        with open("config.json", "r") as f:
            self.config = Dict2Obj(loads(f.read()))

    @property
    def handler(self):
        if self.message:
            try:
                type_, id_, from_, t, sender, isGroupMsg, chat, caption, isMedia, mimetype, quotedMsg, quotedMsgObj, mentionedJidList = (
                    self.message["type"],
                    self.message["id"],
                    self.message["from"],
                    self.message.t,
                    self.message.sender,
                    self.message.isGroupMsg,
                    self.message.chat,
                    self.message.caption,
                    self.message.isMedia,
                    self.message.mimetype,
                    self.message.quotedMsg,
                    self.message.quotedMsgObj,
                    self.message.mentionedJidList,
                )
                body = self.message.body if self.message.body else ""
                caption = self.message.caption if self.message.caption else ""
                name, formattedTitle = chat.name, chat.formattedTitle
                pushname, verifiedName, formattedName = (sender.pushname, sender.verifiedName, sender.formattedName)
                pushname = pushname or verifiedName or formattedName
                botNumber = self.client.getHostNumber() + "@c.us"
                groupId = chat.groupMetadata.id if isGroupMsg else None
                groupAdmins = self.client.getGroupAdmins(groupId) if isGroupMsg else None

                isImage = type_ == "image"
                isVideo = type_ == "video"
                isGif = mimetype == "image/gif"

                isQuotedImage = quotedMsg and quotedMsg.type == "image"
                isQuotedVideo = quotedMsg and quotedMsg.type == "video"
                isQuotedGif = quotedMsg and quotedMsg.mimetype == "image/gif"

                chats = body if type == "chat" else caption if (type == "image" or type == "video") else None
                body = body if (type_ == "chat" and body.startswith(self.config.prefix)) else caption \
                    if (type_ == "image" or type_ == "video") and caption.startswith(self.config.prefix) \
                    else ""
                command = body.split(" ")[0][1:].lower()
                args = body.split(" ")[1:]
                isCmd = body.startswith(self.config.prefix)

                if isCmd and not isGroupMsg:
                    print(f"{colorize('[Exec]','cyan')} -> {colorize(command, 'green')} -> {colorize(str(args.__len__()), 'yellow')}")
                elif isCmd and isGroupMsg:
                    print(f"{colorize('[Exec]','cyan')} -> {colorize(command, 'green')} -> {colorize(str(args.__len__()), 'yellow')} -> in {colorize(name, 'magenta')} -> from {colorize(pushname, 'magenta')}")

                if command in ["help", "menu"]:
                    help_text = (f"\n"
                                 f"*Genshin Impact Achievement Generator*\n"
                                 f"*Command:*\n"
                                 f"*{self.config.prefix}achievement* _text_\n"
                                 f"*Example:*\n"
                                 f"*{self.config.prefix}achievement* _Hello World_\n"
                                 f"\n"
                                 f"*{self.config.prefix}help* _to show this message_\n"
                                 f"\n"
                                 f"*{self.config.prefix}ping* _to show bot's ping_\n"
                                 f"\n"
                                 f"*Sticker Commands:*\n"
                                 f"*{self.config.prefix}sticker* _to reply image or gif (todo)_\n"
                                 f"\n"
                                 f"*Sticker Taker Commands:*\n"
                                 f"*{self.config.prefix}take* _to reply sticker_\n"
                                 )
                    self.client.sendText(from_, help_text)
                elif command == "ping":
                    self.client.sendText(from_, "pong")
                elif command in ["take", "takestick"]:
                    if quotedMsg and quotedMsg.type == "sticker":
                        self.client.sendImageAsSticker(
                            from_,
                            self.client.decryptMedia(quotedMsg.__dict__),
                            {"author": self.config.authorSticker, "pack": self.config.packSticker},
                        )
                    else:
                        self.client.sendText(from_, "Reply sticker with !take")
                elif command in ["stiker", "sticker"]:
                    if isMedia and isImage or isQuotedImage:
                        self.client.sendImageAsSticker(
                            from_,
                            self.client.decryptMedia(self.message.__dict__ if isImage else quotedMsg.__dict__),
                            {"author": self.config.authorSticker, "pack": self.config.packSticker, "keepScale": True}
                        )
                    else:
                        self.client.sendText(from_, "Reply image with !stiker")
                elif command in ["giachievement", "achievement"]:
                    if len(args) == 0:
                        return self.client.sendText(from_, "Usage: !achievement <text>")
                    io = BytesIO()
                    genshin_achievement(" ".join(args)).save(io, format="PNG")
                    base64img = "data:image/png;base64," + b64encode(io.getvalue()).decode("utf-8")
                    self.client.sendImageAsSticker(
                        from_,
                        base64img,
                        {"author": self.config.authorSticker, "pack": self.config.packSticker, "keepScale": True}
                    )
                else:
                    pass
            except Exception as e:
                print(e)
