import pytest
from unittest.mock import patch, MagicMock
import os
import csv

from modules.classes.project import Project
from modules.classes.employee import Employee
from modules.classes.logger import Logger
from modules.managers.employee_manager import EmployeeManager  # Assuming this is the correct import path

import os
from unittest.mock import MagicMock, patch
import pytest


# Test cases
@pytest.fixture
def mock_employee():
    return MagicMock(spec=Employee)


@pytest.fixture
def mock_order():
    return "Order123"


@patch("os.path.exists")
@patch("os.path.getsize")
@patch("builtins.open", new_callable=MagicMock)
@patch.object(Logger, 'log')
def test_add_employee(mock_log, mock_open, mock_getsize, mock_exists, mock_employee):
    mock_exists.return_value = True
    mock_getsize.return_value = 100
    mock_open.return_value.__enter__.return_value = MagicMock()

    mock_employee.name = "John"
    mock_employee.surname = "Doe"

    employee_manager = EmployeeManager()

    # Add employee
    employee_manager.add_employee(mock_employee)

    # Check that the file is opened twice (first for reading, then for writing)
    assert mock_open.call_count == 2

    # Check the first call (reading)
    mock_open.assert_any_call("data/employee_list.csv", mode='r', newline='')

    # Check the second call (writing)
    mock_open.assert_any_call("data/employee_list.csv", mode='w', newline='')

    # Verify the log message
    mock_log.assert_called_once_with("Added employee John Doe")


@patch("os.path.exists")
@patch("os.path.getsize")
@patch("builtins.open", new_callable=MagicMock)
@patch.object(Logger, 'log')
def test_remove_employee(mock_log, mock_open, mock_getsize, mock_exists, mock_employee):
    mock_exists.return_value = True
    mock_getsize.return_value = 100
    mock_open.return_value.__enter__.return_value = MagicMock()

    mock_employee.name = "John"
    mock_employee.surname = "Doe"

    employee_manager = EmployeeManager()

    # Remove employee
    employee_manager.remove_employee(mock_employee)

    # Check that the file is opened twice (first for reading, then for writing)
    assert mock_open.call_count == 2

    # Check the first call (reading)
    mock_open.assert_any_call("data/employee_list.csv", mode='r', newline='')

    # Check the second call (writing)
    mock_open.assert_any_call("data/employee_list.csv", mode='w', newline='')

    # Verify the log message
    mock_log.assert_called_once_with("Removed employee John Doe")


@patch("os.path.exists")
@patch("os.path.getsize")
@patch("builtins.open", new_callable=MagicMock)
@patch.object(Logger, 'log')
def test_assign_order(mock_log, mock_open, mock_getsize, mock_exists, mock_employee, mock_order):
    mock_exists.return_value = True
    mock_getsize.return_value = 100
    mock_open.return_value.__enter__.return_value = MagicMock()

    mock_employee.name = "John"
    mock_employee.surname = "Doe"

    employee_manager = EmployeeManager()

    # Assign order
    employee_manager.assign_order(mock_employee, mock_order)

    # Check that the file is opened twice (first for reading, then for writing)
    assert mock_open.call_count == 2

    # Check the first call (reading)
    mock_open.assert_any_call("data/employee_list.csv", mode='r', newline='')

    # Check the second call (writing)
    mock_open.assert_any_call("data/employee_list.csv", mode='w', newline='')

    # Verify the log message
    mock_log.assert_called_once_with(f"Assigned order {mock_order} to employee John Doe")


@patch("os.path.exists")
@patch("os.path.getsize")
@patch("builtins.open", new_callable=MagicMock)
@patch.object(Logger, 'log')
def test_unassign_order(mock_log, mock_open, mock_getsize, mock_exists, mock_employee, mock_order):
    mock_exists.return_value = True
    mock_getsize.return_value = 100
    mock_open.return_value.__enter__.return_value = MagicMock()

    mock_employee.name = "John"
    mock_employee.surname = "Doe"

    employee_manager = EmployeeManager()

    # Unassign order
    employee_manager.unassign_order(mock_employee, mock_order)

    # Check that the file is opened twice (first for reading, then for writing)
    assert mock_open.call_count == 2

    # Check the first call (reading)
    mock_open.assert_any_call("data/employee_list.csv", mode='r', newline='')

    # Check the second call (writing)
    mock_open.assert_any_call("data/employee_list.csv", mode='w', newline='')

    # Verify the log message
    mock_log.assert_called_once_with(f"Unassigned order {mock_order} from employee John Doe")
