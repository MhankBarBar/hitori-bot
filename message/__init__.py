from base64 import b64encode
from datetime import datetime
from io import BytesIO
from json import loads, dumps

from lib.dalle import Dalle
from lib.genshin_achievement import genshin_achievement
from lib.jadi_anime import AnimeConverter
from lib.tiktok import TikTok
from lib.chatGPT import chatGPT
from src.utils import Dict2Obj, colorize, processTime, h2k, get_config
from .lang import ind


class msgHandler:
    def __init__(self, client, message, start) -> None:
        self.hitori = client
        self.message = Dict2Obj(message["data"]) if isinstance(message, dict) else None
        self.config = get_config()
        self.lang = ind
        self.start = start

    def handler(self):
        if not self.message:
            return
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
            body = self.message.body or ""
            caption = self.message.caption or ""
            name, formattedTitle = chat.name, chat.formattedTitle
            pushname, verifiedName, formattedName = (sender.pushname, sender.verifiedName, sender.formattedName)
            pushname = pushname or verifiedName or formattedName
            botNumber = f"{self.hitori.getHostNumber()}@c.us"
            groupId = chat.groupMetadata.id if isGroupMsg else None
            groupAdmins = self.hitori.getGroupAdmins(groupId) if isGroupMsg else None

            isOwner = sender.id == self.config.owner
            isBotGroupAdmins = groupId is not None and botNumber in groupAdmins
            isGroupAdmins = groupId is not None and sender.id in groupAdmins

            chats = (
                body
                if type_ == "chat"
                else caption
                if type_ in ["image", "video"]
                else None
            )
            body = (
                body
                if (type_ == "chat" and body.startswith(self.config.prefix))
                else caption
                if type_ in ["image", "video"] and caption.startswith(self.config.prefix)
                else ""
            )

            isImage = type_ == "image"
            isVideo = type_ == "video"
            isGif = mimetype == "image/gif"

            isQuotedImage = quotedMsg and quotedMsg.type == "image"
            isQuotedVideo = quotedMsg and quotedMsg.type == "video"
            isQuotedGif = quotedMsg and quotedMsg.mimetype == "image/gif"

            command = body.split(" ")[0][1:].lower()
            args = body.split(" ")[1:]
            isCmd = body.startswith(self.config.prefix)

            if isCmd and not isGroupMsg:
                print(
                    f"{colorize('✥', 'green')} "
                    f"{colorize(datetime.fromtimestamp(t).strftime('%Y-%m-%d %H:%M:%S'), 'white')} -> "
                    f"{colorize('[Exec]', 'cyan')} -> {colorize(command, 'green')} -> "
                    f"{colorize(str(args.__len__()), 'yellow')} -> {colorize(pushname, 'magenta')}")
            elif isCmd and isGroupMsg:
                print(
                    f"{colorize('✥', 'green')} "
                    f"{colorize(datetime.fromtimestamp(t).strftime('%Y-%m-%d %H:%M:%S'), 'white')} -> "
                    f"{colorize('[Exec]', 'cyan')} -> {colorize(command, 'green')} -> "
                    f"{colorize(str(args.__len__()), 'yellow')} -> "
                    f"in {colorize(name or formattedTitle, 'magenta')} -> from {colorize(pushname, 'magenta')}")

            # Help and Menu Commands
            if command in ["help", "menu"]:
                if len(args) == 0:
                    with open("assets/images/banner.jpeg", "rb") as f:
                        self.hitori.sendImage(
                            from_,
                            "data:image/png;base64," + b64encode(f.read()).decode("utf-8"),
                            "banner.jpeg",
                            self.lang.MENU.menu)
                else:
                    if pesan := self.lang.MENU.get(args[0].lower()):
                        self.hitori.sendText(from_, pesan)
                    else:
                        self.hitori.sendText(from_, self.lang.MENU.not_available)
            elif command in ["p", "ping"]:
                self.hitori.sendText(from_, f"_pong!!_\n{processTime(t, datetime.now())} seconds")
            elif command in ["about", "tentang", "info"]:
                self.hitori.sendText(from_, self.lang.INFO)
            elif command in ["usage", "penggunaan"]:
                if len(args) == 0:
                    return self.hitori.sendText(from_, self.lang.USAGE.usage)
                if pesan := self.lang.USAGE.get(args[0].lower()):
                    self.hitori.sendText(from_, pesan)
                else:
                    self.hitori.sendText(from_, self.lang.USAGE.not_available)

            # Other Commands
            elif command == "runtime":
                total = datetime.now() - self.start
                self.hitori.sendText(from_, f"Bot has been running for {str(total).split('.')[0]}")

            # Sticker Commands
            elif command in ["take", "takestick"]:
                if quotedMsg and quotedMsg.type == "sticker":
                    if len(args) < 2:
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

            # Genshin Impact Commands
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
                    res = anime.to_anime(
                        self.hitori.decryptMedia(self.message.__dict__ if isImage else quotedMsg.__dict__))
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
            elif command == "dalle":
                if len(args) == 0:
                    return self.hitori.reply(from_, self.lang.USAGE.dalle, id_)
                elif len(" ".join(args)) > 100:
                    return self.hitori.reply(from_, "terlalu panjang", id_)
                self.hitori.reply(from_, "Mohon tunggu selama kurang lebih 2 menit", id_)
                dalle = Dalle(" ".join(args), sender.id.split("@")[0])
                res = dalle.generate()
                if isinstance(res, str):
                    self.hitori.sendImage(
                        from_,
                        res,
                        "dalle.png",
                        f"Result for {' '.join(args)}"
                    )
                else:
                    self.hitori.sendText(from_, "Dalle error")

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

            # Group Only Commands
            elif command in ["add", "tambah"]:
                if not isGroupMsg:
                    return self.hitori.reply(from_, self.lang.ERR.not_group, id_)
                if len(args) == 0:
                    return self.hitori.reply(from_, self.lang.USAGE.add, id_)
                if not isGroupAdmins:
                    return self.hitori.reply(from_, self.lang.ERR.not_admin, id_)
                if not isBotGroupAdmins:
                    return self.hitori.reply(from_, self.lang.ERR.bot_not_admin, id_)
                if check := self.hitori.checkNumberStatus(args[0]):
                    if check['status'] != 200:
                        return self.hitori.reply(from_, self.lang.ERR.not_contact, id_)
                add = self.hitori.addParticipant(from_, f"{args[0]}@c.us")
                if add is True:
                    self.hitori.reply(from_, self.lang.SUCCESS.add, id_)
                else:
                    self.hitori.reply(from_, self.lang.ERR.add % args[0], id_)
            elif command in ["kick", "tendang"]:
                if not isGroupMsg:
                    return self.hitori.reply(from_, self.lang.ERR.not_group, id_)
                if len(mentionedJidList) == 0:
                    return self.hitori.reply(from_, self.lang.USAGE.kick, id_)
                if not isGroupAdmins:
                    return self.hitori.reply(from_, self.lang.ERR.not_admin, id_)
                if not isBotGroupAdmins:
                    return self.hitori.reply(from_, self.lang.ERR.bot_not_admin, id_)
                self.hitori.sendTextWithMentions(
                    from_,
                    f"Goodbye {', '.join(['@' + x.split('@')[0] for x in mentionedJidList])}"
                )
                for x in mentionedJidList:
                    self.hitori.removeParticipant(from_, x)
            elif command == "promote":
                if not isGroupMsg:
                    return self.hitori.reply(from_, self.lang.ERR.not_group, id_)
                if len(mentionedJidList) == 0:
                    return self.hitori.reply(from_, self.lang.USAGE.promote, id_)
                if not isGroupAdmins:
                    return self.hitori.reply(from_, self.lang.ERR.not_admin, id_)
                if not isBotGroupAdmins:
                    return self.hitori.reply(from_, self.lang.ERR.bot_not_admin, id_)
                for x in mentionedJidList:
                    self.hitori.promoteParticipant(from_, x)
                self.hitori.sendTextWithMentions(
                    from_,
                    f"Congrats {', '.join(['@' + x.split('@')[0] for x in mentionedJidList])} for being promoted"
                )
            elif command == "demote":
                if not isGroupMsg:
                    return self.hitori.reply(from_, self.lang.ERR.not_group, id_)
                if len(mentionedJidList) == 0:
                    return self.hitori.reply(from_, self.lang.USAGE.demote, id_)
                if not isGroupAdmins:
                    return self.hitori.reply(from_, self.lang.ERR.not_admin, id_)
                if not isBotGroupAdmins:
                    return self.hitori.reply(from_, self.lang.ERR.bot_not_admin, id_)
                for x in mentionedJidList:
                    self.hitori.demoteParticipant(from_, x)
                self.hitori.sendTextWithMentions(
                    from_,
                    f"Sadly {', '.join(['@' + x.split('@')[0] for x in mentionedJidList])} for being demoted"
                )
            elif command in ["mentionall", "all", "everyone"]:
                if not isGroupMsg:
                    return self.hitori.reply(from_, self.lang.ERR.not_group, id_)
                if not isGroupAdmins:
                    return self.hitori.reply(from_, self.lang.ERR.not_admin, id_)
                if len(args) == 0:
                    return self.hitori.reply(from_, self.lang.USAGE.mentionall, id_)
                members = self.hitori.getGroupMembersId(groupId)
                msg = f"{' '.join(args)}\n\n {', '.join(['@' + x.split('@')[0] for x in members])}"
                self.hitori.sendTextWithMentions(from_, msg)
            elif command in ["grouplink", "linkgrup", "linkgroup"]:
                if not isGroupMsg:
                    return self.hitori.reply(from_, self.lang.ERR.not_group, id_)
                if not isGroupAdmins:
                    return self.hitori.reply(from_, self.lang.ERR.not_admin, id_)
                if not isBotGroupAdmins:
                    return self.hitori.reply(from_, self.lang.ERR.bot_not_admin, id_)
                link = self.hitori.getGroupInviteLink(groupId)
                self.hitori.sendLinkWithAutoPreview(from_, link, link)
            elif command == "setgroupicon":
                if not isGroupMsg:
                    return self.hitori.reply(from_, self.lang.ERR.not_group, id_)
                if not isGroupAdmins:
                    return self.hitori.reply(from_, self.lang.ERR.not_admin, id_)
                if not isBotGroupAdmins:
                    return self.hitori.reply(from_, self.lang.ERR.bot_not_admin, id_)
                if isMedia and isImage or isQuotedImage:
                    self.hitori.setGroupIcon(
                        groupId,
                        self.hitori.decryptMedia(self.message.__dict__ if isImage else quotedMsg.__dict__)
                    )
                    self.hitori.reply(from_, self.lang.SUCCESS.set_group_icon, id_)
                else:
                    self.hitori.reply(from_, self.lang.ERR.not_image, id_)

            # Owner Commands
            elif command == "setprefix":
                # this command disabled for now
                return
                if not isOwner:
                    return self.hitori.reply(from_, self.lang.ERR.not_owner, id_)
                if len(args) == 0:
                    return self.hitori.reply(from_, self.lang.USAGE.setprefix, id_)
                self.config.prefix = args[0]
                with open("config.json", "w") as f:
                    f.write(dumps(self.config.__dict__, indent=4))
                self.hitori.reply(from_, self.lang.SUCCESS.set_prefix % args[0], id_)

            # Other Commands
            elif command in ["chatgpt", "gpt"]:
                if len(args) == 0:
                    return self.hitori.reply(from_, self.lang.USAGE.chatgpt, id_)
                self.hitori.reply(from_, self.lang.PROCESSING, id_)
                self.hitori.reply(from_, chatGPT(" ".join(args)), id_)

        except Exception as e:
            print(e)
