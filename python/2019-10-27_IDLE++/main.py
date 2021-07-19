import os
import platform
import traceback
import subprocess
import sys

global clear


def clear():
    system = platform.system()
    if system == "Windows":
        os.system("cls")
    elif system == "Linux":
        os.system("clear")
    else:
        print("Unknown system, cannot clear")


global execute


def execute(cmdstring):
    cmd = subprocess.Popen(cmdstring, shell=True, stdout=subprocess.PIPE,
                           stderr=subprocess.PIPE, stdin=subprocess.PIPE)
    output_bytes = cmd.stdout.read() + cmd.stderr.read()
    output_str = str(output_bytes, "utf-8")
    output_str = output_str.strip()
    print(output_str)


global quit

def quit():
    sys.exit(0)


global exit

def exit():
    print("Use quit() to exit")

clear()


def main():
    while True:
        directory = os.getcwd()
        command = input("(" + directory + ") >>> ")
        command = command.strip()
        if command[-1] == ":":
            line = "example"
            while line != "":
                line = input("....")
                command += "\n" + line
        if command == "clear()":
            clear()
            continue
        try:
            exec("print({})".format(command))
        except:
            try:
                exec(command)
            except:
                tb = traceback.format_exc().strip()
                print(tb)
                    


if __name__ == "__main__":
    main()
