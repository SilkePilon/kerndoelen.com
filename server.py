from math import inf
import os,time,re
from shutil import which
from flask import Flask
from flask import render_template
from nltk.corpus import *
from PyDictionary import PyDictionary
import base64
from werkzeug.utils import send_from_directory
import wikipedia
import json
from datetime import datetime
from collections import Counter
import urllib.request
from better_profanity import profanity
from openpyxl import load_workbook
from datetime import datetime
from flask import request
from flask import jsonify
import requests
from flask import Flask,redirect
from flask import Markup
import sys
from flask import make_response
from flask import send_file
from flask import send_from_directory, current_app as app
from flask import Flask, abort, render_template, Response
from json import dumps
from flask import Flask, redirect, url_for
from werkzeug import *
from werkzeug.utils import secure_filename
from werkzeug.datastructures import  FileStorage
from netifaces import AF_INET, AF_INET6, AF_LINK
import netifaces as ni
from pandas import DataFrame, read_csv
import matplotlib.pyplot as plt
import pandas as pd 
import numpy as np
import pyexcel as p
import fnmatch

# config for server
app = Flask(__name__,static_folder='/root/server/school/static',template_folder='/root/server/school/templates')

app.config['UPLOAD_FOLDER'] = "/upload"

app.config['MAX_CONTENT_PATH'] = 1000000000000
ip_address = "kerndoelen.com"

run_ip_address = f"167.172.47.127"

app.config["CACHE_TYPE"] = "null"


ip_port = "80"

# block ips
@app.route('/blocklist')
def blocklist():
    with open("block.txt", "r") as f:
        ips = f.read()
    return ips

# block ips
@app.before_request
def blockip():
        
    if request.headers.getlist("X-Forwarded-For"):
       ip = request.headers.getlist("X-Forwarded-For")[0]
    else:
        ip = request.remote_addr
   
    
    with open("block.txt", "r") as f:
        blockedips = f.read()
    if "blocklist" in request.url:
        redirect("/blocklist")
        pass
    if ip in blockedips:
        abort(403, f"je IP '{ip}' is in de lijst met geblokerde IP's!") 
    else:
        pass


@app.route('/icon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, '/root/server/school/static'),
                               'icon.ico', mimetype='image/vnd.microsoft.icon')
    
@app.route('/info.docx')
def word():
    return send_from_directory(os.path.join(app.root_path, '/root/server/school/static'),
                               'info.docx', mimetype='pdf')

    
# admin panel
@app.route('/1TDUVBHPP6L21D21XFRJ5KAHY03AZCOBXDV0P2WFQ9N8PPV25RDNCS0WLOYYKELLZVVXDTXBRN58D7AUP96TLDLDSFMNWAKIRK1C/<user>')
def admin(user):
    with open("adminusers.txt", "r") as adminuser:
        admins = adminuser.read()
        admins = admins.split("\n")
        if user in admins:
            with open("ips.txt", "r") as F:
                ips = ""
                text = F.read().replace("\n", "<br/>")
                return text
        else:
            print("not good")
            return redirect(f"https://{ip_address}/login", code=302)
        
        
     


    
@app.route('/login', methods=['GET', 'POST'])
def login():
    with open("ips.txt", "a") as F:
        timeatm = datetime.now()
        if request.headers.getlist("X-Forwarded-For"):
            curip = request.headers.getlist("X-Forwarded-For")[0]
        else:
            curip = request.remote_addr
        inf = request.method
        url = request.url
        F.write(f"{timeatm} --  {curip} -> {inf} -> {url} -> admin page\n")
        F.close()
    with open("adminusers.txt", "r") as adminuser:
        admins = adminuser.read()
        admins = admins.split("\n")
        print(admins)
    error = ""
    if request.method == 'POST':
        for username in admins:
            print(username)
            if request.form['username'] != username or request.form['password'] != 'Landrover01':
                error = 'Verkeerde naam of wachtwoord. porbeer opnieuw'
            else:
                user = request.form['username']
                return redirect(f"https://{ip_address}/1TDUVBHPP6L21D21XFRJ5KAHY03AZCOBXDV0P2WFQ9N8PPV25RDNCS0WLOYYKELLZVVXDTXBRN58D7AUP96TLDLDSFMNWAKIRK1C/{user}", code=302)
    return render_template('login.html', error=error, ip=ip_address)
    
# upload files  
@app.route('/upload')
def upload_file1():
    name = []
    with open("urls.json") as jsonFile:
        data = json.load(jsonFile)
        jsonData = data["emp_details"]
        for x in jsonData:
            name2 = str(x['emp_name'])
            name2 = name2.split("\n")
            name += name2
           
        
        
        print(name)
    return render_template('profile.html', ip=ip_address, names=name)



def update_kern(url):
    projectpath = url
    print(url)
    from urllib.request import urlopen
    from urllib.request import urlretrieve
    import cgi
    
    remotefile = urlopen(projectpath)
    blah = remotefile.info()['Content-Disposition']
    value, params = cgi.parse_header(blah)
    filename = params["filename"]
    
    
    
    
    
    username = filename.replace(".xls", "").replace("_", "").replace("Skills", "")
    filename = filename.replace("Skills_", "").replace("_", "")
    count = 1
    filename = re.sub(r"\d+", "", str(filename)) 
    filename = filename.replace(" ", "")
    username = re.sub(r"\d+", "", str(username)) 
    username = username.replace(" ", "")
    
    
    
    if not ".xls"  in filename:
        return redirect("https://kerndoelen.com", code=302)
    else:
        try:
            
            os.remove("upload/" + secure_filename(filename) + '.xlsx')
            os.remove("upload/" + secure_filename(filename) + '.xlsx' + '.txt')
        except:
            print("cant delete")
        
        urlretrieve(projectpath, "upload/" + secure_filename(filename))
        p.save_book_as(file_name="upload/" + secure_filename(filename), dest_file_name='upload/'+ secure_filename(filename) + '.xlsx')
        os.remove("upload/" + secure_filename(filename))
        with open("upload/" + secure_filename(filename) + '.xlsx' + '.txt', 'w') as file:
            pd.read_excel("upload/" + secure_filename(filename) + '.xlsx').to_string(file, index=False)
    

        
        
      



@app.route('/handle_data', methods=['POST'])
def handle_data():
    projectpath = request.form['projectFilepath']
    email = request.form['email']
    if "https://www.peppels.net/app?o=Shared::Skills&f=leerling_skills_export&leerling=" in projectpath:
            # print(projectpath.split("leerling=",1)[1])
            # print(projectpath.split("&security_token=",1)[1])
            
            
            from urllib.request import urlopen
            from urllib.request import urlretrieve
            import cgi
            
            remotefile = urlopen(projectpath)
            blah = remotefile.info()['Content-Disposition']
            value, params = cgi.parse_header(blah)
            filename = params["filename"]
            
            
            
            
            
            username = filename.replace(".xls", "").replace("_", "").replace("Skills", "")
            filename = filename.replace("Skills_", "").replace("_", "")
            count = 1
            filename = re.sub(r"\d+", "", str(filename)) 
            filename = filename.replace(" ", "")
            username = re.sub(r"\d+", "", str(username)) 
            username = username.replace(" ", "")
            
            if not ".xls"  in filename:
                return redirect("https://kerndoelen.com", code=302)
            else:
                urlretrieve(projectpath, "upload/" + secure_filename(filename))
                p.save_book_as(file_name="upload/" + secure_filename(filename), dest_file_name='upload/'+ secure_filename(filename) + '.xlsx')
                os.remove("upload/" + secure_filename(filename))
                with open("upload/" + secure_filename(filename) + '.xlsx' + '.txt', 'w') as file:
                    pd.read_excel("upload/" + secure_filename(filename) + '.xlsx').to_string(file, index=False)
            
            def write_json(new_data, filename='urls.json'):
                with open(filename,'r+') as file:
                    # First we load existing data into a dict.
                    file_data = json.load(file)
                    # Join new_data with file_data inside emp_details
                    file_data["emp_details"].append(new_data)
                    # Sets file's current position at offset.
                    file.seek(0)
                    # convert back to json.
                    json.dump(file_data, file, indent = 4)
            
            
            
                # python object to be appended
            y = {"emp_name": f"{username}",
                 "data": {"url": f"{projectpath}", "email": f"{email}"}}
                
                
            write_json(y)
            os.system(f"python3 email/gmail/quickstart.py {email} welkom_bij_kerndoelen.com welkom_{username}_bij_kerndoelen.com+Deze_site_is_nog_steeds_in_ontwikkeling.+Voor_vragen_of_suggesties_kun_je_mailen_naar_:_team@kerndoelen.com+++met_hartelijke_groet,++het_kerndoelen.com_team")
            time = datetime.now()
            os.system(f"python3 email/gmail/quickstart.py silkepilon2009@gmail.com {username}_is_nieuw_op_kerndoelen.com name_:_{username}+time_:_{time}+email_:_{email}")
            
            # urluser = {'{username}': f'{projectpath}'}
            # with open('urls.json', 'w', encoding='utf-8') as f:
            #     json.dump(urluser, f, ensure_ascii=False, indent=4)
            # with open('urls.json') as json_file:
            #     data = json.load(json_file)
            #     print(data)
            
    else:
        return render_template('uploadurl.html', ip=ip_address, url="verkeerde url")
    return redirect(f"https://kerndoelen.com/upload", code=302)





@app.route('/githublogs')
def logsforgithub():
    os.system("python3 github.py 'log update from site'")
    return redirect(f"https://{ip_address}/", code=302)



@app.route('/urlupload', methods = ['GET', 'POST'])
def urlupload():
    if request.method == 'POST':
        text_input = request.form["data"]
        if "https://www.peppels.net/app?o=Shared::Skills&f=leerling_skills_export&leerling=" in text_input:
            print(" ")
        else:
            return render_template('uploadurl.html', ip=ip_address, url="probeer opnieuw")
    else:
        text = request.url
        source = request.args.get('url')
        return render_template('uploadurl.html', ip=ip_address, url="")
    
@app.route('/cookies', methods = ['GET', 'POST'])
def cookie():
    return render_template('cookie.html')

@app.route('/portfolio', methods = ['GET'])
def portfolio():
    return render_template('portfolio.html')

@app.route('/delcookies', methods = ['GET', 'POST'])
def delcookie():
    return render_template('delcookie.html')


# upload files	
@app.route('/uploader', methods = ['GET', 'POST'])
def upload_file():
    
    
    
    if request.method == 'POST':
        
        def find(pattern, path):
            result = []
            for root, dirs, files in os.walk(path):
                for name in files:
                    if fnmatch.fnmatch(name, pattern):
                        result.append(os.path.join(root, name))
            return result
        
        f = request.files['file']
        username = f.filename.replace(".xls", "").replace("_", "").replace("Skills", "")
        filename = f.filename.replace("Skills_", "").replace("_", "")
        count = 1
        filename = re.sub(r"\d+", "", str(filename)) 
        filename = filename.replace(" ", "")
        username = re.sub(r"\d+", "", str(username)) 
        username = username.replace(" ", "")
        

        try:
            if username in find(f"{username}*.xlsx", "upload/")[0]:
                os.remove(find(f"{username}*.xlsx", "upload/")[0])
                os.remove(find(f"{username}*.xlsx.txt", "upload/")[0])
        except:
            pass
        if not ".xls"  in f.filename:
            return redirect("https://kerndoelen.com", code=302)
        else:
            f.save("upload/" + secure_filename(filename))
            p.save_book_as(file_name="upload/" + secure_filename(filename),
               dest_file_name='upload/'+ secure_filename(filename) + '.xlsx')
            os.remove("upload/" + secure_filename(filename))
            return redirect(f"https://kerndoelen.com/kern/{username}", code=302)
    else:
        return "you just found a eester egg !"


@app.route('/update/<name>')
def update_kerndoel(name):
    def find(pattern, path):
        result = []
        for root, dirs, files in os.walk(path):
            for name in files:
                if fnmatch.fnmatch(name, pattern):
                    result.append(os.path.join(root, name))
        return result
    
    
    file12 = find(f"{name}*.xlsx", "upload/")[0]
    
    username_id = str(file12).replace(".xls.xlsx", "").replace("upload/", "")
    
    f = open('urls.json')

    # returns JSON object as
    # a dictionary
    data = json.load(f)
    
    # Iterating through the json
    # list
    for i in data['emp_details']:
        if i['emp_name'] == f'{username_id}':
            
            url = i['data']['url']
            update_kern(url)
            break
    
    # Closing file
    f.close()
    
    return redirect(f"https://kerndoelen.com/kern/{username_id}", code=302)


@app.route('/kern/<name>')
def mijnkerndoelen(name):
    
    namexDd = []
    with open("urls.json") as jsonFile:
        dataxDe = json.load(jsonFile)
        jsonDataxDxD = dataxDe["emp_details"]
        for x in jsonDataxDxD:
            name2 = str(x['emp_name'])
            name2 = name2.split("\n")
            namexDd += name2
    
    
    pd.set_option("display.max_rows", None, "display.max_columns", None,'display.max_colwidth', None)
    
    def find(pattern, path):
        result = []
        for root, dirs, files in os.walk(path):
            for name in files:
                if fnmatch.fnmatch(name, pattern):
                    result.append(os.path.join(root, name))
        return result
    telcount = 0
    try:
        
        
        file12 = find(f"{name}*.xlsx", "upload/")[0]
        
        username_id = str(file12).replace(".xls.xlsx", "").replace("upload/", "")
        
        f = open('urls.json')
 
        # returns JSON object as
        # a dictionary
        data = json.load(f)
        
        # Iterating through the json
        # list
        
        
        # Closing file
        f.close()
        
        
        with open(f"{file12}.txt", 'w') as file:
            pd.read_excel(f"{file12}").to_string(file, index=False)
        with open(f"{file12}.txt", 'r') as text:
            text1 = text.read()
            text1 = text1.split("Next Skills", 1)
            text1 = text1[0]
            telcount = text1.count("70%")
            telcount2 = text1.count("100%")
            telcount = telcount + telcount2
        telcount = str(telcount)
        with open(f"{file12}.txt", "r") as fp:
            lines = fp.readlines()
            lines = lines[1].replace("Data", "").replace(" ", "").replace("NaN", "").replace("Datum", "").replace("\\n", "").replace("-", "/")
            
            
    
           

    except:
        return render_template('profile.html', names=namexDd)
    return render_template('profile.html', names=namexDd, name=username_id, tel=f"{telcount} kerndoelen gehaald!", tel2=f"{telcount}/35", tel3=f"laatst geüpdate op {lines}")



# block ips
@app.route('/block/<ip>')
def block(ip):
    with open("block.txt", "r") as x:
        ips = x.read()
        if ip in ips:
            return f"{ip} is alredy blocked"
        else:
            with open("block.txt", "a") as f:
                f.write(ip+"\n")
            return redirect("https://kerndoelen.com", code=302)

# unblock ip     
@app.route('/unblock/<ip>')
def unblock(ip):
    with open("block.txt", "r") as x:
        ips = x.read()
        if not ip in ips:
            return f"{ip} is not in list"
        else:
            f = open('block.txt', 'r+')
            f.truncate(0) # need '0' when using r+
            f.seek(0)
            f.close()
            with open("block.txt", "a") as f:
                ips = ips.replace(ip, "")
                f.write(ips)
                return redirect("https://kerndoelen.com", code=302)
        
        
        

# kerndoelenmap
@app.route('/kerndoelenmap')
def Skills():
    return send_file('templates/pdf/main.pdf', download_name='main.pdf')
@app.route('/info')
def wordfile():
    return send_file('static/info.docx', download_name='info.docx')

@app.route('/begripen')
def begripen():
    return render_template('begrippen.html')

@app.route('/begripen2')
def begripen2():
    return render_template('begrippen2.html')
# @app.route('/kgt')
# def kgt():
#     return send_file('Templates/pdf/main.pdf', download_name='main.pdf')

# @app.route('/havo')
# def havo():
#     return send_file('Templates/pdf/main.pdf', download_name='main.pdf')

# @app.route('/tl')
# def tl():
#     return send_file('Templates/pdf/main.pdf', download_name='main.pdf')


#

# kerndoelen zoeker
@app.route('/<ni>/Aardrijkskunde')
def Aardrijkskundex(ni):
    
    Aardrijkskunde_kern = ""
    
    my_file = open(f"kerndoelen/{ni}-Aardrijkskunde.txt", "r")
    content = my_file.read()
    content_list = content.split("\n")
    my_file.close()
    Aardrijkskunde = list(content_list)
    for item in Aardrijkskunde:
        Aardrijkskunde_kern += item + "<br>"
            
    file = open(f"kerndoelen/{ni}-Aardrijkskunde.txt", "r")
    Aardrijkskunde_line_count = 0
    for line in file:
        if line != "\n":
            Aardrijkskunde_line_count += 1
            
    file.close()
    Aardrijkskunde_line_count = str(Aardrijkskunde_line_count) + " kerndoelen gevonden"
    Aardrijkskunde_kern = Markup(Aardrijkskunde_kern)
    return render_template('test.html', value=Aardrijkskunde_kern, countkern=Aardrijkskunde_line_count, info="", find="Aardrijkskunde", countkern1="", ni1=ni)
        




@app.route('/<ni>/Biologie')
def Biologiex(ni): 
    
    Biologie_kern = ""
    
    
    my_file = open(f"kerndoelen/{ni}-Biologie.txt", "r")
    content = my_file.read()
    content_list = content.split("\n")
    my_file.close()
    Biologie = list(content_list)
    for item in Biologie:
        Biologie_kern += str(item) + "<br>"
            
    file = open(f"kerndoelen/{ni}-Biologie.txt", "r")
    Biologie_line_count = 0
    for line in file:
        if line != "\n":
            Biologie_line_count += 1
    file.close()

    Biologie_line_count = str(Biologie_line_count) + " kerndoelen gevonden"
    Biologie_kern = Markup(Biologie_kern)
    return render_template('test.html', value=Biologie_kern, countkern=Biologie_line_count, info="", find="Biologie", countkern1="", ni1=ni)
            
    
@app.route('/<ni>/Economie')
def Economiex(ni):  
    
    Economie_kern = ""
    
      
    my_file = open(f"kerndoelen/{ni}-Economie.txt", "r")
    content = my_file.read()
    content_list = content.split("\n")
    my_file.close()
    Economie = list(content_list)
    for item in Economie:
        Economie_kern += str(item) + "<br>"
            
    file = open(f"kerndoelen/{ni}-Economie.txt", "r")
    Economie_line_count = 0
    for line in file:
        if line != "\n":
            Economie_line_count += 1
    file.close()

    Economie_line_count = str(Economie_line_count) + " kerndoelen gevonden"
    
    Economie_kern = Markup(Economie_kern)
    return render_template('test.html', value=Economie_kern, countkern=Economie_line_count, info="", find="Economie", countkern1="", ni1=ni)
    


@app.route('/<ni>/Geschiedenis')
def Geschiedenisx(ni):    
    
    Geschiedenis_kern = ""
    
     
    my_file = open(f"kerndoelen/{ni}-Geschiedenis.txt", "r")
    content = my_file.read()
    content_list = content.split("\n")
    my_file.close()
    Geschiedenis = list(content_list)
    for item in Geschiedenis:
        Geschiedenis_kern += item + "<br>"
            
    file = open(f"kerndoelen/{ni}-Geschiedenis.txt", "r")
    Geschiedenis_line_count = 0
    for line in file:
        if line != "\n":
            Geschiedenis_line_count += 1
    file.close()

    Geschiedenis_line_count = str(Geschiedenis_line_count) + " kerndoelen gevonden"
    Geschiedenis_kern = Markup(Geschiedenis_kern)
    return render_template('test.html', value=Geschiedenis_kern, countkern=Geschiedenis_line_count, info="", find="Geschiedenis", countkern1="", ni1=ni)
            

@app.route('/<ni>/Natuurkunde')
def Natuurkundex(ni):      
    
    Natuurkunde_kern = ""
    
    
    my_file = open(f"kerndoelen/{ni}-Natuurkunde.txt", "r")
    content = my_file.read()
    content_list = content.split("\n")
    my_file.close()
    Natuurkunde = list(content_list)
    for item in Natuurkunde:
        Natuurkunde_kern += item + "<br>"
            
    file = open(f"kerndoelen/{ni}-Natuurkunde.txt", "r")
    Natuurkunde_line_count = 0
    for line in file:
        if line != "\n":
            Natuurkunde_line_count += 1
    file.close()

    Natuurkunde_line_count = str(Natuurkunde_line_count) + " kerndoelen gevonden"
    Natuurkunde_kern = Markup(Natuurkunde_kern)
    return render_template('test.html', value=Natuurkunde_kern, countkern=Natuurkunde_line_count, info="", find="Natuurkunde", countkern1="", ni1=ni)


@app.route('/<ni>/Scheikunde')
def Scheikundex(ni):      
    
    Scheikunde_kern = ""
    
    
    my_file = open(f"kerndoelen/{ni}-Scheikunde.txt", "r")
    content = my_file.read()
    content_list = content.split("\n")
    my_file.close()
    Scheikunde = list(content_list)
    for item in Scheikunde:
        Scheikunde_kern += item + "<br>"
            
    file = open(f"kerndoelen/{ni}-Scheikunde.txt", "r")
    Scheikunde_line_count = 0
    for line in file:
        if line != "\n":
            Scheikunde_line_count += 1
    file.close()

    Natuurkunde_line_count = str(Scheikunde_line_count) + " kerndoelen gevonden"
    Natuurkunde_kern = Markup(Scheikunde_kern)
    return render_template('test.html', value=Scheikunde_kern, countkern=Scheikunde_line_count, info="", find="Scheikunde", countkern1="", ni1=ni)
    
# restart de server
@app.route('/restart')
def restart():
    os.execl(sys.executable, sys.executable, *sys.argv)

# eester egg "rickroll"
@app.route('/rickroll')
def test():
    return redirect("https://www.youtube.com/embed/QB7ACr7pUuE?rel=0&autoplay=1", code=302)

@app.route('/kgt/')
def kgtred():
    return redirect(f"https://{ip_address}/", code=302)

# suport page
@app.route('/support')
def support():
    return """
<script>
      alert("pagina om de webipdata te steunen komt er aan!");
</script>

"""


def remov_duplicates(input):
     
    # split input string separated by space
    input = input.split(" ")
 
    # joins two adjacent elements in iterable way
    for i in range(0, len(input)):
        input[i] = "".join(input[i])
 
    # now create dictionary using counter method
    # which will have strings as key and their
    # frequencies as value
    UniqW = Counter(input)
 
    # joins two adjacent elements in iterable way
    s = " ".join(UniqW.keys())
    
    return s

    
# home page
@app.route('/')
def home():
    with open("usercount.txt", "a") as usercounter:
        usercounter.write("1\n")
    with open("usercount.txt", "r") as usercounter:
        usercount = usercounter.read()
        usercount = usercount.count("1\n")
       
        
    countwords3 = 0
    with open("lookup.txt", "r") as FFF:
        words = FFF.read()
        words = words.split('\n')
        
        
    with open("ips.txt", "a") as F:
            timeatm = datetime.now()
            if request.headers.getlist("X-Forwarded-For"):
                curip = request.headers.getlist("X-Forwarded-For")[0]
            else:
                curip = request.remote_addr
            inf = request.method
            url = request.url
            F.write(f"{timeatm} --  {curip} -> {inf} -> {url}\n")
            F.close()
    for wurd in words:
            countwords3 += 1
    countwords3 -= 1
    ip_address = "kerndoelen.com"
    return render_template('mainv2.html', ipdata=ip_address, info=words, value="Gebruikers sins 2/6/2022 : " + str(usercount), value2="Opgezochten worden sins 2/6/2022 : " + str(countwords3))
    return "<title>kerndoelen.com</title>hi"
    # return redirect(str(request.url) + "home", code=302)







def line_prepender(filename, line):
    with open(filename, 'r+') as f:
        content = f.read()
        f.seek(0, 0)
        f.write(line.rstrip('\r\n') + '\n' + content)

# find
@app.route('/<niveaw>/<find>')
def hello(find, niveaw):
    
    
    
    if "77.162.15.236" in request.url:
        return "<title>kerndoelen.com</title>no direct ip"
    else:
        with open("ips.txt", "a") as F:
            timeatm = datetime.now()
            if request.headers.getlist("X-Forwarded-For"):
                curip = request.headers.getlist("X-Forwarded-For")[0]
            else:
                curip = request.remote_addr
            inf = request.method
            url = request.url
            F.write(f"{timeatm} --  {curip} -> {inf} -> {url} -> {find}\n")
            F.close()
        count = 0
        find = f"{find}"
        find = find.lower()
        kenrs = ""
        
        
        
        if "rickroll" in find:
            return redirect("https://www.youtube.com/embed/QB7ACr7pUuE?rel=0&autoplay=1", code=302)
        
        
        
        
        # translated_find = GoogleTranslator(source='auto', target='en').translate(find)
        # dictionary=PyDictionary(translated_find)

        my_file = open(f"kerndoelen/{niveaw}-Aardrijkskunde.txt", "r")
        content = my_file.read()
        content_list = content.split("\n")
        my_file.close()
        Aardrijkskunde = list(content_list)
        
        file = open(f"kerndoelen/{niveaw}-Aardrijkskunde.txt", "r")
        Aardrijkskunde_line_count = 0
        for line in file:
            if line != "\n":
                Aardrijkskunde_line_count += 1
        file.close()

        Aardrijkskunde_line_count = Aardrijkskunde_line_count
        
        my_file = open(f"kerndoelen/{niveaw}-Biologie.txt", "r")
        content = my_file.read()
        content_list = content.split("\n")
        my_file.close()
        Biologie = list(content_list)
        
        file = open(f"kerndoelen/{niveaw}-Biologie.txt", "r")
        Biologie_line_count = 0
        for line in file:
            if line != "\n":
                Biologie_line_count += 1
        file.close()

        Biologie_line_count = Biologie_line_count
        
        my_file = open(f"kerndoelen/{niveaw}-Economie.txt", "r")
        content = my_file.read()
        content_list = content.split("\n")
        my_file.close()
        Economie = list(content_list)
        
        file = open(f"kerndoelen/{niveaw}-Economie.txt", "r")
        Economie_line_count = 0
        for line in file:
            if line != "\n":
                Economie_line_count += 1
        file.close()

        Economie_line_count = Economie_line_count
        
        my_file = open(f"kerndoelen/{niveaw}-Geschiedenis.txt", "r")
        content = my_file.read()
        content_list = content.split("\n")
        my_file.close()
        Geschiedenis = list(content_list)
        
        file = open(f"kerndoelen/{niveaw}-Geschiedenis.txt", "r")
        Geschiedenis_line_count = 0
        for line in file:
            if line != "\n":
                Geschiedenis_line_count += 1
        file.close()

        Geschiedenis_line_count = Geschiedenis_line_count
        
        my_file = open(f"kerndoelen/{niveaw}-Natuurkunde.txt", "r")
        content = my_file.read()
        content_list = content.split("\n")
        my_file.close()
        Natuurkunde = list(content_list)
        
        file = open(f"kerndoelen/{niveaw}-Natuurkunde.txt", "r")
        Natuurkunde_line_count = 0
        for line in file:
            if line != "\n":
                Natuurkunde_line_count += 1
        file.close()

        Natuurkunde_line_count = Natuurkunde_line_count
        
        
        # if re.search(find, kern) or re.search(find, kern.capitalize()) or re.search(find, "het" + " " + kern) or re.search(find, "de" + " " + kern) or re.search(find, "een" + " " + kern):
        #                 print(re.search(find, kern) or re.search(find, "het" + " " + kern) or re.search(find, "de" + " " + kern) or re.search(find, "een" + " " + kern))
        #                 count += 1
        #                 kenrs += kern + "<br><br>"
        #                 print(count)
        
        
        line_count = 0
        while True:
            for kern in Aardrijkskunde:
                if find == "":
                    continue
                else:
                    if re.search(find, kern) or re.search(find, kern.capitalize()) or re.search(find, "het" + " " + kern) or re.search(find, "de" + " " + kern) or re.search(find, "een" + " " + kern):
                        print(re.search(find, kern) or re.search(find, "het" + " " + kern) or re.search(find, "de" + " " + kern) or re.search(find, "een" + " " + kern))
                        count += 1
                        kenrs += kern + "<br><br>"
                        print(count)
                        line_count = Aardrijkskunde_line_count
                    # else: 
                    #     return "geen kerndoelen gevonden"
            
            
            for kern in Biologie:
                if find == "":
                    continue
                else:
                    if re.search(find, kern) or re.search(find, kern.capitalize()) or re.search(find, "het" + " " + kern) or re.search(find, "de" + " " + kern) or re.search(find, "een" + " " + kern):
                        print(re.search(find, kern) or re.search(find, "het" + " " + kern) or re.search(find, "de" + " " + kern) or re.search(find, "een" + " " + kern))
                        count += 1
                        kenrs += kern + "<br><br>"
                        print(count)
                        line_count = Biologie_line_count
                    # else: 
                    #     return "geen kerndoelen gevonden"
                    
            for kern in Economie:
                if find == "":
                    continue
                else:
                    if re.search(find, kern) or re.search(find, kern.capitalize()) or re.search(find, "het" + " " + kern) or re.search(find, "de" + " " + kern) or re.search(find, "een" + " " + kern):
                        print(re.search(find, kern) or re.search(find, "het" + " " + kern) or re.search(find, "de" + " " + kern) or re.search(find, "een" + " " + kern))
                        count += 1
                        kenrs += kern + "<br><br>"
                        print(count)
                        line_count = Economie_line_count
                    # else: 
                    #     return "geen kerndoelen gevonden"
                    
            
            
            for kern in Geschiedenis:
                if find == "":
                    continue
                else:
                    if re.search(find, kern) or re.search(find, kern.capitalize()) or re.search(find, "het" + " " + kern) or re.search(find, "de" + " " + kern) or re.search(find, "een" + " " + kern):
                        print(re.search(find, kern) or re.search(find, "het" + " " + kern) or re.search(find, "de" + " " + kern) or re.search(find, "een" + " " + kern))
                        count += 1
                        kenrs += kern + "<br><br>"
                        print(count)
                        line_count = Geschiedenis_line_count
                    # else: 
                    #     return "geen kerndoelen gevonden"
            
            
            for kern in Natuurkunde:
                if find == "":
                    continue
                else:
                    if re.search(find, kern) or re.search(find, kern.capitalize()) or re.search(find, "het" + " " + kern) or re.search(find, "de" + " " + kern) or re.search(find, "een" + " " + kern):
                        print(re.search(find, kern) or re.search(find, "het" + " " + kern) or re.search(find, "de" + " " + kern) or re.search(find, "een" + " " + kern))
                        count += 1
                        kenrs += kern + "<br><br>"
                        print(count)
                        line_count = Natuurkunde_line_count
                    # else: 
                    # 
                    #   return "geen kerndoelen gevonden"
            break
            
        # Then, we're going to use the term "program" to find synsets like so:
        # print (dictionary.getSynonyms()['Noun'])
        wikipedia.set_lang("nl")
        for i in range(0, 1):
            try:
                # translated = GoogleTranslator(source='nl', target='en').translate(find)
                # print(translated)
                infox = wikipedia.summary(find, sentences=3, features="lxml")
                print(infox)
                store = True
                # info_new = GoogleTranslator(source='en', target='nl').translate(info)
                # print(info_new)
            except wikipedia.exceptions.DisambiguationError:
                pass
                infox = "niks gevonden, sorry"
                store = False
            except:
                pass
                store = False
                infox = "sorry geen wikipedia infomatie gevonden over " + find
            
        find = find.lower()
        if store == True or not kenrs == "":
            with open("lookup.txt", "r") as FFF2:
                if os.path.getsize('lookup.txt') == 0:
                    print("File is empty!") 
                    datawords = False
                else:
                    try:
                        datawords = list(FFF2.readlines())
                        print(datawords)
                                
                    except:
                        datawords = list(FFF2.read())
                        print(datawords)
                    print(os.path.getsize('lookup.txt'))
                
            with open("lookup.txt", "r+") as FFF:
                censored = profanity.censor(find)
                censored = censored.replace("*", "")
                # FFF.write(censored + "\n")
                if datawords == False:
                    FFF.write(censored + "\n")
                else:
                    allowd = True
                    for words in datawords:
                        if censored in words:
                            allowd = False
                    
                    if allowd == True:
                        if not len(censored) >= 20:
                            content = FFF.read()
                            FFF.seek(0, 0)
                            FFF.write(censored.rstrip('\r\n') + '\n' + content)
                        # FFF.write(censored + "\n")
        print(infox)
        print(kenrs)
        text = Markup(kenrs)
        hoeveelheid = str(count) + " kerndoel(en) gevonden over " + '"' + find + '"'
        findxD = find
        find = "wikipedia informatie over " + find
        xDxD = str(line_count) + " kerndoelen in database"
        ip_address = "kerndoelen.com"
        return render_template('test.html', ipdata=ip_address, value=text, countkern=hoeveelheid, info=infox, find=find,find2=findxD, countkern1=xDxD)
        return f'<title>kerndoelen.com</title><h1> {count} gevonden kerndoelen</h1><br/><p>infomatie over wat je hebt opgezocht : </p><p>{info}</p><br/><br/><p>{kenrs}</p>'
    
    # ssl_context=('server.crt', 'server.key')


# main loop
if __name__ == "__main__":
    app.run(host=run_ip_address, port=ip_port, debug=True)
# app.run(host="192.168.2.16", port=80)
