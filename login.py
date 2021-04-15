from tkinter import *
import tkinter as tk
from tkinter import ttk, messagebox
import pymysql
import requests
import json
from PIL import ImageTk, Image
import io
from io import BytesIO




#-------------- Clear Screen ------------------
def clearWindow(widgets=[]) :
  _list = win.winfo_children()
  for l in _list:
    l.destroy()




#-------------- User Info----------------------

user_name = ""
user_isDev = False
user_id = ""
user_email = ""
user_active_issues = ""
user_created_issues = ""
user_solved_issues = 9


#---------------Login Function --------------------------------------
def clear():
	userentry.delete(0,END)
	passentry.delete(0,END)

def offTester():
  tester_checkBox.deselect()

def offDeveloper():
  dev_checkBox.deselect()

def close():
	win.destroy()	


def login():
  if user_name_entry.get()=="" or password_entry.get()=="":
    messagebox.showerror("Error", "Enter User Name and Password", parent=win)
  else:
    url = 'http://track-my-bug.herokuapp.com/user/login'
    isDev = checkBox1.get()
    myobj = {'email': user_name_entry.get(), 'password': password_entry.get(), 'isDev': isDev}
    x = requests.post(url, data = myobj)
    y = json.loads(x.text)['data']
    if y['userFound']:
      global user_name,user_id,user_email,user_active_issues,user_created_issues,user_solved_issues
      user_id = y['id']
      user_name = y['username']
      user_email = y['email']
      user_active_issues = y['activeIssues']
      user_created_issues = y['createdIssues']
      user_solved_issues = y['solvedIssues'] + 1
      clearWindow()
      dashboard()
    else :
      messagebox.showinfo("Error" , "No user found having these credentials!" , parent = win)

#------------------------------------------------------------ Login Window -----------------------------------------


win = Tk()

bg_img_url = "https://image.freepik.com/free-photo/blurred-pop-abstract-background-pink_58702-1699.jpg"
response = requests.get(bg_img_url)
bg_img_data = response.content
bg_img = Image.open(BytesIO(bg_img_data))
bg_img = bg_img.resize((800, 500), Image.ANTIALIAS)
bg_img = bg_img.rotate(75)
bg_img = ImageTk.PhotoImage(bg_img)
Label(win, image = bg_img).pack(fill=BOTH, expand=YES)

bug_img_url = "https://ak.picdn.net/shutterstock/videos/19220965/thumb/6.jpg"
response = requests.get(bug_img_url)
bug_img_data = response.content
bug_img = Image.open(BytesIO(bug_img_data))
bug_img = bug_img.resize((300, 300), Image.ANTIALIAS)
bug_img = ImageTk.PhotoImage(bug_img)
Label(win, image = bug_img,bd=0).place(x=650,y=300)



# app title
win.title("Bug Tracker App")

# window size
win.maxsize(width=800 ,  height=500)
win.minsize(width=800 ,  height=500)


l=Frame(win,height=260,width=500,bg="white")
l.place(x=20,y=130)

#heading label
heading = Label(win , text = "Bug Tracker" , font = 'Verdana 25 bold',bg='white',fg="teal")
heading.place(x=80 , y=150)


username = Label(win, text= "User Name :" , font='Verdana 10 bold',bg='white',fg='black')
username.place(x=80,y=220)

userpass = Label(win, text= "Password :" , font='Verdana 10 bold',bg='white',fg='black')
userpass.place(x=80,y=260)

# Entry Box
user_name_entry = StringVar()
password_entry = StringVar()
	
userentry = Entry(win, width=40 , textvariable = user_name_entry,bg='white',bd=0)
userentry.focus()
userentry.place(x=200 , y=223)
userentryborder=Frame(win,height=1,width=160,bg="black")
userentryborder.place(x=200,y=240)

passentry = Entry(win, width=40, show="*" ,textvariable = password_entry,bg='white',bd=0)
passentry.place(x=200 , y=260)
passentryborder=Frame(win,height=1,width=160,bg="black")
passentryborder.place(x=200,y=277)

checkBox1 = IntVar()
dev_checkBox = Checkbutton(win, text = "Developer", variable = checkBox1,onvalue = True, offvalue = False,command=offTester,bg='white',fg='black')
dev_checkBox.place(x=200,y=300)

checkBox2 = IntVar()
tester_checkBox = Checkbutton(win, text = "Tester", variable = checkBox2,onvalue = True, offvalue = False,command=offDeveloper,bg='white',fg='black')
tester_checkBox.place(x=280,y=300)



btn_login = Button(win, width=20,font="Helvetica 15 bold", text="Login" ,borderwidth=0,command = login,bg="white",fg="deep pink",cursor="hand2")
btn_login.place(x=150, y=340)

#--------------------- Open Bug Detail Page -------------------
def open_bug_detail_page(bugid,name,severity,description,sprintId):

  def pick_bug():
    url = 'http://track-my-bug.herokuapp.com/assignbug'
    myobj = {'bugId': bugid, 'devId': 2}
    user_bugs_request = requests.post(url, data = myobj)
    user_bugs_response = json.loads(user_bugs_request.text)['data']
    if(user_bugs_response['updated']):
      messagebox.showinfo("Assigned" , "You are assigned this bug!" , parent = win)
      pick_bug_btn["state"] = "disabled"
      pick_bug_btn["text"] = "This bug is assigned to you!"
    else:
      messagebox.showinfo("Error" , "Something went wrong!" , parent = win)
    

  clearWindow()
  btn=Button(win, text = user_name ,font='Verdana 10 bold', width = 20, command = dashboard, bg="teal")
  btn.place(x=20, y=20)

  logout_btn=Button(win, text = "Logout" ,font='Verdana 10 bold', width = 10, command = dashboard, bg="teal")
  logout_btn.place(x=670, y=20)
  
  a=Frame(win,height=1,width=800,bg="black")
  a.place(x=0,y=60)

  bug_id_label = Label(win, text= "Bug ID : " , font='Verdana 10 bold',bg='Teal',fg='White')
  bug_id_label.place(x=80,y=10+70)
  bug_id = Label(win, text= bugid , font='Verdana 10 bold',bg='Teal',fg='White')
  bug_id.place(x=140,y=10+70)

  bug_description_label = Label(win, text= "Bug Description : " , font='Verdana 10 bold',bg='Teal',fg='White')
  bug_description_label.place(x=400,y=10+70)
  bug_description = Message( win, text=description, relief=RAISED ,bg='Teal',fg='White')
  bug_description.place(x=570,y=10+70)

  bug_name_label = Label(win, text= "Bug Name : " , font='Verdana 10 bold',bg='Teal',fg='White')
  bug_name_label.place(x=80,y=50+70)
  bug_name = Label(win, text= name , font='Verdana 10 bold',bg='Teal',fg='White')
  bug_name.place(x=170,y=50+70)
  
  bug_severity_label = Label(win, text= "Bug Severity : " , font='Verdana 10 bold',bg='Teal',fg='White')
  bug_severity_label.place(x=80,y=90+70)
  bug_severity = Label(win, text= severity , font='Verdana 10 bold',bg='Teal',fg='White')
  bug_severity.place(x=190,y=90+70)

  bug_sprint_label = Label(win, text= "Bug Sprint : " + str(sprintId), font='Verdana 10 bold',bg='Teal',fg='White')
  bug_sprint_label.place(x=80,y=130+70)
  

  pick_bug_btn=Button(win, text = "Pick Up this bug?" ,font='Verdana 10 bold', width = 30, command = pick_bug, bg='Teal',fg='Black')
  pick_bug_btn.place(x=300, y=250)


#---------------------------- Recent Bug Detail Page --------------



def recent_bug_detail_page(bugid,name,severity,description,sprintId,status,assigned_to,tested_by):

  clearWindow()
  btn=Button(win, text = user_name ,font='Verdana 10 bold', width = 20, command = dashboard, bg="teal")
  btn.place(x=20, y=20)

  logout_btn=Button(win, text = "Logout" ,font='Verdana 10 bold', width = 10, command = dashboard, bg="teal")
  logout_btn.place(x=670, y=20)
  
  a=Frame(win,height=1,width=800,bg="black")
  a.place(x=0,y=60)

  bug_id_label = Label(win, text= "Bug ID : " , font='Verdana 10 bold')
  bug_id_label.place(x=80,y=10+70)
  bug_id = Label(win, text= bugid , font='Verdana 10 bold')
  bug_id.place(x=140,y=10+70)

  bug_description_label = Label(win, text= "Bug Description : " , font='Verdana 10 bold')
  bug_description_label.place(x=400,y=10+70)
  bug_description = Message( win, text=description, relief=RAISED )
  bug_description.place(x=570,y=10+70)

  bug_name_label = Label(win, text= "Bug Name : " , font='Verdana 10 bold')
  bug_name_label.place(x=80,y=50+70)
  bug_name = Label(win, text= name , font='Verdana 10 bold')
  bug_name.place(x=170,y=50+70)
  
  bug_severity_label = Label(win, text= "Bug Severity : " , font='Verdana 10 bold')
  bug_severity_label.place(x=80,y=90+70)
  bug_severity = Label(win, text= severity , font='Verdana 10 bold')
  bug_severity.place(x=190,y=90+70)

  bug_sprint_label = Label(win, text= "Bug Sprint : " , font='Verdana 10 bold')
  bug_sprint_label.place(x=80,y=130+70)
  bug_sprint = Label(win, text= sprintId , font='Verdana 10 bold')
  bug_sprint.place(x=180,y=130+70)

  if tested_by == 0:
    tested_by = "Not picked up by annyone yet!"

  if status == 'testing':
    bug_status_label = Label(win, text= "Bug Status : " , font='Verdana 10 bold')
    bug_status_label.place(x=80,y=170+70)
    bug_status = Label(win, text= "Bug is in testing phase!" , font='Verdana 10 bold')
    bug_status.place(x=180,y=170+70)

    bug_solvedby_label = Label(win, text= "Bug was fixed by : " , font='Verdana 10 bold')
    bug_solvedby_label.place(x=80,y=210+70)
    bug_solvedby = Label(win, text= assigned_to , font='Verdana 10 bold')
    bug_solvedby.place(x=220,y=210+70)

    bug_testedby_label = Label(win, text= "Bug is being tested by : " , font='Verdana 10 bold')
    bug_testedby_label.place(x=80,y=250+70)
    bug_testedby = Label(win, text= tested_by , font='Verdana 10 bold')
    bug_testedby.place(x=255,y=250+70)

  elif status == 'active':
    bug_status_label = Label(win, text= "Bug Status : " , font='Verdana 10 bold')
    bug_status_label.place(x=80,y=170+70)
    bug_status = Label(win, text= "Bug is in active phase!" , font='Verdana 10 bold')
    bug_status.place(x=180,y=170+70)

    bug_solvedby_label = Label(win, text= "Bug is being fixed by : " , font='Verdana 10 bold')
    bug_solvedby_label.place(x=80,y=210+70)
    bug_solvedby = Label(win, text= assigned_to , font='Verdana 10 bold')
    bug_solvedby.place(x=250,y=210+70)

  else :
    bug_status_label = Label(win, text= "Bug Status : " , font='Verdana 10 bold')
    bug_status_label.place(x=80,y=170+70)
    bug_status = Label(win, text= "Bug has been solved successfuly!" , font='Verdana 10 bold')
    bug_status.place(x=180,y=170+70)

    bug_solvedby_label = Label(win, text= "Bug was fixed by : " , font='Verdana 10 bold')
    bug_solvedby_label.place(x=80,y=210+70)
    bug_solvedby = Label(win, text= assigned_to , font='Verdana 10 bold')
    bug_solvedby.place(x=220,y=210+70)

    bug_testedby_label = Label(win, text= "Bug was tested by : " , font='Verdana 10 bold')
    bug_testedby_label.place(x=80,y=250+70)
    bug_testedby = Label(win, text= tested_by , font='Verdana 10 bold')
    bug_testedby.place(x=230,y=250+70)


#---------------------------------------------------- User Bug Details -----------------------------------------




def user_bug_detail_page(bugid,name,severity,description,sprintId,status,tested_by):


  def send_to_testing():
    url = 'http://track-my-bug.herokuapp.com/sendtotesting'
    myobj = {'bugId': bugid,'devId':user_id}
    print(user_id)
    user_bugs_request = requests.post(url, data = myobj)
    user_bugs_response = json.loads(user_bugs_request.text)['data']
    if(user_bugs_response['updated']):
      messagebox.showinfo("Assigned" , "Your bug hs  been sent for testing!" , parent = win)
      send_bug_btn["state"] = "disabled"
      send_bug_btn["text"] = "Bus is sent for testing!"
    else:
      messagebox.showinfo("Error" , "Something went wrong!" , parent = win)
  
  clearWindow()
  btn=Button(win, text = user_name ,font='Verdana 10 bold', width = 20, command = dashboard, bg="teal")
  btn.place(x=20, y=20)

  logout_btn=Button(win, text = "Logout" ,font='Verdana 10 bold', width = 10, command = dashboard, bg="teal")
  logout_btn.place(x=670, y=20)
  
  a=Frame(win,height=1,width=800,bg="black")
  a.place(x=0,y=60)

  bug_id_label = Label(win, text= "Bug ID : " +str(bugid) , font='Verdana 10 bold')
  bug_id_label.place(x=80,y=10+70)
  

  bug_description_label = Label(win, text= "Bug Description : " , font='Verdana 10 bold')
  bug_description_label.place(x=400,y=10+70)
  bug_description = Message( win, text=description, relief=RAISED )
  bug_description.place(x=570,y=10+70)

  bug_name_label = Label(win, text= "Bug Name : " + str(name ) , font='Verdana 10 bold')
  bug_name_label.place(x=80,y=50+70)

  
  bug_severity_label = Label(win, text= "Bug Severity : " + str(severity), font='Verdana 10 bold')
  bug_severity_label.place(x=80,y=90+70)

  bug_sprint_label = Label(win, text= "Bug Sprint : " + str(sprintId), font='Verdana 10 bold')
  bug_sprint_label.place(x=80,y=130+70)
  
  if tested_by == 0:
    tested_by = "Not picked up by annyone yet!"

  if status == 'testing':
    bug_status_label = Label(win, text= "Bug Status : Bug is in testing phase!" , font='Verdana 10 bold')
    bug_status_label.place(x=80,y=170+70)
  
    bug_testedby_label = Label(win, text= "Bug tester : " + str(tested_by) , font='Verdana 10 bold')
    bug_testedby_label.place(x=80,y=250+35)
    
  elif status == 'active':
    bug_status_label = Label(win, text= "Bug Status : " , font='Verdana 10 bold')
    bug_status_label.place(x=80,y=170+70)
    bug_status = Label(win, text= "Bug is in active phase!" , font='Verdana 10 bold')
    bug_status.place(x=180,y=170+70)

    send_bug_btn=Button(win, text = "Send to testing phase?" ,font='Verdana 10 bold', width = 30, command = send_to_testing, bg="teal")
    send_bug_btn.place(x=300, y=300)

  else :
    bug_status_label = Label(win, text= "Bug Status : " , font='Verdana 10 bold')
    bug_status_label.place(x=80,y=170+70)
    bug_status = Label(win, text= "Bug has been solved successfuly!" , font='Verdana 10 bold')
    bug_status.place(x=180,y=170+70)

    bug_testedby_label = Label(win, text= "Bug was tested by : " , font='Verdana 10 bold')
    bug_testedby_label.place(x=80,y=250+35)
    bug_testedby = Label(win, text= tested_by , font='Verdana 10 bold')
    bug_testedby.place(x=230,y=250+35)





#---------------------------------------------------- DeshBoard Panel -----------------------------------------


def recent_bug_detail(btn_id):
  bug_id = recent_bugs_response[btn_id]['id']
  myobj = {'bugId': bug_id}
  url = 'http://track-my-bug.herokuapp.com/getbugdetail'
  val_request = requests.post(url, data = myobj)
  val_response = json.loads(val_request.text)['data']
  bug_name = recent_bugs_response[btn_id]['name']
  bug_severity = recent_bugs_response[btn_id]['severity']
  bug_status = val_response['bug'][0]['status']
  bug_description = val_response['bug'][0]['description']
  bug_assignedTo = val_response['bug'][0]['assignedTo']
  bug_testedBy = val_response['bug'][0]['testedBy']
  bug_sprintId = val_response['bug'][0]['sprintId']
  if(bug_status=='open'):
    open_bug_detail_page(bug_id,bug_name,bug_severity,bug_description,bug_sprintId)
  else:
    recent_bug_detail_page(bug_id,bug_name,bug_severity,bug_description,bug_sprintId,bug_status,bug_assignedTo,bug_testedBy)

def open_bug_detail(btn_id):
  bug_id = open_bugs_response[btn_id]['id']
  bug_name = open_bugs_response[btn_id]['name']
  bug_description = open_bugs_response[btn_id]['description']
  bug_severity = open_bugs_response[btn_id]['severity']
  bug_sprintId = open_bugs_response[btn_id]['sprintId']
  open_bug_detail_page(bug_id,bug_name,bug_severity,bug_description,bug_sprintId)



def user_bug_detail(btn_id):
  bug_id = user_bugs_response[btn_id]['id']
  myobj = {'bugId': bug_id}
  url = 'http://track-my-bug.herokuapp.com/getbugdetail'
  val_request = requests.post(url, data = myobj)
  val_response = json.loads(val_request.text)['data']
  bug_name = user_bugs_response[btn_id]['name']
  bug_severity = user_bugs_response[btn_id]['severity']
  bug_status = val_response['bug'][0]['status']
  bug_description = val_response['bug'][0]['description']
  bug_assignedTo = val_response['bug'][0]['assignedTo']
  bug_testedBy = val_response['bug'][0]['testedBy']
  bug_sprintId = val_response['bug'][0]['sprintId']
  user_bug_detail_page(bug_id,bug_name,bug_severity,bug_description,bug_sprintId,bug_status,bug_testedBy)

  


def dashboard():
  clearWindow()
  win.configure(bg='black')

  boxcol = "teal"

  btn=Button(win, text = user_name ,font='Verdana 10 bold', width = 20, command = dashboard, bg=boxcol,fg="white")
  btn.place(x=20, y=20)

  
  Frame(win,height=300,width=220,bg=boxcol).place(x=23,y=130)
  Frame(win,height=300,width=220,bg=boxcol).place(x=23+267,y=130)
  Frame(win,height=300,width=220,bg=boxcol).place(x=23+267+267,y=130)
  
  recent_bugs = Label(win, text= "Recent bugs" , font='Verdana 14',bg="black",fg="white")
  recent_bugs.place(x=75,y=90)

  recent_bugs_request = requests.get("http://track-my-bug.herokuapp.com/getbugs")
  global recent_bugs_response
  recent_bugs_response = json.loads(recent_bugs_request.content)
  recent_bugs_response = recent_bugs_response['data']
  recent_bugs_list = []
  for i in range (len(recent_bugs_response)):
    recent_bugs_list.append(Button(win, text=recent_bugs_response[i]['name'], width = 22, font='Verdana 10 bold',cursor="hand2", bg='black',fg='white',bd=0,command=lambda c=i: recent_bug_detail(c)))
    recent_bugs_list[i].place(x=30, y=140+i*30)

  open_bugs = Label(win, text= "Open bugs" , font='Verdana 14',bg="black",fg="white")
  open_bugs.place(x=345,y=90)

  open_bugs_request = requests.get("http://track-my-bug.herokuapp.com/getopenbugs")
  global open_bugs_response 
  open_bugs_response= json.loads(open_bugs_request.content)
  open_bugs_response = open_bugs_response['data']['bugFound']
  open_bugs_list = []
  if type(open_bugs_response) is not bool:
    for i in range (len(open_bugs_response)):
      open_bugs_list.append(Button(win, text=open_bugs_response[i]['name'], width = 22, font='Verdana 10 bold', cursor="hand2",  bg='black',fg='white',bd=0,command=lambda c=i: open_bug_detail(c)))
      open_bugs_list[i].place(x=297, y=140+i*30)

  user_bugs = Label(win, text= "Bugs assigned to You" , font='Verdana 14',bg="black",fg="white")
  user_bugs.place(x=560,y=90)

  url = 'http://track-my-bug.herokuapp.com/getbugsbyid'
  myobj = {'id': user_id, 'isDev': True}
  user_bugs_request = requests.post(url, data = myobj)
  global user_bugs_response
  user_bugs_response = json.loads(user_bugs_request.text)['data']
  if type(user_bugs_response) is not dict:
	  user_bugs_list = []
	  for i in range (len(user_bugs_response)):
		  user_bugs_list.append(Button(win, text=user_bugs_response[i]['name'], width = 22, font='Verdana 10 bold',cursor="hand2",bg='black',fg='white',bd=0,command=lambda c=i: user_bug_detail(c)))
		  user_bugs_list[i].place(x=564, y=140+i*30)





win.mainloop()

