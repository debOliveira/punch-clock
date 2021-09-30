# please run "pip install gitpython"
# please configure your name down in "name"
# make sure your git user and password are already configured in bash

from datetime import datetime
import os
from git import Repo

name = "name"

now = datetime.now()
myfolder = os.path.abspath(os.getcwd())


current_time = now.strftime("%H:%M:%S")
current_day = datetime.today().strftime('%Y-%m-%d')
task = input("Enter what you've done: ")
text = current_day+" - "+current_time+" >> "+task+"\n"
msg = "Punch created for "+name+" at "+current_day+" - "+current_time

f = open('./punchClock/'+name+'.txt','a')
f.write(text)
f.close()
print(msg)

PATH_OF_GIT_REPO = myfolder+'\.git'  # make sure .git folder is properly configured
repo = Repo(PATH_OF_GIT_REPO)
repo.git.add(myfolder+'./punchClock/'+name+'.txt')
repo.index.commit(msg)
origin = repo.remote(name='origin')
origin.push()
