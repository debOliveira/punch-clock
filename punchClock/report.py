# please install git python
# please configure your name down in "name"
# just run the code and follow the instructions
# make sure your git user and password are already configured in bash
from git import Repo
from datetime import datetime
import os

name = "christian"

now = datetime.now()
current_time = now.strftime("%H:%M:%S")
current_day = datetime.today().strftime('%Y-%m-%d')
task = input("Enter what you've done: ")
text = current_day+" - "+current_time+" >> "+task+"\n"
msg = "Punch created for "+name+" at "+current_day+" - "+current_time

f = open('./punchClock/'+name+'.txt','a')
#f.write(text)
f.close()
print(msg)

gitPath = '.git'
try:
    repo = Repo(gitPath)
    repo.git.add(update=True)
    repo.index.commit(msg)
    origin = repo.remote(name='origin')
    origin.push()
except:
    print('Some error occured while pushing the code')
