
import praw
from functions import clear, select_feed, make_feed, edit_settings, edit_feed, delete_feed, send_feed
import os
import random
import emailing

reddit = praw.Reddit(client_id='[REDACTED]',
                     client_secret='[REDACTED]',
                     user_agent='[REDACTED]')

if __name__ == "__main__":
    clear()
    while True:
        try:
            clear()
            command = input("Main menu commands:\n\"settings\": accesses the settings for the program\n\"new\": makes a new feed\n\"edit\": edits a feed\n\"delete\": deletes a feed\n\"send\": sends a feed to your inbox\n\"exit\": exits the program\nEnter a command: ")
            command = command.lower().strip()
            if command == "settings":
                try:
                    clear()
                    edit_settings()
                except KeyboardInterrupt:
                    clear()
                    input("Operation canceled. Press enter to continue. ")
                    continue
            elif command == "send":
                try:
                    clear()
                    name, feed = select_feed()
                    send_feed(reddit, name, feed)
                    clear()
                except KeyboardInterrupt:
                    clear()
                    input("Operation canceled. Press enter to continue. ")
                    continue
            elif command == "new":
                try:
                    make_feed(reddit)
                except KeyboardInterrupt:
                    clear()
                    input("Operation canceled. Press enter to continue. ")
                    continue
            elif command == "edit":
                try:
                    edit_feed(reddit)
                except KeyboardInterrupt:
                    clear()
                    input("Operation canceled. Press enter to continue. ")
                    continue
            elif command == "delete":
                try:
                    clear()
                    delete_feed()
                except KeyboardInterrupt:
                    clear()
                    input("Operation canceled. Press enter to continue. ")
                    continue
            elif command == "exit":
                raise KeyboardInterrupt
            else:
                input("Invalid command. Press enter to continue. ")
                continue
        except KeyboardInterrupt:
            clear()
            try:
                input("Exiting. Press enter to continue. ")
            except:
                pass
            clear()
            break
