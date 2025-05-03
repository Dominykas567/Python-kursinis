# Printed Circuit Board Management Business System

## The Program

My application is designed to store and manage various data related to PCB (printed circuit board) manufacturing. To run the program, simply type the following command in your command prompt: `python main.py`. Once the program is open, you will see a sidebar with several options to choose from, depending on your intended actions.

## How does the program cover functional requirements

**4 OOP pillar examples in the code:**

 1. Polymorphism
```python
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
```
Depending on the `frame_name` variable, the class constructor initializes different functions, creating different data windows with each iteration.

 2. Abstraction
```python
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
```
Here you can see the main classes for the buttons used in the UI. When initialized, they simply pass arguments to the `DataFrame` class, which in turn creates a UI window displaying the corresponding data.

 3. Inheritance
```python
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
```
Inheritance is used here to extend or modify the behavior of the **CustomTkinter** framework. The `App` class played a key role in many functions to shape the UI according to the user's needs.

 4. Encapsulation
```python
class Component:  
    def __init__(self, __component_name, __component_type, __component_value, __component_unit, __amount):  
        self.__component_name = __component_name  
        self.__component_type = __component_type  
        self.__component_value = __component_value  
        self.__component_unit = __component_unit  
        self.__amount = __amount  
  
    def get_component_values(self):  
        return [self.__component_name, self.__component_type, self.__component_value, self.__component_unit, self.__amount]  
  
    def get_component_values_without_amount(self):  
        return [self.__component_name, self.__component_type, self.__component_value, self.__component_unit]  
  
    def get_component_name(self):  
        return self.__component_name  
  
    def get_component_amount(self):  
        return self.__amount
        
```
Here you can see the `Component` class, which applies the principle of encapsulation to better control the flow of information within the program.

**"Decorator" design pattern usage:**
```python
def with_cooldown(button, func, cooldown_ms=1000):  
    def wrapper():  
        button.configure(state="disabled")  
        func()  
        button.after(cooldown_ms, lambda: button.configure(state="normal"))  
    return wrapper
```
This design pattern was essential for implementing a cooldown period on the menu buttons in the UI, during which they could not be pressed.

**Composition principle usage:**
```python
class DataFrame:  
    def __init__(self, app, frame_name):  
  
        self.search_bar = None  
  self.search_var = None  
  self.button1 = None  
  self.button2 = None  
  self.option_menu = None  
```
Without the `DataFrame` class, no buttons can exist, as they must be assigned to the correct frame in order to function properly.

**Reading from file & writing to file:**
```python
class ProjectManager:  
  
    def create_project(self, project_name, status, required_components=None):  
        if required_components is None:  
            required_components = []  
        original_directory = os.getcwd()  
        if self: os.chdir('../../')  
  
        folder = "outdated_projects" if status else "active_projects"  
  
  project_dir = os.path.join("data", folder, project_name)  
  
        os.makedirs(project_dir, exist_ok=True)  
  
        required_components_path = os.path.join(project_dir, "required_components.csv")  
        project_data_path = os.path.join(project_dir, "project.csv")  
  
  
        with open(required_components_path, mode='w', newline='') as f:  
            writer = csv.writer(f)  
            writer.writerow(["Component Name", "Type", "Value", "Unit", "Amount"])  
            if required_components:  
                for row in required_components:  
                    writer.writerow(row.get_component_values())  
  
  
        with open(project_data_path, mode='w', newline='') as f:  
            writer = csv.writer(f)  
            writer.writerow(["Project Name", "Status"])  
            writer.writerow([project_name, status])  
  
        os.chdir(original_directory)  
        Logger.log(f"Created project {project_name}")
```
Reading and writing data is a key part of the program’s functionality. For example, a method in the `ProjectManager` class creates a new record in its respective `.csv` file. This newly added record then becomes visible in the "Projects" section of the program.

## Results and Summary
**Results:**

A new program has been created that allows for relatively controlled management of various data. The program also includes its own user interface, through which users can view, add, and remove different types of records in the corresponding `.csv` files.

**Conclusion:**

In conclusion, the process of creating this program provided valuable experience and improved problem-solving skills. The program uses the **CustomTkinter** framework for the user interface, which was initially challenging to implement, but eventually became fairly familiar. Developing the program helped deepen the understanding of object-oriented programming (OOP) principles and introduced a new framework for creating visual elements. Although the program is still in a very early and basic stage, it could serve as a useful example for future projects.
