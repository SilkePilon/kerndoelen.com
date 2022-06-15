import codecs

import os
with codecs.open("README.md", "r+", "utf-8") as F:
    readme = F.read()
    with open("test2.log", "r") as X:
        data = X.read()
    newdata = str(readme).replace("logdata", data)
    F.write(newdata)
    F.write(u'\ufeff')
os.system("git rm -r --cached --ignore-unmatch .")
os.system("git add .")
msg = input("message: ")
msg = '"' + msg + '"'
os.system("git commit -m " + msg )
os.system("git push origin master")
