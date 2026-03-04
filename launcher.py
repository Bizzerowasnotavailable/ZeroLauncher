import tkinter as tk
from tkinter import messagebox
import subprocess
import os
import requests
from PIL import Image, ImageTk
from io import BytesIO

def toggle_server_mode():
    if is_server_var.get():
        server_entry.config(state="disabled", disabledbackground="#000000")
        name_label.config(text="Server name (not world):")
    else:
        server_entry.config(state="normal")
        name_label.config(text="Player name:")

def launch_minecraft():
    name = name_entry.get().strip()
    server = server_entry.get().strip()
    minecraft_path = path_entry.get().strip()

    if not name:
        messagebox.showerror("Error", "Name is required.")
        return

    if not minecraft_path:
        messagebox.showerror("Error", "Minecraft.Client path is required.")
        return

    if not os.path.exists(minecraft_path):
        messagebox.showerror("Error", f"{minecraft_path} not found.")
        return

    args = [minecraft_path, "-name", name]

    if is_server_var.get():
        args.append("-server")
    elif server:
        args.extend(["-ip", server])

    try:
        subprocess.Popen(args)
    except Exception as e:
        messagebox.showerror("Launch Error", str(e))

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
        logo = None  # if there's ALSO no local file, try the nuclear option, aka don't show any logo at all

# creating lable ONLY if logo exists
if logo:
    logo_label = tk.Label(root, image=logo, bg="#000000")
    logo_label.pack(pady=10)
    

name_label = tk.Label(root, text="Player name:", bg="#000000", fg="white")
name_label.pack(pady=(10, 0))

name_entry = tk.Entry(root, width=30)
name_entry.pack()

tk.Label(
    root,
    text="Server IP (leave blank if you don't want to play online)",
    bg="#000000",
    fg="white"
).pack(pady=(10, 0))

server_entry = tk.Entry(root, width=30)
server_entry.pack()

is_server_var = tk.BooleanVar()
server_checkbox = tk.Checkbutton(
    root,
    text="Server mode",
    variable=is_server_var,
    command=toggle_server_mode,
    bg="#000000",
    fg="yellow",
    selectcolor="#000000",
    activebackground="#000000",
    activeforeground="cyan"
)
server_checkbox.pack(pady=5)

tk.Label(root, text="Minecraft.Client path:", bg="#000000", fg="white").pack(pady=(10, 0))
path_entry = tk.Entry(root, width=40)
path_entry.pack()

tk.Button(root, text="Launch LCE", command=launch_minecraft, width=40, height=3).pack(pady=20)


root.mainloop()