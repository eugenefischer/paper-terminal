#!/usr/bin/env python
from __future__ import print_function, unicode_literals
# import signal
from paperterm import display_thread
from paperterm import login_screen
from paperterm import shell_thread
from logging.handlers import SysLogHandler
import logging
import argparse
import sys
import Queue

parser = argparse.ArgumentParser()
parser.add_argument("--no-loadkeys", help="Disable loadkeys being ran prior to shell", action="store_true")
parser.add_argument("--loadkeys-config", help="Config file for key remapping", default='/home/pi/keys')
parser.add_argument("--term-width", help="Width of the terminal", default=49, type=int)
parser.add_argument("--term-height", help="Height of the terminal", default=8, type=int)
parser.add_argument("--log-file", help="Location of logfile", default="debug.log")
parser.add_argument("--use-syslog", help="Use syslog for logging", action="store_true")

args = parser.parse_args()

logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s:%(levelname)s:%(module)sf:%(funcName)s: %(message)s"
    )

logger = logging.getLogger()

if args.use_syslog:
    logger.addHandler(SysLogHandler('/dev/log'))
else:
    logger.addHandler(logging.FileHandler(args.log_file))

logging.info("--------[ INIT ]--------")

# def signal_handler(signal, frame):
#     PaperTerminal.KILLALL = True
#     sys.exit(0)

TERM_WIDTH=args.term_width
TERM_HEIGHT=args.term_height

def start():
    display_q = Queue.Queue()

    logging.debug("Starting DisplayThread with dimensions: %s x %s" % (TERM_WIDTH, TERM_HEIGHT))
    display_thread = DisplayThread(TERM_WIDTH, TERM_HEIGHT, display_q)
    display_thread.start()
    logging.debug("DisplayThread started sucessfully")

    display_thread.cursor_enabled = False
    login_screen = LoginScreen(display_q)
    login_screen.run()
    display_thread.cursor_enabled = True

    if login_screen.authenticated:
        shell_thread = ShellThread(TERM_WIDTH, TERM_HEIGHT, login_screen.username, display_q)
        shell_thread.start()
    else:
        sys.exit(0)

    while shell_thread.is_alive():
        shell_thread.getchr()
        # shell_thread.write(r)

    display_thread.join()

if __name__ == "__main__":
    import logging
    if not args.no_loadkeys:
        try:
            import subprocess
            subprocess.call(['loadkeys', args.loadkeys_config])
        except Exception as e:
            logging.exception("loadkeys error")
    try:
        start()
    except Exception as e:
        logging.exception("message")

    # signal.signal(signal.SIGINT, signal_handler)

