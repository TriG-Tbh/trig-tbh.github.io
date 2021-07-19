# Teams Assignment Puller (TAP) 

The purpose of this program is to take a user's assignments on Microsoft Teams and transfer them to an app that is easier to use (Notion).

## Setup

1. ### **Download the release for your system.**

    Releases are offered as packaged executables for Windows, Mac OS X and Linux, as well as Python source files. 

    For packaged executables:
    1. Go to ____ and download the .zip file that contains the executable for your system.
    2. Once the file has finished downloading, extract the folder contained in the file. You should now have a new folder that contains the executable.

    For the Python source files:
    1. If you do not have Python installed, go to the [Python downloads page](https://www.python.org/downloads/) and download the installer for your system. Run the installer, and follow that the instructions that the installer gives you. **Make sure to add Python to your PATH if you are prompted to.**
    2. Go to ______ and download the .zip file containing the Python (.py) files.
    3. Once the file has finished downloading, extract the folder contained in the file. You should now have a new folder that contains the Python file, as well as `requirements.txt`.
    4. Ensure you have pip installed by running `pip -V`.
    5. Navigate to the folder that contains the Python file and open a command prompt there.
    6. Run `pip install -r requirements.txt`. This installs all required modules.

2. ### **Open your default browser and log in to Teams.**

    Visit [Teams](http://teams.microsoft.com/) and log in. 

3. ### **Navigate to where you installed the program and create a `.config` file.**

    This file will be used to determine what Teams to pull assignments from.

4. ### **Copy the general channel links to the `.config` file.**

    For every Team, right click on the General channel, click `Get link to channel`, copy the link shown and paste it in `.config`, along with a newline.

5. ### **Set up Notion**

    1. Log into [Notion](https://www.notion.so) (or create an account if you don't have one).
    2. Press Ctrl+Shift+I to open the developer tools.
    3. Select the Application tab, scroll down to Cookies and click the first link. A table will appear with a lot of values.
    4. Find the entry in the table called `token_v2` and copy the value of that entry. **This token is used to control your account. Make sure you do not give it to anyone.**
    5. Paste the token in `.config`. **Make sure it is the last line in the file.**

