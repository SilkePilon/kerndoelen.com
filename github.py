import os
with open("README.md", "r+") as F:
    readme = F.read()
    with open("test2.log", "r") as X:
        data = X.read()
    newdata = str(readme).replace("logdata", data)
    F.write(newdata)
os.system("git rm -r --cached --ignore-unmatch .")
os.system("git add .")
msg = input("message: ")
msg = '"' + msg + '"'
os.system("git commit -m " + msg )
os.system("git push origin master")
