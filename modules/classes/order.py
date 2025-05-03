class Order:
    def __init__(self, __invoice_number, __project_name, __amount, __must_be_done_by, __priority_level="medium", __progress_to_completion = 0):
        self.__invoice_number = __invoice_number
        self.__project_name = __project_name
        self.__amount = __amount
        self.__must_be_done_by = __must_be_done_by
        self.__priority_level = __priority_level
        self.__progress_to_completion = __progress_to_completion

    def get_order_info(self):
        return [self.__invoice_number, self.__project_name, self.__amount, self.__must_be_done_by, self.__priority_level, self.__progress_to_completion]

    def get_order_invoice_number(self):
        return self.__invoice_number