import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash

conn = sqlite3.connect('todo_lang.db')
cursor = conn.cursor()

cursor.execute('''
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE,
    password TEXT
)
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS tasks (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    title TEXT,
    priority TEXT,
    due TEXT,
    completed INTEGER DEFAULT 0
)
''')
conn.commit()

# Language dictionary
LANG = {
    "en": {
        "login": "Login",
        "signup": "Signup",
        "username": "Username",
        "password": "Password",
        "task": "Task",
        "priority": "Priority",
        "due": "Due Date (YYYY-MM-DD HH:MM)",
        "add": "Add Task",
        "complete": "Mark Complete",
        "delete": "Delete",
        "search": "Search",
        "title": "Title",
        "status": "Status",
        "done": "✔️ Done",
        "pending": "⏳ Pending",
        "select_lang": "Select Language",
        "back": "Back",
        "register": "Register",
        "task_required": "Task title is required!",
        "user_exists": "Username already exists!",
        "registered": "Registered successfully!",
        "invalid": "Invalid credentials!",
        "select_task": "Please select a task.",
        "dashboard": "To-Do Dashboard"
    },
    "hi": {
        "login": "लॉगिन",
        "signup": "नया खाता",
        "username": "उपयोगकर्ता नाम",
        "password": "पासवर्ड",
        "task": "कार्य",
        "priority": "प्राथमिकता",
        "due": "नियत दिनांक (YYYY-MM-DD HH:MM)",
        "add": "कार्य जोड़ें",
        "complete": "पूरा करें",
        "delete": "हटाएं",
        "search": "खोजें",
        "title": "शीर्षक",
        "status": "स्थिति",
        "done": "✔️ पूर्ण",
        "pending": "⏳ लंबित",
        "select_lang": "भाषा चुनें",
        "back": "पीछे",
        "register": "पंजीकरण करें",
        "task_required": "कार्य शीर्षक आवश्यक है!",
        "user_exists": "उपयोगकर्ता नाम पहले से मौजूद है!",
        "registered": "पंजीकरण सफल!",
        "invalid": "गलत जानकारी!",
        "select_task": "कृपया कार्य चुनें।",
        "dashboard": "कार्य सूची"
    }
}

class ToDoApp:
    def __init__(self, root):
        self.root = root
        self.lang = "en"
        self.root.geometry("850x650")
        self.select_language()

    def get(self, key):
        return LANG[self.lang].get(key, key)

    def clear(self):
        for widget in self.root.winfo_children():
            widget.destroy()

    def select_language(self):
        self.clear()
        self.root.title("To-Do App - Language Selection")
        tk.Label(self.root, text=self.get("select_lang"), font=("Arial", 20)).pack(pady=30)
        ttk.Button(self.root, text="English", command=lambda: self.set_lang("en")).pack(pady=10)
        ttk.Button(self.root, text="हिन्दी", command=lambda: self.set_lang("hi")).pack()

    def set_lang(self, lang):
        self.lang = lang
        self.login_screen()

    def login_screen(self):
        self.clear()
        self.root.title(f"{self.get('login')} | {self.get('dashboard')}")
        tk.Label(self.root, text=self.get("login"), font=("Arial", 24)).pack(pady=20)

        tk.Label(self.root, text=self.get("username")).pack()
        self.username_entry = tk.Entry(self.root, font=("Arial", 14))
        self.username_entry.pack(pady=5)

        tk.Label(self.root, text=self.get("password")).pack()
        self.password_entry = tk.Entry(self.root, show="*", font=("Arial", 14))
        self.password_entry.pack(pady=5)

        ttk.Button(self.root, text=self.get("login"), command=self.login).pack(pady=10)
        ttk.Button(self.root, text=self.get("signup"), command=self.signup_screen).pack()

    def signup_screen(self):
        self.clear()
        tk.Label(self.root, text=self.get("signup"), font=("Arial", 24)).pack(pady=20)

        tk.Label(self.root, text=self.get("username")).pack()
        self.new_username = tk.Entry(self.root, font=("Arial", 14))
        self.new_username.pack(pady=5)

        tk.Label(self.root, text=self.get("password")).pack()
        self.new_password = tk.Entry(self.root, show="*", font=("Arial", 14))
        self.new_password.pack(pady=5)

        ttk.Button(self.root, text=self.get("register"), command=self.signup).pack(pady=10)
        ttk.Button(self.root, text=self.get("back"), command=self.login_screen).pack()

    def signup(self):
        username = self.new_username.get()
        password = self.new_password.get()
        try:
            hashed = generate_password_hash(password)
            cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, hashed))
            conn.commit()
            messagebox.showinfo("Success", self.get("registered"))
            self.login_screen()
        except sqlite3.IntegrityError:
            messagebox.showerror("Error", self.get("user_exists"))

    def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        cursor.execute("SELECT id, password FROM users WHERE username=?", (username,))
        user = cursor.fetchone()
        if user and check_password_hash(user[1], password):
            self.user_id = user[0]
            self.dashboard()
        else:
            messagebox.showerror(self.get("login"), self.get("invalid"))

    def dashboard(self):
        self.clear()
        self.root.title(f"{self.get('dashboard')}")
        tk.Label(self.root, text=self.get("dashboard"), font=("Arial", 22)).pack(pady=10)

        input_frame = tk.Frame(self.root)
        input_frame.pack(pady=10)

        tk.Label(input_frame, text=self.get("task")).grid(row=0, column=0)
        self.task_entry = tk.Entry(input_frame, font=("Arial", 12), width=30)
        self.task_entry.grid(row=0, column=1, padx=5)

        tk.Label(input_frame, text=self.get("priority")).grid(row=1, column=0)
        self.priority_box = ttk.Combobox(input_frame, values=["Low", "Medium", "High"])
        self.priority_box.set("Medium")
        self.priority_box.grid(row=1, column=1, padx=5)

        tk.Label(input_frame, text=self.get("due")).grid(row=2, column=0)
        self.due_entry = tk.Entry(input_frame, font=("Arial", 12))
        self.due_entry.grid(row=2, column=1, padx=5)
        self.due_entry.insert(0, datetime.now().strftime("%Y-%m-%d %H:%M"))

        ttk.Button(input_frame, text=self.get("add"), command=self.add_task).grid(row=3, column=1, pady=10)

        # 🔍 Search bar
        search_frame = tk.Frame(self.root)
        search_frame.pack(pady=5)
        tk.Label(search_frame, text=f"{self.get('search')}:").grid(row=0, column=0)
        self.search_entry = tk.Entry(search_frame, font=("Arial", 12), width=30)
        self.search_entry.grid(row=0, column=1, padx=5)
        ttk.Button(search_frame, text=self.get("search"), command=self.search_tasks).grid(row=0, column=2)

        # 📋 Treeview
        self.tree = ttk.Treeview(self.root, columns=("Title", "Priority", "Due", "Status"), show="headings", height=12)
        self.tree.heading("Title", text=self.get("title"))
        self.tree.heading("Priority", text=self.get("priority"))
        self.tree.heading("Due", text=self.get("due"))
        self.tree.heading("Status", text=self.get("status"))
        self.tree.column("Title", width=200)
        self.tree.column("Priority", width=100)
        self.tree.column("Due", width=150)
        self.tree.column("Status", width=100)
        self.tree.pack(pady=10)

        btn_frame = tk.Frame(self.root)
        btn_frame.pack(pady=5)
        ttk.Button(btn_frame, text=self.get("complete"), command=self.complete_task).grid(row=0, column=0, padx=5)
        ttk.Button(btn_frame, text=self.get("delete"), command=self.delete_task).grid(row=0, column=1, padx=5)

        self.display_tasks()

    def add_task(self):
        title = self.task_entry.get().strip()
        priority = self.priority_box.get()
        due = self.due_entry.get().strip()

        if not title:
            messagebox.showerror("Error", self.get("task_required"))
            return

        cursor.execute("INSERT INTO tasks (user_id, title, priority, due, completed) VALUES (?, ?, ?, ?, 0)",
                       (self.user_id, title, priority, due))
        conn.commit()
        self.task_entry.delete(0, tk.END)
        self.display_tasks()

    def display_tasks(self, filter_text=""):
        for row in self.tree.get_children():
            self.tree.delete(row)

        if filter_text:
            cursor.execute("SELECT id, title, priority, due, completed FROM tasks WHERE user_id=? AND title LIKE ?",
                           (self.user_id, f'%{filter_text}%'))
        else:
            cursor.execute("SELECT id, title, priority, due, completed FROM tasks WHERE user_id=?",
                           (self.user_id,))

        tasks = cursor.fetchall()
        for task in tasks:
            status = self.get("done") if task[4] else self.get("pending")
            self.tree.insert("", "end", iid=task[0], values=(task[1], task[2], task[3], status))

    def search_tasks(self):
        query = self.search_entry.get().strip()
        self.display_tasks(query)

    def complete_task(self):
        selected = self.tree.focus()
        if selected:
            cursor.execute("UPDATE tasks SET completed=1 WHERE id=?", (selected,))
            conn.commit()
            self.display_tasks()
        else:
            messagebox.showwarning("Warning", self.get("select_task"))

    def delete_task(self):
        selected = self.tree.focus()
        if selected:
            cursor.execute("DELETE FROM tasks WHERE id=?", (selected,))
            conn.commit()
            self.display_tasks()
        else:
            messagebox.showwarning("Warning", self.get("select_task"))

if __name__ == "__main__":
    root = tk.Tk()
    app = ToDoApp(root)
    root.mainloop()
