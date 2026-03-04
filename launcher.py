import tkinter as tk
from tkinter import messagebox
import subprocess
import os
import requests
from PIL import Image, ImageTk
from io import BytesIO
import webbrowser
import re

# loading settings to file
def load_settings():
    if os.path.exists("zerolauncher.txt"):
        with open("zerolauncher.txt", "r") as f:
            lines = f.readlines()
            if len(lines) >= 2:
                name_entry.insert(0, lines[0].strip())
                path_entry.insert(0, lines[1].strip())

# save settings to file
def save_settings(name, minecraft_path):
    with open("zerolauncher.txt", "w") as f:
        f.write(f"{name}\n{minecraft_path}\n")

def is_ipv4(ip):
    """Validate the IPv4 address."""
    regex = r"^(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$"
    return re.match(regex, ip) is not None

def launch_minecraft():
    name = name_entry.get().strip()
    server = server_entry.get().strip()
    minecraft_path = path_entry.get().strip()

    # Check name length ( must be <= 16 characters cuz that's the game's limit anyway )
    if len(name) > 16:
        messagebox.showerror("Error", "Player name cannot be more than 16 characters.")
        return

    # Check if the server name length is > 16 characters (only if server mode is enabled)
    if is_server_var.get() and len(server) > 16:
        messagebox.showerror("Error", "Server name cannot be more than 16 characters.")
        return

    # Validate IP address (if provided)
    if server and not is_ipv4(server):
        messagebox.showerror("Error", "Please enter a valid IPv4 address for the server.")
        return

    # Validate Minecraft path
    if not minecraft_path:
        messagebox.showerror("Error", "Minecraft.Client path is required, make sure you add the exe to the path")
        return

    if not os.path.exists(minecraft_path):
        messagebox.showerror("Error", f"{minecraft_path} not found.")
        return

    # Save the settings to the file
    save_settings(name, minecraft_path)

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
root.geometry("800x600")
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
        # if there's no local file, just don't do anything
    except Exception:
        logo = None

# creating label ONLY if logo exists
if logo:
    logo_label = tk.Label(root, image=logo, bg="#000000")
    logo_label.pack(pady=10)

name_label = tk.Label(root, text="Player name:", bg="#000000", fg="cyan")
name_label.pack(pady=(10, 0))

name_entry = tk.Entry(root, width=17)
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

is_server_var.trace("w", update_labels)

tk.Label(root, text="Minecraft.Client path INCLUDING THE EXE:", bg="#000000", fg="white").pack(pady=(10, 0))
path_entry = tk.Entry(root, width=67)
path_entry.pack()

tk.Button(root, text="Launch LCE", command=launch_minecraft, width=40, height=3).pack(pady=20)

def open_url(url):
    webbrowser.open(url)

download_button = tk.Button(root, text="Download LCE", command=lambda: open_url("https://github.com/smartcmd/MinecraftConsoles/releases/download/nightly/LCEWindows64.zip"), width=40, height=3)
download_button.pack(side='left', padx=10, pady=20)

star_repo_button = tk.Button(root, text="Star the Repo", command=lambda: open_url("https://github.com/Bizzerowasnotavailable/ZeroLauncher"), width=40, height=3)
star_repo_button.pack(side='right', padx=10, pady=20)


load_settings() # loads settings....

root.mainloop()