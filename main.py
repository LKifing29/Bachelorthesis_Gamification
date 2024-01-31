# This is a sample Python script.

# Press Umschalt+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.


def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press Strg+F8 to toggle the breakpoint.


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    print_hi('PyCharm')
    print(5 + 5)
    x = 27
    print(x ** 2)
    print("Isn\'t")
    digits = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
    print(digits[-3:])
    print(len(digits))
    # x = int(input("Please enter an integer: "))


    # Create a sample collection
    users = {'Hans': 'active', 'Éléonore': 'inactive', '景太郎': 'active'}

    print(users.items())
    # Strategy:  Iterate over a copy
    for user, status in users.copy().items():
        if status == 'inactive':
            del users[user]

    # Strategy:  Create a new collection
    active_users = {}
    for user, status in users.items():
        if status == 'active':
            active_users[user] = status


# See PyCharm help at https://www.jetbrains.com/help/pycharm/
