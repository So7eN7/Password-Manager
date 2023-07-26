from tkinter import *
from tkinter import messagebox
import string
import random
import json

# Simple password generator


def password_generator():
    # From string module we set our letters/numbers/symbols
    letters = string.ascii_letters
    numbers = string.digits
    symbols = string.punctuation
    # List comprehension really helps us here. We fill our lists here
    password_letters = [random.choice(letters) for i in range(random.randint(8, 10))]
    password_numbers = [random.choice(numbers) for i in range(random.randint(2, 4))]
    password_symbols = [random.choice(symbols) for i in range(random.randint(2, 4))]
    # Combining our lists and shuffling them
    password_list = password_letters + password_numbers + password_symbols
    random.shuffle(password_list)
    # Make a string and put it inside the password box
    password = "".join(password_list)
    password_entry.insert(0, password)

# Saving the data that's entered


def save_password_data():
    # Getting what's entered
    website = website_entry.get()
    email = email_entry.get()
    password = password_entry.get()
    new_data = {
        website: {
            "email": email,
            "password": password,
        }
    }

    # Making sure that no fields are empty. If empty show the messagebox
    if len(website) == 0 or len(email) == 0 or len(password) == 0:
        messagebox.showinfo(title="Error", message="Please make sure to not leave any empty fields.")
    else:
        try: # If the json file doesn't exist we need to create it
             with open("Password_Data.json", "r") as data_file:
                # Reading old data
                data = json.load(data_file)
        except FileNotFoundError: # Creating the json file
            with open("Password_Data.json", "w") as data_file:
                json.dump(new_data, data_file, indent=4)
        else: # Updating the json file
            data.update(new_data)
            with open("Password_Data.json", "w") as data_file:
                # Saving updated data
                json.dump(data, data_file, indent=4)

# Search button function, finding passwords related to the website you're looking for


def search_password():
    website = website_entry.get()
    try: # Loading the data
        with open("Password_Data.json") as data_file:
            data = json.load(data_file)
    except FileNotFoundError: # Some basic error checking
        messagebox.showinfo(title="Error", message="No data file found")
    else: # Finding data if it's available
        if website in data:
            email = data[website]["email"]
            password = data[website]["password"]
            messagebox.showinfo(title=website, message=f"Email: {email}\n Password: {password}\n")
        else:
            messagebox.showinfo(title="Error", message=f"No details for {website} exists.")

# GUI/main


window = Tk()
window.title("Password Manager")
window.config(padx=50, pady=50)
# Setting the icon and the logo
canvas = Canvas(height=400, width=400)
logo_image = PhotoImage(file="icon.png")
canvas.create_image(200, 200, image=logo_image)
canvas.grid(row=0, column=1)
window.iconphoto(False, logo_image)
# Text labels
website_label = Label(text="Website:")
website_label.grid(row=1, column=0)
email_label = Label(text="Email/Username:")
email_label.grid(row=2, column=0)
password_label = Label(text="Password:")
password_label.grid(row=3, column=0)
# Text fields
website_entry = Entry(width=35)
website_entry.grid(row=1, column=1, columnspan=2)
website_entry.focus()
email_entry = Entry(width=35)
email_entry.grid(row=2, column=1, columnspan=2)
# email_entry.insert(0, "example@mail.com")
password_entry = Entry(width=35)
password_entry.grid(row=3, column=1, columnspan=2)
# Buttons
search_button = Button(text="Search", width=15, command=search_password)
search_button.grid(row=1, column=2)
generate_password = Button(text="Generate Password", command=password_generator)
generate_password.grid(row=3, column=2)
add_button = Button(text="Add", width=30, command=save_password_data)
add_button.grid(row=4, column=1, columnspan=2)

window.mainloop()