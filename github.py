import codecs

import os
with open("server.log", "r") as x:
    log = x.readlines()
with open("readme.txt", "r") as f:
    contents = f.readlines()

contents.insert(105, str(log) + "\n")

with open("README.md", "w") as f:
    contents = "".join(contents)
    f.write(contents)
os.system("git rm -r --cached --ignore-unmatch .")
os.system("git add .")
msg = input("message: ")
msg = '"' + msg + '"'
os.system("git commit -m " + msg )
os.system("git push origin master")
