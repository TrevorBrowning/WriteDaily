from tkinter import Tk, Menu, Text, filedialog, ttk, messagebox, PhotoImage, Scrollbar
import tkinter.font as tkfont
from tkinter import *
from datetime import datetime
import webbrowser
import time
import json
import os
import sys


if getattr(sys, 'frozen', False):
    asset_dir = sys._MEIPASS
    user_dir = os.path.dirname(sys.executable)
else:
    asset_dir = os.path.dirname(os.path.abspath(__file__))
    user_dir = asset_dir



    # Create new entry (Ability to save)

def new_entry():
    confirm = messagebox.askyesno('Create New', 'Would you like to save before creating a new entry?')
    if confirm:
        save_entry()
        text_area.delete(1.0, 'end')
    
    if not confirm:
        text_area.delete(1.0, 'end')

   
    # Create a save (Saves go into Entries folder, both .txt/.json)

def save_entry():
    entry_text = text_area.get("1.0", "end").strip()
    date = time.strftime("%m-%d-%Y")
    time_stamp = time.strftime("%I:%M %p")

    entries_dir = os.path.join(user_dir, "Entries")
    os.makedirs(entries_dir, exist_ok=True)

    file_path = os.path.join(entries_dir, f"{date}.txt")
    
    with open(file_path, "a", encoding="utf-8") as file:
        file.write(f"\n\n--- {time_stamp} ---\n{entry_text}")

    json_path = os.path.join(user_dir, "journal_entries.json")
   
    # Load existing data or create new
    if os.path.exists(json_path):
        with open(json_path, "r", encoding="utf-8") as f:
            journal_data = json.load(f)
    else:
        journal_data = {}

    # Append entry
    journal_data.setdefault(date, []).append({
        "time": time_stamp,
        "content": entry_text
    })

    # Save updated data
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(journal_data, f, indent=4)


def load_entries():
    json_path = os.path.join(user_dir, "journal_entries.json")
    if os.path.exists(json_path):
        with open(json_path, "r", encoding="utf-8") as f:
            journal_data = json.load(f)

            date_strings = list(journal_data.keys())
            
            parsed_dates = []
            for date in date_strings:
                date_obj = datetime.strptime(date, "%m-%d-%Y")  
                parsed_dates.append(date_obj)  
            
            parsed_dates.sort(reverse=True)
            load_bar['values'] = [str(d.strftime("%m-%d-%Y")) for d in parsed_dates]


def load_selected_entry(event):
    selected_date = load_bar.get()
    json_path = os.path.join(user_dir, "journal_entries.json")

    if not os.path.exists(json_path):
        messagebox.showerror("Error", "No saved entries found.")
        return

    with open(json_path, "r", encoding="utf-8") as f:
        journal_data = json.load(f)

    entries = journal_data.get(selected_date, [])

    if not entries:
        messagebox.showinfo("No Entry", f"No entries found for {selected_date}.")
        return

    formatted = ""
    for entry in entries:
        time_stamp = entry.get("time", "Unknown Time")
        content = entry.get("content", "")
        formatted += f"--- {time_stamp} ---\n{content}\n\n"

    read_area.config(state='normal')
    read_area.delete("1.0", "end")
    read_area.insert("1.0", formatted)
    read_area.config(state='disabled')
    text_frame.select(read_tab)




    # Exit Program 

def exit_program():
    confirm = messagebox.askyesnocancel("Exit Write Daily", "Would you like to save before exiting?")
    if confirm == True:
        save_entry()
        root.destroy()
    
    elif confirm == False:
        root.destroy()



    # Tooltips for About

class ToolTip:
    def __init__(self, widget, text):
        self.widget = widget
        self.text = text
        self.tooltip = None

        widget.bind("<Enter>", self.show)
        widget.bind("<Leave>", self.hide)

    def show(self, event=None):
        if self.tooltip:
            return
        x = self.widget.winfo_rootx() + 25
        y = self.widget.winfo_rooty() + 20
        self.tooltip = Toplevel(self.widget)
        self.tooltip.wm_overrideredirect(True)
        self.tooltip.geometry(f"+{x}+{y}")
        label = Label(self.tooltip, text=self.text, background="lightyellow", relief="solid", borderwidth=1, font=("Segoe UI", 9))
        label.pack()

    def hide(self, event=None):
        if self.tooltip:
            self.tooltip.destroy()
            self.tooltip = None



    # About Page (Window/Theme)


def show_about():

    about = Toplevel(root)


    about.update_idletasks()  
    w = about.winfo_width()
    h = about.winfo_height()
    x = (about.winfo_screenwidth() // 2) - (w // 2)
    y = (about.winfo_screenheight() // 2) - (h // 2)
    about.geometry(f"+{x}+{y}")
    
    about.title("About")
    about.geometry("400x200")
    about.resizable(False, False)
  

   
    wrapper = Frame(about, bg="lightgrey", bd=2, relief="groove")
    wrapper.pack(fill='both', expand=True, padx=20, pady=20)
        


    Label(wrapper, text="WriteDaily v1.0", font=("Segoe UI", 14, "bold"), background='lightgrey').pack(pady=10)
    Label(wrapper, text="Created by Trevor Browning", font=("Segoe UI", 11), bg='lightgrey').pack()

  
    Frame(about, height=10).pack()

   
    icon_row = Frame(wrapper, background='lightgrey')
    icon_row.pack(pady=25, padx=25)

    Label(icon_row, image=icons["github"], cursor="hand2", bg='lightgrey').pack(side="left", padx=10)
    Label(icon_row, image=icons["twitter"], cursor="hand2", bg='lightgrey').pack(side="left", padx=10)
    Label(icon_row, image=icons["bluesky"], cursor="hand2", bg='lightgrey').pack(side="left", padx=10)

    
    icon_row.winfo_children()[0].bind("<Button-1>", lambda e: webbrowser.open_new("https://TrevorBrowning.github.io"))
    icon_row.winfo_children()[1].bind("<Button-1>", lambda e: webbrowser.open_new("https://twitter.com/BrowningRTrevor"))
    icon_row.winfo_children()[2].bind("<Button-1>", lambda e: webbrowser.open_new("https://bsky.app/profile/TrevorBrowning.bsky.social"))
    ToolTip(icon_row.winfo_children()[0], "Open GitHub")
    ToolTip(icon_row.winfo_children()[1], "Follow on Twitter")
    ToolTip(icon_row.winfo_children()[2], "Visit Bluesky Profile")


    # Font Options

def theme_options():
    available_fonts = ["Arial", "Courier New", "Times New Roman", "Verdana", "Georgia", "Trebuchet MS"]

    
    font_bar['values'] = sorted(available_fonts)

    
    # Font Size Options

def font_size_options():
    available_font_sizes = [8, 10, 12, 14, 16, 18, 20, 22, 24, 26, 28, 30]
    font_size_bar['values'] = sorted(available_font_sizes)


    # Font / Size Selector

def font_selector(event=None):
    selected_font = font_bar.get()
    selected_size = font_size_bar.get()

    if selected_font == "":
        selected_font = "Segoe UI"

    if selected_size == "":
        selected_size = 18
    else:
        selected_size = int(selected_size)

    text_area.config(font=(selected_font, selected_size))
    read_area.config(font=(selected_font, selected_size))

    
    # Hide toolbar while in focus mode

def hide_toolbar(event=None):
    if focus_mode.get():
        toolbar.pack_forget()
        root.attributes("-fullscreen", True)
        text_area.config(bg='#1e1e1e', fg='#dcdcdc', insertbackground='#dcdcdc')
        text_frame.configure(style="Hidden.TNotebook")
        read_area.config(bg='#1e1e1e', fg='#dcdcdc')

        

    # Show toolbar while focus mode disabled

def show_toolbar():
    root.attributes("-fullscreen", False)
    
    
    toolbar.pack_forget()
    text_frame.pack_forget()
    toolbar.pack(side='top', fill='x')
    text_frame.pack(fill='both', expand=True)

    
    text_area.config(bg='lightgrey', fg='black', insertbackground='black')
    read_area.config(bg='lightgrey', fg='black')


    exit_focus_btn.lower()
    text_frame.configure(style="TNotebook")


    # Disable Focus Mode

def disable_focus_mode():
    focus_mode.set(False)
    focus_toggle()


    # Focus Mode Toggle

def focus_toggle():
    if focus_mode.get():
        hide_toolbar()
        exit_focus_btn.lift()
    else:
        show_toolbar()


    # Root Window Config

root = Tk()
root.title("WriteDaily")
root.geometry("1200x800")
root.minsize(1200, 800)
root.after(0, theme_options)
root.after(0, font_size_options)
root.bind("<Escape>", lambda event: disable_focus_mode())

if getattr(sys, 'frozen', False):
    icon_path = os.path.join(sys._MEIPASS, "WriteDaily.ico")
else:
    icon_path = os.path.join(os.path.dirname(__file__), "WriteDaily.ico")

root.iconbitmap(icon_path)






base_dir = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(sys.executable if getattr(sys, 'frozen', False) else __file__)))

icons = {
    "github": PhotoImage(file=os.path.join(base_dir, "Assets", "Icons", "Github.png")),
    "twitter": PhotoImage(file=os.path.join(base_dir, "Assets", "Icons", "Twitter.png")),
    "bluesky": PhotoImage(file=os.path.join(base_dir, "Assets", "Icons", "Bluesky.png")),
}



root.columnconfigure(0, weight=1)
root.rowconfigure(0, weight=1)

focus_mode = BooleanVar()

    
    # Root Window Default Styles

style = ttk.Style()
style.configure('TButton', font=('Segoe UI', 12))  
style.configure('TNotebook.Tab', font=('Segoe UI', 12))
style.configure('TNotebook.Tab', padding=[10, 5])
style.configure("Toolbar.TCheckbutton", font=("Segoe UI", 12))
style.layout("Hidden.TNotebook.Tab", []) 


 # Exit Focus Button

exit_focus_btn = Button(root, text="✕", font=("Segoe UI", 10), command=disable_focus_mode, bd=0, relief="flat", bg="#1e1e1e", fg="#dcdcdc", activebackground="#2a2a2a", activeforeground="#ffffff")
exit_focus_btn.place(x=10, y=10)
exit_focus_btn.lower()
exit_focus_btn.place(x=5, y=5) 
exit_focus_btn.lower()  




    # Toolbar Frame

toolbar = ttk.Frame(root)
toolbar.pack(side='top', fill='x')
toolbar_frame = ttk.Frame(toolbar)
toolbar_frame.pack(side='left')

    # Buttons (New/Save)

ttk.Button(toolbar_frame, text='New', command=new_entry).pack(side='left', padx=6, pady=6)
ttk.Button(toolbar_frame, text='Save', command=save_entry).pack(side='left', padx=6, pady=6)
ttk.Separator(toolbar_frame, orient='vertical').pack(side='left', fill='y', padx=5)

    # Focus Mode Checkbox

ttk.Checkbutton(toolbar_frame, text="Focus Mode", style='Toolbar.TCheckbutton', variable=focus_mode, command=focus_toggle).pack(side='left', padx=6)


    # Load Entries Combobox

load_bar = ttk.Combobox(toolbar_frame, text='Search', font=('Segoe UI', 12), state='readonly')
load_bar.pack(side='left', padx=(6, 0), pady=6)
load_bar.set("View Previous Entry")
load_entries()
load_bar.bind("<<ComboboxSelected>>", load_selected_entry)



# Theme Options (Font / Size )

ttk.Separator(toolbar_frame, orient='vertical').pack(side='left', fill='y', padx=5)

ttk.Label(toolbar_frame, text='Theme:', font=('Segue UI', 12)).pack(side='left', pady=6)

font_bar = ttk.Combobox(toolbar_frame, text='Font', font=('Segoe UI', 12), width=10, state='readonly')
font_bar.pack(side='left', padx=(6, 0), pady=6)
font_bar.bind("<<ComboboxSelected>>", font_selector)
font_bar.set("Segoe UI")

font_size_bar = ttk.Combobox(toolbar_frame, text='size', font=('Segoe UI', 12), width=4, state='readonly')
font_size_bar.pack(side='left', padx=(6, 0), pady=6)
font_size_bar.bind("<<ComboboxSelected>>", font_selector)
font_size_bar.set("18")


ttk.Separator(toolbar_frame, orient='vertical').pack(side='left', fill='y', padx=5)


    # Buttons (About / Exit Program)

ttk.Button(toolbar_frame, text='About', command=show_about).pack(side='left', padx=6, pady=6)
ttk.Button(toolbar_frame, text='Exit', command=exit_program).pack(side='left', padx=6, pady=6)



    # Text/Read Area

text_frame = ttk.Notebook(root)
text_frame.pack(fill='both', expand=True)


write_tab = ttk.Frame(text_frame)
text_frame.add(write_tab, text='Write')

write_container = Frame(write_tab)
write_container.pack(fill='both', expand=True)

write_scrollbar = Scrollbar(write_container)
write_scrollbar.pack(side='right', fill='y')

text_area = Text(write_container, font=('Courier New', 18), bg='lightgrey', yscrollcommand=write_scrollbar.set, wrap='word')
text_area.pack(side='left', fill='both', expand=True)
text_area.config(padx=15, pady=10)

write_scrollbar.config(command=text_area.yview)


# Auto-hide scrollbar logic

def toggle_write_scrollbar(*args):
    write_scrollbar.set(*args)
    if text_area.yview() == (0.0, 1.0):
        write_scrollbar.pack_forget()
    else:
        write_scrollbar.pack(side='right', fill='y')

text_area.config(yscrollcommand=toggle_write_scrollbar)


read_tab = ttk.Frame(text_frame)
text_frame.add(read_tab, text='Read')

read_container = Frame(read_tab)
read_container.pack(fill='both', expand=True)

read_scrollbar = Scrollbar(read_container)
read_scrollbar.pack(side='right', fill='y')

read_area = Text(read_container, font=('Courier New', 18), bg='lightgrey', state=DISABLED, wrap='word')
read_area.pack(side='left', fill='both', expand=True)
read_area.config(padx=15, pady=10, yscrollcommand=read_scrollbar.set)

read_scrollbar.config(command=read_area.yview)

def toggle_read_scrollbar(*args):
    read_scrollbar.set(*args)
    if read_area.yview() == (0.0, 1.0):
        read_scrollbar.pack_forget()
    else:
        read_scrollbar.pack(side='right', fill='y')

read_area.config(yscrollcommand=toggle_read_scrollbar)


def bind_mousewheel(widget, target):
    def _on_mousewheel(event):
        target.yview_scroll(int(-1 * (event.delta / 120)), "units")
        return "break"
    widget.bind_all("<MouseWheel>", _on_mousewheel)

bind_mousewheel(text_area, text_area)
bind_mousewheel(read_area, read_area)






root.mainloop()
