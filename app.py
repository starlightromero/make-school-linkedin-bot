"""Import webdriver and sleep."""
from selenium import webdriver
from time import sleep
from getpass import getpass


class Linkedin:
    """Bot which automakes LinkedIn connections from a Google Sheet."""

    def __init__(self):
        """Initilize Linkedin."""
        self.driver = webdriver.Chrome()

    def signin(self, email, password):
        """Sign into LinkedIn."""
        self.driver.get("https://www.linkedin.com/")
        sleep(2)
        email_input = self.driver.find_element_by_xpath(
            "//*[@id='session_key']"
        )
        email_input.send_keys(email)
        sleep(2)
        password_input = self.driver.find_element_by_xpath(
            "//*[@id='session_password']"
        )
        password_input.send_keys(password)
        sleep(2)
        signin = self.driver.find_element_by_xpath(
            "/html/body/main/section[1]/div[2]/form/button"
        )
        signin.click()

    def connect(self, name, url, conc, count):
        """Access LinkedIn Connection."""
        self.driver.get(url)
        sleep(2)
        try:
            connect_button = self.driver.find_element_by_xpath(
                "//button[contains(@aria-label, 'Connect')]"
            )
            connect_button.click()
            confirm_button = self.driver.find_element_by_xpath(
                "//button[contains(@aria-label, 'Send Now')]"
            )
            connect_button.click()
            print(f"You are now connected with {name}!")
            count += 1
        except:
            print(f"You are already connected with {name}.")
        return count


class Data:
    """Access LinkedIn data."""

    def __init__(self):
        """Initialize Data class."""
        pass

    def read(self):
        with open("data.txt", "r") as file:
            data = [line[:-1] for line in file]
        sorted_data = []
        for d in data:
            sorted_data.append(d.split(","))
        return sorted_data

    def append(self, name, url, conc):
        with open("data.txt", "a") as file:
            data = f"{name},{url},{conc}"
            file.write(data)
            print(f"{name} has been added!")


class Display:
    """User interface methods."""

    @staticmethod
    def greeting():
        """Print a greeting message.."""
        print(
            "{:-^80}\n".format(
                "Welcome to Make School's LinkedIn Connection"
            ).upper()
        )

    @staticmethod
    def get_user_input():
        """Get user input."""
        print(
            "{:-^80}\n".format(
                "I am your LinkedIn connection bot. How can I help you?"
            ).upper()
        )
        print("1: Make connections with the Make School community")
        print("2: Add a profile to share with the Make School community")
        print("q: quit")
        return input("Enter your selection: ")

    @staticmethod
    def filter():
        """Get user's filter preferences."""
        print("ALL | FEW | BEW | MOB | DS | UNDECIDED")
        while True:
            filter = input(
                "Enter who you would like to connect with: "
            ).upper()
            if (
                filter == "ALL"
                or filter == "FEW"
                or filter == "BEW"
                or filter == "MOB"
                or filter == "DS"
                or filter == "UNDECIDED"
            ):
                return filter

    @staticmethod
    def get_email():
        """Get user's LinkedIn email."""
        return input("Enter your LinkedIn email: ")

    @staticmethod
    def get_password():
        """Get user's LinkedIn password."""
        return getpass("Enter your LinkedIn password: ")

    @staticmethod
    def get_name():
        """Get user's name."""
        name = ""
        while not name:
            name = input("Enter your name: ")
        return name

    @staticmethod
    def get_url():
        """Get user's LinkedIn URL."""
        while True:
            url = input("Enter your LinkedIn URL: ")
            if "https://www.linkedin.com/" in url:
                break
            elif "linkedin.com" in url:
                print("Please enter a https secure url.")
            else:
                print("Please enter a valid LinkedIn URL.")
        return url

    @staticmethod
    def get_concentration():
        """Get user's concentration."""
        print("FEW | BEW | MOB | DS | UNDECIDED")
        primary = input("Enter your concentration: ").upper()
        if primary == "UNDECIDED":
            return f"{primary}"
        while True:
            another = input("Do you have a second concentration (y/n)? ")
            if another == "y":
                secondary = input("Enter your second concentration: ")
                return f"{primary}/{secondary}"
            elif another == "n":
                return f"{primary}"

    @staticmethod
    def wait():
        """Print a waiting message."""
        print(
            "\n{:-^80}\n".format(
                "Please wait while your connections are processed"
            ).upper()
        )
        sleep(1)

    @staticmethod
    def farewell():
        """Print for exiting the user interface."""
        print(
            "{:-^80}\n".format(
                "Thank you for choosing me as your connection bot."
            ).upper()
        )

    def ui(self):
        """Process user input."""
        self.greeting()
        while True:
            user_input = self.get_user_input()
            if user_input == "1":
                filter = self.filter()
                email = self.get_email()
                password = self.get_password()
                self.wait()
                bot = Linkedin()
                bot.signin(email, password)
                data = Data()
                sorted_data = data.read()
                count = 0
                for name, url, conc in sorted_data:
                    if filter == "ALL":
                        count = bot.connect(name, url, conc, count)
                    if filter in conc:
                        count = bot.connect(name, url, conc, count)
                print(
                    "\n{:-^80}\n".format(
                        f"You have made {count} new connections!"
                    ).upper()
                )
            if user_input == "2":
                name = self.get_name()
                url = self.get_url()
                conc = self.get_concentration()
                data = Data()
                data.append(name, url, conc)
            if user_input == "q":
                break
        self.farewell()


display = Display()
display.ui()
