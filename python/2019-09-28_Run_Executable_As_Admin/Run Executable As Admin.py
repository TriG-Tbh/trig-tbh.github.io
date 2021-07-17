def main():
    import os
    import sys
    dirpath = os.path.realpath(os.path.dirname(__file__))
    if len(sys.argv) != 2:
        print("Usage: \"" + dirpath + "\\Run Executable As Admin.py\" C:\\path\\to\\executable.exe")
        sys.exit(1)
    else:
        path = sys.argv[1]
        if not os.path.exists(path):
            print("Path \"" + path + "\" does not exist.")
            print("Usage: \"" + dirpath +
                  "\\Run Executable As Admin.py\" C:\\path\\to\\executable.exe")
            sys.exit(1)
        command = """
Set ApplicationPath="{}"
cmd /min /C "set __COMPAT_LAYER=RUNASINVOKER && start "" %ApplicationPath%"
""".format(path)
        with open(dirpath + "\\Run Executable As Admin.bat", "w") as f:
            f.write(command)
        try:
            run = "cmd /k \"" + dirpath + "\\Run Executable As Admin.bat\""
            print(run)
            os.system(run)
        except:
            print(run)

if __name__ == "__main__":
    main()
