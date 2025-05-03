import datetime

from functools import partial

from .frames import *

GREEN_COLOR = "#1a8f3f"
DARK_GREEN_COLOR = "#0d6e2c"
HOVER_GREEN = "#0f993b"
WHITE_COLOR = "#dcdedc"
PALE_COLOR = "#ffffff"
PALE_GREEN_COLOR = "#b0ffb3"

def with_cooldown(button, func, cooldown_ms=1000):
    def wrapper():
        button.configure(state="disabled")
        func()
        button.after(cooldown_ms, lambda: button.configure(state="normal"))
    return wrapper

def button_manager(app, btn_name):
    for button in app.sidebar_frame.winfo_children():
        text = button.cget("text")
        button.configure(hover_color=WHITE_COLOR, fg_color=WHITE_COLOR,text_color = DARK_GREEN_COLOR) if btn_name == text else button.configure(hover_color=HOVER_GREEN, fg_color=DARK_GREEN_COLOR,text_color = WHITE_COLOR)

    for widget in app.main_frame.winfo_children():
        widget.destroy()

def open_frame(app, frame_class, display_name):
    button_manager(app, display_name)
    tool_frame = frame_class(app)

def time_of_day():
    if 5 <= datetime.now().hour < 12:
        return "morning"
    elif 12 <= datetime.now().hour < 18:
        return "afternoon"
    else:
        return "evening"


sb_btn_list = [
    ["Projects", 0.1, lambda app: open_frame(app, ProjectFrame, "Projects")],
    ["Orders", 0.3, lambda app: open_frame(app, OrderFrame, "Orders")],
    ["Employees", 0.5, lambda app: open_frame(app, EmployeeFrame, "Employees")],
    ["Storage", 0.7, lambda app: open_frame(app, StorageFrame, "Storage")],
    ["Activity Log", 0.9, lambda app: open_frame(app, ActivityLogFrame, "Activity Log")],
]


def create_sidebar_btn(root, text, y_pos, cmd, app):

    button = ctk.CTkButton(root, text=text, hover_color=HOVER_GREEN, fg_color=DARK_GREEN_COLOR,
                                corner_radius=10, text_color = WHITE_COLOR,
                                font=("Arial", 36), border_spacing=10,width=200, command=None
                                )
    button.place(relx=0.5, rely=y_pos, anchor="center")
    button.configure(command=with_cooldown(button, partial(cmd, app), cooldown_ms=400))

class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        ctk.deactivate_automatic_dpi_awareness()
        set_appearance_mode("light")
        self.title("Business Manager 2000")
        self.geometry("1400x700")
        self.resizable(False, False)
        self.main_frame = CTkFrame(master=self, width=1100, height=680, fg_color=WHITE_COLOR)
        self.sidebar_frame = CTkFrame(master=self, width=250, height=680, fg_color=GREEN_COLOR)
        self.create_launch_frames()

    def create_launch_frames(self):
        self.main_frame = CTkFrame(master=self, width=1100, height=680, fg_color=WHITE_COLOR)
        self.main_frame.place(relx=0.6, rely=0.5, anchor="center")

        welcome_note = ctk.CTkLabel(master=self.main_frame, text=f"Good {time_of_day()}!", text_color=GREEN_COLOR,font=("Arial", 60))
        welcome_note.place(relx=0.5, rely=0.45, anchor="center")

        self.sidebar_frame.place(relx=0.1, rely=0.5, anchor="center")

        for i in sb_btn_list:
            create_sidebar_btn(self.sidebar_frame, i[0], i[1], i[2], self)

