import os.path
import getpass
import random
import math

#  Formula to wrap around (((char - 33) % 94) + 33)
File_Name = "Info.txt"  # Name of the file with the user information to save to
USERS = {}
split_value = "~,!"


class Encryption:
    def __init__(self, unencrypted=["", ""], encrypted=["", ""], formula=[]):
        self.unencrypted = unencrypted
        self.encrypted = encrypted
        self.formula = formula

    def create(self, info):
        temp = info.replace(" ", "")
        temp = temp.split(split_value)
        self.encrypted[0] = temp[0]
        self.encrypted[1] = temp[1]
        temp.pop(0)
        temp.pop(0)
        self.make_formula(temp)
        self.decrypt()

    def encrypt(self):
        self.encrypted = ["", ""]
        for i in range(len(self.unencrypted)):
            word = self.unencrypted[i]
            temp = ""
            position = 1
            for letter in range(len(word)):
                shift = self.calculate(position)
                out = ord(word[letter]) + shift
                out = (((out - 33) % 94) + 33)
                temp += chr(int(out))
                position += 1
            self.encrypted[i] = temp
            # print()

    def decrypt(self):
        self.unencrypted = ["", ""]
        for i in range(len(self.encrypted)):
            word = self.encrypted[i]
            temp = ""
            position = 1
            for letter in range(len(word)):
                # print(position, ":", word[letter])
                shift = self.calculate(position)
                out = ord(word[letter]) - shift
                out = (((out - 33) % 94) + 33)
                temp += chr(int(out))
                position += 1
            self.unencrypted[i] = temp
            # print()

    def validate(self):
        temp_unencrypted = ["", ""]
        for i in range(len(self.encrypted)):
            word = self.encrypted[i]
            temp = ""
            position = 1
            for letter in range(len(word)):
                shift = self.calculate(position)
                out = ord(word[letter]) - shift
                out = (((out - 33) % 94) + 33)
                temp += chr(int(out))
                position += 1
            temp_unencrypted[i] = temp
        return self.unencrypted[0] == temp_unencrypted[0] and self.unencrypted[1] == temp_unencrypted[1]

    def calculate(self, index):
        out = index
        for power in range(len(self.formula)):
            out = self.formula[power] * math.pow(index, power)
        return out

    def make_formula(self, inputs):
        self.formula = []
        for i in range(len(inputs)):
            self.formula.append(int(inputs[i]))

    def get_username(self) -> str:
        return self.unencrypted[0]

    def get_password(self) -> str:
        return self.unencrypted[1]

    def toString(self) -> str:
        form = ""
        for i in range(len(self.formula)):
            form += split_value + str(self.formula[i])
        return self.encrypted[0] + split_value + self.encrypted[1] + form

    def __str__(self):
        return "{["+self.unencrypted[0]+", "+self.unencrypted[1] +\
               "], ["+self.encrypted[0]+", "+self.encrypted[1]+"], " +\
               self.formula.__str__()+"}"

    def __repr__(self):
        return "{["+self.unencrypted[0]+", "+self.unencrypted[1] +\
               "], ["+self.encrypted[0]+", "+self.encrypted[1]+"], " +\
               self.formula.__str__()+"}"


def scan_file(filename):
    if os.path.exists(filename):
        with open(filename, 'r') as f:
            user_data = f.read()
            user_data = user_data.split('\n')
            global split_value
            split_value = user_data[0]
            for line in range(1, len(user_data)):
                if user_data[line] != "" and user_data[line] != split_value:
                    temp = Encryption()
                    temp.create(user_data[line])
                    USERS[temp.get_username()] = temp


def load_file(filename):
    temp_users = {}
    if os.path.exists(filename):
        with open(filename, 'r') as f:
            user_data = f.read()
            user_data = user_data.split('\n')
            global split_value
            split_value = user_data[0]
            for line in range(1, len(user_data)):
                if user_data[line] != "" and user_data[line] != split_value:
                    temp = Encryption()
                    temp.create(user_data[line])
                    temp_users[temp.get_username()] = temp
    return temp_users


def save_file(filename):
    global split_value
    split_value = ""
    for i in range(3):
        split_value += chr(random.randint(33, 127))

    output = ""
    output += split_value + "\n"
    print_users()
    for key, user in USERS.items():
        print(user.toString())
        output += user.toString()+"\n"
    # print(output)
    with open(filename, 'w') as f:
        f.write(output)


def print_users():
    print("Current User file:")
    for x, y in USERS.items():
        print(x, ":", y.formula)
    print()


def main():
    scan_file(File_Name)
    print_users()

    change = False
    option = ""
    while option != "quit":
        option = input("Do you want to add a new entry, remove an existing one, or update the encryption of an entry?"
                       " (\'add\', \'remove\', \'update\', or \'quit\'):\n").lower()
        while option != 'add' and option != 'remove' and option != 'update' and option != 'quit':
            option = input("Please enter \'add\', \'remove\', \'update\', or \'quit\': ").lower()

        if option == "add":
            user = input('Enter your username: ')
            while user in USERS:
                user = input('That username is taken, please enter another: ')
            psk = getpass.getpass('Enter your password: ')
            psk2 = getpass.getpass('Confirm password:')

            while psk != psk2:
                print("The passwords entered didn't match. Please try again...")
                psk = getpass.getpass('Enter your password: :')
                psk2 = getpass.getpass('Confirm password:')

            valid = False
            while not valid:
                crypt = input('Do you want a custom encryption or random? (\'custom\' or \'random\'): ').lower()
                while crypt != 'custom' and crypt != 'random':
                    crypt = input('Please enter \'custom\' or \'random\': ').lower()

                if crypt == "custom":
                    inputs = []
                    power = int(input("What is the highest exponent you want? (x^#): "))
                    for i in range(power + 1):
                        temp = input("What is the coefficient to x^"+str(i)+": ")
                        inputs.append(temp)
                    new_user = Encryption([user, psk])
                    new_user.make_formula(inputs)
                    new_user.encrypt()
                    valid = new_user.validate()
                    if valid:
                        USERS[new_user.get_username()] = new_user

                if crypt == "random":
                    inputs = []
                    power = int(input("What is the highest exponent you want? (x^#): "))
                    for i in range(power + 1):
                        temp = str(random.randint(-255, 255))
                        inputs.append(temp)
                    new_user = Encryption([user, psk])
                    new_user.make_formula(inputs)
                    new_user.encrypt()
                    valid = new_user.validate()
                    if valid:
                        USERS[new_user.get_username()] = new_user

                if not valid:
                    print("The encryption has failed, please try again...")

        if option == "remove":
            user = input('Enter the username to remove: ')
            if USERS.get(user) is not None:
                USERS.pop(user)

        if option == "update":
            user = input('Enter the username to update: ')
            if USERS.get(user) is not None:
                temp_user = USERS[user]
                inputs = []

                valid = False
                while not valid:
                    crypt = input('Do you want a custom encryption or random? (\'custom\' or \'random\'): ').lower()
                    while crypt != 'custom' and crypt != 'random':
                        crypt = input('Please enter \'custom\' or \'random\': ').lower()

                    if crypt == "custom":
                        power = int(input("What is the highest exponent you want? (x^#): "))
                        for i in range(power + 1):
                            temp = input("What is the coefficient to x^"+str(i)+": ")
                            inputs.append(temp)

                            temp_user.make_formula(inputs)
                            temp_user.encrypt()
                            valid = temp_user.validate()

                    if crypt == "random":
                        power = int(input("What is the highest exponent you want? (x^#): "))
                        # added the loop to the random if statement, need to implement the loop
                        loop_count = 0
                        while not valid and loop_count < 5:
                            for i in range(power + 1):
                                temp = str(random.randint(-255, 255))
                                inputs.append(temp)

                                temp_user.make_formula(inputs)
                                temp_user.encrypt()
                                valid = temp_user.validate()

                    if valid:
                        USERS[user] = temp_user
                    else:
                        print("The encryption has failed, please try again...")
            else:
                print("That username doesn't exist...")

        if option != "quit":
            change = True
            print_users()
    if change:
        save_file(File_Name)


if __name__ == '__main__':
    main()
