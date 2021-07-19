import datetime
import functions
import os
import getpass
import json
import shutil

basename = os.path.dirname(os.path.realpath(__file__))

if __name__ == "__main__":
    functions.clear()
    password = getpass.getpass("Password: ")
    if not functions.login(password):
        import sys
        print("Invalid password")
        sys.exit(1)


def read():
    shutil.copyfile(os.path.join(basename, "journal.txt"),
                    os.path.join(basename, "temp.txt"))
    temp = functions.decodepath(os.path.join(
        basename, "temp.txt"), delete=False)
    with open(temp) as f:
        string = f.read()
    temp = json.loads(string)
    if type(temp) != dict:
        journal = json.loads(temp)
    else:
        journal = temp
    os.remove(os.path.join(basename, "temp.txt"))
    return journal


def write(journal):
    with open(os.path.join(basename, "temp.txt"), "w") as f:
        json.dump(journal, f)
    save = functions.encodepath(os.path.join(basename, "temp.txt"))
    with open(save) as old:
        with open(os.path.join(basename, "journal.txt"), "w") as new:
            new.write(old.read())
    os.remove(os.path.join(basename, "temp.enc"))
    journal = read()
    return journal


def chunk(l, n):
    x = [l[i:i + n] for i in range(0, len(l), n)]
    return x


def select(journal):
    chunked = chunk(list(journal.keys()), 5)
    pointer = 0
    selected = False
    while not selected:
        functions.clear()
        message = "\"f\": View next 5 entries\n\"b\": View previous 5 entries\n\"0-4\": Select the entry corresponding with that number\n\nPage: {}/{}\n".format(
            pointer + 1, len(chunked))
        if len(list(journal.keys())) == 0:
            input("No entries found. Press enter to continue. ")
            return None
        for i in range(len(chunked[pointer])):
            message += "{}: {}\n".format(i, chunked[pointer][i])
        message = message.strip()
        print(message)
        selection = input("Select an option: ")
        try:
            selection = int(selection)
        except:
            if selection.strip().lower().lstrip() == "f":
                if pointer + 1 < len(chunked):
                    pointer += 1

            elif selection.strip().lower().lstrip() == "b":
                if pointer > 0:
                    pointer -= 1
            continue
        if selection not in list(range(0, len(chunked[pointer]))):
            continue
        return {chunked[pointer][selection]: journal[chunked[pointer][selection]]}


if not os.path.exists(os.path.join(basename, "journal.txt")):
    journal = write("{}")
else:
    journal = read()

while True:
    functions.clear()
    print("Journal")
    print("Use Ctrl+C to return back to this menu, or use it here to exit.\n")
    try:
        action = input(
            "1: Add an entry\n2: Delete an entry\n3: Read an entry\nSelect an option: ")
    except KeyboardInterrupt:
        break
    try:
        action = int(action)
    except:
        continue
    if action > 3 or action < 1:
        continue
    if action == 1:
        try:
            functions.clear()
            entry = input("Type your entry here.\n\n")
            functions.clear()
            title = input("Title (leave blank for no title): ")
            functions.clear()
            if title == "":
                title = "No Title"
            confirm = input(
                "Title: {}\n\n{}\n\nDo you want to add this entry (y/n)? ".format(title, entry))
            if confirm.strip().lstrip().lower() != "y":
                continue

            dt = datetime.datetime.now()
            journal[dt.strftime("%m/%d/%Y at %I:%M:%S %p")
                    ] = "{}|{} ".format(title, entry)
            journal = write(journal)
            functions.clear()
            input("Entry added. Press enter to continue. ")
        except KeyboardInterrupt:
            continue
    elif action == 2:
        try:
            selection = select(journal)
            if selection is None:
                continue
            functions.clear()
            print("Date: {}\nTitle: {}\n\n{}".format(list(selection.keys())[0], selection[list(
                selection.keys())[0]].split("|")[0], "|".join(selection[list(selection.keys())[0]].split("|")[1:])))
            confirm = input(
                "Are you sure you want to delete this entry (y/n)? ")
            if confirm.lower().strip().lstrip() != "y":
                continue
            del journal[list(selection.keys())[0]]
            journal = write(journal)
            functions.clear()
            input("Entry deleted. Press enter to continue. ")
        except KeyboardInterrupt:
            continue
    elif action == 3:
        try:
            selection = select(journal)
            if selection is None:
                continue
            functions.clear()
            print("Date: {}\nTitle: {}\n\n{}".format(list(selection.keys())[0], selection[list(
                selection.keys())[0]].split("|")[0], "|".join(selection[list(selection.keys())[0]].split("|")[1:])))
            input("\nPress enter to continue. ")
        except KeyboardInterrupt:
            continue
functions.clear()
