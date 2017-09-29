from getpass import getpass
import os, sys, tty, termios
import fcntl, pty

class LoginScreen(object):
    def __init__(self, display_q):
        self.display_q = display_q
        self.display_q.put("Paper Terminal v0.1 login\n\r")

    def getchr():
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        try:
            tty.setraw(sys.stdin.fileno())
            ch = sys.stdin.read(1)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        return ch

    def run(self):
        while True:
            self.display_q.put("Login: ")
            print("Login: ")
            self.username = ""
            while True:
                c = self.getchr()
                self.display_q.put(c)
                if c == "\r":
                    self.display_q.put("\n\r")
                    break
                else:
                    self.username += c
            self.display_q.put("Password:\n\r")
            self.password = getpass("Password: ")
            if pam.authenticate(self.username, self.password):
                self.password = None # such security! :D
                self.authenticated = True
                break
            else:
                self.authenticated = False
                display_q.put("Wrong user/pass\n\r")

