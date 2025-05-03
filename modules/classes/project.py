class Project:
    def __init__(self, __project_name, __required_components,__outdated=False):
        self.__project_name = __project_name
        self.__required_components = __required_components
        self.__outdated = __outdated

    def get_project_name(self):
        return self.__project_name

    def get_required_components(self):
        return self.__required_components

    def is_outdated(self):
        return self.__outdated
