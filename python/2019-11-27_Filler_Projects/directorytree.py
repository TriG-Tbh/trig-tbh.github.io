import os
import glob

indentation = 0

def dir_walk(directory, indentation):
    message = ""
    os.chdir(directory)
    for filename in glob.glob("*"):
        if os.path.isdir(os.path.join(directory, filename)):
            #print(os.path.join(directory, filename))
            #message += ("\t" * indentation) + directory + "\n"
            message += dir_walk(os.path.join(directory, filename), indentation + 1) + "\n"
        else:
            if os.path.isfile(os.path.join(directory, filename)):
                message += ("\t" * indentation) + filename + "\n"
    return message


print(dir_walk(input(), indentation))
#dir_walk(input(), indentation)