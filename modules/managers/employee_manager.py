import os
import csv

from modules.classes.project import Project

from modules.classes.logger import Logger


class EmployeeManager:

    def make_list(self):
        original_directory = os.getcwd()

        data = None

        if self: os.chdir('../../')
        project_dir = os.path.join("data", "employee_list.csv")

        if os.path.exists(project_dir) and (not (os.path.getsize(project_dir) == 0)):
            with open(project_dir, mode='r', newline='') as f:
                reader = csv.reader(f)
                data = list(reader)[1:]

        os.chdir(original_directory)

        return data

    def add_employee(self, employee):
        original_directory = os.getcwd()
        if self: os.chdir('../../')

        file_name = "employee_list.csv"
        project_dir = os.path.join("data", file_name)


        name_surname = employee.employee_get_personal_info()

        if os.path.exists(project_dir) and (not (os.path.getsize(project_dir) == 0)):
            with open(project_dir, mode='r', newline='') as f:
                reader = csv.reader(f)
                employees = list(reader)

            if employees:
                 header = employees[0]
                 data = employees[1:]
            else:
                header = ["Name", "Surname","Assigned Orders"]
                data = []

            updated = False
            for row in data:
                 if row is not None and (row[0] == name_surname[0] and row[1] == name_surname[1]):
                    updated = True
                    break

            if not updated:
                data.append([name_surname[0],name_surname[1],""])

            with open(project_dir, mode='w', newline='') as f:
                writer = csv.writer(f)
                writer.writerow(header)
                writer.writerows(data)

        else:
            os.chdir('../../')
            with open(project_dir, mode='w', newline='') as f:
                writer = csv.writer(f)
                writer.writerow(["Name","Surname","Assigned Orders"])
                writer.writerow([name_surname[0],name_surname[1],""])

        os.chdir(original_directory)
        Logger.log(f"Added employee {name_surname[0]} {name_surname[1]}")

    def remove_employee(self, employee):
        original_directory = os.getcwd()
        if self: os.chdir('../../')

        file_name = "employee_list.csv"
        project_dir = os.path.join("data", file_name)


        name_surname = employee.employee_get_personal_info()

        if os.path.exists(project_dir) and (not (os.path.getsize(project_dir) == 0)):
            with open(project_dir, mode='r', newline='') as f:
                reader = csv.reader(f)
                employees = list(reader)

            if employees:
                 header = employees[0]
                 data = employees[1:]
            else:
                header = ["Name", "Surname","Assigned Orders"]
                data = []

            rows_to_keep = []
            for row in data:

                row.clear() if row is not None and (row[0] == name_surname[0] and row[1] == name_surname[1]) else rows_to_keep.append(row)
                data = rows_to_keep

            with open(project_dir, mode='w', newline='') as f:
                writer = csv.writer(f)
                writer.writerow(header)
                writer.writerows(data)

        os.chdir(original_directory)
        Logger.log(f"Removed employee {name_surname[0]} {name_surname[1]}")

    def assign_order(self, employee, order):
        original_directory = os.getcwd()
        if self: os.chdir('../../')

        file_name = "employee_list.csv"
        project_dir = os.path.join("data", file_name)

        name_surname = employee.employee_get_personal_info()

        if os.path.exists(project_dir) and (not (os.path.getsize(project_dir) == 0)):
            with open(project_dir, mode='r', newline='') as f:
                reader = csv.reader(f)
                employees = list(reader)

            if employees:
                header = employees[0]
                data = employees[1:]
            else:
                header = ["Name", "Surname", "Assigned Orders"]
                data = []

            for row in data:
                if row is not None and (row[0] == name_surname[0] and row[1] == name_surname[1]):
                        if order.get_order_invoice_number() not in row:
                            if len(row) > 2 and row[2] == "": row[2]=order.get_order_invoice_number()
                            else: row.append(order.get_order_invoice_number())

            with open(project_dir, mode='w', newline='') as f:
                writer = csv.writer(f)
                writer.writerow(header)
                writer.writerows(data)

        os.chdir(original_directory)
        Logger.log(f"Order {order.get_order_invoice_number()} assigned to {name_surname[0]} {name_surname[1]}")

    def unassign_order(self, employee, order):
        original_directory = os.getcwd()
        if self: os.chdir('../../')

        file_name = "employee_list.csv"
        project_dir = os.path.join("data", file_name)

        name_surname = employee.employee_get_personal_info()


        if os.path.exists(project_dir) and (not (os.path.getsize(project_dir) == 0)):
            with open(project_dir, mode='r', newline='') as f:
                reader = csv.reader(f)
                employees = list(reader)

            if employees:
                header = employees[0]
                data = employees[1:]
            else:
                header = ["Name", "Surname", "Assigned Orders"]
                data = []

            invoice_number = order.get_order_invoice_number()
            for row in data:
                if row is not None and (row[0] == name_surname[0] and row[1] == name_surname[1]):
                    sublist = row[2:]
                    if invoice_number in sublist:
                        sublist.remove(invoice_number)
                    row[:] = row[:2] + sublist

            with open(project_dir, mode='w', newline='') as f:
                writer = csv.writer(f)
                writer.writerow(header)
                writer.writerows(data)

        os.chdir(original_directory)
        Logger.log(f"Order {order.get_order_invoice_number()} unassigned from {name_surname[0]} {name_surname[1]}")


