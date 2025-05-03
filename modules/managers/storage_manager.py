import os
import csv

from modules.classes.logger import Logger

class StorageManager:

    def add_component(self, component, location):
        original_directory = os.getcwd()
        if self: os.chdir('../../')

        if location == "library":
            file_name = "components_in_library.csv"
            project_dir = os.path.join("data", file_name)

            if os.path.exists(project_dir) and (not (os.path.getsize(project_dir) == 0)):
                with open(project_dir, mode='r', newline='') as f:
                    reader = csv.reader(f)
                    components = list(reader)

                if components:
                    header = components[0]
                    data = components[1:]
                else:
                    header = ["Component Name", "Type", "Value", "Unit"]
                    data = []

                updated = False
                for row in data:
                    if row is not None:
                        if row[0] == component.get_component_name():
                            updated = True
                            break

                if not updated:
                    data.append(component.get_component_values())

                with open(project_dir, mode='w', newline='') as f:
                    writer = csv.writer(f)
                    writer.writerow(header)
                    writer.writerows(data)
            else:

                with open(project_dir, mode='a', newline='') as f:
                    writer = csv.writer(f)
                    writer.writerow(["Component Name", "Type", "Value", "Unit"])
                    writer.writerow(component.get_component_values_without_amount())

        elif location == "storage":
            file_name = "components_in_storage.csv"
            project_dir = os.path.join("data", file_name)

            if os.path.exists(project_dir) and (not (os.path.getsize(project_dir) == 0)):
                with open(project_dir, mode='r', newline='') as f:
                    reader = csv.reader(f)
                    components = list(reader)

                if components:
                    header = components[0]
                    data = components[1:]
                else:
                    header = ["Component Name", "Type", "Value", "Unit", "Amount"]
                    data = []

                updated = False
                for row in data:
                    if row is not None:
                        if row[0] == component.get_component_name():
                            row[4] = str(int(row[4]) + int(component.get_component_amount()))
                            updated = True
                            break

                if not updated:
                    data.append(component.get_component_values())

                with open(project_dir, mode='w', newline='') as f:
                    writer = csv.writer(f)
                    writer.writerow(header)
                    writer.writerows(data)

            else:
                os.chdir('../../')
                with open(project_dir, mode='w', newline='') as f:
                    writer = csv.writer(f)
                    writer.writerow(["Component Name", "Type", "Value", "Unit", "Amount"])
                    writer.writerow(component.get_component_values())

        os.chdir(original_directory)
        Logger.log(f"Added new component(s) {component.get_component_values() if location=="storage" else component.get_component_values_without_amount()} to {location}")

    def remove_component(self, component, location):
        original_directory = os.getcwd()
        if self: os.chdir('../../')

        if location == "library":
            file_name = "components_in_library.csv"
            project_dir = os.path.join("data", file_name)

            if os.path.exists(project_dir) and (not (os.path.getsize(project_dir) == 0)):
                with open(project_dir, mode='r', newline='') as f:
                    reader = csv.reader(f)
                    components = list(reader)

                if components:
                    header = components[0]
                    data = components[1:]
                else:
                    header = ["Component Name", "Type", "Value", "Unit"]
                    data = []

                rows_to_keep = []
                for row in data:

                    if row is not None:
                        if row[0] == component.get_component_name():
                            row.clear()

                        else:
                            rows_to_keep.append(row)
                    data = rows_to_keep

                with open(project_dir, mode='w', newline='') as f:
                    writer = csv.writer(f)
                    writer.writerow(header)
                    writer.writerows(data)

        elif location == "storage":
            file_name = "components_in_storage.csv"
            project_dir = os.path.join("data", file_name)

            if os.path.exists(project_dir) and (not (os.path.getsize(project_dir) == 0)):
                with open(project_dir, mode='r', newline='') as f:
                    reader = csv.reader(f)
                    components = list(reader)

                if components:
                    header = components[0]
                    data = components[1:]
                else:
                    header = ["Component Name", "Type", "Value", "Unit", "Amount"]
                    data = []

                rows_to_keep = []
                for row in data:

                    if row is not None:
                        if row[0] == component.get_component_name():
                            row[4] = str(int(row[4]) - int(component.get_component_amount()))

                            if int(row[4])== 0:
                                row.clear()
                            else:
                                rows_to_keep.append(row)
                        else:
                            rows_to_keep.append(row)

                    data = rows_to_keep

                with open(project_dir, mode='w', newline='') as f:
                    writer = csv.writer(f)
                    writer.writerow(header)
                    writer.writerows(data)

        os.chdir(original_directory)
        Logger.log(f"Removed component(s) {component.get_component_values() if location == "storage" else component.get_component_values_without_amount()} from {location}")
