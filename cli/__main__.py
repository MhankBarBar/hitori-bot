from __future__ import annotations
from .color import Color
from pathlib import Path
from sys import stderr, stdout
import sys
import json
from argparse import ArgumentParser
from time import sleep
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler, FileClosedEvent
from ptyprocess.ptyprocess import PtyProcess
from signal import signal, SIGWINCH
import re
import os


class HitoriBotHandler(FileSystemEventHandler):
    main = (Path(__file__).parent.parent / 'main.py').__str__()

    def __init__(self) -> None:
        super().__init__()
        self.shell: PtyProcess = PtyProcess.spawn(
            [sys.orig_argv[0], self.main]
        )
        print(
            Color.GREEN.box_bracket(
                Color.YELLOW.icon(0xf2dd)
            ) + Color.YELLOW.text(' Started')
        )
        signal(SIGWINCH, self.terminal_on_change)

    def terminal_on_change(self, *args, **kwargs):
        if not self.shell.closed:
            tsize = os.get_terminal_size()
            self.shell.setwinsize(tsize.lines, tsize.columns)

    def read(self):
        while True:
            try:
                if isinstance(
                    self.shell.exitstatus,
                    int
                ) or self.shell.flag_eof:
                    sleep(1)
                elif not self.shell.terminated:
                    stdout.write(self.shell.read(1024).decode())
                    stdout.flush()
            except Exception:
                if self.shell.flag_eof:
                    print(
                        Color.GREEN.box_bracket(
                            Color.BLUE.icon(0xebe9)
                        ),
                        Color.BLUE.text("Finished")
                    )
                    sleep(1)

    def on_any_event(self, event: FileClosedEvent):
        if isinstance(
            event,
            FileClosedEvent
        ) and not event.is_directory and not (
            re.match(
                r'.*\.py$',
                event.src_path
            ) is None
        ):
            print(
                Color.GREEN.box_bracket(
                    Color.CYAN.icon(0xead2)
                ),
                Color.CYAN.text('Restarted')
            )
            self.shell.close()
            self.shell: PtyProcess = PtyProcess.spawn(
                [sys.orig_argv[0], self.main]
            )


if __name__ == "__main__":
    arg = ArgumentParser()
    actions = arg.add_subparsers(title="Actions", dest='action')
    run = actions.add_parser('run', help='run bot')
    run.add_argument('--debug', action='store_true')
    config = actions.add_parser('set', help='set config json')
    config.add_argument('config', type=str, nargs="*")
    parse = arg.parse_args()
    if parse.action == "run":
        if parse.debug:
            event_handler = HitoriBotHandler()
            observer = Observer()
            observer.schedule(event_handler, '.', recursive=True)
            observer.start()
            try:
                event_handler.read()
            finally:
                observer.stop()
                observer.join()
        else:
            os.system(sys.orig_argv[0] + ' ' + HitoriBotHandler.main)
    elif parse.action == "set":
        config = json.load(open('./config.json'))
        if parse.config.__len__() < 1:
            arg.print_help(stderr)
        elif parse.config[0] not in config:
            arg.print_help(stderr)
        else:
            config[parse.config[0]] = parse.config[1]
            json.dump(config, open('./config.json', 'w'), indent=4)
