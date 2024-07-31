import sqlite3
import tkinter as tk
from tkinter import messagebox
from tkinter import ttk

# Function to create database and table
def create_db_and_table():
    conn = sqlite3.connect('goals.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Goals (
            goal_id INTEGER PRIMARY KEY AUTOINCREMENT,
            goal_name TEXT NOT NULL,
            goal_description TEXT
        )
    ''')
    conn.commit()
    conn.close()

# Function to add a goal
def add_goal():
    goal_name = entry_name.get()
    goal_description = entry_description.get()
    
    conn = sqlite3.connect('goals.db')
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO Goals (goal_name, goal_description)
        VALUES (?, ?)
    ''', (goal_name, goal_description))
    conn.commit()
    conn.close()
    messagebox.showinfo('Success', 'Goal added successfully')
    read_goals()
    clear_fields()

# Function to read goals and populate the listbox
def read_goals():
    conn = sqlite3.connect('goals.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM Goals')
    rows = cursor.fetchall()
    conn.close()
    
    listbox_goals.delete(0, tk.END)
    for row in rows:
        listbox_goals.insert(tk.END, f"{row[1]}: {row[2]}")

# Function to update a goal
def update_goal():
    selected_goal = listbox_goals.curselection()
    if not selected_goal:
        messagebox.showwarning('Warning', 'Please select a goal to update')
        return
    
    goal_name, goal_description = listbox_goals.get(selected_goal).split(': ', 1)
    
    conn = sqlite3.connect('goals.db')
    cursor = conn.cursor()
    cursor.execute('''
        SELECT goal_id FROM Goals WHERE goal_name = ? AND goal_description = ?
    ''', (goal_name, goal_description))
    goal_id = cursor.fetchone()[0]
    
    new_name = entry_name.get()
    new_description = entry_description.get()
    
    cursor.execute('''
        UPDATE Goals
        SET goal_name = ?, goal_description = ?
        WHERE goal_id = ?
    ''', (new_name, new_description, goal_id))
    conn.commit()
    conn.close()
    messagebox.showinfo('Success', 'Goal updated successfully')
    read_goals()
    clear_fields()

# Function to delete a goal
def delete_goal():
    selected_goal = listbox_goals.curselection()
    if not selected_goal:
        messagebox.showwarning('Warning', 'Please select a goal to delete')
        return
    
    goal_name, goal_description = listbox_goals.get(selected_goal).split(': ', 1)
    
    conn = sqlite3.connect('goals.db')
    cursor = conn.cursor()
    cursor.execute('''
        SELECT goal_id FROM Goals WHERE goal_name = ? AND goal_description = ?
    ''', (goal_name, goal_description))
    goal_id = cursor.fetchone()[0]
    
    cursor.execute('DELETE FROM Goals WHERE goal_id = ?', (goal_id,))
    conn.commit()
    conn.close()
    messagebox.showinfo('Success', 'Goal deleted successfully')
    read_goals()
    clear_fields()

# Function to clear the text fields
def clear_fields():
    entry_name.delete(0, tk.END)
    entry_description.delete(0, tk.END)

# Function to populate the text fields when a goal is selected
def on_goal_select(event):
    selected_goal = listbox_goals.curselection()
    if not selected_goal:
        return
    
    goal_name, goal_description = listbox_goals.get(selected_goal).split(': ', 1)
    entry_name.delete(0, tk.END)
    entry_name.insert(0, goal_name)
    entry_description.delete(0, tk.END)
    entry_description.insert(0, goal_description)

# Creating the Tkinter window
root = tk.Tk()
root.title('Goals Manager')

# Apply a built-in theme for a better look
style = ttk.Style(root)
style.theme_use("clam")  # You can use "clam", "alt", "default", "classic", etc.

# Creating and placing widgets within a frame
frame = ttk.Frame(root, padding="10")
frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

ttk.Label(frame, text='Goal Name: ').grid(row=0, column=0, padx=5, pady=5)
entry_name = ttk.Entry(frame, width=30)
entry_name.grid(row=0, column=1, padx=5, pady=5)

ttk.Label(frame, text='Goal Description: ').grid(row=1, column=0, padx=5, pady=5)
entry_description = ttk.Entry(frame, width=30)
entry_description.grid(row=1, column=1, padx=5, pady=5)

button_add = ttk.Button(frame, text='Add Goal', command=add_goal)
button_add.grid(row=2, column=0, padx=5, pady=5)

button_update = ttk.Button(frame, text='Update Goal', command=update_goal)
button_update.grid(row=2, column=1, padx=5, pady=5)

button_delete = ttk.Button(frame, text='Delete Goal', command=delete_goal)
button_delete.grid(row=2, column=2, padx=5, pady=5)

# Frame for the listbox and scrollbar
listbox_frame = ttk.Frame(root, padding="10")
listbox_frame.grid(row=3, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

# Listbox to display goals
listbox_goals = tk.Listbox(listbox_frame, height=10, width=50)
listbox_goals.grid(row=0, column=0, padx=5, pady=5)
listbox_goals.bind('<<ListboxSelect>>', on_goal_select)

# Adding a scrollbar to the listbox
scrollbar = ttk.Scrollbar(listbox_frame, orient=tk.VERTICAL, command=listbox_goals.yview)
scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))
listbox_goals['yscrollcommand'] = scrollbar.set

# Initial call to read goals and populate the listbox
read_goals()

# Ensure the database and table are created
create_db_and_table()

# Running the Tkinter main loop
root.mainloop()
