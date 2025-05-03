import os
import csv

from modules.classes.employee import Employee
from modules.managers.employee_manager import EmployeeManager

from modules.classes.logger import Logger

class OrderManager:

    def make_list(self):
        original_directory = os.getcwd()

        data = None

        if self: os.chdir('../../')
        project_dir = os.path.join("data", "active_orders.csv")

        if os.path.exists(project_dir) and (not (os.path.getsize(project_dir) == 0)):
            with open(project_dir, mode='r', newline='') as f:
                reader = csv.reader(f)
                data = list(reader)[1:]

        os.chdir(original_directory)

        return data

    def add_order(self, order):
        original_directory = os.getcwd()
        if self: os.chdir('../../')

        file_name = "active_orders.csv"
        project_dir = os.path.join("data", file_name)

        if os.path.exists(project_dir) and (not (os.path.getsize(project_dir) == 0)):
            with open(project_dir, mode='r', newline='') as f:
                reader = csv.reader(f)
                orders = list(reader)

            if orders:
                header = orders[0]
                data = orders[1:]
            else:
                header = ["Invoice Number", "Project Name", "Amount", "Must Be Done By", "Priority Level", "Progress To Completion"]
                data = []

            updated = False
            for row in data:
                if row is not None:
                    if row[0] == order.get_order_invoice_number():
                        updated = True
                        break

            if not updated:
                data.append(order.get_order_info())

            with open(project_dir, mode='w', newline='') as f:
                writer = csv.writer(f)
                writer.writerow(header)
                writer.writerows(data)
        else:
            os.chdir('../../')
            with open(project_dir, mode='a', newline='') as f:
                writer = csv.writer(f)
                writer.writerow(["Invoice Number", "Project Name", "Amount", "Must Be Done By", "Priority Level", "Progress To Completion"])
                writer.writerow(order.get_order_info())

        os.chdir(original_directory)
        Logger.log(f"Added order {order.get_order_info()}")

    def cancel_order(self, order):
        original_directory = os.getcwd()
        if self: os.chdir('../../')

        file_name = "active_orders.csv"
        project_dir = os.path.join("data", file_name)

        if os.path.exists(project_dir) and (not (os.path.getsize(project_dir) == 0)):
            with open(project_dir, mode='r', newline='') as f:
                reader = csv.reader(f)
                orders = list(reader)

            if orders:
                header = orders[0]
                data = orders[1:]
            else:
                header = ["Invoice Number", "Project Name", "Amount", "Must Be Done By", "Priority Level", "Progress To Completion"]
                data = []

            rows_to_keep = []
            for row in data:

                if row is not None:
                    if row[0] == order.get_order_invoice_number():
                        row.clear()

                    else:
                        rows_to_keep.append(row)
                data = rows_to_keep

            with open(project_dir, mode='w', newline='') as f:
                writer = csv.writer(f)
                writer.writerow(header)
                writer.writerows(data)

            employees = EmployeeManager.make_list(None)
            for employee in employees: EmployeeManager.unassign_order(None,Employee(employee[0],employee[1]), order)

        os.chdir(original_directory)
        Logger.log(f"Canceled order {order.get_order_info()}")

