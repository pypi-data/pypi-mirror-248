"""

\t\t\t\t  
بسم الله الرحمن الرحيم
=
\t\n
Pamylka python package\n
Created by Ahmed Elbehairy
Created at 13/3/1445 Higri


"""
__creator__ = "Ahmed Elbehairy"
__Founder__ = "Ahmed Elbehairy"
__copyrights__ = "All copyrights reserved at pamylka.com"
__version__ = "00.03.12"

from re import compile
from selenium.webdriver import Chrome
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from fake_useragent import UserAgent
from pyodbc import Connection, connect
from arabic_reshaper import reshape
from os import walk, path
from json import dumps
from datetime import datetime
from traceback import print_exc
from time import sleep


DOMAIN = "pamylka.com/"
H = "https://"
SUBDOMAINS = ["shop."]
SHOPURL = H + SUBDOMAINS[0] + DOMAIN


class InApp:
    ...


class App:
    """The official applications class for any project Assigned to Pamylka\n
    Set by: Ahmed Elbehairy"""

    def __init__(
        self,
        name: str,
        version: str,
        type: str,
        date: str,
        creator: str = __creator__,
        app: str = "app",
        extension: str = "py",
        execute: bool = True,
    ):
        """
        Parameters
        -
        :param str name: The name of the program or application you want to initialize
        :param str version: The version of the application at the moment which have to be edited manually
        :param str type: the type of the application, it usually means what this application do or what type of program is it is, is it a web scraper or a desktop application
        :param str date: The date when the program created
        :param str creator: The creator of the application
        :param str app: the app class of what you are

        Return
        -
        :return: an Application object
        :rtype: App
        """
        self.name = name
        self.version = version
        self.creator = creator
        self.type = type
        self.date = date
        self.app = app

        try:
            file_path = find(f"{self.name}.{extension}")
            with open(file_path, "r", encoding="utf-8") as file:
                pattern = compile("[_ ]{0,2}?version[_ ]{0,2}?")
                file_lines = file.readlines()
                for i in range(len(file_lines)):
                    if pattern.search(file_lines[i]):
                        file_lines[i] = f'__version__ = "{self.version}"\n'
                        with open(file_path, "w", encoding="utf-8") as file:
                            file.writelines(file_lines)
                        if not execute:
                            return
                        with open(f"{file_path}pam", "w", encoding="utf-8") as file:
                            file.writelines(file_lines)
                        return
        except FileNotFoundError:
            return

    def __str__(self) -> str:
        """
        Prety printing the app
        """
        return f"\n\n{self.name} - version: {self.version} - Get from: {SHOPURL}{self.name.lower()}\ntype: {self.type}\n\nCreated by: {self.creator} at {self.date}\n"


class AlphaApp(App):
    def __init__(
        self,
        name: str,
        version: str,
        type: str,
        date: str,
        creator: str = __creator__,
        app: str = "app",
        extension: str = "py",
        execute: bool = True,
    ):
        super().__init__(name, version, type, date, creator, app, extension, execute)
        self.Application = {
            "The Alpha app": {"Name": name, "Apptype": app, "App": self}
        }
        self.count = 1

    def include(self, app: InApp):
        self.Application[len(self.Application)] = {
            "Name": app.name,
            "Apptype": app.app,
            "App": app,
        }

    def printApplication(self) -> dict:
        """Prints the apps included in the application"""

        print("\n\nApplication includes:\n")
        for index in self.Application:
            print(
                f"::: {index} ::: ",
                f"Name: {self.Application[index]['Name']}",
                f"App: {self.Application[index]['Apptype']}\n",
                sep="\n",
            )

        return self.Application

    def printApps(self) -> None:
        """Prints the apps of the application but with the __str__ format"""

        for index in self.Application:
            input(f"Next >>>> {index}")
            print(self.Application[index]["App"])

    def __len__(self) -> int:
        return len(self.Application)


class BaseApp(AlphaApp):
    """The class for the big base application of the project"""

    def __init__(
        self,
        name: str,
        version: str,
        category: str,
        type: str,
        date: str,
        creator: str = __creator__,
        application_nu: int = 1,
        extension: str = "py",
        execute: bool = True,
    ):
        super().__init__(
            name,
            version,
            type,
            date,
            creator,
            extension=extension,
            app="Base App",
            execute=execute,
        )
        """
        Parameters
        -
        :param int application_nu: Just to tell the class how many apps or files are in the project
        :param str category: Mostly indicates the field where the application is used
        
        Return
        -
        :return: The BaseApp object
        :rtype: BaseApp
        """
        self.count = application_nu
        self.category = category

    def __str__(self) -> str:
        return f"\n\n{self.name} - version: {self.version} - Get from: {SHOPURL}{self.name.lower()}\nCategory: {self.category}\ntype: {self.type}\n\nCreated by: {self.creator} at {self.date}\n"


class HeroApp(AlphaApp):
    """The class for the biggest Pamylka apps"""

    def __init__(
        self,
        name: str,
        version: str,
        category: str,
        type: str,
        date: str,
        creator: str = __creator__,
        application_nu: int = 1,
        extension: str = "py",
        execute: bool = True,
    ):
        super().__init__(
            name,
            version,
            type,
            date,
            creator,
            extension=extension,
            app="Hero App",
            execute=execute,
        )
        """
        Parameters
        -
        :param int application_nu: Just to tell the class how many apps or files are in the project
        :param str category: Mostly indicates the field where the application is used
        
        Return
        -
        :return: The HeroApp object
        :rtype: BaseApp
        """
        self.count = application_nu
        self.category = category

    def __str__(self) -> str:
        return f"\n\n{self.name} - version: {self.version} - Get from: {H}{self.name.lower()}.{DOMAIN}\nCategory: {self.category}\ntype: {self.type}\n\nCreated by: {self.creator} at {self.date}\n"


class InApp(App):
    """The class for the apps included in the application"""

    def __init__(
        self,
        name: str,
        ver: str,
        date: str,
        use: str,
        base: BaseApp | HeroApp,
        creator: str = __creator__,
        extension: str = "py",
        execute: bool = True,
    ):
        super().__init__(
            name,
            ver,
            type,
            date,
            creator,
            extension=extension,
            app="Inside App",
            execute=execute,
        )
        """
        Parameters
        -
        :param str use: The use of the mini application or file
        :param int num: What's the index of the application order
        :param str base: What's the parent of this application
        
        Return
        -
        :return: The InApp object
        :rtype: BaseApp
        """
        self.appUse = use
        self.base = base
        base.include(self)
        base.count += 1
        self.appnum = base.count

    def __str__(self) -> str:
        return f"\n\n{self.name} - version: {self.version} - Base app: {self.base.name}\nUsage: {self.appUse}\n\nCreated by: {self.creator} at {self.date}\n"


def db_connect(
    database: str,
    driver: str = "ODBC Driver 17 for SQL Server",
    server: str = "AHMED-ELBEHAIRY",
    trstconn: str = "yes",
) -> Connection:
    """
    Connect to database
    =
    """
    conn = connect(
        f"Driver={driver};"
        f"Server={server};"
        f"Database={database};"
        f"Trusted_Connection={trstconn};"
    )

    crsr = conn.cursor()

    return conn, crsr


def crsrexec(prompt: str, crsr: Connection.cursor) -> None:
    """Execute the querty and commit it right after"""
    crsr.execute(prompt)
    crsr.commit()


def find(name: str, file_path: str = "../") -> str:
    """
    Find the file if it doesn't exist in the first directory
    """

    if path.isfile(file_path):
        return file_path

    for root, dirs, files in walk(file_path):
        if name in files:
            return path.join(root, name)
    raise FileNotFoundError(f"{name} is not found")


def get_key(di: dict, val):
    for key, value in di.items():
        if val == value:
            return key


def aprint(string: str):
    for line in string.splitlines():
        for word in line.split()[::-1]:
            if word.isascii():
                print(word)
                continue
            print(reshape(word), end=" ")
        print()


def driver_setup(
    profile_dir="Default",
    executable_path="C:\Selenium\chromedriver-win64\chromedriver.exe",
    detach=True,
):
    # OPTIONS SETUP
    options = Options()  # Defining options for the driver
    options.add_experimental_option(
        "detach", detach
    )  # Force the browser to stay open even after fininshing
    user_data_dir = r"C:\Users\ideapad\AppData\Local\Google\Chrome Dev\User Data"  # Path for user data
    options.add_argument(
        f"--user-data-dir={user_data_dir}"
    )  # Inputing the user data path for the driver
    options.add_argument(
        f"--profile-directory={profile_dir}"
    )  # Specifing the profile directory
    options.add_argument(f"--user-agent={UserAgent().random}")

    # DRIVER SETUP
    driver = Chrome(
        service=Service(executable_path=executable_path), options=options
    )  # Specifing the driver with the chromedriver path
    driver.implicitly_wait(30)

    return driver


def check_results(function):
    def wrapper(*args, **kwargs):
        while True:
            returned = function(*args, **kwargs)
            print(dumps(list(returned), indent=4))
            match input("Are you happy with the results? y\\n\n").lower():
                case "y":
                    return returned
                case _:
                    continue

    return wrapper


def retry_on_error(function):
    def wrapper(*args, **kwargs):
        for _ in range(10):
            try:
                return function(*args, **kwargs)
            except BaseException:
                print_exc()
                save_log('err.log', f"An error occured at {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}:\n\n")

                with open("err.log", "a") as file:
                    print_exc(file=file)
                    file.write("\n\n\n\n")

                save_log(
                    "funcdata.log",
                    str({"function": function, "args": args, "kwargs": kwargs}),
                )
                print("Taking a break...")
                sleep(1000)
                continue

    return wrapper


def save_log(file_name, text):
    if not path.exists(file_name):
        with open(file_name, "w") as file:
            file.write(text)
            return

    with open(file_name, "a") as file:
        file.write(text)


if __name__ == "__main__":
    pam = AlphaApp(
        "pam",
        "00.03.12",
        "Programming",
        "13/3/1445 Higri",
        app="python module",
        execute=False,
    )
    with open(find("pyproject.toml", "../")) as file:
        toml = file.readlines()

    for i in range(len(toml)):
        if "version" in toml[i]:
            toml[i] = f'version = "{pam.version}"\n'

    with open(find("pyproject.toml", "../"), "w") as file:
        file.writelines(toml)

    print(pam)
