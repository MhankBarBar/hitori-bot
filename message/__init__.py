from src.utils import Dict2Obj, colorize, processTime, h2k
from lib.genshin_achievement import genshin_achievement
from lib.jadi_anime import AnimeConverter
from lib.tiktok import TikTok
from io import BytesIO
from base64 import b64encode
from json import loads
from datetime import datetime
from .lang import ind


class msgHandler:
    def __init__(self, client, message) -> None:
        self.hitori = client
        self.message = Dict2Obj(message["data"]) if isinstance(message, dict) else None
        with open("config.json", "r") as f:
            self.config = Dict2Obj(loads(f.read()))
        self.lang = ind

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
                        f"{colorize('✥', 'green')} {colorize(datetime.fromtimestamp(t).strftime('%Y-%m-%d %H:%M:%S'), 'white')} -> "
                        f"{colorize('[Exec]', 'cyan')} -> {colorize(command, 'green')} -> "
                        f"{colorize(str(args.__len__()), 'yellow')} -> {colorize(pushname, 'magenta')}")
                elif isCmd and isGroupMsg:
                    print(
                        f"{colorize('✥', 'green')} {colorize(datetime.fromtimestamp(t).strftime('%Y-%m-%d %H:%M:%S'), 'white')} -> "
                        f"{colorize('[Exec]', 'cyan')} -> {colorize(command, 'green')} -> "
                        f"{colorize(str(args.__len__()), 'yellow')} -> "
                        f"in {colorize(name or formattedTitle, 'magenta')} -> from {colorize(pushname, 'magenta')}")

                # Help and Menu Commands
                if command in ["help", "menu"]:
                    with open("assets/images/banner.jpeg", "rb") as f:
                        self.hitori.sendImage(
                            from_,
                            "data:image/png;base64," + b64encode(f.read()).decode("utf-8"),
                            "banner.jpeg",
                            self.lang.MENU.menu)
                elif command in ["p", "ping"]:
                    self.hitori.sendText(from_, f"_pong!!_\n{processTime(t, datetime.now())} seconds")
                elif command in ["about", "tentang", "info"]:
                    self.hitori.sendText(from_, self.lang.INFO)
                elif command in ["usage", "penggunaan"]:
                    if args.__len__() == 0:
                        return self.hitori.sendText(from_, self.lang.USAGE.usage)
                    pesan = self.lang.USAGE.get(args[0].lower())
                    if pesan:
                        self.hitori.sendText(from_, pesan)
                    else:
                        self.hitori.sendText(from_, self.lang.USAGE.not_available)

                # Sticker Commands
                elif command in ["take", "takestick"]:
                    if quotedMsg and quotedMsg.type == "sticker":
                        if args.__len__() < 2:
                            return self.hitori.reply(from_, self.lang.USAGE.take, id_)
                        self.hitori.sendImageAsSticker(
                            from_,
                            self.hitori.decryptMedia(quotedMsg.__dict__),
                            {"author": args[0], "pack": args[1]},
                        )
                    else:
                        self.hitori.reply(from_, self.lang.USAGE.take, id_)
                elif command in ["stiker", "sticker", "s"]:
                    if isMedia and isImage or isQuotedImage:
                        self.hitori.sendImageAsSticker(
                            from_,
                            self.hitori.decryptMedia(self.message.__dict__ if isImage else quotedMsg.__dict__),
                            {"author": self.config.authorSticker, "pack": self.config.packSticker, "keepScale": True}
                        )
                    else:
                        self.hitori.reply(from_, self.lang.USAGE.sticker, id_)
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
                        self.hitori.reply(from_, self.lang.USAGE.stickergif, id_)
                elif command in ["giachievement", "achievement", "ach"]:
                    if len(args) == 0:
                        return self.hitori.reply(from_, self.lang.USAGE.achievement, id_)
                    io = BytesIO()
                    genshin_achievement(" ".join(args)).save(io, format="PNG")
                    self.hitori.sendImageAsSticker(
                        from_,
                        "data:image/png;base64," + b64encode(io.getvalue()).decode("utf-8"),
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
                            return self.hitori.sendText(from_, f"Error: {res['msg']}")
                        self.hitori.sendImage(
                            from_,
                            "data:image/png;base64," + b64encode(io.getvalue()).decode("utf-8")
                        )
                    else:
                        self.hitori.reply(from_, self.lang.USAGE.toanime, id_)

                # Download Commands
                elif command in ["tiktok", "tt"]:
                    if len(args) == 0:
                        return self.hitori.reply(from_, self.lang.USAGE.tiktok, id_)
                    self.hitori.reply(from_, self.lang.PROCESSING, id_)
                    try:
                        tiktok = TikTok()
                        res = tiktok.download(args[0])
                        if not res.get('error'):
                            self.hitori.sendFileFromUrl(
                                from_,
                                tiktok.BASE_URL + res.get('play'),
                                "tiktok.mp4",
                                self.lang.CAPTION.tiktok % (
                                    res.get('author').get('nickname'),
                                    res.get('title'),
                                    h2k(res.get('play_count')),
                                    h2k(res.get('digg_count')),
                                    h2k(res.get('comment_count')),
                                    h2k(res.get('share_count')),
                                    res.get('duration'),
                                    res.get('music_info').get('title')
                                ),
                                id_
                            )
                        else:
                            self.hitori.reply(from_, res['error'])
                    except Exception as e:
                        print(e)
                        self.hitori.sendText(from_, f"Error: {e}")
                else:
                    pass
            except Exception as e:
                print(e)
