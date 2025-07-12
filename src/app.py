import tkinter as tk
import tkinter.font as tkFont
from tkinter import messagebox, ttk
import sqlite3
import os

# Ensure 'dat' Folder Exists
DATA_FOLDER = 'dat'
os.makedirs(DATA_FOLDER, exist_ok=True)
DB_PATH = os.path.join(DATA_FOLDER, 'gift_catalog.db')

# Style Initialisations
BG_COLOR = '#0d0d0d'
ACCENT_COLOR = '#00ffff'
TEXT_COLOR = '#ffffff'
HEADER_BG = '#1a1a2e'
HEADER_FG = '#ff77ff'
FONT = ('Consolas', 10, 'bold')


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

# Multi-Input Pop-up Window
def synthwave_multi_input(title, prefill=None):
    def on_submit():
        nonlocal user_input
        try:
            price_val = float(price_entry.get()) if price_entry.get().strip() else 0.0
        except ValueError:
            messagebox.showerror('Invalid Input', 'Please Enter a Valid Numeric Price.', parent=popup)
            return
        try:
            priority_val = int(priority_entry.get()) if priority_entry.get().strip() else 10
        except ValueError:
            messagebox.showerror('Invalid Input', 'Please Enter a Valid Numeric Priority.', parent=popup)
            return

        if not name_entry.get().strip():
            messagebox.showerror('Invalid Input', 'Gift Name is Required.', parent=popup)
            return

        user_input = {
            'name': name_entry.get().strip(),
            'desc': desc_entry.get().strip(),
            'price': price_val,
            'link': link_entry.get().strip(),
            'priority': priority_val
        }
        popup.destroy()

    def on_cancel():
        popup.destroy()

    user_input = None
    popup = tk.Toplevel(root)
    popup.title(title)
    popup.configure(bg=BG_COLOR)
    popup.geometry('400x400')
    popup.grab_set()

    fields = [
        ('Gift Name:', 'name'),
        ('Description:', 'desc'),
        ('Price:', 'price'),
        ('Link:', 'link'),
        ('Priority:', 'priority')
    ]

    entries = {}

    for idx, (label_text, key) in enumerate(fields):
        label = tk.Label(popup, text=label_text, bg=BG_COLOR, fg=ACCENT_COLOR, font=FONT, anchor='w')
        label.pack(pady=(10 if idx == 0 else 5, 0), fill='x', padx=20)
        entry = tk.Entry(popup, bg=HEADER_BG, fg=ACCENT_COLOR, font=FONT, insertbackground=ACCENT_COLOR)
        entry.pack(pady=5, fill='x', padx=20)
        entries[key] = entry

    name_entry = entries['name']
    desc_entry = entries['desc']
    price_entry = entries['price']
    link_entry = entries['link']
    priority_entry = entries['priority']

    # Pre-fill if Editing
    if prefill:
        name_entry.insert(0, prefill.get('name', ''))
        desc_entry.insert(0, prefill.get('desc', ''))
        price_entry.insert(0, str(prefill.get('price', '')))
        link_entry.insert(0, prefill.get('link', ''))
        priority_entry.insert(0, str(prefill.get('priority', '')))

    name_entry.focus_set()

    btn_frame = tk.Frame(popup, bg=BG_COLOR)
    btn_frame.pack(pady=20)

    submit_btn = tk.Button(btn_frame, text='Submit', command=on_submit, bg=HEADER_BG, fg=ACCENT_COLOR, font=FONT, activebackground=ACCENT_COLOR, activeforeground=BG_COLOR, width=10)
    submit_btn.pack(side='left', padx=10)

    cancel_btn = tk.Button(btn_frame, text='Cancel', command=on_cancel, bg=HEADER_BG, fg=ACCENT_COLOR, font=FONT, activebackground=ACCENT_COLOR, activeforeground=BG_COLOR, width=10)
    cancel_btn.pack(side='left', padx=10)

    popup.wait_window()
    return user_input

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
        current_data = {
            'name': result[0],
            'desc': result[1],
            'price': result[2],
            'link': result[3],
            'priority': result[4]
        }
        updated_data = synthwave_multi_input('Edit Gift', prefill=current_data)
        if updated_data:
            conn = sqlite3.connect(DB_PATH)
            c = conn.cursor()
            c.execute('''
                UPDATE gifts
                SET name=?, description=?, price=?, link=?, priority=?
                WHERE id=?
            ''', (
                updated_data['name'],
                updated_data['desc'],
                updated_data['price'],
                updated_data['link'],
                updated_data['priority'],
                gift_id
            ))
            conn.commit()
            conn.close()
            load_gifts()
            messagebox.showinfo('Gift Edited', 'The Gift Details have been Updated.')

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
    result = synthwave_multi_input('Add Gift')
    if result:
        add_gift(
            result['name'],
            result['desc'],
            result['price'],
            result['link'],
            result['priority']
        )

# GUI Setup
root = tk.Tk()
root.title('Gift Catalog')
root.geometry('950x500')

style = ttk.Style()
style.theme_use('default')
style.configure('Treeview',
                background=BG_COLOR,
                foreground=TEXT_COLOR,
                fieldbackground=BG_COLOR,
                rowheight=25,
                font=FONT)
style.configure('Treeview.Heading',
                background=HEADER_BG,
                foreground=ACCENT_COLOR,
                font=FONT)
style.map('Treeview', background=[('selected', ACCENT_COLOR)], foreground=[('selected', BG_COLOR)])

# Treeview for Displaying Gifts
columns = ('#', 'Name', 'Description', 'Price', 'Link', 'Priority', 'Purchased')
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
button_frame = tk.Frame(root, bg=BG_COLOR)
button_frame.pack(fill='x')

# Sytling of Buttons
def styled_button(master, text, command):
    btn = tk.Button(master, text=text, command=command, bg=HEADER_BG, fg=ACCENT_COLOR, font=FONT,
                    activebackground=ACCENT_COLOR, activeforeground=BG_COLOR)
    btn.pack(side='left', padx=5, pady=5)
    return btn

add_btn = styled_button(button_frame, 'Add Gift', open_add_gift_dialog)
edit_btn = styled_button(button_frame, 'Edit Gift', edit_gift)
delete_btn = styled_button(button_frame, 'Delete Gift', delete_gift)
mark_btn = styled_button(button_frame, 'Mark as Purchased', mark_purchased)
refresh_btn = styled_button(button_frame, 'Refresh', load_gifts)


# Initialize and Load Gifts
init_db()
load_gifts()

root.mainloop()