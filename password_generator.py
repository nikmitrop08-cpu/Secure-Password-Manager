#how long / uppercase / include numbers / inlcude symbols
import random
while True:
    length = input("Enter the length of the password: ")
    if length.isdigit():
        length = int(length)
        break


uppercase = "ABCDEFGHIJKLMN"
numbers = "0123456789"
lowercase = "abcdefghijklmn"
symbols = "!@#$%^&*()"
password = ""
selection = lowercase

while True:
    uppercase_access = input("Include uppercase letters?(Y/N): ").upper()
    if uppercase_access == "Y":
        selection += uppercase
        break
    elif uppercase_access == "N":
        break
    else:
        continue
while True:
    numbers_access = input("Include numbers?(Y/N): ").upper()
    if numbers_access == "Y":
        selection += numbers
        break
    elif numbers_access == "N":
        break
    else:
        continue
while True:
    symbols_access = input("Include symbols?(Y/N): ").upper()
    if symbols_access == "Y":
        selection += symbols
        break
    elif symbols_access == "N":
        break
    else:
        continue

for i in range(length):
    password += random.choice(selection)

print(password)

