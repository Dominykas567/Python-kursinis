from datetime import datetime

import customtkinter as ctk
from customtkinter import *

import csv, os, subprocess

from modules.classes.logger import Logger

from modules.classes.employee import Employee
from modules.managers.employee_manager import EmployeeManager
from modules.classes.order import Order
from modules.managers.order_manager import OrderManager
from modules.managers.project_manager import ProjectManager
from modules.classes.component import Component
from modules.managers.storage_manager import StorageManager

GREEN_COLOR = "#1a8f3f"
DARK_GREEN_COLOR = "#0d6e2c"
HOVER_GREEN = "#0f993b"
WHITE_COLOR = "#dcdedc"
PALE_COLOR = "#ffffff"
PALE_GREEN_COLOR = "#b0ffb3"
OBJECT_GREEN = "#cef0d1"
X_RED_COLOR="#db5a46"

class DataFrame:
    def __init__(self, app, frame_name):

        self.search_bar = None
        self.search_var = None
        self.button1 = None
        self.button2 = None
        self.option_menu = None

        if frame_name != "Activity Log":
            self.tool_frame = CTkFrame(master=app.main_frame, width=1000, height=100, fg_color=WHITE_COLOR,border_color=GREEN_COLOR,border_width=5)
            self.tool_frame.place(relx=0.5, rely=0.1, anchor="center")
            self.create_search_bar(frame_name)
            if frame_name != "Employees":
                self.create_option_menu(frame_name)
                self.create_buttons(frame_name)
            else: self.create_buttons(frame_name)

            self.data_frame = CTkScrollableFrame(master=app.main_frame, width=975, height=500, fg_color=WHITE_COLOR,border_color=GREEN_COLOR, border_width=5, scrollbar_fg_color="transparent",scrollbar_button_color=HOVER_GREEN, scrollbar_button_hover_color=DARK_GREEN_COLOR)
            self.data_frame.place(relx=0.5, rely=0.975, anchor="s")

            if frame_name == "Projects": self.project_frame_obj()
            elif frame_name == "Orders": self.order_frame_obj()
            elif frame_name == "Employees": self.employees_frame_obj()
            elif frame_name == "Storage": self.storage_frame_obj()


        else: Logger.open_file()

    def open_add_project_window(self):
        window = ctk.CTkToplevel()
        window.title("Add a New Project")
        window.geometry("400x200")
        window.grab_set()  # Makes it modal
        window.attributes("-topmost", True)
        window.after(100, lambda: window.attributes("-topmost", False))

        entry_label = ctk.CTkLabel(window, text="Enter Project Name:", font=("Arial", 18))
        entry_label.pack(pady=(20, 5))

        project_name_var = ctk.StringVar()
        entry = ctk.CTkEntry(window, textvariable=project_name_var, font=("Arial", 18), width=250)
        entry.pack(pady=5)

        self.tool_frame.update_idletasks()
        main_x = self.tool_frame.winfo_rootx()
        main_y = self.tool_frame.winfo_rooty()
        main_width = self.tool_frame.winfo_width()
        main_height = self.tool_frame.winfo_height()

        win_width = 400
        win_height = 200
        pos_x = main_x + (main_width // 2) - (win_width // 2)
        pos_y = main_y + (main_height // 2) - (win_height // 2)
        window.geometry(f"{win_width}x{win_height}+{pos_x}+{pos_y}")

        def submit():
            project_name = project_name_var.get().strip()
            if project_name:
                ProjectManager.create_project(None,project_name,self.option_menu.get()=="Outdated")
                window.destroy()
                self.project_frame_obj()

        submit_button = ctk.CTkButton(window, text="Create Project", font=("Arial", 18), command=submit)
        submit_button.pack(pady=(20, 10))

    def project_frame_obj(self):


        for widget in self.data_frame.winfo_children():
            widget.destroy()

        original_directory = os.getcwd()

        folder = "outdated_projects" if self.option_menu.get()=="Outdated" else "active_projects"
        dir = os.path.join("data", folder)

        search_query = self.search_var.get().lower() if hasattr(self, "search_var") else ""

        for entry in os.listdir(dir):
            if not entry.lower().startswith(search_query):
                continue

            full_path = os.path.join(dir, entry)
            if os.path.isdir(full_path):

                project_dir = os.path.join("data", folder,entry,"project.csv")
                with open(project_dir, mode='r', newline='') as f:
                    reader = csv.reader(f)
                    project_data = list(reader)[1]

                components_dir = os.path.join("data", folder, entry, "required_components.csv")
                with open(components_dir, mode='r', newline='') as f:
                    reader = csv.reader(f)
                    components_data = list(reader)[1:]


                frame = ctk.CTkFrame(self.data_frame, height=80,corner_radius=10, fg_color=OBJECT_GREEN)
                frame.pack(fill="x", pady=5, padx=10)
                frame.pack_propagate(False)

                label = ctk.CTkLabel(frame, text=f"Project: {project_data[0]}", font=("Arial", 18),text_color=GREEN_COLOR)
                label.pack(padx=50, pady=10, side="left")

                option_menu = ctk.CTkOptionMenu(master=frame, width=110, height=35, corner_radius=6, font=("Arial", 18),
                                  text_color=GREEN_COLOR, dropdown_font=("Arial", 18), dropdown_text_color=GREEN_COLOR,
                                  fg_color=PALE_COLOR, dropdown_fg_color=PALE_COLOR,
                                  dropdown_hover_color=PALE_GREEN_COLOR,
                                  button_color=(HOVER_GREEN, DARK_GREEN_COLOR),
                                  button_hover_color=(DARK_GREEN_COLOR, HOVER_GREEN),
                                  values=["Active","Outdated"], command=lambda option_value,name=project_data[0], status=project_data[1]: (ProjectManager.change_status(None,option_value=option_value,project_name=name,status=eval(status)), self.project_frame_obj())
                                  )
                option_menu.set("Outdated" if eval(project_data[1]) else "Active")
                option_menu.pack(padx=0, pady=20, side="left")

                button = ctk.CTkButton(frame, text="View Components", hover_color=HOVER_GREEN,
                                             fg_color=GREEN_COLOR,
                                             corner_radius=16, text_color=WHITE_COLOR,
                                             font=("Arial", 18), border_spacing=8, width=120,
                                             command=lambda path=components_dir: subprocess.Popen(["notepad.exe", path])
                                             )
                button.pack(padx=40, pady=0, side="left")

                close_button = ctk.CTkButton(frame, text="✖", width=20, height=50,
                                             font=("Arial", 20), corner_radius=64, border_color=X_RED_COLOR, border_width=2,border_spacing=5,
                                             fg_color="white", text_color=X_RED_COLOR,hover_color=WHITE_COLOR,
                                             command=lambda name=project_data[0], status=project_data[1]:(ProjectManager.remove_project(None,name,eval(status)), self.project_frame_obj()))
                close_button.pack(padx=40, pady=20, side="right")


        os.chdir(original_directory)

    def open_add_order_window(self):
        win_width = 700
        win_height = 300

        window = ctk.CTkToplevel()
        window.title("Add a New Order")
        window.geometry(f"{win_width}x{win_height}")
        window.grab_set()
        window.attributes("-topmost", True)
        window.after(100, lambda: window.attributes("-topmost", False))

        entry_label = ctk.CTkLabel(window, text="Enter Order Info:", font=("Arial", 18))
        entry_label.pack(pady=(20, 5))
        notice_label = ctk.CTkLabel(window, text="STRUCTURE: Invoice Number,Project Name,Amount,Must Be Done By,Priority Level", font=("Arial", 18))
        notice_label.pack(pady=(20, 5))
        structure_label = ctk.CTkLabel(window,text="string,string,integer,YYYY-MM-DD,string(low,medium,high)",font=("Arial", 18))
        structure_label.pack(pady=(20, 5))

        order_var = ctk.StringVar()
        entry = ctk.CTkEntry(window, textvariable=order_var, font=("Arial", 18), width=250)
        entry.pack(pady=5)

        self.tool_frame.update_idletasks()
        main_x = self.tool_frame.winfo_rootx()
        main_y = self.tool_frame.winfo_rooty()
        main_width = self.tool_frame.winfo_width()
        main_height = self.tool_frame.winfo_height()


        pos_x = main_x + (main_width // 2) - (win_width // 2)
        pos_y = main_y + (main_height // 2) - (win_height // 2)
        window.geometry(f"{win_width}x{win_height}+{pos_x}+{pos_y}")

        def submit():
            order_info_list = order_var.get().strip().split(",")
            if order_info_list:
                OrderManager.add_order(None,Order(order_info_list[0], order_info_list[1],order_info_list[2],order_info_list[3],order_info_list[4]))
                window.destroy()
                self.order_frame_obj()

        submit_button = ctk.CTkButton(window, text="Add an Order", font=("Arial", 18), command=submit)
        submit_button.pack(pady=(20, 10))

    def order_frame_obj(self):

        for widget in self.data_frame.winfo_children():
            widget.destroy()

        original_directory = os.getcwd()

        search_query = self.search_var.get().lower() if hasattr(self, "search_var") else ""

        order_dir = os.path.join("data", "active_orders.csv")
        with open(order_dir, mode='r', newline='') as f:
            reader = csv.reader(f)
            order_data = list(reader)[1:]

        if self.option_menu.get() == "Priority":
            priority_order = {"high": 0, "medium": 1, "low": 2}
            order_data.sort(key=lambda x: priority_order.get(x[4].lower(), 99))
        elif self.option_menu.get() == "Progress":
            order_data.sort(key=lambda x: float(x[5]), reverse=True)
        elif self.option_menu.get() == "Due Date":
            order_data.sort(key=lambda x: datetime.strptime(x[3].strip(), "%Y-%m-%d"))

        for order in order_data:
            if not order[0].lower().startswith(search_query):
                continue

            frame = ctk.CTkFrame(self.data_frame, height=180, corner_radius=10, fg_color=OBJECT_GREEN)
            frame.pack(fill="x", pady=5, padx=10)
            frame.pack_propagate(False)

            label1 = ctk.CTkLabel(frame, text=f"Order: {order[0]}", font=("Arial", 20), text_color=GREEN_COLOR)
            label1.pack(padx=10, pady=15, anchor="nw")

            progress_frame = ctk.CTkFrame(frame, fg_color="transparent")
            progress_frame.pack(padx=50, pady=10, anchor="w")

            progress_bar = ctk.CTkProgressBar(progress_frame, width=400, height=20,
                                              border_width=3, border_color=DARK_GREEN_COLOR,
                                              progress_color=GREEN_COLOR,fg_color=PALE_GREEN_COLOR)
            progress_bar.set(float(order[5]))
            progress_bar.pack(side="left")

            label6 = ctk.CTkLabel(progress_frame, text=f"{int(float(order[5]) * 100)}%", font=("Arial", 16),
                                  text_color=GREEN_COLOR)
            label6.pack(side="left", padx=(10, 0))

            close_button = ctk.CTkButton(frame, text="✖", width=20, height=50,
                                         font=("Arial", 20), corner_radius=64,
                                         border_color=X_RED_COLOR, border_width=2, border_spacing=5,
                                         fg_color="white", text_color=X_RED_COLOR, hover_color=WHITE_COLOR,
                                         command=lambda invoice=order[0], project=order[1], amount=order[2],
                                                        date=order[3], priority=order[4], progress=order[5]:
                                         (OrderManager.cancel_order(None,
                                                                    Order(invoice, project, amount, date, priority,
                                                                          progress)), self.order_frame_obj()))
            close_button.place(relx=1.0, rely=0.5, anchor="e", x=-10)

            label2 = ctk.CTkLabel(frame, text=f"Project: {order[1]}", font=("Arial", 18), text_color=GREEN_COLOR)
            label2.pack(padx=20, pady=10, side="left")

            label3 = ctk.CTkLabel(frame, text=f"Amount: {order[2]}", font=("Arial", 18), text_color=GREEN_COLOR)
            label3.pack(padx=20, pady=10, side="left")

            label4 = ctk.CTkLabel(frame, text=f"Due Date: {order[3]}", font=("Arial", 18), text_color=GREEN_COLOR)
            label4.pack(padx=20, pady=10, side="left")

            label5 = ctk.CTkLabel(frame, text=f"Priority: {order[4]}", font=("Arial", 18), text_color=GREEN_COLOR)
            label5.pack(padx=20, pady=10, side="left")

        os.chdir(original_directory)

    def add_employee_window(self):
        window = ctk.CTkToplevel()
        window.title("Add a New Employee")
        window.grab_set()
        window.attributes("-topmost", True)
        window.after(100, lambda: window.attributes("-topmost", False))

        entry_label1 = ctk.CTkLabel(window, text="Name:", font=("Arial", 18))
        entry_label1.pack(pady=(50,5))
        name_var = ctk.StringVar()
        entry1 = ctk.CTkEntry(window, textvariable=name_var, font=("Arial", 18), width=250)
        entry1.pack(pady=5)

        entry_label2 = ctk.CTkLabel(window, text="Surname:", font=("Arial", 18))
        entry_label2.pack(pady=5)
        surname_var = ctk.StringVar()
        entry2 = ctk.CTkEntry(window, textvariable=surname_var, font=("Arial", 18), width=250)
        entry2.pack(pady=5)




        self.tool_frame.update_idletasks()
        main_x = self.tool_frame.winfo_rootx()
        main_y = self.tool_frame.winfo_rooty()
        main_width = self.tool_frame.winfo_width()
        main_height = self.tool_frame.winfo_height()

        win_width = 400
        win_height = 300
        pos_x = main_x + (main_width // 2) - (win_width // 2)
        pos_y = main_y + (main_height // 2) - (win_height // 2)
        window.geometry(f"{win_width}x{win_height}+{pos_x}+{pos_y}")

        def submit():
            name = name_var.get().strip()
            surname = surname_var.get().strip()
            if name and surname:
                EmployeeManager.add_employee(None, Employee(name, surname))
                window.destroy()
                self.employees_frame_obj()

        submit_button = ctk.CTkButton(window, text="Add Employee", font=("Arial", 18), command=submit)
        submit_button.pack(pady=(20, 10))

    def assign_unassign_order_window(self):
        window = ctk.CTkToplevel()
        window.title("Assign/Unassign Order")
        window.grab_set()
        window.attributes("-topmost", True)
        window.after(100, lambda: window.attributes("-topmost", False))

        # Position the window centered over main tool_frame
        self.tool_frame.update_idletasks()
        main_x = self.tool_frame.winfo_rootx()
        main_y = self.tool_frame.winfo_rooty()
        main_width = self.tool_frame.winfo_width()
        main_height = self.tool_frame.winfo_height()

        win_width = 600
        win_height = 300
        pos_x = main_x + (main_width // 2) - (win_width // 2)
        pos_y = main_y + (main_height // 2) - (win_height // 2)
        window.geometry(f"{win_width}x{win_height}+{pos_x}+{pos_y}")

        # -- Load and map employees/orders --
        employee_list = EmployeeManager.make_list(None)
        order_list = OrderManager.make_list(None)

        # Create actual objects
        employees = [Employee(e[0], e[1]) for e in employee_list]
        orders = [Order(*o) for o in order_list]

        # Create lookup maps
        employee_map = {f"{e.get_name()} {e.get_surname()}": e for e in employees}
        order_map = {o.get_order_invoice_number(): o for o in orders}

        # -- UI Labels and OptionMenus --
        employee_label = ctk.CTkLabel(window, text="Employee:", font=("Arial", 18))
        employee_label.pack(pady=(40, 5))

        employee_var = ctk.StringVar()
        employee_options = ctk.CTkOptionMenu(window, font=("Arial", 18), width=250,
                                             values=list(employee_map.keys()), variable=employee_var)
        employee_options.pack(pady=5)

        order_label = ctk.CTkLabel(window, text="Order Invoice #:", font=("Arial", 18))
        order_label.pack(pady=5)

        order_var = ctk.StringVar()
        order_options = ctk.CTkOptionMenu(window, font=("Arial", 18), width=250,
                                          values=list(order_map.keys()), variable=order_var)
        order_options.pack(pady=5)

        # -- Button Logic --
        def assign():
            e = employee_map.get(employee_var.get())
            o = order_map.get(order_var.get())
            if e and o:
                EmployeeManager.assign_order(None, e, o)

        def unassign():
            e = employee_map.get(employee_var.get())
            o = order_map.get(order_var.get())
            if e and o:
                EmployeeManager.unassign_order(None, e, o)

        assign_button = ctk.CTkButton(window, text="Assign", font=("Arial", 18), command=assign)
        assign_button.pack(pady=(20, 5))

        unassign_button = ctk.CTkButton(window, text="Unassign", font=("Arial", 18), command=unassign)
        unassign_button.pack(pady=5)

    def employees_frame_obj(self):

        for widget in self.data_frame.winfo_children():
            widget.destroy()

        original_directory = os.getcwd()

        search_query = self.search_var.get().lower() if hasattr(self, "search_var") else ""

        employee_dir = os.path.join("data", "employee_list.csv")
        with open(employee_dir, mode='r', newline='') as f:
            reader = csv.reader(f)
            employee_data = list(reader)[1:]

        for employee in employee_data:
            if not (employee[0].lower().startswith(search_query) or employee[1].lower().startswith(search_query)):
                continue

            frame = ctk.CTkFrame(self.data_frame, height=80, corner_radius=10, fg_color=OBJECT_GREEN)
            frame.pack(fill="x", pady=5, padx=10)
            frame.pack_propagate(False)

            label1 = ctk.CTkLabel(frame, text=f"Name: {employee[0]}", font=("Arial", 22), text_color=GREEN_COLOR)
            label1.pack(padx=25, pady=10, side="left")
            label2 = ctk.CTkLabel(frame, text=f"Surname: {employee[1]}", font=("Arial", 22), text_color=GREEN_COLOR)
            label2.pack(padx=25, pady=10, side="left")

            def view_assignments(data):
                win_width = 700
                win_height = 400

                window = ctk.CTkToplevel()
                window.title("Assignments")
                window.geometry(f"{win_width}x{win_height}")
                window.grab_set()
                window.attributes("-topmost", True)
                window.after(100, lambda: window.attributes("-topmost", False))

                textbox = ctk.CTkTextbox(window, font=("Arial", 18), width=500, height=250)
                textbox.insert("end", data)
                textbox.configure(state="disabled")
                textbox.pack(pady=(20, 5))

                self.tool_frame.update_idletasks()
                main_x = self.tool_frame.winfo_rootx()
                main_y = self.tool_frame.winfo_rooty()
                main_width = self.tool_frame.winfo_width()
                main_height = self.tool_frame.winfo_height()

                pos_x = main_x + (main_width // 2) - (win_width // 2)
                pos_y = main_y + (main_height // 2) - (win_height // 2)
                window.geometry(f"{win_width}x{win_height}+{pos_x}+{pos_y}")

                submit_button = ctk.CTkButton(window, text="Go Back", font=("Arial", 18), command=window.destroy)
                submit_button.pack(pady=(20, 10))

            button = ctk.CTkButton(frame, text="View Assignments", hover_color=HOVER_GREEN,
                                   fg_color=GREEN_COLOR,
                                   corner_radius=16, text_color=WHITE_COLOR,
                                   font=("Arial", 20), border_spacing=8, width=120,
                                   command=lambda data=employee[2:]: view_assignments(str(data))
                                   )
            button.pack(padx=40, pady=0, side="left")

            close_button = ctk.CTkButton(frame, text="✖", width=20, height=50,
                                         font=("Arial", 20), corner_radius=64, border_color=X_RED_COLOR, border_width=2,
                                         border_spacing=5,
                                         fg_color="white", text_color=X_RED_COLOR, hover_color=WHITE_COLOR,
                                         command=lambda name=employee[0], surname=employee[1]: (
                                         EmployeeManager.remove_employee(None, Employee(name, surname)),
                                         self.employees_frame_obj()))
            close_button.pack(padx=40, pady=20, side="right")



        os.chdir(original_directory)

    def storage_window(self):
        win_width = 700
        win_height = 350

        window = ctk.CTkToplevel()
        window.title(f"Add/Remove Components to/from {self.option_menu.get()}")
        window.geometry(f"{win_width}x{win_height}")
        window.grab_set()
        window.attributes("-topmost", True)
        window.after(100, lambda: window.attributes("-topmost", False))

        entry_label = ctk.CTkLabel(window, text="Enter Component(s) Info:", font=("Arial", 18))
        entry_label.pack(pady=(20, 5))
        notice_label = ctk.CTkLabel(window,
                                    text="STRUCTURE: Component Name, Type, Value, Unit, Amount",
                                    font=("Arial", 18))
        notice_label.pack(pady=(20, 5))
        structure_label = ctk.CTkLabel(window, text="string,string,float,string,integer",
                                       font=("Arial", 18))
        structure_label.pack(pady=(20, 5))

        component_var = ctk.StringVar()
        entry = ctk.CTkEntry(window, textvariable=component_var, font=("Arial", 18), width=250)
        entry.pack(pady=5)

        self.tool_frame.update_idletasks()
        main_x = self.tool_frame.winfo_rootx()
        main_y = self.tool_frame.winfo_rooty()
        main_width = self.tool_frame.winfo_width()
        main_height = self.tool_frame.winfo_height()

        pos_x = main_x + (main_width // 2) - (win_width // 2)
        pos_y = main_y + (main_height // 2) - (win_height // 2)
        window.geometry(f"{win_width}x{win_height}+{pos_x}+{pos_y}")

        def add():
            location = self.option_menu.get().lower()
            component_info_list = component_var.get().strip().split(",")
            if location == "storage":
                StorageManager.add_component(None, Component(component_info_list[0], component_info_list[1],component_info_list[2], component_info_list[3],component_info_list[4]), location)
            else:
                StorageManager.add_component(None, Component(component_info_list[0], component_info_list[1],component_info_list[2], component_info_list[3], None),location)

            self.storage_frame_obj()

        def remove():
            location = self.option_menu.get().lower()
            component_info_list = component_var.get().strip().split(",")
            if location == "storage":
                StorageManager.remove_component(None, Component(component_info_list[0], component_info_list[1],component_info_list[2], component_info_list[3],component_info_list[4]), location)
            else:
                StorageManager.remove_component(None, Component(component_info_list[0], component_info_list[1],component_info_list[2], component_info_list[3], None), location)

            self.storage_frame_obj()


        submit_button1 = ctk.CTkButton(window, text="Add Component(s)", font=("Arial", 18), command=add)
        submit_button1.pack(pady=(20, 10))
        submit_button2 = ctk.CTkButton(window, text="Remove Component(s)", font=("Arial", 18), command=remove)
        submit_button2.pack(pady=(20, 10))

    def storage_frame_obj(self):

        for widget in self.data_frame.winfo_children():
            widget.destroy()

        original_directory = os.getcwd()

        file = "components_in_storage.csv" if self.option_menu.get()=="Storage" else "components_in_library.csv"
        file_path = os.path.join("data", file)

        search_query = self.search_var.get().lower() if hasattr(self, "search_var") else ""
        with open(file_path, mode='r', newline='', encoding='utf-8') as f:
            reader = csv.reader(f)
            all_data = list(reader)
            headers = all_data[0]
            component_data = all_data[1:]


        component_data = [row for row in component_data if row[0].lower().startswith(search_query)]

        for col, header in enumerate(headers):
            label = ctk.CTkLabel(self.data_frame, text=header, font=("Arial", 24, "bold"), text_color=DARK_GREEN_COLOR)
            label.grid(row=0, column=col, padx=10, pady=5, sticky="nsew")

        # Make all columns expand to fill the frame
        for col in range(len(headers)):
            self.data_frame.grid_columnconfigure(col, weight=1)

        # Set rows
        for row_index, component in enumerate(component_data, start=1):
            for col_index, value in enumerate(component):
                cell = ctk.CTkLabel(self.data_frame, text=value, font=("Arial", 20), text_color=GREEN_COLOR)
                cell.grid(row=row_index, column=col_index, padx=10, pady=5, sticky="nsew")


        os.chdir(original_directory)

    def create_search_bar(self,frame_name):
        self.search_var = ctk.StringVar()
        self.search_var.trace_add("write", lambda *args: self.project_frame_obj() if frame_name=="Projects" else (self.order_frame_obj() if frame_name == "Orders" else
                                                (self.employees_frame_obj() if frame_name == "Employees" else self.storage_frame_obj())))

        self.search_bar = ctk.CTkEntry(master=self.tool_frame,textvariable=self.search_var, font=("Arial", 20), placeholder_text="Search...",width=300, height=45,corner_radius=12, text_color=GREEN_COLOR)
        self.search_bar.place(relx=0.05, rely=0.5, anchor="w")

    def create_option_menu(self, frame_name):
        if frame_name == "Projects": options = [["Active","Outdated"],"Status:"]
        if frame_name == "Orders": options = [["Priority","Progress", "Due Date"],"Sort By:"]
        if frame_name == "Storage": options = [["Storage", "Library"],"Location:"]

        option_label = ctk.CTkLabel(master=self.tool_frame,font=("Arial", 26),text_color=GREEN_COLOR, text=options[1])
        self.option_menu=ctk.CTkOptionMenu(master=self.tool_frame,width=150,height=45,corner_radius=12, font=("Arial", 26),
                                      text_color=GREEN_COLOR, dropdown_font=("Arial", 20), dropdown_text_color=GREEN_COLOR,
                                      fg_color=PALE_COLOR,dropdown_fg_color=PALE_COLOR,dropdown_hover_color=PALE_GREEN_COLOR,
                                      button_color=(HOVER_GREEN, DARK_GREEN_COLOR),button_hover_color=(DARK_GREEN_COLOR,HOVER_GREEN),
                                      values=options[0],command= lambda value: (self.project_frame_obj() if frame_name == "Projects" else
                                      (self.order_frame_obj() if frame_name == "Orders" else self.storage_frame_obj()))
                                      )
        option_label.place(relx=0.52, rely=0.5, anchor="e")
        self.option_menu.place(relx=0.53, rely=0.5, anchor="w")

    def create_buttons(self, frame_name):
        if frame_name == "Projects":
            self.button1 = ctk.CTkButton(self.tool_frame, text="Add a Project", hover_color=HOVER_GREEN, fg_color=GREEN_COLOR,
                                   corner_radius=26, text_color=WHITE_COLOR,
                                   font=("Arial", 26), border_spacing=10, width=150, command=self.open_add_project_window
                                   )
            self.button1.place(relx=0.95, rely=0.5, anchor="e")
        elif frame_name == "Orders":
            self.button1 = ctk.CTkButton(self.tool_frame, text="Add an Order", hover_color=HOVER_GREEN, fg_color=GREEN_COLOR,
                                   corner_radius=26, text_color=WHITE_COLOR,
                                   font=("Arial", 26), border_spacing=10, width=150, command=self.open_add_order_window
                                   )
            self.button1.place(relx=0.95, rely=0.5, anchor="e")
        elif frame_name == "Storage":
            self.button1 = ctk.CTkButton(self.tool_frame, text="Add/Remove\nComponents",hover_color=HOVER_GREEN, fg_color=GREEN_COLOR,
                                   corner_radius=26, text_color=WHITE_COLOR,
                                   font=("Arial", 22), border_spacing=8, width=150, command=self.storage_window
                                   )
            self.button1.place(relx=0.95, rely=0.5, anchor="e")
        else:
            self.button1 = ctk.CTkButton(self.tool_frame, text="Add an\nEmployee", hover_color=HOVER_GREEN,
                                   fg_color=GREEN_COLOR,
                                   corner_radius=26, text_color=WHITE_COLOR,
                                   font=("Arial", 22), border_spacing=8, width=150, command=self.add_employee_window
                                   )
            self.button1.place(relx=0.6, rely=0.5, anchor="center")
            self.button2 = ctk.CTkButton(self.tool_frame, text="Assign/Unassign\nAn Order", hover_color=HOVER_GREEN,
                                   fg_color=GREEN_COLOR,
                                   corner_radius=26, text_color=WHITE_COLOR,
                                   font=("Arial", 22), border_spacing=8, width=150, command=self.assign_unassign_order_window
                                   )
            self.button2.place(relx=0.95, rely=0.5, anchor="e")

class ProjectFrame(DataFrame):
    def __init__(self, app):
        super().__init__(app, "Projects")

class OrderFrame(DataFrame):
    def __init__(self, app):
        super().__init__(app, "Orders")

class EmployeeFrame(DataFrame):
    def __init__(self, app):
        super().__init__(app, "Employees")

class StorageFrame(DataFrame):
    def __init__(self, app):
        super().__init__(app, "Storage")

class ActivityLogFrame(DataFrame):
    def __init__(self, app):
        super().__init__(app, "Activity Log")