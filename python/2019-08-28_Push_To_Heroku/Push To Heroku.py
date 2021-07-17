import os
os.chdir("/media/trig/5B55-6159/APB/")
os.system("git add .")
os.system("git commit -am \"cool\"")
os.system("git push heroku master")
os.system("heroku logs -a apb-bot")