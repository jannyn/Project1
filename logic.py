from PyQt6.QtWidgets import *
from gui import *
import csv


class Logic(QMainWindow, Ui_MainWindow):
    def __init__(self) -> None:
        """
        method for the ATM/bank
        """
        super().__init__()
        self.setupUi(self)
        self.special_characters = "~`!@#$%^&*()_+={[}]| :;" + "'" + '"' + '<,>.?' + "\\" + "/"

        self.stackedWidget.setCurrentWidget(self.screen_login)
        self.label_value_handling.clear()
        self.button_login.clicked.connect(lambda: self.login())
        self.button_create_account.clicked.connect(lambda: self.create_account_page())
        self.button_confirm_account.clicked.connect(lambda: self.create_account())
        self.button_back.clicked.connect(lambda: self.login_page())
        self.button_logout.clicked.connect(lambda: self.login_page())
        self.button_confirm_amount.clicked.connect(lambda: self.confirm_amount())
        self.button_clear.clicked.connect(lambda: self.clear_atm())

    def login(self) -> None:
        """
        method that checks for valid/invalid logins
        """
        try:
            self.label_value_handling.clear()
            self.clear_atm()
            self.first_name = self.input_first_name.text().strip()
            self.last_name = self.input_last_name.text().strip()
            self.password = self.input_password.text().strip()

            self.account_details = [self.first_name, self.last_name, self.password]

            for item in self.account_details:
                if item == '':
                    raise TypeError('Please make sure to fill out all inputs.')

            with open('accounts.csv', 'r') as csv_file:
                csv_reader = csv.reader(csv_file)
                for line in csv_reader:
                    if line == self.account_details:
                        self.atm_page()
                        self.input_first_name.clear()
                        self.input_last_name.clear()
                        self.input_password.clear()
                        self.label_login_handling.clear()
                        raise ValueError('')

                raise ValueError('Account was not found. Try creating an account or re-entering details.')

        except TypeError as e:
            self.label_login_handling.setText(f'{e}')
        except ValueError as e:
            self.label_login_handling.setText(f'{e}')
            self.input_first_name.clear()
            self.input_last_name.clear()
            self.input_password.clear()
        except FileNotFoundError:
            self.label_login_handling.setText('Account was not found. Try creating an account or re-entering details.')
            self.input_first_name.clear()
            self.input_last_name.clear()
            self.input_password.clear()

    def create_account(self) -> None:
        """
        method that deals with valid and invalid account creations
        """
        try:
            self.first_name = self.input_first_name_create.text().strip()
            self.last_name = self.input_last_name_create.text().strip()
            self.password = self.input_password_create.text().strip()
            self.confirm_password = self.input_password_create_2.text().strip()

            self.account_details = [self.first_name, self.last_name, self.password, self.confirm_password]

            for item in self.account_details:
                if item == '':
                    raise ValueError('Please make sure to fill out all inputs.')

            for char in self.account_details[0]:
                for special_char in self.special_characters:
                    if char.isdigit() or char == special_char:
                        raise TypeError('Please do not include numbers or special characters for the first name.'
                                        + f' Special characters include: {self.special_characters} and space characters')

            for char in self.account_details[1]:
                for special_char in self.special_characters:
                    if char.isdigit() or char == special_char:
                        raise TypeError('Please do not include numbers or special characters for the last name.'
                                        + f' Special characters include: {self.special_characters} and space characters')

            for char in self.account_details[2]:
                if char.isspace():
                    raise TypeError('Please do not include spaces in your password, special characters are allowed.')

            if len(self.account_details[2]) < 8:
                raise ValueError('Please make a password that is 8 or more characters long.')

            if self.account_details[2] != self.account_details[3]:
                raise ValueError('Please make sure that the password inputs match.')

            self.account_details = self.account_details[:3]

            self.input_first_name_create.clear()
            self.input_last_name_create.clear()
            self.input_password_create.clear()
            self.input_password_create_2.clear()
            self.label_confirm_output.clear()

            with open('accounts.csv', 'a+', newline='') as csv_file:
                csv_file.seek(0)
                csv_reader = csv.reader(csv_file)
                for line in csv_reader:
                    if line == self.account_details:
                        raise ValueError('An account has already been made with these details.')
                csv_writer = csv.writer(csv_file)
                csv_writer.writerow(self.account_details)


            with open(f'{self.first_name}_{self.last_name}.csv', 'w', newline='') as csv_balance_file:
                csv_writer = csv.writer(csv_balance_file)
                csv_writer.writerow(['1', 'deposited', '0'])

            self.stackedWidget.setCurrentWidget(self.screen_login)

        except ValueError as e:
            self.label_confirm_output.setText(f'{e}')
        except TypeError as e:
            self.label_confirm_output.setText(f'{e}')

    def confirm_amount(self) -> None:
        """
        method that confirms the withdrawal and deposit amount, also deals with invalid data
        """
        try:
            self.amount = self.input_amount.text().strip()
            self.amount = float(self.amount)
            if self.amount <= 0:
                raise ValueError
            if self.radioButton_deposit.isChecked() or self.radioButton_withdraw.isChecked():
                if self.radioButton_deposit.isChecked():
                    self.deposit(self.amount)
                else:
                    self.withdraw(self.amount)
        except ValueError:
            self.label_value_handling.setText('Entry must be numeric (e.g. 10.25 not $10.25) and not less than 0.')
        except TypeError as e:
            self.label_value_handling.setText(f'{e}')


    def login_page(self) -> None:
        """
        method that changes the screen to the login page
        """
        self.stackedWidget.setCurrentWidget(self.screen_login)

    def create_account_page(self) -> None:
        """
        method that changes the screen to the create account page
        """
        self.stackedWidget.setCurrentWidget(self.screen_create_account)

    def get_total_balance(self) -> float:
        """
        method that sums up all the withdrawals and deposits
        :return: the overall account balance
        """
        self.total_balance = 0
        with open(f'{self.first_name}_{self.last_name}.csv', 'r') as csv_balance_file:
            csv_reader = csv.reader(csv_balance_file)
            for line in csv_reader:
                amount = float(line[2])
                self.total_balance += amount
        return self.total_balance

    def deposit(self, amount) -> None:
        """
        method that writes the deposited amount to a csv file and refreshes the ATM page
        :param amount: how much money that is being put into the deposit
        """
        with open(f'{self.first_name}_{self.last_name}.csv', 'a+', newline='') as csv_balance_file:
            csv_writer = csv.writer(csv_balance_file)
            amount = str(amount)
            csv_writer.writerow([str(self.modify_modification_number()), 'deposited', amount])
        self.atm_page()

    def withdraw(self, amount) -> None:
        """
        method that checks for invalid withdrawals and writes it to a csv file and refreshes the ATM page
        :param amount: how much money is within the withdrawal
        """
        if amount > self.get_total_balance():
            raise TypeError('Cannot withdraw more than account balance.')
        else:
            with open(f'{self.first_name}_{self.last_name}.csv', 'a+', newline='') as csv_balance_file:
                csv_writer = csv.writer(csv_balance_file)
                amount = '-' + str(amount)
                csv_writer.writerow([str(self.modify_modification_number()), 'withdrew', amount])
        self.atm_page()

    def modify_modification_number(self) -> int:
        """
        method that records how many deposits/withdrawals have been made
        :return: returns the most recent number of modifications
        """
        self.modification_number = 1
        with open(f'{self.first_name}_{self.last_name}.csv', 'r') as csv_balance_file:
            csv_reader = csv.reader(csv_balance_file)
            for line in csv_reader:
                modification_number = int(line[0])
            self.modification_number += modification_number
        return self.modification_number

    def atm_page(self) -> None:
        """
        method that reads from the csv file to update the account history
        """
        self.label_welcome.setText(f'Welcome, {self.first_name}')
        self.account_history = ''
        with open(f'{self.first_name}_{self.last_name}.csv', 'a+') as csv_balance_file:
            csv_balance_file.seek(0)
            csv_reader = csv.reader(csv_balance_file)
            for line in csv_reader:
                modification_number = int(line[0])
                modification = line[1]
                amount = float(line[2])
                self.account_history += f'modification #{modification_number}: {modification} ${abs(amount):.2f}' + '\n'
                self.label_history.setText(f'{self.account_history}')
                self.label_balance.setText(f'${self.get_total_balance():.2f}')

        self.stackedWidget.setCurrentWidget(self.screen_ATM)

    def clear_atm(self) -> None:
        """
        method that clears all radio buttons
        """
        self.buttonGroup.setExclusive(False)
        self.radioButton_withdraw.setChecked(False)
        self.radioButton_deposit.setChecked(False)
        self.buttonGroup.setExclusive(True)
        self.input_amount.clear()
        self.label_value_handling.clear()