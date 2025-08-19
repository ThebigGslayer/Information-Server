import tkinter as tk
from tkinter import messagebox, ttk
import sqlite3

# Create or connect to SQLite database
conn = sqlite3.connect("user_data.db")
cursor = conn.cursor()

# Create table if it doesn't exist
cursor.execute("""
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL,
    password TEXT NOT NULL,
    additional_info TEXT
)
""")
conn.commit()

# Save user data
def save_data():
    username = username_entry.get()
    password = password_entry.get()
    additional_info = info_entry.get("1.0", tk.END).strip()

    if not username or not password:
        messagebox.showwarning("Input Error", "Username and Password are required!")
        return
    
    cursor.execute("INSERT INTO users (username, password, additional_info) VALUES (?, ?, ?)",
                   (username, password, additional_info))
    conn.commit()
    messagebox.showinfo("Success", "Data saved successfully!")
    clear_entries()

# Clear input fields
def clear_entries():
    username_entry.delete(0, tk.END)
    password_entry.delete(0, tk.END)
    info_entry.delete("1.0", tk.END)

# View, Edit, and Delete user data
def view_data():
    def load_selected_record(event):
        selected_item = tree.selection()
        if not selected_item:
            return
        record = tree.item(selected_item[0])["values"]
        edit_id.set(record[0])
        edit_username.set(record[1])
        edit_password.set(record[2])
        edit_info.delete("1.0", tk.END)
        edit_info.insert(tk.END, record[3])

    def update_record():
        if not edit_id.get():
            messagebox.showwarning("Selection Error", "Please select a record to edit!")
            return
        
        username = edit_username.get()
        password = edit_password.get()
        additional_info = edit_info.get("1.0", tk.END).strip()

        if not username or not password:
            messagebox.showwarning("Input Error", "Username and Password are required!")
            return

        cursor.execute("""
        UPDATE users
        SET username = ?, password = ?, additional_info = ?
        WHERE id = ?
        """, (username, password, additional_info, edit_id.get()))
        conn.commit()
        messagebox.showinfo("Success", "Record updated successfully!")
        load_data()

    def delete_record():
        selected_items = tree.selection()
        if not selected_items:
            messagebox.showwarning("Selection Error", "Please select record(s) to delete!")
            return
        
        confirm = messagebox.askyesno("Confirm Delete", f"Are you sure you want to delete {len(selected_items)} record(s)?")
        if confirm:
            for item in selected_items:
                record = tree.item(item)["values"]
                cursor.execute("DELETE FROM users WHERE id = ?", (record[0],))
            conn.commit()
            messagebox.showinfo("Success", "Selected record(s) deleted successfully!")
            load_data()

    def select_all_records():
        tree.selection_set(tree.get_children())

    def load_data():
        for row in tree.get_children():
            tree.delete(row)
        cursor.execute("SELECT id, username, password, additional_info FROM users")
        rows = cursor.fetchall()
        for row in rows:
            tree.insert("", tk.END, values=row)

    # Create a new window for viewing, editing, and deleting data
    view_window = tk.Toplevel(root)
    view_window.title("View, Edit, and Delete Data")
    view_window.geometry("500x500")
    view_window.configure(bg="#1e1e2e")
    
    # Add a scrollable treeview to display data
    columns = ("ID", "Username", "Password", "Name Of Website/App")
    tree = ttk.Treeview(view_window, columns=columns, show="headings")
    
    for col in columns:
        tree.heading(col, text=col)
        tree.column(col, width=120)
    tree.pack(fill=tk.BOTH, expand=True, pady=10, padx=10)
    
    # Add scrollbar
    scrollbar = ttk.Scrollbar(view_window, orient=tk.VERTICAL, command=tree.yview)
    tree.configure(yscroll=scrollbar.set)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    # Form to edit selected record
    tk.Label(view_window, text="Edit Record", font=("Arial", 12, "bold"), bg="#1e1e2e", fg="cyan").pack(pady=10)
    
    edit_id = tk.StringVar()
    edit_username = tk.StringVar()
    edit_password = tk.StringVar()
    
    tk.Label(view_window, text="Username:", bg="#1e1e2e", fg="white").pack()
    edit_username_entry = tk.Entry(view_window, textvariable=edit_username, width=30, bg="#2e2e3e", fg="cyan")
    edit_username_entry.pack()

    tk.Label(view_window, text="Password:", bg="#1e1e2e", fg="white").pack()
    edit_password_entry = tk.Entry(view_window, textvariable=edit_password, width=30, show="*", bg="#2e2e3e", fg="cyan")
    edit_password_entry.pack()

    tk.Label(view_window, text="Additional Info:", bg="#1e1e2e", fg="white").pack()
    edit_info = tk.Text(view_window, height=5, width=40, bg="#2e2e3e", fg="cyan")
    edit_info.pack()

    # Update button
    update_button = tk.Button(view_window, text="Update", command=update_record, bg="orange", fg="white", font=("Arial", 10))
    update_button.pack(pady=5)

    # Delete button
    delete_button = tk.Button(view_window, text="Delete Selected", command=delete_record, bg="red", fg="white", font=("Arial", 10))
    delete_button.pack(pady=5)

    # Select All button
    select_all_button = tk.Button(view_window, text="Select All", command=select_all_records, bg="blue", fg="white", font=("Arial", 10))
    select_all_button.pack(pady=5)

    # Load data into the TreeView
    load_data()

    # Bind row selection to load data into edit fields
    tree.bind("<<TreeviewSelect>>", load_selected_record)

# Create the main application window
root = tk.Tk()
root.title("Zino Info Saver")
root.geometry("500x500")
root.resizable(False, False)
root.configure(bg="#1e1e2e")

# Username label and entry
tk.Label(root, text="Username:", font=("Arial", 10), bg="#1e1e2e", fg="white").pack(pady=5)
username_entry = tk.Entry(root, width=30, bg="#2e2e3e", fg="cyan")
username_entry.pack()

# Password label and entry
tk.Label(root, text="Password:", font=("Arial", 10), bg="#1e1e2e", fg="white").pack(pady=5)
password_entry = tk.Entry(root, width=30, show="*", bg="#2e2e3e", fg="cyan")
password_entry.pack()

# Additional info label and entry
tk.Label(root, text="Additional Info:", font=("Arial", 10), bg="#1e1e2e", fg="white").pack(pady=5)
info_entry = tk.Text(root, height=5, width=30, bg="#2e2e3e", fg="cyan")
info_entry.pack()

# Save button
save_button = tk.Button(root, text="Save", command=save_data, bg="#005500", fg="white", font=("Arial", 10))
save_button.pack(pady=10)

# View button
view_button = tk.Button(root, text="View, Edit, and Delete Data", command=view_data, bg="#000066", fg="white", font=("Arial", 10))
view_button.pack(pady=10)

# Run the application
root.mainloop()

# Close database connection when done
conn.close()
