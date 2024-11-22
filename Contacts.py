import tkinter as tk
from tkinter import messagebox, simpledialog
import json

FILENAME = "contacts.json"

def load_contacts():
    try:
        with open(FILENAME, "r") as file:
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        return {}

def save_contacts(contacts):
    with open(FILENAME, "w") as file:
        json.dump(contacts, file, indent=4)

class ContactManagerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("NJONGO Contact Manager")
        self.contacts = load_contacts()

        # GUI Components
        self.listbox = tk.Listbox(root, width=50, height=15)
        self.listbox.pack(pady=10)
        self.update_contact_list()

        tk.Button(root, text="Add Contact", command=self.add_contact).pack(pady=5)
        tk.Button(root, text="View Contact", command=self.view_contact).pack(pady=5)
        tk.Button(root, text="Edit Contact", command=self.edit_contact).pack(pady=5)
        tk.Button(root, text="Delete Contact", command=self.delete_contact).pack(pady=5)
        tk.Button(root, text="Exit", command=self.exit_app).pack(pady=10)

    def update_contact_list(self):
        self.listbox.delete(0, tk.END)
        for name in self.contacts:
            self.listbox.insert(tk.END, name)

    def add_contact(self):
        name = simpledialog.askstring("Add Contact", "Enter name:")
        if not name:
            return
        phone = simpledialog.askstring("Add Contact", "Enter phone number:")
        email = simpledialog.askstring("Add Contact", "Enter email address:")
        if name and phone and email:
            self.contacts[name] = {"phone": phone, "email": email}
            self.update_contact_list()
            save_contacts(self.contacts)
            messagebox.showinfo("Success", f"Contact '{name}' added successfully!")

    def view_contact(self):
        selected = self.listbox.curselection()
        if not selected:
            messagebox.showerror("Error", "Please select a contact to view.")
            return
        name = self.listbox.get(selected)
        details = self.contacts[name]
        messagebox.showinfo("Contact Details", f"Name: {name}\nPhone: {details['phone']}\nEmail: {details['email']}")

    def edit_contact(self):
        selected = self.listbox.curselection()
        if not selected:
            messagebox.showerror("Error", "Please select a contact to edit.")
            return
        name = self.listbox.get(selected)
        phone = simpledialog.askstring("Edit Contact", f"Enter new phone number (current: {self.contacts[name]['phone']}):")
        email = simpledialog.askstring("Edit Contact", f"Enter new email address (current: {self.contacts[name]['email']}):")
        if phone and email:
            self.contacts[name] = {"phone": phone, "email": email}
            save_contacts(self.contacts)
            messagebox.showinfo("Success", f"Contact '{name}' updated successfully!")

    def delete_contact(self):
        selected = self.listbox.curselection()
        if not selected:
            messagebox.showerror("Error", "Please select a contact to delete.")
            return
        name = self.listbox.get(selected)
        confirm = messagebox.askyesno("Confirm Delete", f"Are you sure you want to delete '{name}'?")
        if confirm:
            del self.contacts[name]
            self.update_contact_list()
            save_contacts(self.contacts)
            messagebox.showinfo("Success", f"Contact '{name}' deleted successfully!")

    def exit_app(self):
        save_contacts(self.contacts)
        self.root.destroy()

# Main Program
if __name__ == "__main__":
    root = tk.Tk()
    app = ContactManagerApp(root)
    root.mainloop()
