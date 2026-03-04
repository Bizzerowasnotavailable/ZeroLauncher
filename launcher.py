import tkinter as tk
from tkinter import messagebox
import subprocess
import os
import requests
from PIL import Image, ImageTk
from io import BytesIO

def launch_minecraft():
    name = name_entry.get().strip()
    server = server_entry.get().strip()
    minecraft_path = path_entry.get().strip()

    # checks every textfield and freaks out if some stuff isn't specified
    if not name:
        messagebox.showerror("Error", "Name is required.")
        return

    if not minecraft_path:
        messagebox.showerror("Error", "Minecraft.Client path is required, make sure you add the exe to the path")
        return

    if not os.path.exists(minecraft_path):
        messagebox.showerror("Error", f"{minecraft_path} not found.")
        return

    args = [minecraft_path, "-name", name]

    # Server mode logic
    if is_server_var.get():
        args.append("-server")
        if server:  
            args.extend(["-ip", server])
    elif server:
        args.extend(["-ip", server])

    try:
        subprocess.Popen(args)
    except Exception as e:
        messagebox.showerror("Launch Error", str(e))

# change textbox names if the launcher is set to server mode
def update_labels(*args):
    if is_server_var.get():
        name_label.config(text="Server display name (not world name):")
        server_label.config(text="Custom IP (leave blank for default):")
    else:
        name_label.config(text="Player name:")
        server_label.config(text="online server IP")

# graphics stuff


root = tk.Tk()
root.title("LCE ZeroLauncher")
root.geometry("800x500")
root.resizable(False, False)
root.configure(bg="#000000")

url = "https://raw.githubusercontent.com/Bizzerowasnotavailable/ZeroLauncher/refs/heads/main/logo.png"

logo = None

try:
    response = requests.get(url, timeout=5)
    response.raise_for_status()
    img_data = Image.open(BytesIO(response.content))
    img_data = img_data.resize((819, 164))
    logo = ImageTk.PhotoImage(img_data)

except Exception:
    # if there's no wifi, try using the local file
    try:
        img_data = Image.open("logo.png")
        img_data = img_data.resize((819, 164))
        logo = ImageTk.PhotoImage(img_data)
    except Exception:
        logo = None  # if there's ALSO no local file, try the nuclear option, aka don't show any logo at all,
        # thinking about it, I could add a funky ahh comic sans logo when nothing else works :3

# creating label ONLY if logo exists
if logo:
    logo_label = tk.Label(root, image=logo, bg="#000000")
    logo_label.pack(pady=10)

name_label = tk.Label(root, text="Player name:", bg="#000000", fg="white")
name_label.pack(pady=(10, 0))

name_entry = tk.Entry(root, width=30)
name_entry.pack()

server_label = tk.Label(root, text="online server IP", bg="#000000", fg="white")
server_label.pack(pady=(10, 0))

server_entry = tk.Entry(root, width=30)
server_entry.pack()

is_server_var = tk.BooleanVar()
server_checkbox = tk.Checkbutton(
    root,
    text="Server mode",
    variable=is_server_var,
    bg="#000000",
    fg="yellow",
    selectcolor="#000000",
    activebackground="#000000",
    activeforeground="cyan"
)
server_checkbox.pack(pady=5)

# Bind the checkbox change to update the labels
is_server_var.trace("w", update_labels)

tk.Label(root, text="Minecraft.Client path INCLUDING THE EXE:", bg="#000000", fg="white").pack(pady=(10, 0))
path_entry = tk.Entry(root, width=67) # SIX SEVEEEEEN ( god kill me )
path_entry.pack()

tk.Button(root, text="Launch LCE", command=launch_minecraft, width=40, height=3).pack(pady=20)

root.mainloop()