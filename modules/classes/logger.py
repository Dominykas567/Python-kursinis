import datetime, os, subprocess

class Logger:

    @staticmethod
    def log(action: str):
        original_directory = os.getcwd()

        file_dir = os.path.join("data", "log.txt")

        time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        with open(file_dir, "a") as file:
            file.write(f"[{time}] {action}\n")

        os.chdir(original_directory)

    @staticmethod
    def clear():
        original_directory = os.getcwd()

        file_dir = os.path.join("data", "log.txt")
        with open(file_dir, "w") as file:
            file.write("")

        os.chdir(original_directory)

    @staticmethod
    def open_file():
        original_directory = os.getcwd()

        file_dir = os.path.join("data", "log.txt")
        print(file_dir)
        subprocess.Popen(["notepad.exe", file_dir])
        os.chdir(original_directory)