from __future__ import annotations
from .color import Color
from .icon import Icon
from pathlib import Path
from sys import stderr, stdout
import sys
import json
from argparse import ArgumentParser
from time import sleep
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler, FileClosedEvent, FileModifiedEvent
from signal import signal
import re
import os
from threading import Thread
if os.name == 'nt':
    try:
        from winpty import PtyProcess
    except ModuleNotFoundError:
        import pip
        pip.main(['install', 'pywinpty'])
else:
    from ptyprocess.ptyprocess import PtyProcess
    from signal import SIGWINCH



class HitoriBotHandler(FileSystemEventHandler):
    main = (Path(__file__).parent.parent / 'main.py').__str__()

    def __init__(self, skip: int = 1, nerdfont: bool = False) -> None:
        super().__init__()
        self.icon = Icon(nerdfont)
        self.skip = skip
        self.n_skip = 0
        self.shell: PtyProcess = PtyProcess.spawn(
            [sys.orig_argv[0], self.main]
        )
        print(
            Color.GREEN.box_bracket(
                Color.YELLOW.icon(self.icon.STARTED)
            ), Color.YELLOW.text('Started')
        )
        if os.name != 'nt':
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
                elif not (self.shell.exitstatus if os.name == 'nt' else self.shell.terminated):
                    std_out = self.shell.read(1024)
                    if os.name != 'nt':
                        std_out = std_out.decode()
                    stdout.write(std_out)
                    stdout.flush()
            except Exception as e:
                if self.shell.flag_eof:
                    print(
                        Color.GREEN.box_bracket(
                            Color.BLUE.icon(self.icon.FINISHED)
                        ),
                        Color.BLUE.text("Finished")
                    )
                    sleep(1)

    def on_any_event(self, event: FileClosedEvent | FileModifiedEvent):
        if ((
            os.name != 'nt' and isinstance(
                event,
                FileClosedEvent
            )) or (
                os.name == 'nt' and isinstance(event, FileModifiedEvent))
            ) and not event.is_directory and not (
            re.match(
                r'.*\.py$',
                event.src_path
            ) is None
        ):
            self.n_skip += 1
            if self.n_skip >= self.skip:
                print(
                    Color.GREEN.box_bracket(
                        Color.CYAN.icon(self.icon.RESTARTED)
                    ),
                    Color.CYAN.text('Restarted')
                )
                self.shell.close()
                self.shell: PtyProcess = PtyProcess.spawn(
                    [sys.orig_argv[0], self.main]
                )
                self.n_skip = 0

    def win_read(self):
        th = Thread(target=self.read)
        th.daemon = True
        th.start()
        while True:
            try:
                sleep(3600)
            except KeyboardInterrupt:
                print(
                    Color.GREEN.box_bracket(Color.CYAN.icon(self.icon.EXIT)),
                    Color.CYAN.text('INTERRUPTED')
                )
                break

if __name__ == "__main__":
    arg = ArgumentParser()
    actions = arg.add_subparsers(title="Actions", dest='action')
    run = actions.add_parser('run', help='run bot')
    run.add_argument('--debug', action='store_true')
    run.add_argument('--skip', type=int, default=1)
    run.add_argument('--nerdfont', action='store_true')
    config = actions.add_parser('set', help='set config json')
    config.add_argument('config', type=str, nargs="*")
    parse = arg.parse_args()
    if parse.action == "run":
        if parse.debug:
            event_handler = HitoriBotHandler(parse.skip, parse.nerdfont)
            observer = Observer()
            observer.schedule(event_handler, '.', recursive=True)
            observer.start()
            try:
                if os.name == 'nt':
                    event_handler.win_read()
                else:
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
