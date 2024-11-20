import os
import shutil
import json
import tkinter as tk
import subprocess
from tkinter import messagebox

# Create the main window
wroot = tk.Tk()
wroot.title("Project Manager")
wroot.geometry("300x100")

def build_project():
    os.chdir("..")
    subprocess.run(['premake5', 'vs2022'])
    messagebox.showinfo("Done!", "You can now open the .sln file for building!")
    quit()

def clean_project():
        # Prompt the user to confirm the clean action
    confirm = messagebox.askyesno("Clean", 
    "Are you sure you want to clean the project?\ncleaning will remove ALL built project files!")
    if not confirm:
        return

    # File extension loading to delete
    f = open("clean_items.json", 'r')
    jf = json.load(f)
    extensions_to_delete = jf["VisualStudio"]["files"]
    dirs_to_delete = jf["VisualStudio"]["dirs"]
    f.close()

    # Directory to start cleaning from
    os.chdir("..")
    start_dir = os.getcwd()  # Change this if you want a specific directory

    files_deleted = 0
    for root, dirs, files in os.walk(start_dir):
        for file in files:
            if any(file.endswith(ext) for ext in extensions_to_delete):
                file_path = os.path.join(root, file)
                try:
                    os.remove(file_path)
                    files_deleted += 1
                    print(f"Deleted: {file_path}")
                except Exception as e:
                    print(f"Error deleting {file_path}: {e}")
        
                # Delete matching directories
        dirs_deleted = 0
        for dir_name in dirs:
            if dir_name in dirs_to_delete:
                dir_path = os.path.join(root, dir_name)
                try:
                    shutil.rmtree(dir_path)
                    dirs_deleted += 1
                    print(f"Deleted directory: {dir_path}")
                except Exception as e:
                    print(f"Error deleting directory {dir_path}: {e}")

    messagebox.showinfo("Clean", "Project is cleaned!")
    quit()

# Add buttons
build_button = tk.Button(wroot, text="Build Project Files", command=build_project, width=20)
build_button.pack(pady=10)

clean_button = tk.Button(wroot, text="Clean Project Files", command=clean_project, width=20)
clean_button.pack(pady=10)

def main():
    screen_width = wroot.winfo_screenwidth()
    screen_height = wroot.winfo_screenheight()
    x = (screen_width - 300) // 2
    y = (screen_height - 100) // 2
    wroot.geometry(f"{300}x{100}+{x}+{y}")
    
    wroot.mainloop()
    
if __name__ == "__main__":
    main()