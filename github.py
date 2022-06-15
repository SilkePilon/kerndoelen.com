import codecs
import sys
import os
with open("server.log", "r") as x:
    log = x.readlines()
with open("readme.txt", "r") as f:
    contents = f.readlines()

log = str(log).replace("'", "").replace(",", "\n").replace('"', '').replace("[", "").replace("]", "").replace("http://167.172.47.127:80", "i hide my ip")
contents.insert(105, "```" + log + "\n" + "```")


with open("README.md", "w") as f:
    contents = "".join(contents)
    f.write(contents)
os.system("git rm --quiet -r --cached --ignore-unmatch .")
os.system("git add .")
try:
    msg = str(sys.argv[1])
except:
    msg = "log update"
msg = '"' + msg + '"'
os.system("git commit -m " + msg )
os.system("git push origin master")
