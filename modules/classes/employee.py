class Employee:
    def __init__(self, __name, __surname):
        self.__assigned_orders = []
        self.__name = __name
        self.__surname = __surname

    def employee_get_info(self):
        return [self.__name, self.__surname, self.__assigned_orders]

    def employee_get_personal_info(self):
        return [self.__name, self.__surname]

    def employee_get_assigned_orders(self):
        return self.__assigned_orders

    def get_name(self):
        return self.__name

    def get_surname(self):
        return self.__surname