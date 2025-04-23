import customtkinter
import tkinter.messagebox as messagebox  # Add this import at the top
from backend import *
import threading
import subprocess
import os
import traceback
import json

customtkinter.set_appearance_mode("System")
customtkinter.set_default_color_theme("green")
CORNER_RADIUS = 10
SIDEBAR_WIDTH = 150
WINDOW_WIDTH = 850
WINDOW_HEIGHT = 480
SRW_WIDTH = 300
SRW_HEIGHT = 300

SW_WIDTH = 300
SW_HEIGHT = 340

SETTINGS_FILE = "settings.json"

# === Sidebar Class ===
class SidebarContent(customtkinter.CTkFrame):
    def __init__(self, master, sidebar_width=100, start_callback=None, checkbox_callback=None, settings_callback=None, **kwargs):
        super().__init__(master, width=sidebar_width, corner_radius=CORNER_RADIUS, **kwargs)

        self.start_callback = start_callback
        self.checkbox_callback = checkbox_callback
        self.settings_callback = settings_callback
        
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=2)

        # === Top Sidebar ===
        self.sidebar_frame_top = customtkinter.CTkFrame(self, corner_radius=CORNER_RADIUS)
        self.sidebar_frame_top.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

        self.sidebar_frame_top.grid_rowconfigure(0, weight=1)
        self.sidebar_frame_top.grid_rowconfigure(1, weight=1)
        self.sidebar_frame_top.grid_columnconfigure(0, weight=1)

        self.title_frame = customtkinter.CTkFrame(self.sidebar_frame_top, corner_radius=CORNER_RADIUS)
        self.title_frame.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")
        self.title_frame.grid_columnconfigure(0, weight=1)
        self.title_frame.grid_rowconfigure(0, weight=1)

        self.logo_label = customtkinter.CTkLabel(
            self.title_frame, text="Linkedin Bot", font=customtkinter.CTkFont(size=20, weight="bold")
        )
        self.logo_label.grid(row=0, column=0, padx=10, pady=10, sticky="ew")

        self.slider_frame = customtkinter.CTkFrame(self.sidebar_frame_top, corner_radius=CORNER_RADIUS)
        self.slider_frame.grid(row=1, column=0, padx=10, pady=10, sticky="ew")

        self.delay_slider_label = customtkinter.CTkLabel(self.slider_frame, text="delay", font=customtkinter.CTkFont(weight="bold"))
        self.delay_slider_label.grid(row=0, column=0, padx=(10, 5), pady=10, sticky="w")

        self.delay_slider = customtkinter.CTkSlider(
            self.slider_frame, from_=1, to=9, number_of_steps=8, width=150, command=self.update_slider_value
        )
        self.delay_slider.set(3)
        self.delay_slider.grid(row=1, column=0, padx=5, pady=0, sticky="ew")

        self.delay_value_label = customtkinter.CTkLabel(self.slider_frame, text="3")
        self.delay_value_label.grid(row=1, column=1, padx=5, pady=0, sticky="ew")

        self.buttons_frame_bottom = customtkinter.CTkFrame(self.sidebar_frame_top, corner_radius=CORNER_RADIUS)
        self.buttons_frame_bottom.grid(row=2, column=0, padx=10, pady=10, sticky="nsew")
        self.buttons_frame_bottom.grid_columnconfigure(0, weight=1)

        self.start_button = customtkinter.CTkButton(self.buttons_frame_bottom, text="start", command=self.start_script)
        self.start_button.grid(row=0, column=0, padx=10, pady=10, sticky="ew")

        self.excel_button = customtkinter.CTkButton(self.buttons_frame_bottom, text="excel file", command=self.open_excel_file)
        self.excel_button.grid(row=1, column=0, padx=10, pady=10, sticky="ew")

        self.settings_button = customtkinter.CTkButton(self.buttons_frame_bottom, text="settings", command=self.open_settings)
        self.settings_button.grid(row=2, column=0, padx=10, pady=10, sticky="ew")
        
        self.check_boxes_frame = customtkinter.CTkFrame(self.sidebar_frame_top, corner_radius=CORNER_RADIUS)
        self.check_boxes_frame.grid(row=3, column=0, padx=10, pady=10, sticky="nsew")
        self.check_boxes_frame.grid_columnconfigure(0, weight=1)

        self.company_check_var = customtkinter.StringVar(value="off")
        self.company_checkbox = customtkinter.CTkCheckBox(
            self.check_boxes_frame,
            text='Companies Entered',
            command=lambda: self.checkbox_callback("company", self.company_check_var.get()),
            variable=self.company_check_var,
            onvalue="on",
            offvalue="off"
        )
        self.company_checkbox.grid(row=0,column=0,padx=10,pady=(10,5),sticky="ew")
        
        self.jobtitle_check_var = customtkinter.StringVar(value="off")
        self.jobtitle_checkbox = customtkinter.CTkCheckBox(
            self.check_boxes_frame,
            text='Job Titles Entered',
            command=lambda: self.checkbox_callback("jobtitle", self.jobtitle_check_var.get()),
            variable=self.jobtitle_check_var,
            onvalue="on",
            offvalue="off"
        )
        self.jobtitle_checkbox.grid(row=1,column=0,padx=10,pady=(5,10),sticky="ew")

    def update_slider_value(self, value):
        self.delay_value_label.configure(text=str(round(value)))

    def start_script(self):
        print("Script Started!")
        if self.start_callback:
            self.start_callback()

    def disable_start_button(self):
        self.start_button.configure(state="disabled")

    def enable_start_button(self):
        self.start_button.configure(state="normal")

    def open_settings(self):
        print("Opening Settings!")
        if self.settings_callback:
            self.settings_callback()
    
    def control_settings_button(self, status):
        if status:
            self.settings_button.configure(state="normal")
        else:
            self.settings_button.configure(state="disabled")
    

    def open_excel_file(self):
        excel_path = self.master.xlsx_path
        if excel_path:
            try:
                # Check if the Excel file exists
                if not os.path.isfile(excel_path):
                    messagebox.showerror("File Not Found", f"Excel file:\n{excel_path} doesn't exist.")
                    return

                # Try opening the Excel file
                try:
                    subprocess.Popen(['start', '', excel_path], shell=True)
                except Exception as e:
                    messagebox.showerror("Failed to Open Excel", f"Failed to open Excel file:\n{excel_path}\n\nError:\n{str(e)}")
            
            except Exception as e:
                tb = traceback.format_exc()
                messagebox.showerror("Unexpected Error", f"An unexpected error occurred:\n{str(e)}\n\nTraceback:\n{tb}")



# === Main Content Class ===
class MainContent(customtkinter.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, corner_radius=CORNER_RADIUS, **kwargs)

        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=2)

        self.textbox_placeholders = {}
        
        # === Company Section ===
        self.company_frame = customtkinter.CTkFrame(self, corner_radius=CORNER_RADIUS)
        self.company_frame.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")
        self.company_frame.grid_columnconfigure(0, weight=1)
        self.company_frame.grid_rowconfigure(1, weight=3)
        self.company_frame.grid_rowconfigure(2, weight=1)

        self.company_label_frame = customtkinter.CTkFrame(self.company_frame, corner_radius=CORNER_RADIUS)
        self.company_label_frame.grid(row=0, column=0, padx=10, pady=(10,10), sticky="nsew")
        self.company_label_frame.grid_columnconfigure(0, weight=1)

        self.company_label = customtkinter.CTkLabel(self.company_label_frame, text="Company", font=customtkinter.CTkFont(size=20, weight="bold"))
        self.company_label.grid(row=0, column=0, padx=20, pady=10, sticky="ew")

        self.company_entry_frame = customtkinter.CTkFrame(self.company_frame, corner_radius=CORNER_RADIUS)
        self.company_entry_frame.grid(row=1, column=0, padx=10, pady=10, rowspan=2, sticky='nsew')
        self.company_entry_frame.grid_columnconfigure(0, weight=1)
        self.company_entry_frame.grid_rowconfigure(0, weight=1)

        self.company_textbox = customtkinter.CTkTextbox(self.company_entry_frame, corner_radius=CORNER_RADIUS)
        self.company_textbox.grid(row=0,column=0,padx=10,pady=10,sticky='nsew')

        # === Job Title Section ===
        self.jobtitle_frame = customtkinter.CTkFrame(self, corner_radius=CORNER_RADIUS)
        self.jobtitle_frame.grid(row=0,column=1,padx=10,pady=10,sticky='nsew')
        self.jobtitle_frame.grid_columnconfigure(0, weight=1)
        self.jobtitle_frame.grid_rowconfigure(1, weight=3)
        self.jobtitle_frame.grid_rowconfigure(2, weight=1)

        self.jobtitle_label_frame = customtkinter.CTkFrame(self.jobtitle_frame, corner_radius=CORNER_RADIUS)
        self.jobtitle_label_frame.grid(row=0, column=0, padx=10, pady=(10,10), sticky="nsew")
        self.jobtitle_label_frame.grid_columnconfigure(0, weight=1)

        self.jobtitle_label = customtkinter.CTkLabel(self.jobtitle_label_frame, text="Job Titles", font=customtkinter.CTkFont(size=20, weight="bold"))
        self.jobtitle_label.grid(row=0, column=0, padx=20, pady=10, sticky="ew")

        self.jobtitle_entry_frame = customtkinter.CTkFrame(self.jobtitle_frame, corner_radius=CORNER_RADIUS)
        self.jobtitle_entry_frame.grid(row=1, column=0, padx=10, pady=10, rowspan=2, sticky='nsew')
        self.jobtitle_entry_frame.grid_columnconfigure(0, weight=1)
        self.jobtitle_entry_frame.grid_rowconfigure(0,weight=1)

        self.jobtitle_textbox = customtkinter.CTkTextbox(self.jobtitle_entry_frame, corner_radius=CORNER_RADIUS)
        self.jobtitle_textbox.grid(row=0,column=0,padx=10,pady=10,sticky='nsew')
       

class SettingsWindow(customtkinter.CTkToplevel):
    def __init__(self, master, *args, **kwargs):
        super().__init__(master,*args,**kwargs)
        self.geometry(f"{SW_WIDTH}x{SW_HEIGHT}")
        self.resizable(False,False)
        self.title("Settings")

        self.transient(master)
        self.grab_set()
        self.focus()

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0,weight=1)

        self.main_frame = customtkinter.CTkFrame(self, corner_radius=CORNER_RADIUS)
        self.main_frame.grid(row=0,column=0,padx=10,pady=10,sticky='nsew')
        self.main_frame.grid_columnconfigure(0, weight=1)
        self.main_frame.grid_rowconfigure(1, weight=1)

        self.settings_title = customtkinter.CTkLabel(self.main_frame, text="SETTINGS", font=customtkinter.CTkFont(size=20, weight="bold"))
        self.settings_title.grid(row=0,column=0,padx=10,pady=(10,0),sticky='ew')
        
        self.buttons_frame = customtkinter.CTkFrame(self.main_frame, corner_radius=CORNER_RADIUS)
        self.buttons_frame.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")
        self.buttons_frame.grid_columnconfigure(0, weight=1)

        self.username_entry = customtkinter.CTkEntry(self.buttons_frame, placeholder_text="username")
        self.username_entry.grid(row=0, column=0, padx=10, pady=(20, 10), sticky="ew")
        if self.master.username:
            self.username_entry.insert(0, self.master.username)

        self.password_entry = customtkinter.CTkEntry(self.buttons_frame, placeholder_text="password", show='*')
        self.password_entry.grid(row=1, column=0, padx=10, pady=(10, 10), sticky="ew")
        if self.master.password:
            self.password_entry.insert(0, self.master.password)


        self.driver_path_entry = customtkinter.CTkEntry(self.buttons_frame, placeholder_text="driver path")
        self.driver_path_entry.grid(row=2, column=0, padx=10, pady=(10, 10), sticky="ew")
        if self.master.driver_path:
            self.driver_path_entry.insert(0, self.master.driver_path)

        self.csv_path_entry = customtkinter.CTkEntry(self.buttons_frame, placeholder_text="csv path")
        self.csv_path_entry.grid(row=3, column=0, padx=10, pady=(10, 10), sticky="ew")
        if self.master.csv_path:
            self.csv_path_entry.insert(0, self.master.csv_path)


        self.xlsx_path_entry = customtkinter.CTkEntry(self.buttons_frame, placeholder_text="xlsx path")
        self.xlsx_path_entry.grid(row=4, column=0, padx=10, pady=(10, 20), sticky="ew")
        if self.master.xlsx_path:
            self.xlsx_path_entry.insert(0, self.master.xlsx_path)



class ScriptRunningWindow(customtkinter.CTkToplevel):
    def __init__(self, master, stop_event, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        self.geometry(f"{SRW_WIDTH}x{SRW_HEIGHT}")
        self.resizable(False, False)  # fixed typo
        self.title("Running Script")

        self.transient(master)
        self.grab_set()  # Optional: lock input to this window
        self.focus()  # Bring to front

        self.stop_event = stop_event

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.main_frame = customtkinter.CTkFrame(self, corner_radius=CORNER_RADIUS)
        self.main_frame.grid(row=0,column=0,padx=10,pady=10,sticky="nsew")
        self.main_frame.grid_columnconfigure(0, weight=1)

        self.stop_button = customtkinter.CTkButton(self.main_frame,text='stop',command=self.stop_script)
        self.stop_button.grid(row=0, column=0, padx=10, pady=10, sticky='ew')

        self.confirm_login = customtkinter.CTkCheckBox(self.main_frame, text='confirm login')
        self.confirm_login.grid(row=1, column=0, padx=10, pady=5, sticky='ew')

        self.companies_frame = customtkinter.CTkFrame(self.main_frame, corner_radius=CORNER_RADIUS)
        self.companies_frame.grid(row=2, column=0, padx=10, pady=5, sticky='nsew')
        self.companies_label = customtkinter.CTkLabel(self.companies_frame, text="Companies: ")
        self.companies_label.grid(row=0, column=0, padx=(5,0), pady=5, sticky="ew")
        self.companies_number = customtkinter.CTkLabel(self.companies_frame, text='0')
        self.companies_number.grid(row=0, column=1, padx=(0,5), pady=5, sticky="ew")

        self.job_title_frame = customtkinter.CTkFrame(self.main_frame, corner_radius=CORNER_RADIUS)
        self.job_title_frame.grid(row=3, column=0, padx=10, pady=5, sticky='nsew')
        self.job_title_label = customtkinter.CTkLabel(self.job_title_frame, text="Job Titles: ")
        self.job_title_label.grid(row=0, column=0, padx=(5,0), pady=5, sticky="ew")
        self.job_title_number = customtkinter.CTkLabel(self.job_title_frame, text='0')
        self.job_title_number.grid(row=0, column=1, padx=(0,5), pady=5, sticky="ew")

        self.current_search_text = customtkinter.CTkFrame(self.main_frame, corner_radius=CORNER_RADIUS)
        self.current_search_text.grid(row=4, column=0, padx=10, pady=5, sticky='nsew')
        self.companies_label = customtkinter.CTkLabel(self.current_search_text, text="Current Search Value")
        self.companies_label.grid(row=0, column=0, padx=(5,0), pady=5, sticky="ew")

        self.progress_status = customtkinter.CTkLabel(self.main_frame, text=f"Progress: {0}%")
        self.progress_status.grid(row=5, column=0, padx=10, pady=5, sticky="nsew")
        self.progressbar = customtkinter.CTkProgressBar(self.main_frame, orientation="horizontal")
        self.progressbar.set(0)
        self.progressbar.grid(row=6, column=0, padx=10, pady=5, sticky="nsew")

    def stop_script(self):
        print("Stop button clicked!")
        self.stop_event.set()

    def update_status(self, message: str):
        self.title(message)
    
    def update_companies(self, count: int):
        self.companies_number.configure(text=str(count))
    
    def update_titles(self, count: int):
        self.job_title_number.configure(text=str(count))

    def update_search(self, search_value: str):
        self.companies_label.configure(text=search_value)
    
    def update_progress(self, progress: float):
        self.progressbar.set(progress)
        self.progress_status.configure(text=f"Progress: {round(int(progress*100))}%")
        
# === App Class ===
class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        self.title("Linkedin Helper")
        self.geometry(f"{WINDOW_WIDTH}x{WINDOW_HEIGHT}")
        self.resizable(False, False)

        self.script_window = None

        # Layout
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=0)
        self.grid_columnconfigure(1, weight=1)

        self.sidebar = SidebarContent(self, sidebar_width=SIDEBAR_WIDTH, start_callback=self.open_script_window, checkbox_callback=self.checkbox_event, settings_callback=self.open_settings_window)
        self.sidebar.grid(row=0, column=0, padx=5, pady=10, sticky="ns")

        self.main_content = MainContent(self)
        self.main_content.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")

        self.settings = self.load_settings()
        print(self.settings)
        self.username = self.settings.get("username", "")
        self.password = self.settings.get("password", "")
        self.driver_path = self.settings.get("driver_path", "")
        self.csv_path = self.settings.get("csv_path", "")
        self.xlsx_path = self.settings.get("xlsx_path", "")

    def save_settings(self):
        if self.settings:
            with open(SETTINGS_FILE, "w") as file:
                json.dump(self.settings, file)
            print("Settings saved.")
        else:
            print("Settings undefined. Failed to save.")

    def load_settings(self):
        try:
            with open(SETTINGS_FILE, "r") as file:
                return json.load(file)
        except FileNotFoundError:
            print("Settings File Not Found.")
            return {}

    def checkbox_event(self, source, value):
        print(f"{source.capitalize()} checkbox is now: {value}")

    def open_settings_window(self):
        self.settings_window = SettingsWindow(self)
        self.sidebar.control_settings_button(False)
        
        def on_close():
            self.username = self.settings_window.username_entry.get().strip()
            self.password = self.settings_window.password_entry.get().strip()
            self.driver_path = self.settings_window.driver_path_entry.get().strip()
            self.csv_path = self.settings_window.csv_path_entry.get().strip()
            self.xlsx_path = self.settings_window.xlsx_path_entry.get().strip()

            self.settings = {
                "username": self.username,
                "password": self.password,
                "driver_path": self.driver_path,
                "csv_path": self.csv_path,
                "xlsx_path": self.xlsx_path
            }
            self.save_settings()

            self.settings_window.destroy()
            self.settings_window = None
            self.sidebar.control_settings_button(True)
            print(f"\tUsername: {self.username}\n\tPassword: {len(self.password)}\n\tDriver Path: {self.driver_path}\n\tCSV Path: {self.csv_path}\n\tXLSX Path: {self.xlsx_path}")

        self.settings_window.protocol("WM_DELETE_WINDOW", on_close)
        self.settings_window.focus()

    def open_script_window(self):
        if self.script_window is not None:
            print("Window already open!")
            return
        
        company_done = self.sidebar.company_check_var.get()
        jobtitle_done = self.sidebar.jobtitle_check_var.get()

        if company_done != "on" or jobtitle_done != "on":
            messagebox.showerror("Incomplete Fields", "Please confirm both checkboxes under Company and Job Titles before starting.")
            return

        # === Get input values ===
        delay = round(self.sidebar.delay_slider.get())
        # companies = self.main_content.company_textbox.get("0.0", "end").strip().splitlines()
        # titles = self.main_content.jobtitle_textbox.get("0.0", "end").strip().splitlines()
        companies = [line.strip() for line in self.main_content.company_textbox.get("0.0", "end").splitlines() if line.strip()]
        titles = [line.strip() for line in self.main_content.jobtitle_textbox.get("0.0", "end").splitlines() if line.strip()]


        # === Validate ===
        if not self.username or not self.password:
            messagebox.showerror("Missing Credentials", "Username and password cannot be empty.")
            return

        if not self.driver_path:
            messagebox.showerror("Missing Driver Path", "Input the path for the driver")
            return 
        
        if not self.csv_path:
            messagebox.showerror("Missing CSV Path", "Input CSV Path.")
            return

           
        if not self.xlsx_path:
            messagebox.showerror("Missing XLSX Path", "Input XLSX Path.")
            return


        if not companies:
            messagebox.showerror("Missing Input", "Please enter at least one company.")
            return

        if not titles:
            messagebox.showerror("Missing Input", "Please enter at least one job title.")
            return

        # === All inputs are valid; proceed ===
        print("Launching Script with:")
        print(f"  Username: {self.username}")
        print(f"  Password: {self.password}")
        print(f"  Delay: {delay}")
        print(f"  Companies: {companies}")
        print(f"  Job Titles: {titles}")
        print(f"  Driver Path: {self.driver_path}")
        print(f"  CSV Path: {self.csv_path}")
        print(f"  XLSX Path: {self.xlsx_path}")

        self.stop_event = threading.Event()
        
        # Launch script window
        self.script_window = ScriptRunningWindow(self, stop_event=self.stop_event)
        self.sidebar.disable_start_button()

        self.script_window.update_companies(len(companies))
        self.script_window.update_titles(len(titles))

        threading.Thread(
            target=main_script,
            args=(self.username, self.password, delay, companies, titles, self.driver_path, self.csv_path, self.xlsx_path, self.script_window, self.stop_event), #self.status_queue),
            daemon = True
        ).start()

        def on_close():
            self.stop_event.set()
            self.script_window.destroy()
            self.script_window = None
            self.sidebar.enable_start_button()
            print("Script window closed")

        self.script_window.protocol("WM_DELETE_WINDOW", on_close)
        self.script_window.focus()



if __name__ == "__main__":
    app = App()
    app.mainloop()
