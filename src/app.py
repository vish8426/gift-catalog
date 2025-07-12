import tkinter as tk
from tkinter import messagebox, simpledialog, ttk
import sqlite3
import os

# Ensure 'dat' Folder Exists
DATA_FOLDER = 'dat'
os.makedirs(DATA_FOLDER, exist_ok=True)

DB_PATH = os.path.join(DATA_FOLDER, 'gift_catalog.db')

# Initialize DB
def init_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS gifts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            description TEXT,
            price REAL,
            link TEXT,
            priority INTEGER,
            purchased BOOLEAN DEFAULT 0
        )
    ''')

    conn.commit()
    conn.close()

# Add Gift to DB
def add_gift(name, desc, price, link, priority):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    c.execute('INSERT INTO gifts (name, description, price, link, priority) VALUES (?, ?, ?, ?, ?)',
              (name, desc, price, link, priority))
    
    conn.commit()
    conn.close()
    load_gifts()

# Load Gifts from DB into Treeview
def load_gifts():
    for row in tree.get_children():
        tree.delete(row)

    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('SELECT id, name, description, price, link, priority, purchased FROM gifts ORDER BY priority ASC')

    for idx, row in enumerate(c.fetchall(), start=1):
        purchased_text = 'Yes' if row[6] else 'No'
        tree.insert('', 'end', values=(idx, row[1], row[2], row[3], row[4], row[5], purchased_text), iid=str(row[0]))

    conn.close()

# Edit selected Gift
def edit_gift():
    selected = tree.selection()
    if not selected:
        messagebox.showwarning('Warning', 'No Gift Selected.')
        return

    gift_id = int(selected[0])

    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('SELECT name, description, price, link, priority FROM gifts WHERE id=?', (gift_id,))
    result = c.fetchone()
    conn.close()

    if result:
        current_name, current_desc, current_price, current_link, current_priority = result

        name = simpledialog.askstring('Edit Name', 'Enter Gift Name:', initialvalue=current_name, parent=root)
        if not name:
            return
        desc = simpledialog.askstring('Edit Description', 'Enter Description (Optional):', initialvalue=current_desc, parent=root) or ''
        
        while True:
            price_input = simpledialog.askstring('Edit Price', 'Enter Price (Optional):', initialvalue=str(current_price), parent=root)
            if price_input is None:
                price = current_price
                break
            elif price_input.strip() == '':
                price = 0
                break
            try:
                price = float(price_input)
                break
            except ValueError:
                messagebox.showerror('Invalid Input', 'Please Enter a Valid Numeric Price.')

        link = simpledialog.askstring('Edit Link', 'Enter Link (Optional):', initialvalue=current_link, parent=root) or ''
        
        while True:
            priority_input = simpledialog.askstring('Edit Priority', 'Enter Priority (1=Highest):', initialvalue=str(current_priority), parent=root)
            if priority_input is None:
                priority = current_priority
                break
            elif priority_input.strip() == '':
                priority = 10
                break
            try:
                priority = int(priority_input)
                break
            except ValueError:
                messagebox.showerror('Invalid Input', 'Please Enter a Valid Numeric Priority.')

        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        c.execute('''
            UPDATE gifts
            SET name=?, description=?, price=?, link=?, priority=?
            WHERE id=?
        ''', (name, desc, price, link, priority, gift_id))
        conn.commit()
        conn.close()

        load_gifts()
        messagebox.showinfo('Gift Edited', 'The Gift details have been Updated.')

# Delete selected Gift
def delete_gift():
    selected = tree.selection()

    if not selected:
        messagebox.showwarning('Warning', 'No gift selected.')
        return

    gift_id = int(selected[0])
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    c.execute('DELETE FROM gifts WHERE id=?', (gift_id,))

    conn.commit()
    conn.close()

    load_gifts()

# Mark selected Gift as Purchased
def mark_purchased():
    selected = tree.selection()

    if not selected:
        messagebox.showwarning('Warning', 'No gift selected.')
        return

    gift_id = int(selected[0])
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    c.execute('UPDATE gifts SET purchased=1 WHERE id=?', (gift_id,))

    conn.commit()
    conn.close()

    load_gifts()
    
    messagebox.showinfo('Marked as Purchased', f'Gift ID {gift_id} has been Marked as Purchased')

# Add Gift Dialog
def open_add_gift_dialog():
    name = simpledialog.askstring('Gift Name', 'Enter the Gift Name:', parent=root)

    if not name:
        return
    desc = simpledialog.askstring('Description', 'Enter Description (Optional):', parent=root) or ''
    try:
        price = float(simpledialog.askstring('Price', 'Enter Price (Optional):', parent=root) or 0)
    except:
        price = 0
    link = simpledialog.askstring('Link', 'Enter Link (Optional):', parent=root) or ''
    try:
        priority = int(simpledialog.askstring('Priority', 'Enter Priority (1=Highest):', parent=root) or 10)
    except:
        priority = 10

    add_gift(name, desc, price, link, priority)

# GUI Setup
root = tk.Tk()
root.title('Gift Catalog Application')
root.geometry('800x400')

# Treeview for Displaying Gifts
columns = ('ID', 'Name', 'Description', 'Price', 'Link', 'Priority', 'Purchased')
tree = ttk.Treeview(root, columns=columns, show='headings')

for col in columns:
    tree.heading(col, text=col)
    
    if col == '#':
        tree.column(col, width=40, anchor='center')
    elif col == 'Name':
        tree.column(col, width=150, anchor='center')
    elif col == 'Description':
        tree.column(col, width=200, anchor='center')
    elif col == 'Price':
        tree.column(col, width=80, anchor='center')
    elif col == 'Link':
        tree.column(col, width=150, anchor='center')
    elif col == 'Priority':
        tree.column(col, width=80, anchor='center')
    elif col == 'Purchased':
        tree.column(col, width=80, anchor='center')

tree.pack(fill='both', expand=True)

# Button Frame
button_frame = tk.Frame(root)
button_frame.pack(fill='x')

add_btn = tk.Button(button_frame, text='Add Gift', command=open_add_gift_dialog)
add_btn.pack(side='left', padx=5, pady=5)

edit_btn = tk.Button(button_frame, text='Edit Gift', command=edit_gift)
edit_btn.pack(side='left', padx=5, pady=5)

delete_btn = tk.Button(button_frame, text='Delete Gift', command=delete_gift)
delete_btn.pack(side='left', padx=5, pady=5)

mark_btn = tk.Button(button_frame, text='Mark as Purchased', command=mark_purchased)
mark_btn.pack(side='left', padx=5, pady=5)

refresh_btn = tk.Button(button_frame, text='Refresh', command=load_gifts)
refresh_btn.pack(side='left', padx=5, pady=5)

# Initialize and Load Gifts
init_db()
load_gifts()

root.mainloop()