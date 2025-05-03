import os
import csv
import shutil

from modules.classes.logger import Logger

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


        print(f"Project '{project_name}' created in '{folder}' with required CSV files.")

        os.chdir(original_directory)
        Logger.log(f"Created project {project_name}")

    def remove_project(self, project_name, status):

        original_directory = os.getcwd()
        if self: os.chdir('../../')

        folder = "outdated_projects" if status else "active_projects"

        project_dir = os.path.join("data", folder, project_name)

        os.chdir(project_dir)
        delete_path = os.getcwd()
        os.chdir(original_directory)
        Logger.log(f"Removed project {project_name}")

        if os.path.exists(delete_path) and os.path.isdir(delete_path):
            try:
                shutil.rmtree(delete_path)
                print(f"Directory '{delete_path}' and its contents have been deleted.")
            except Exception as e:
                print(f"Error occurred while deleting the directory: {e}")

    def change_status(self,project_name, status, option_value):

        if (option_value == "Outdated" and status==False) or (option_value == "Active" and status==True):
            original_directory = os.getcwd()
            folder = "outdated_projects" if status else "active_projects"

            project_dir = os.path.join(os.getcwd(),"data", folder, project_name)
            os.chdir(original_directory)
            folder = "outdated_projects" if not status else "active_projects"
            destination_path = os.path.join("data", folder,project_name)

            try:
                shutil.move(project_dir, destination_path)
                print(f"Folder moved successfully from {project_dir} to {destination_path}")
            except Exception as e:
                print(f"Error occurred: {e}")

            file_path=os.path.join(destination_path, "project.csv")
            with open(file_path, mode='w', newline='') as f:
                writer = csv.writer(f)
                writer.writerow(["Project Name", "Status"])
                writer.writerow([project_name, str(not status)])

            os.chdir(original_directory)
            Logger.log(f"Changed {project_name} status to {option_value}")

