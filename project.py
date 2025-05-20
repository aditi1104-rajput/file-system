import os
import time
import tkinter as tk
from tkinter import filedialog, ttk, messagebox

def analyze_directory(path):
    file_data = []
    total_files = 0
    total_size = 0

    for root, dirs, files in os.walk(path):
        for file in files:
            try:
                filepath = os.path.join(root, file)
                size = os.path.getsize(filepath)
                extension = os.path.splitext(file)[1] or "No Extension"
                last_modified = time.ctime(os.path.getmtime(filepath))

                file_data.append([filepath, size, extension, last_modified])
                total_files += 1
                total_size += size
            except Exception as e:
                print(f"Error reading {file}: {e}")
    return file_data, total_files, total_size

def browse_folder():
    folder = filedialog.askdirectory()
    if folder:
        results.delete(*results.get_children())
        data, total_files, total_size = analyze_directory(folder)

        for row in data:
            results.insert("", "end", values=row)
        
        summary_var.set(f"Total Files: {total_files} | Total Size: {total_size / (1024*1024):.2f} MB")

# GUI setup
root = tk.Tk()
root.title("File System Analyzer")
root.geometry("900x500")

frame = tk.Frame(root)
frame.pack(pady=10)

btn_browse = tk.Button(frame, text="Select Folder", command=browse_folder)
btn_browse.pack()

summary_var = tk.StringVar()
label_summary = tk.Label(root, textvariable=summary_var, font=("Arial", 10))
label_summary.pack(pady=5)

cols = ("File Path", "Size (Bytes)", "Extension", "Last Modified")
results = ttk.Treeview(root, columns=cols, show="headings")
for col in cols:
    results.heading(col, text=col)
    results.column(col, width=200 if col == "File Path" else 100)
results.pack(expand=True, fill="both")

scrollbar = ttk.Scrollbar(root, orient="vertical", command=results.yview)
results.configure(yscroll=scrollbar.set)
scrollbar.pack(side="right", fill="y")

root.mainloop()
