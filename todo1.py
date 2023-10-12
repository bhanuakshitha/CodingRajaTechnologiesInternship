import tkinter as tk
from tkinter import messagebox
from datetime import datetime
import mysql.connector
try:
    mydb=mysql.connector.connect(host="localhost",user="root",password="root",database="toda",charset="utf8")
    mycursor=mydb.cursor()
    
except:
    print('Database Connection Failed.')

def add_task():
    task=task_entry.get()
    priority=priority_entry.get()
    duedate=duedate_entry.get()
    if task:
        mycursor=mydb.cursor()
        mycursor.execute("INSERT INTO task(tasks,priority,duedate)VALUES(%s,%s,%s)",(task,priority,duedate))
        mydb.commit()
        mycursor.close()
        update_list()
        task_entry.delete(0,tk.END)
        priority_entry.delete(0,tk.END)
        duedate_entry.delete(0,tk.END)
    else:
        messagebox.showwarning("Warning","Please enter a task.")
def delete_task():
    selected_task=task_listbox.get(tk.ACTIVE)
    if selected_task:
        mycursor=mydb.cursor()
        mycursor.execute("DELETE FROM task WHERE tasks=%s",(selected_task,))
        mydb.commit()
        update_list()
        mycursor.close()
def mark_task():
    selected_task=task_listbox.get(tk.ACTIVE)
    if selected_task:
        mycursor=mydb.cursor()
        mycursor.execute("UPDATE task SET status='1' WHERE tasks=%s",(selected_task,))
        mydb.commit()
        update_list()
        mycursor.close()
    else:
        messagebox.showwarning("error","Cannot mark as completed.")
def update_list():
    mycursor=mydb.cursor()
    mycursor.execute("SELECT tasks FROM task WHERE status IS NULL")
    task=mycursor.fetchall()
    mycursor.close()
    task_listbox.delete(0,tk.END)
    for task in task:
        task_listbox.insert(tk.END,task[0])

root=tk.Tk()
root.title("To_Do List App")

task_entry=tk.Entry(root,width=30)
priority_entry=tk.Entry(root,width=30)
duedate_entry=tk.Entry(root,width=30)
add_button=tk.Button(root,text="Add Task",command=add_task)
delete_button=tk.Button(root,text="Delete Task",command=delete_task)
mark_button=tk.Button(root,text="Mark as completed",command=mark_task)
task_entry.pack(pady=10)
priority_entry.pack(pady=10)
duedate_entry.pack(pady=10)
add_button.pack()
delete_button.pack()
mark_button.pack()


task_listbox=tk.Listbox(root,width=40)
task_listbox.pack()
root.mainloop()
