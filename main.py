from tkinter import *
from tkinter import messagebox
import random
import pyperclip
import json

BACKGROUND_COLOR = "#FFFFFF"


# Password generator
def generate_password():
    letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u',
               'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P',
               'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']

    password_list = []

    [password_list.append(random.choice(letters)) for _ in range(random.randint(8, 10))]
    [password_list.append(random.choice(symbols)) for _ in range(random.randint(2, 4))]
    [password_list.append(random.choice(numbers)) for _ in range(random.randint(2, 4))]

    random.shuffle(password_list)
    final_password = "".join(password_list)
    password_entry.delete(0, END)
    password_entry.insert(0, final_password)
    pyperclip.copy(final_password)


# Save data (website, username and password into a file) into a txt file
def save():
    website = website_entry.get()
    username = username_entry.get()
    password = password_entry.get()
    data_pass = {
        website: {
            "username": username,
            "password": password
        }
    }

    if len(website) == 0 or len(password) == 0:
        messagebox.showinfo(title="Attention!", message="Please don't leave any fields empty!")
    else:
        try:
            with open("data.json", mode="r") as data_file:
                # Reading old data
                data = json.load(data_file)
        except FileNotFoundError:
            with open("data.json", mode="w") as data_file:
                # Write new data in json file
                json.dump(data_pass, data_file, indent=4)
        else:
            # Update old data with new data
            data.update(data_pass)
            with open("data.json", mode="w") as data_file:
                # Write new data in json file
                json.dump(data, data_file, indent=4)
        finally:
            website_entry.delete(0, END)
            password_entry.delete(0, END)


# Try to find the password that the user entered
def find_password():
    website = website_entry.get()
    try:
        with open("data.json", mode="r") as data_file:
            data = json.load(data_file)
    except FileNotFoundError:
        # File not found message pop-up
        messagebox.showerror(title="Error", message="Sorry, data file not found.")
    else:
        try:
            username_found = data[website]["username"]
            password_found = data[website]["password"]
        except KeyError:
            # Website not found message pop-up
            messagebox.showerror(title="Error", message="Sorry, website not found.")
        else:
            # Username with password message pop-up
            messagebox.showinfo(title="Website info", message=f"Username: {username_found}\n"
                                                              f"Password: {password_found}")


# Window settings
window = Tk()
window.title("Password manager")
window.config(padx=50, pady=50, bg=BACKGROUND_COLOR)

# Canvas and image
padlock_img = PhotoImage(file="logo.png")
canvas = Canvas(width=200, height=200, highlightthickness=0, bg=BACKGROUND_COLOR)
canvas.create_image(100, 100, image=padlock_img)
canvas.grid(row=0, column=1)

# Labels, entries and buttons
website_label = Label(text="Website:", bg=BACKGROUND_COLOR)
website_label.grid(row=1, column=0)
website_entry = Entry()
website_entry.focus()
website_entry.grid(row=1, column=1, columnspan=1, sticky='EW')
search = Button(text="Search", command=find_password)
search.grid(row=1, column=2, sticky='EW')

username_label = Label(text="Email/Username:", bg=BACKGROUND_COLOR)
username_label.grid(row=2, column=0)
username_entry = Entry()
username_entry.insert(0, "name@email.com")
username_entry.grid(row=2, column=1, columnspan=2, sticky='EW')

password_label = Label(text="Password:", bg=BACKGROUND_COLOR)
password_label.grid(row=3, column=0)
password_entry = Entry()
password_entry.grid(row=3, column=1, sticky='EW')
generate_pass = Button(text="Generate Password", command=generate_password)
generate_pass.grid(row=3, column=2, sticky='EW')

add = Button(text="Add", command=save)
add.grid(row=4, column=1, columnspan=2, sticky='EW')

window.mainloop()
