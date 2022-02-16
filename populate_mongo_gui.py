# -*- coding: utf-8 -*-

import pymongo
import pandas as pd
import csv
from datetime import date, datetime
import tkinter as tk
from tkinter import filedialog#, PhotoImage
from tkinter import *
import socket
from pathlib import Path



#change this name if you need an experimenal Database, if not procceed as is
databaseName = 'place_holder_base' #collection name

#other variables are updated in the script before use
componentName = "tempCollection"
fileName = ""
operatorName = ""
componentDF = pd.DataFrame() #empty dataframe to read file into
filePath = ""
appMessage = ""
existing_user = ""
existing_pass = ""
connectMessage = "Connected: "
browseMessage = "File Loaded: "


#Connect To DB
def connect():
    try:
        print("Attempting connection...\n")
        conn = pymongo.MongoClient("mongodb+srv://Name_and_credentials_here.mongodb.net/myFirstDatabase?retryWrites=true&w=majority",  tls=True, tlsAllowInvalidCertificates=True)
        mydb = conn[databaseName]
        mycol = mydb[componentName]        
        connectMessage = "Connected: Yes"
        connectMsg = tk.Label(m, text=connectMessage).grid(row=0, column=3)
        print("connected here")
    except ValueError:
        print("Oops! Value error")
        connectMessage = "Connected: No"
    
def getCol():
    try:
	#can put credential string here, or use the gui at run time
        conn = pymongo.MongoClient("mongodb+srv://Name_and_credentials_here.mongodb.net/myFirstDatabase?retryWrites=true&w=majority",  tls=True, tlsAllowInvalidCertificates=True)
        mydb = conn[databaseName]
        mycol = mydb[componentName]
        connectMessage = "Connected: Yes" 
        return mycol
    except ValueError:
        print("Oops! Value error")
        connectMessage = "Connected: No"

# Read CSV
# To Read the CSV I am using the pandas read_csv function or read_excel. This takes a local file path to be written into a Pandas Dataframe.

# Browse for file, then read it into a dataframe with gui interface
def browse():
    file = filedialog.askopenfile(parent=m,mode='rb',title='Choose a file')
    print("file:: ", file)
    if file:
        global filePath
        global componentDF
        global componentName
        global fileName
        filePath = file.name
        print("filePath", filePath)
        fileName = file.name.split("/")
        fileName = componentName[len(componentName) - 1]
        fileName = componentName.split(".")[0]
        componentName = variable.get() 
        print("compName:", componentName)
        
        

        try: #first we try to read as csv
            print('hi')
            componentDF = pd.read_csv(file, encoding='iso-8859-1', skip_blank_lines=True)#, lineterminator='\n')
        except Exception: #if that doesn't work, we try to read as excel file
        
        
        
            print('excel ent') #excel 
            componentDF = pd.read_excel(file, sheet_name=None)
            componentDF = pd.concat(pd.read_excel(file, sheet_name=None), ignore_index=True)
            type(componentDF)
            #componentDF = componentDF.parse(componentDF.sheet_names[0])
            #componentDF = componentDF.dropna()
            
            
            
        print("DropperFile\n", componentDF)
        data = file.read()
        file.close()
        print ("I got %d bytes from this file." % len(data))
        browseMessage = "File Loaded: Yes"
        browseMsg = tk.Label(m, text=browseMessage).grid(row=3, column=3)
        appMessage = "File read"

# "Records" indicates each row will become a dictionary, where its key is the column name, while the value remains the data in the cell.

def populate():
    print(type(componentDF))
    componentDict = componentDF.to_dict("records")
    mycol = getCol()
    print("mycol:", mycol)
    print("DropperFILE AGAIN\n", componentDF)
#Database Population
#The database is populated using Mongoose insert_one to loop over our full dictionary of components, and insert each one at a time.

   #use these two lines to wipe out collection as needed when troubleshooting
   # x = mycol.delete_many({}) 
   # print("|  ", x.deleted_count, " documents deleted.  |")
   
   
   
    count = 0
    tempDF = pd.DataFrame()
    print("-----------------------------")
    print("-----------------------------")   

#iterate through dataframe and insert each row into DB as a document
    for val in componentDict:
           
        print("Adding...")
        print(val)
        count+=1
        for x in val:
            print(x, ":", val[x])
        try:
            #db.collection.update(doc, doc, {upsert:true})
            mycol.insert_one(val)
            tempDF.append(val, ignore_index=True)

            print("------------------------------------------------------------------------------------------------------------------------")
            
        except Exception:
            print("oops, something's wrong with an insert_one call at document number: ", count)
 
#Create Completed CSV
#Finally, our written objects are added back into a dataframe before creating a new CSV file in the completed folder.
    today = str(date.today())
    now = (datetime.now())
    dt_now = now.strftime("%d-%m-%Y_%H.%M.%S")
    print("Today: ", today)
    print("Now: ", now)
    print("DT Now: ", dt_now)
    if operatorName == "":
        save_path = ("backups/" + (fileName) + "_" + dt_now + ".csv")
    else:
        save_path = ("backups/" + (fileName) + "_" + dt_now + "_" + operatorName + ".csv")
    print(save_path)

    
    
    
    print("--------------------------------------------------------")
    print("| Saved to:", save_path, "|")
    print("--------------------------------------------------------")
    appMessage = "Added", count, "documents"
    uploadMessage = "Uploaded " + str(count) + "\ndocuments"
    browseMsg = tk.Label(m, text=uploadMessage).grid(row=4, column=3)

    saveMessage = ("Saved Backup CSV to:\n"+ save_path)
    saveMsg = tk.Label(m, text=saveMessage).grid(row=7, column=1)


#initialize the tk interface. program execution starts here
# m = master
m = tk.Tk()
m.geometry('700x300')

login = Path("login.txt")
print("testing..")
if login.is_file():  
    
    with open(login) as f:
        data = f.readlines()
        data = [x.strip() for x in data] 
    try:
        existing_user = data[0].split(" ")[1]
        existing_pass = data[1].split(" ")[1]
        print ("I got %d bytes from this Login file." % len(data))
        appMessage = "Loaded existing user\n"+ existing_user
    except IndexError:
        print("Auth error")
        
        
# we can add new options to the components as we add them and the project grows, partTypes each represent a sepereate collection.
partTypes = ["Kit", "Frame", "Dropper"]
variable = StringVar(m)
variable.set(partTypes[0]) #default value showing
drop = OptionMenu(m, variable, *partTypes)
drop.grid(row=1, column=12)
tk.Label(m, text="Pick a component collection: ").grid(row=0, column=12)


tk.Label(m, text='Enter Mongo Username').grid(row=0)
mongoUser = tk.Entry(m, textvariable = "mongoURL")
mongoUser.grid(row=0, column=1)

mongoUser.insert(0, existing_user)

tk.Label(m, text='Mongo Password: ').grid(row=1)
mongoPass = tk.Entry(m, textvariable = "mongoPassword")
mongoPass.grid(row=1, column=1)

mongoPass.insert(0, existing_pass)

tk.Label(m, text='Choose file to upload').grid(row=3)
tk.Label(m, text='Populate').grid(row=4)

tk.Label(m, text='').grid(row=2)

b = tk.Button(m, text="Connect",
        command=connect)
b.grid(row=1, column=3)

b2 = tk.Button(m, text="Browse",
        command=browse)
b2.grid(row=3, column=1)

b3 = tk.Button(m, text="Upload",
        command=populate)
b3.grid(row=4, column=1)

tk.Label(m, text='').grid(row=5)
errorMsg = tk.Label(m, text=appMessage).grid(row=6)


m.wm_title('MongoDB Population Tool')


m.mainloop()




"""
Spyder Editor

This script will upload data to a mongoDB. Name which DB you are adding to, then use the gui to select 
a new or existing collection that correlates to the data you are uploading.


Ongoing and planned upgrades for this script:
•   Work directly from Google Drive (testing stage)
•   Check for duplicates
•	Add update info toggle for making changes to existing documents
•	Reafactor tkinter code
•	Add photo functionality
•	Package for non-dev usage.


working on changes for option to upload directly from google drive:
This code to be added to main script when complete.

CWD should contain a Json file, 'client_secrets.json' If this file is missing visit this site and get those installed (specify scope to access all):  https://pythonhosted.org/PyDrive/quickstart.html


from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
gauth = GoogleAuth() #returns client_secrets file
gauth.LocalWebserverAuth() #authenticate connection
drive = GoogleDrive(gauth) #create drive access object

#file1 = drive.CreateFile({'title': 'Hello.txt'})
#file1.SetContentString('Hello')
#file1.Upload() # Files.insert()

#fullText contains 'hello'
#this will allow us to search for component by unique headers!

def download_file(drive_obj, file_id, output_fname):
    gfile = drive_obj.CreateFile({'id': file_id})
    if output_fname is None:
        output_fname = file_id
    gfile.GetContentFile(output_fname)

    return output_fname

#file_list = drive.ListFile({'q': "'root' in parents and trashed=false"}).GetList()
#for file1 in file_list:
  #print('title: %s, id: %s' % (file1['title'], file1['id']))
  #content = file1.GetContentString()
  #print(content)
  #cat = download_file(drive, file1['id'], "Helloo")
  #print(cat)
#docsfile.GetContentFile('ComponentList.csv', mimetype='csv')

file_list = drive.ListFile({'q': "title contains 'Hello' and trashed=false"}).GetList()
print(file_list[0]['title']) # should be the title of the file we just created
file_id = file_list[0]['id'] # get the file ID

file = drive.CreateFile({'id': file_id})

#file.Delete() #put file in google drive trash

"""
