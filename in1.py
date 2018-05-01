from flask import Flask, render_template, redirect
from flask import jsonify, request
from flask import Flask, render_template, flash, request, url_for
from pymongo import MongoClient
import datetime
import requests
client=MongoClient()
Session=[]
mydatabase=client['PhotoGallery']
mycollection=mydatabase['User']
users=[]


app=Flask(__name__)
@app.route('/')
def home():
    if(len(Session)==1):
        return redirect(url_for('login'))
    return render_template("index.html")

@app.route('/showSignUp')
def signuppage():
    if(len(Session)==1):
        return redirect(url_for('login'))
    return render_template("signup.html")

#delete album
@app.route('/RemoveAlbum')
def delalb():
    if(len(Session)==1):
        return render_template("RemoveAlbum.html")
    return render_template("Error.html")



@app.route('/removealbum', methods=['POST'])
def delal():
    if(len(Session)==0):
        return redirect(url_for('login'))
    usr=Session[0]
    albname=request.form.get('AlbName')
    r=mydatabase.User.find({"Email": usr})
    rec=r[0]
    fl=0
    for alb in rec["Album"]:
        if alb["Name"]==albname:
            print(alb)
            fl=1
            break
    if(fl==1):
        Albumcollect=rec["Album"]
        print(Albumcollect)
        Albumcollect.remove(alb)
        print(Albumcollect)
        rec["Album"]=Albumcollect
        #print(rec)
        mydatabase.User.delete_many({"Email": usr})
        mydatabase.User.insert(rec)
        return redirect(url_for('login'))
    return render_template("Error.html") 
        


#delete picture
@app.route('/RemovePicture')
def delalb1():
    if(len(Session)==1):
        return render_template("RemovePicture.html")
    return render_template("Error.html")

@app.route('/removepicture', methods=['POST'])
def delp():
    if(len(Session)==0):
        return redirect(url_for('login'))
    usr=Session[0]
    albname=request.form.get('AlbumName')
    picturename=request.form.get('PictureName')
    r=mydatabase.User.find({"Email": usr})
    rec=r[0]
    fl=0
    for alb in rec["Album"]:
        if alb["Name"]==albname:
            for pictures in alb["Pictures"]:
                if pictures["Name"]==picturename:
                    fl=1
                    break
        if fl==1:
            break

    print(fl)
    if fl==1:
        x=rec["Album"]
        x.remove(alb)
        alb["Pictures"].remove(pictures)
        x.append(alb)
        rec["Album"]=x
        mydatabase.User.delete_many({"Email": usr})
        mydatabase.User.insert(rec)
        return render_template("user.html", User=rec, t="2")
        #print(rec)

    return render_template("Error.html")

@app.route('/login', methods=['POST'])
def login():
    if(len(Session)==0):
        print(request.form.get('userid'))
        userid=request.form.get('userid')
        password=request.form.get('password')
        l=mydatabase.User.find({"Email": userid}).count()
        if(l==0):
            return render_template("index.html")
        r=mydatabase.User.find({"Email": userid})
        #print(r)
        print(password)
        print(request.form.get('password'))
        print(r[0]["Password"])
        if(r[0]["Password"]==password):
            Session.append(userid)
            return render_template("user.html", User=r[0], t="2")
        else:
            return render_template("index.html")
    return redirect(url_for('login'))

@app.route('/RemoveUser')
def remu():
    if(len(Session)==1):
        usr=Session[0]
        mydatabase.User.delete_many({"Email": usr})
        Session.pop() 
    return render_template("index.html")

@app.route('/login', methods=['GET'])
def login1():
    if(len(Session)==1):
        usr=Session[0]
        r=mydatabase.User.find({"Email": usr})
        return render_template("user.html", User=r[0], t="2")
    else:
        return render_template("index.html")

#edit user
@app.route('/EditProfile', methods=['GET'])
def ed():
    if(len(Session)==1):
        usr=Session[0]
        r=mydatabase.User.find({"Email": usr})
        return render_template("EditUser.html", user=r[0], t="2")
    return redirect(url_for('login'))
        

@app.route('/User', methods=['POST'])
def edi():
    FirstName=request.form.get('inputFName')
    LastName=request.form.get('inputLName')
    Gender=request.form.get('inputGender')
    Email=request.form.get('inputEmail')
    Password=request.form.get('inputPassword')
    ProfilePicture=request.form.get('inputProfilePicture')
    usr=Session[0]
    r=mydatabase.User.find({"Email": usr})
    rec=r[0]
    Alb=rec["Album"]
    
    mydatabase.User.delete_many({"Email": usr})
    mydatabase.User.insert({"FirstName": FirstName, "LastName": LastName, "Gender": Gender, "Email": Email, "Password": Password, "ProfilePicture": ProfilePicture, "Album":Alb })
    r=mydatabase.User.find({"Email": usr})
    return render_template("user.html", User=r[0], t="2")
    



@app.route('/Album', methods=['POST'])
def addalbum():
    CoverPic=request.form.get('Cover')
    AlbumName=request.form.get('Name')
    Secure=request.form.get('Security')
    Description=request.form.get('Description')
    Location=request.form.get('Location')
    Pictures=[{"Link": CoverPic, "Likes": 0, "Security": "Public", "Date": datetime.datetime.now(), "Name": "none", "Description": "none"}]
    Geo=Location
    Dt=datetime.datetime.now()
    usr=Session[0]
    print(usr)
    r=mydatabase.User.find({"Email": usr})
    print(r[0])
    x={"Cover": CoverPic, "geolocation": Location, "Name": AlbumName, "Date": Dt, "Security": Secure, "Pictures": Pictures, "Description": Description, "Likes": 0}
    print(x)
    y=r[0]["Album"]
    y.append(x)
    print(y)
    rec={
        "FirstName": r[0]["FirstName"],
        "LastName": r[0]["LastName"],
        "Password": r[0]["Password"],
        "Email": r[0]["Email"],
        "Gender": r[0]["Gender"],
        "ProfilePicture": r[0]["ProfilePicture"],
        "Album": y
        }
    print(rec)
    #r[0]["Album"].append(x)
    mydatabase.User.delete_many({"Email": usr})
    #mydatabase.Album.delete_many({"Email": usr, })
    #mydatabase.Album.insert(y)
    #mydatabase.Picture.insert({"link": CoverPic, "likes": 0, "Security": "Public"})
    #print(r)
    #print(r[0])
    mydatabase.User.insert(rec)
    return render_template("user.html", User=rec, t="2")

@app.route('/logout')
def logout():
   Session.pop()
   return render_template("index.html")

@app.route('/AddAlbum')
def addhtml():
    if(len(Session)==1):
        return render_template("AddAlbum.html")
    return render_template("Error.html")

@app.route('/error')
def errorf():
    Session.pop()
    return render_template("Error.html")


@app.route('/Picture', methods=['POST'])
def addhl():
    NewPicture=request.form.get('PictureLink')
    Name=request.form.get('Name')
    Security=request.form.get('Security')
    Description=request.form.get('Description')
    Location=request.form.get('Location')
    albumname=request.form.get('AlbumName')
    print(Location)
    if(len(Session)==1):
        usr=Session[0]
        fl=0
        r=mydatabase.User.find({"Email": usr})
        rec=r[0]
        for album in rec["Album"]:
            if(album["Name"]==albumname):
                fl=1
                break
        if(fl==1):
            al=album
            album["Pictures"].append({"Link": NewPicture, "Likes": 0, "Name": Name, "Security": Security, "Description": Description, "Location": Location, "Date": datetime.datetime.now() })
            print(album["Pictures"])
            rec["Album"].remove(al)
            print(rec)
            rec["Album"].append(album)
            print(rec)
            #album.remove()
            #rec.remove()
            #rec["Album"]
            mydatabase.User.delete_many({"Email": Session[0]})
            mydatabase.User.insert(rec)
            x=mydatabase.User.find({"Email": Session[0]})
    return redirect(url_for('login'))

@app.route('/AddPicture')
def addhtm():
    if(len(Session)==1):
        return render_template("AddPicture.html")
    return render_template("Error.html")

@app.route('/Album/<userid>/<albumname>')
def showAlbum(userid, albumname):
    r=mydatabase.User.find({"Email": userid})
    print(r)
    x=r[0]["Album"]
    print(x)
    #l=len(x)
    fl=0
    for alb in x:
        if(alb["Name"]==albumname):
            #fl=1
            y=alb["Pictures"]
            break
    
    if(len(Session)==1 ):
        usr=Session[0]
        if(usr==userid):
            return render_template("Album.html", t="2", Album=y)
        else:
            return render_template("Album.html", t="1", Album=y)
    return render_template("Album.html", t="0", Album=y)


@app.route('/Album/<userid>')
def showA(userid):
    r=mydatabase.User.find({"Email": userid})
    if(len(Session)==1 ):
        usr=Session[0]
        #r=mydatabase.User.find({"Email": usr})
        if(usr==userid):
            return render_template("user.html", t="2", User=r[0])
        else:
            return render_template("user.html", t="1", User=r[0])
    else:
        return render_template("user.html", t="0", User=r[0])


@app.route('/signup',methods=['POST'])
def signUp():
  
    fname = request.form.get('inputFName')
    email = request.form['inputEmail']
    password = request.form['inputPassword']
    lname = request.form.get('inputLName')
    gender = request.form['inputGender']
    l=mydatabase.User.find({"Email": email}).count()
    if(l!=0):
        return render_template("index.html")
    link="http://www.thehindu.com/sci-tech/technology/internet/article17759222.ece/alternates/FREE_660/02th-egg-person"
    rec={
        "FirstName": fname,
        "LastName": lname,
        "Password": password,
        "Email": email,
        "Gender": gender,
        "ProfilePicture": link,
        "Album": [{"geolocation": "xyz", "Cover": link, "Name": "ProfilePicture", "Date": datetime.datetime.now(), "Security": "Public", "Pictures": [{"Link": link, "Likes": 0, "Security": "Public", "Name": "none", "Description": "none", "Date": datetime.datetime.now() }]}]
        }
    mydatabase.User.insert(rec)
    Session.append(email)
    return redirect(url_for('login'))
    #print(fname)
    #add to table
    
 
    
    
app.run(port=5156)
