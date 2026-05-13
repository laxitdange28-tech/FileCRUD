# #project - CRUD Operation with Tkinter UI

from pathlib import Path
import os
import tkinter as tk
from tkinter import messagebox, simpledialog


# ---------------- MAIN WINDOW ---------------- #

root = tk.Tk()
root.title("CRUD File Handling Project")
root.geometry("500x600")
root.config(bg="lightblue")


# ---------------- FUNCTIONS ---------------- #

def show_files():
    try:
        p = Path('')
        items = list(p.rglob('*'))

        text_area.delete(1.0, tk.END)

        if not items:
            text_area.insert(tk.END, "No files/folders found")
        else:
            for index, file in enumerate(items):
                text_area.insert(tk.END, f"{index + 1} - {file}\n")

    except Exception as e:
        messagebox.showerror("Error", str(e))


def create_file():
    try:
        file_name = simpledialog.askstring("Create File", "Enter file name")

        if not file_name:
            return

        p = Path(file_name)

        if p.exists():
            messagebox.showwarning("Warning", "File already exists")

        else:
            content = simpledialog.askstring("Content", "Enter file content")

            with open(file_name, 'w') as file:
                file.write(content if content else "")

            messagebox.showinfo("Success", "File created successfully")
            show_files()

    except Exception as e:
        messagebox.showerror("Error", str(e))


def read_file():
    try:
        file_name = simpledialog.askstring("Read File", "Enter file name")

        if not file_name:
            return

        p = Path(file_name)

        if p.exists():

            with open(file_name, 'r') as file:
                content = file.read()

            text_area.delete(1.0, tk.END)
            text_area.insert(tk.END, content)

        else:
            messagebox.showwarning("Warning", "File not found")

    except Exception as e:
        messagebox.showerror("Error", str(e))


def update_file():
    try:
        file_name = simpledialog.askstring("Update File", "Enter file name")

        if not file_name:
            return

        p = Path(file_name)

        if p.exists():

            choice = simpledialog.askinteger(
                "Choice",
                "Press 1 for overwrite\nPress 2 for append"
            )

            content = simpledialog.askstring(
                "Content",
                "Enter new content"
            )

            if choice == 1:

                with open(file_name, 'w') as file:
                    file.write(content if content else "")

                messagebox.showinfo("Success", "File overwritten")

            elif choice == 2:

                with open(file_name, 'a') as file:
                    file.write(content if content else "")

                messagebox.showinfo("Success", "Content appended")

            else:
                messagebox.showwarning("Warning", "Invalid choice")

        else:
            messagebox.showwarning("Warning", "File not found")

    except Exception as e:
        messagebox.showerror("Error", str(e))


def delete_file():
    try:
        file_name = simpledialog.askstring("Delete File", "Enter file name")

        if not file_name:
            return

        if os.path.exists(file_name):

            os.remove(file_name)

            messagebox.showinfo("Success", "File deleted")
            show_files()

        else:
            messagebox.showwarning("Warning", "File not found")

    except Exception as e:
        messagebox.showerror("Error", str(e))


def rename_file():
    try:
        old_name = simpledialog.askstring(
            "Rename File",
            "Enter current file name"
        )

        if not old_name:
            return

        p = Path(old_name)

        if p.exists():

            new_name = simpledialog.askstring(
                "New Name",
                "Enter new file name"
            )

            os.rename(old_name, new_name)

            messagebox.showinfo("Success", "File renamed")
            show_files()

        else:
            messagebox.showwarning("Warning", "File not found")

    except Exception as e:
        messagebox.showerror("Error", str(e))


def create_folder():
    try:
        folder_name = simpledialog.askstring(
            "Create Folder",
            "Enter folder name"
        )

        if not folder_name:
            return

        p = Path(folder_name)

        if p.exists():

            messagebox.showwarning("Warning", "Folder already exists")

        else:

            p.mkdir()

            messagebox.showinfo("Success", "Folder created")
            show_files()

    except Exception as e:
        messagebox.showerror("Error", str(e))


def remove_folder():
    try:
        folder_name = simpledialog.askstring(
            "Remove Folder",
            "Enter folder name"
        )

        if not folder_name:
            return

        p = Path(folder_name)

        if p.exists():

            p.rmdir()

            messagebox.showinfo("Success", "Folder removed")
            show_files()

        else:
            messagebox.showwarning("Warning", "Folder not found")

    except Exception as e:
        messagebox.showerror("Error", str(e))


def create_file_in_folder():
    try:
        folder_name = simpledialog.askstring(
            "Folder",
            "Enter folder name"
        )

        file_name = simpledialog.askstring(
            "File",
            "Enter file name"
        )

        if not folder_name or not file_name:
            return

        p = Path(folder_name) / file_name

        if p.exists():

            messagebox.showwarning("Warning", "File already exists")

        else:

            content = simpledialog.askstring(
                "Content",
                "Enter file content"
            )

            with open(p, 'w') as file:
                file.write(content if content else "")

            messagebox.showinfo(
                "Success",
                "File created inside folder"
            )

            show_files()

    except Exception as e:
        messagebox.showerror("Error", str(e))


# ---------------- HEADING ---------------- #

title = tk.Label(
    root,
    text="CRUD File Handling Project",
    font=("Arial", 18, "bold"),
    bg="lightblue",
    fg="darkblue"
)

title.pack(pady=10)


# ---------------- BUTTONS ---------------- #

btn1 = tk.Button(root, text="Create File", width=25, command=create_file)
btn1.pack(pady=5)

btn2 = tk.Button(root, text="Read File", width=25, command=read_file)
btn2.pack(pady=5)

btn3 = tk.Button(root, text="Update File", width=25, command=update_file)
btn3.pack(pady=5)

btn4 = tk.Button(root, text="Delete File", width=25, command=delete_file)
btn4.pack(pady=5)

btn5 = tk.Button(root, text="Rename File", width=25, command=rename_file)
btn5.pack(pady=5)

btn6 = tk.Button(root, text="Create Folder", width=25, command=create_folder)
btn6.pack(pady=5)

btn7 = tk.Button(root, text="Remove Folder", width=25, command=remove_folder)
btn7.pack(pady=5)

btn8 = tk.Button(root, text="Create File In Folder", width=25, command=create_file_in_folder)
btn8.pack(pady=5)

btn9 = tk.Button(root, text="Show Files & Folders", width=25, command=show_files)
btn9.pack(pady=5)


# ---------------- TEXT AREA ---------------- #

text_area = tk.Text(root, height=15, width=55)
text_area.pack(pady=10)


# ---------------- RUN WINDOW ---------------- #

root.mainloop()