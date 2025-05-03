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