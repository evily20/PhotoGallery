# PhotoGallery
Photo Gallery is an application which can be used to store albums by each of its users and each album would consist of various photos.

# PreRequisites
Python with flask, pymongo, datetime and requests.

# Platform of the Application
PhotoGallery works using Python with framework Flask in the backend. The database used is MongoDb and in frontend HTML, CSS, Bootstrap is used.

# How to use the Application
The application can be started by executing "in.py" and browser address "http://127.0.0.1:5156/" which can be varied depending upon the port you choose. Replace '5156' with the port number to be used and in "in.py" change port to new port number.
The application starts with '/' extension and it is the home page where the user can either login or sign up. 
If any user tries to login with invalid/incorrect Userid(Email) or Password, the user remains in the same page.
It is required that during sign up already existing Email should not be used.
After logging in User Profile page is present. The user can edit Profile, add Album, delete Album, remove User from here.
All the Albums created by the User are displayed on this page with its cover picture and album name. On clicking on it a page displaying the Album's pictures is shown. Over there option to add/remove picture is present.
Cover Picture and Profile Picture is always Public.
All Pictures/Albums are divided in 3 categories: Public, Private, Only Me. Public can be viewed by any user, Private can be viewed only if someone is logged in, Only Me can be viewed only by the person who has uploaded the picture.
The database stores the Url link of the picture, so the user can only add pictures which are already present Online.

To view any existing user's profile "/Album/Userid" where Userid is Email registered of the user. If you're logged in you can view the Public, Private Albums. If you're not logged in only Public albums can be viewed. If you're the user viewing your profile all 3 Public, Private, Only Me albums can be viewed.

To view any existing user's album "/Album/userid/albumname" where Userid is Email registered of the user and albumname is the name of Album you wish to see. If you're logged in you can view the Public, Private pictures. If you're not logged in only Public pictures can be viewed. If you're the user viewing your profile all 3 Public, Private, Only Me albums can be viewed.
