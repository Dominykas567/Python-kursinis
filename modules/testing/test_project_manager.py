import unittest
from unittest.mock import MagicMock, patch
import os
import shutil
import csv

from modules.classes.logger import Logger
from modules.managers.project_manager import ProjectManager  # Adjust import path if necessary

# Mocking the Logger class import
class MockLogger:
    @staticmethod
    def log(message):
        pass  # Just a dummy function for testing


# Ensure that Logger is properly mocked for the tests
@patch('modules.classes.project_manager.Logger', MockLogger)  # Adjust path if necessary
class TestProjectManager(unittest.TestCase):

    @patch('os.makedirs')
    @patch('builtins.open')
    @patch('os.chdir')
    def test_create_project(self, mock_chdir, mock_open, mock_makedirs):
        # Setup mock objects
        project_name = "TestProject"
        status = False
        required_components = []

        # Create a mock for the file opening
        mock_open.return_value.__enter__.return_value = MagicMock()
        mock_makedirs.return_value = None

        project_manager = ProjectManager()

        # Call the create_project method
        project_manager.create_project(project_name, status, required_components)

        # Check that os.makedirs was called to create the directory
        mock_makedirs.assert_called_once_with(os.path.join("data", "active_projects", project_name), exist_ok=True)

        # Check that the project CSV file was opened for writing
        mock_open.assert_any_call(os.path.join("data", "active_projects", project_name, "project.csv"), mode='w',
                                  newline='')

        # Check that the 'required_components.csv' was opened for writing
        mock_open.assert_any_call(os.path.join("data", "active_projects", project_name, "required_components.csv"),
                                  mode='w', newline='')

    @patch('shutil.rmtree')
    @patch('os.path.exists')
    @patch('os.chdir')
    def test_remove_project(self, mock_chdir, mock_exists, mock_rmtree):
        project_name = "TestProject"
        status = False
        project_dir = os.path.join("data", "active_projects", project_name)

        # Mock file system checks
        mock_exists.return_value = True
        mock_rmtree.return_value = None

        project_manager = ProjectManager()

        # Call the remove_project method
        project_manager.remove_project(project_name, status)

        # Check that shutil.rmtree was called to remove the directory
        mock_rmtree.assert_called_once_with(project_dir)

    @patch('shutil.move')
    @patch('os.path.exists')
    @patch('os.path.isdir')
    @patch('builtins.open')
    def test_change_status(self, mock_open, mock_isdir, mock_exists, mock_move):
        project_name = "TestProject"
        status = False
        option_value = "Outdated"

        # Mock file system checks
        mock_exists.return_value = True
        mock_isdir.return_value = True
        mock_move.return_value = None
        mock_open.return_value.__enter__.return_value = MagicMock()

        project_manager = ProjectManager()

        # Call the change_status method
        project_manager.change_status(project_name, status, option_value)

        # Check that shutil.move was called to move the project folder
        folder_from = os.path.join("data", "active_projects", project_name)
        folder_to = os.path.join("data", "outdated_projects", project_name)
        mock_move.assert_called_once_with(folder_from, folder_to)

        # Check that the project CSV file was opened for writing
        file_path = os.path.join(folder_to, "project.csv")
        mock_open.assert_called_once_with(file_path, mode='w', newline='')


if __name__ == '__main__':
    unittest.main()
