import os
os.system("git filter-branch --index-filter 'git rm -r --cached --ignore-unmatch .' HEAD")
os.system("git add .")
msg = input("message: ")
msg = '"' + msg + '"'
os.system("git commit -m " + msg )
os.system("git push origin master")
