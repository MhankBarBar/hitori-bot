from src.utils import Dict2Obj, colorize
from lib.genshin_achievement import genshin_achievement
from lib.jadi_anime import AnimeConverter
from io import BytesIO
from base64 import b64encode
from json import loads
from .lang import ind


class msgHandler:
    def __init__(self, client, message) -> None:
        self.hitori = client
        self.message = Dict2Obj(message["data"]) if isinstance(message, dict) else None
        with open("config.json", "r") as f:
            self.config = Dict2Obj(loads(f.read()))

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
                botNumber = self.hitori.getHostNumber() + "@c.us"
                groupId = chat.groupMetadata.id if isGroupMsg else None
                groupAdmins = self.hitori.getGroupAdmins(groupId) if isGroupMsg else None

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
                    print(
                        f"{colorize('[Exec]', 'cyan')} -> {colorize(command, 'green')} -> {colorize(str(args.__len__()), 'yellow')}")
                elif isCmd and isGroupMsg:
                    print(
                        f"{colorize('[Exec]', 'cyan')} -> {colorize(command, 'green')} -> {colorize(str(args.__len__()), 'yellow')} -> in {colorize(name or formattedTitle, 'magenta')} -> from {colorize(pushname, 'magenta')}")

                # Help and Menu Commands
                if command in ["help", "menu"]:
                    self.hitori.sendText(from_, ind.Menu(self.config.prefix).help())
                elif command == "ping":
                    self.hitori.sendText(from_, "pong")

                # Sticker Commands
                elif command in ["take", "takestick"]:
                    if quotedMsg and quotedMsg.type == "sticker":
                        self.hitori.sendImageAsSticker(
                            from_,
                            self.hitori.decryptMedia(quotedMsg.__dict__),
                            {"author": self.config.authorSticker, "pack": self.config.packSticker},
                        )
                    else:
                        self.hitori.sendText(from_, "Reply sticker with !take")
                elif command in ["stiker", "sticker", "s"]:
                    if isMedia and isImage or isQuotedImage:
                        self.hitori.sendImageAsSticker(
                            from_,
                            self.hitori.decryptMedia(self.message.__dict__ if isImage else quotedMsg.__dict__),
                            {"author": self.config.authorSticker, "pack": self.config.packSticker, "keepScale": True}
                        )
                    else:
                        self.hitori.sendText(from_, "Reply image with !stiker")
                elif command in ["stikergif", "stickergif", "sgif"]:
                    if isMedia and isGif or isVideo or isQuotedGif or isQuotedVideo:
                        self.hitori.sendMp4AsSticker(
                            from_,
                            self.hitori.decryptMedia(self.message.__dict__ if isGif or isVideo else quotedMsg.__dict__),
                            None,
                            {
                                "author": self.config.authorSticker,
                                "pack": self.config.packSticker,
                                "keepScale": True,
                                "crop": False,
                                "loop": 0,
                            }
                        )
                    else:
                        self.hitori.sendText(from_, "Reply gif with !stikergif")
                elif command in ["giachievement", "achievement", "ach"]:
                    if len(args) == 0:
                        return self.hitori.sendText(from_, "Usage: !achievement <text>")
                    io = BytesIO()
                    genshin_achievement(" ".join(args)).save(io, format="PNG")
                    base64img = "data:image/png;base64," + b64encode(io.getvalue()).decode("utf-8")
                    self.hitori.sendImageAsSticker(
                        from_,
                        base64img,
                        {"author": self.config.authorSticker, "pack": self.config.packSticker, "keepScale": True}
                    )

                # Image Commands
                elif command in ["jadianime", "toanime"]:
                    if isMedia and isImage or isQuotedImage:
                        io = BytesIO()
                        anime = AnimeConverter()
                        res = anime.to_anime(self.hitori.decryptMedia(self.message.__dict__ if isImage else quotedMsg.__dict__))
                        if not isinstance(res, dict):
                            res.save(io, format="PNG")
                        else:
                            return self.hitori.sendText(from_, f"Error: res['msg']")
                        self.hitori.sendImage(
                            from_,
                            "data:image/png;base64," + b64encode(io.getvalue()).decode("utf-8"),
                            {"author": self.config.authorSticker, "pack": self.config.packSticker, "keepScale": True}
                        )
                    else:
                        self.hitori.sendText(from_, "Reply image with !jadianime")
                else:
                    pass
            except Exception as e:
                print(e)
