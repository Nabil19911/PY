from tkinter import *
from tkinter import messagebox
import datetime
import sqlite3

date = datetime.date.today()
window = Tk()
window.geometry("600x700")
window.resizable(width=False, height=False)
window.title("Night Vision Credit list V0.1")
window.iconbitmap("ICON/SC.ico")


# ENTRY (USER INPUT)
user_input = Entry(window, width=23, font=10)
password = Entry(window, show="*", width=23)

# LISTBOX
left_list_box = Listbox(window, width=40, height=41)
right_search_list = Listbox(window, width=40)
right_list_box = Listbox(window, width=40, height=10)
right_list_bank = Listbox(window, width=40, height=5)

# LABEL
available_credit_text = Label(window, text="CREDIT").place(x=405, y=125)
complete_date = Label(window, text=date).place(x=400, y=325)

# MAIN DATABASE
with sqlite3.connect("Store/DataBase/Main.db") as main_db:
    main_cursor = main_db.cursor()

main_cursor.execute("""CREATE TABLE IF NOT EXISTS customer(ID INTEGER PRIMARY KEY, date VARCHAR(20) NOT NULL, username 
VARCHAR(20) NOT NULL, symbol VARCHAR(1) NOT NULL, amount VARCHAR(20) NOT NULL);""")

# DAILY DATABASE
with sqlite3.connect(f"Store/DailyBase/{date}.db") as user_db:
    user_cursor = user_db.cursor()

user_cursor.execute("""CREATE TABLE IF NOT EXISTS users(ID INTEGER PRIMARY KEY, username VARCHAR(20) NOT NULL, 
symbol VARCHAR(1) NOT NULL, amount VARCHAR(20) NOT NULL);""")

# BANK DATABASE
with sqlite3.connect(f"Store/BankBase/bank_({date}).db") as bank_db:
    bank_cursor = bank_db.cursor()

bank_cursor.execute("""CREATE TABLE IF NOT EXISTS bank_users(ID INTEGER PRIMARY KEY, username 
VARCHAR(20) NOT NULL, symbol VARCHAR(1) NOT NULL, amount VARCHAR(20) NOT NULL);""")


# FUNCTIONS
def check_tuple(username):
    if type(username) is tuple:
        return " ".join(username)
    else:
        return username


# Center WINDOW
def center(win):
    win.update_idletasks()
    width = win.winfo_width()
    height = win.winfo_height()
    x = (win.winfo_screenwidth() // 2) - (width // 2)
    y = (win.winfo_screenheight() // 2) - (height // 2)
    win.geometry('{}x{}+{}+{}'.format(width, height, x, y))


# DATABASE ENTRY FUNCTION
def check_user(name, symbol, amount):
    found = 0

    while found == 0:
        with sqlite3.connect(f"Store/DailyBase/{date}.db") as database:
            cur = database.cursor()
            find_user = "SELECT * FROM users WHERE username = ?"
            cur.execute(find_user, [(name)])
        if cur.fetchall():
            update = "UPDATE users SET amount = (?) WHERE username = (?)"
            val = (amount, name)
            cur.execute(update, val)
            database.commit()
            break
        else:
            inserting = """INSERT INTO users(username, symbol, amount) VALUES(?,?,?)"""
            cur.execute(inserting, [name, symbol, amount])
            database.commit()
            found = 1


# MAIN USER DATABASE ENTRY FUNCTION
def main_user_name(day, name, symbol, amount):
    found = 0

    while found == 0:
        with sqlite3.connect(f"Store/DataBase/Main.db") as database:
            cur = database.cursor()
            find_user = "SELECT * FROM customer WHERE username = ?"
            cur.execute(find_user, [(name)])
        if cur.fetchall():
            update = "UPDATE customer SET date = (?), amount = (?) WHERE username = (?)"
            val = (day, amount, name)
            cur.execute(update, val)
            database.commit()
            break
        else:
            inserting = """INSERT INTO customer(date, username, symbol, amount) VALUES(?,?,?,?)"""
            cur.execute(inserting, [day, name, symbol, amount])
            database.commit()
            found = 1


# BANK USER DATABASE ENTRY FUNCTION
def banked(name, symbol, amount):
    found = 0

    while found == 0:
        with sqlite3.connect(f"Store/BankBase/bank_({date}).db") as database:
            cur = database.cursor()
            find_user = "SELECT * FROM bank_users WHERE username = ?"
            cur.execute(find_user, [(name)])
        if cur.fetchall():
            update = "UPDATE bank_users SET amount = (?) WHERE username = (?)"
            val = (amount, name)
            cur.execute(update, val)
            database.commit()
            break
        else:
            inserting = """INSERT INTO bank_users(username, symbol, amount) VALUES(?,?,?)"""
            cur.execute(inserting, [name, symbol, amount])
            database.commit()
            found = 1


# FUNCTIONS OF BUTTONS
def remove():
    # REMOVE AND DELETE ITEM FROM RIGHT LISTBOX
    items = map(int, right_list_box.curselection())
    for item in items:

        get_user = right_list_box.get(item)
        user = check_tuple(get_user)
        get_name = user.split(" ")[0]

        delete_user = "DELETE FROM users WHERE username =?"
        user_cursor.execute(delete_user, [(get_name)])
        user_db.commit()
        right_list_box.delete(item)

    # REMOVE ITEM FROM SEARCH BOX
    items = map(int, right_search_list.curselection())
    for item in items:
        right_search_list.delete(item)

    # REMOVE AND DELETE ITEM FROM LEFT LISTBOX
    items = map(int, left_list_box.curselection())
    for item in items:
        user_password = password.get()
        password_number = "0756061316"
        if user_password != password_number:
            messagebox.showwarning("Warning", "Enter the password to add to database")
            password.delete(0, END)
        else:
            get_user = left_list_box.get(item)
            user = check_tuple(get_user)
            get_name = user.split(" ")[1]

            # print(get_name)
            delete_user = "DELETE FROM customer WHERE username =?"
            main_cursor.execute(delete_user, [(get_name)])
            main_db.commit()
            left_list_box.delete(item)


def search():
    # Getter
    left_list = left_list_box.get(0, END)
    right_search = right_search_list.get(0, END)
    user_entry = user_input.get()
    right_user = right_list_box.get(0, END)

    for user in left_list:
        name = check_tuple(user)
        user_name1 = name.split(" ")[1]

        if len(right_search) == 0:
            if user_name1 == user_entry.upper():
                right_search_list.insert(END, user)
        else:
            for users in right_search:
                name_user_in = check_tuple(users)
                users_name = name_user_in.split(" ")[1]
                if user_name1 != users_name:
                    if user_name1 == user_entry.upper():
                        right_search_list.insert(END, user)
                        break
                    break

    for name in right_user:
        user = check_tuple(name)
        get_user_name = user.split(" ")[0]
        if user_entry.upper() == get_user_name:
            right_list_box.selection_set(right_user.index(name))


def add():
    search()
    user_entry = user_input.get().upper()  # users input getter

    if user_entry == "":
        messagebox.showwarning("Warning", "Enter users name")  # If Empty
    elif user_entry.find(" ") > 0:
        messagebox.showwarning("Warning", "Enter name without space")  # If space
    else:
        right_list = right_list_box.get(0, END)
        user_input.delete(0, END)
        user_input.select_clear()

        # TOP LEVEL WINDOWS
        top = Toplevel(window, relief=RAISED)
        top.title("USER CASH")
        top.geometry("250x150")
        top.resizable(width=False, height=False)
        top.iconbitmap("ICON/SC.ico")
        top.grab_set()  # Disable The Parent Windows
        center(top)

        # WIDGETS
        user_name_in = Label(top, text=user_entry)
        user_amount1 = Spinbox(top, width=5, justify=CENTER, from_=1, to=10000)

        def paid():

            # GETTERS
            amount = user_amount1.get()
            if len(right_list) == 0:

                paid_amount = f"({amount})"
                sym = "="
                user_output = f"{user_entry}" + " = " + paid_amount

                right_list_box.insert(END, user_output)

                # DATABASE ENTRY
                check_user(user_entry, sym, paid_amount)

                top.destroy()
            else:
                for users in right_list:

                    user = check_tuple(users)
                    # print("1: ", user)
                    if user.split(" ")[0] == user_entry:

                        if user.split(" ")[2].find("(") == 0:
                            num = user.split(" ")[2].strip("(").strip(")")
                            answer = int(num) + int(amount)

                            paid_amount = f"({answer})"
                            sym = "="
                            new_str = f"{user_entry}" + " = " + paid_amount

                            right_list_box.activate(int(right_list.index(users)))
                            right_list_box.delete(ACTIVE)

                            right_list_box.insert(END, new_str)

                            # DATABASE ENTRY
                            check_user(user_entry, sym, paid_amount)

                            top.destroy()
                        else:
                            num = user.split(" ")[2]
                            answer = int(num) - int(amount)
                            if answer == 0:
                                # DATABASE
                                paid_amount = f"{answer}"
                                sym = "="

                                check_user(user_entry, sym, paid_amount)

                                delete_user = "DELETE FROM users WHERE amount = 0"
                                user_cursor.execute(delete_user)
                                user_db.commit()

                                right_list_box.activate(int(right_list.index(users)))
                                right_list_box.delete(ACTIVE)

                                top.destroy()

                            elif answer < 0:
                                paid_amount = f"({-answer})"
                                sym = "="
                                new_str = f"{user_entry}" + " = " + paid_amount

                                right_list_box.activate(int(right_list.index(users)))
                                right_list_box.delete(ACTIVE)

                                right_list_box.insert(END, new_str)

                                # DATABASE ENTRY
                                check_user(user_entry, sym, paid_amount)

                                top.destroy()
                            else:
                                paid_amount = f"{answer}"
                                sym = "="
                                new_str = f"{user_entry}" + " = " + paid_amount

                                right_list_box.activate(int(right_list.index(users)))
                                right_list_box.delete(ACTIVE)

                                right_list_box.insert(END, new_str)

                                # DATABASE ENTRY
                                check_user(user_entry, sym, paid_amount)

                                top.destroy()

                        break

                else:
                    paid_amount = f"({amount})"
                    sym = "="
                    user_output = f"{user_entry}" + " = " + paid_amount

                    right_list_box.insert(END, user_output)

                    # DATABASE ENTRY
                    check_user(user_entry, sym, paid_amount)

                    top.destroy()

        def not_paid():

            # GETTERS
            amount = user_amount1.get()
            if len(right_list) == 0:

                paid_amount = f"{amount}"
                sym = "="
                user_output = f"{user_entry}" + " = " + paid_amount

                right_list_box.insert(END, user_output)

                # DATABASE ENTRY
                check_user(user_entry, sym, paid_amount)

                top.destroy()
            else:
                for users in right_list:

                    user = check_tuple(users)

                    if user.split(" ")[0] == user_entry:

                        if user.split(" ")[2].find("(") == 0:
                            num = user.split(" ")[2].strip("(").strip(")")
                            answer = int(num) - int(amount)
                            if answer == 0:

                                # DATABASE
                                paid_amount = f"{answer}"
                                sym = "="

                                check_user(user_entry, sym, paid_amount)

                                delete_user = "DELETE FROM users WHERE amount = 0"
                                user_cursor.execute(delete_user)
                                user_db.commit()

                                right_list_box.activate(int(right_list.index(users)))
                                right_list_box.delete(ACTIVE)
                                top.destroy()

                            elif answer < 0:
                                paid_amount = f"{-answer}"
                                sym = "="
                                new_str = f"{user_entry}" + " = " + paid_amount

                                right_list_box.activate(int(right_list.index(users)))
                                right_list_box.delete(ACTIVE)

                                right_list_box.insert(END, new_str)

                                # DATABASE ENTRY
                                check_user(user_entry, sym, paid_amount)

                                top.destroy()
                            else:
                                paid_amount = f"({answer})"
                                sym = "="
                                new_str = f"{user_entry}" + " = " + paid_amount

                                right_list_box.activate(int(right_list.index(users)))
                                right_list_box.delete(ACTIVE)

                                right_list_box.insert(END, new_str)

                                # DATABASE ENTRY
                                check_user(user_entry, sym, paid_amount)

                                top.destroy()
                        else:
                            num = user.split(" ")[2].strip("(").strip(")")
                            answer = int(num) + int(amount)

                            paid_amount = f"{answer}"
                            sym = "="
                            new_str = f"{user_entry}" + " = " + paid_amount

                            right_list_box.activate(int(right_list.index(users)))
                            right_list_box.delete(ACTIVE)

                            right_list_box.insert(END, new_str)

                            # DATABASE ENTRY
                            check_user(user_entry, sym, paid_amount)

                            top.destroy()
                        break

                else:

                    paid_amount = f"{amount}"
                    sym = "="
                    user_output = f"{user_entry}" + " = " + paid_amount

                    right_list_box.insert(END, user_output)

                    # DATABASE ENTRY
                    check_user(user_entry, sym, paid_amount)

                    top.destroy()

        def bank():

            # GETTERS
            amount = user_amount1.get()

            if len(right_list) == 0:
                # user_name_cap = user_entry.capitalize()
                paid_amount = f"[Banked {amount}]"
                sym = "="
                user_output = f"{user_entry}" + " = " + paid_amount
                right_amount_str = f"{user_entry}" + " = " + f"({amount})"

                right_list_box.insert(END, right_amount_str)
                right_list_bank.insert(END, user_output)

                # DATABASE ENTRY
                banked(user_entry, sym, paid_amount)
                check_user(user_entry, sym, amount)

                top.destroy()
            else:
                for users in right_list:
                    name = check_tuple(users)
                    username = name.split(" ")[0]
                    # print(users)
                    user_amount2 = name.split(" ")[2].strip("]")
                    if username == user_entry:
                        total = int(amount) + int(user_amount2)

                        paid_amount = f"[Banked {total}]"
                        sym = "="
                        user_output = f"{user_entry.capitalize()}" + " = " + paid_amount
                        right_amount_str = f"{user_entry}" + " = " + f"({amount})"

                        right_list_bank.insert(END, user_output)
                        right_list_box.insert(END, right_amount_str)

                        right_list_bank.activate(int(right_list.index(users)))
                        right_list_bank.delete(ACTIVE)

                        # DATABASE ENTRY
                        banked(user_entry, sym, paid_amount)
                        check_user(user_entry, sym, amount)

                        top.destroy()
                        break
                else:

                    paid_amount = f"[Banked {amount}]"
                    sym = "="
                    user_output = f"{user_entry.capitalize()}" + " = " + paid_amount
                    right_amount_str = f"{user_entry}" + " = " + f"({amount})"

                    right_list_bank.insert(END, user_output)
                    right_list_box.insert(END, right_amount_str)

                    # DATABASE ENTRY
                    banked(user_entry, sym, paid_amount)
                    check_user(user_entry, sym, amount)

                    top.destroy()

        paid_btn = Button(top, text="PAID", bg="green", command=paid)
        not_paid_btn = Button(top, text="NOT PAID", bg="red", command=not_paid)
        bank = Button(top, text="BANKED", bg="#7B68EE", command=bank)

        # WIDGETS POSITION
        user_name_in.place(x=65, y=50)
        user_amount1.place(x=155, y=50)
        paid_btn.place(x=65, y=75)
        not_paid_btn.place(x=125, y=75)
        bank.place(x=95, y=110)
        top.mainloop()


def add_to_main():
    user_password = password.get()
    password_number = "0756061316"

    if user_password != password_number:
        messagebox.showwarning("Warning", "Enter the password to add to database")
        password.delete(0, END)

    else:

        # TOP LEVEL WINDOWS
        top = Toplevel(window, relief=RAISED)
        top.title("ADD CASH")
        top.geometry("250x150")
        top.resizable(width=False, height=False)
        top.iconbitmap("ICON/SC.ico")
        top.grab_set()  # Disable The Parent Windows
        center(top)

        # WIDGETS
        day = Spinbox(top, width=5, justify=CENTER, to=31)
        month = Spinbox(top, width=5, justify=CENTER, to=12)
        year = Spinbox(top, width=5, justify=CENTER, to=2050)
        day.delete(0)
        month.delete(0)
        year.delete(0)
        day.insert(END, date.strftime("%d"))
        month.insert(END, date.strftime("%m"))
        year.insert(END, date.strftime("%Y"))

        def add_to():

            # Get The Index Position Of The Selected
            items = map(int, right_list_box.curselection())

            # Get All The Items In Left Listbox
            user_names = left_list_box.get(0, END)

            right_search_list.delete(0, END)  # delete the credit listbox item

            for item in items:

                user = right_list_box.get(item)
                get_item = check_tuple(user)
                if len(user_names) == 0:

                    cur_day = day.get()
                    cur_month = month.get()
                    cur_year = year.get()
                    complete_date1 = f"{cur_day}/{cur_month}/{cur_year}"

                    left_list_box.insert(END, complete_date1 + " " + f"{get_item}")
                    right_list_box.delete(item)  # remove the added name

                    # DATABASE
                    user_list = list(get_item.split(" "))
                    name = user_list[0]
                    sym = user_list[1]
                    amount = user_list[2]

                    main_user_name(complete_date1, name, sym, str(amount))

                    delete_user = "DELETE FROM users WHERE username = ?"
                    user_cursor.execute(delete_user, [(name)])
                    user_db.commit()

                    top.destroy()
                else:

                    # user_name coming from left listbox
                    for names_in in user_names:
                        user = check_tuple(names_in)

                        right_username = get_item.split(" ")[0]
                        left_username = user.split(" ")[1]

                        if right_username == left_username:

                            user = check_tuple(names_in)
                            right_user_amount = get_item.split(" ")[2]
                            left_user_amount = user.split(" ")[3]

                            trim_amount_right = right_user_amount.strip("(").strip(")")
                            trim_amount_left = left_user_amount.strip("(").strip(")")

                            if right_user_amount.find("(") == 0 and left_user_amount.find("(") == 0:
                                # cur_day = day.get()
                                # cur_month = month.get()
                                # cur_year = year.get()
                                # complete_date1 = f"{cur_day}/{cur_month}/{cur_year}"

                                total = int(trim_amount_right) + int(trim_amount_left)

                                answer = f"({total})"
                                sym = "="

                                replace_username = f"{right_username}" + " = " + answer

                                right_list_box.insert(END, replace_username)

                                left_list_box.activate(int(user_names.index(names_in)))
                                left_list_box.delete(ACTIVE)  # replace the new str

                                right_list_box.delete(item)  # remove the added name

                                # DATABASE
                                check_user(right_username, sym, answer)

                                delete_user = "DELETE FROM customer WHERE username = ?"
                                main_cursor.execute(delete_user, [(right_username)])
                                main_db.commit()

                                top.destroy()
                                break

                            elif left_user_amount.find("(") == 0:
                                total = int(trim_amount_left) - int(right_user_amount)

                                if total == 0:
                                    cur_day = day.get()
                                    cur_month = month.get()
                                    cur_year = year.get()
                                    complete_date1 = f"{cur_day}/{cur_month}/{cur_year}"

                                    answer = f"{total}"
                                    sym = "="

                                    # DATABASE
                                    main_user_name(complete_date1, right_username, sym, answer)

                                    delete_user = "DELETE FROM customer WHERE amount = 0"
                                    main_cursor.execute(delete_user)
                                    main_db.commit()

                                    delete_user = "DELETE FROM users WHERE username = ?"
                                    user_cursor.execute(delete_user, [(right_username)])
                                    user_db.commit()

                                    left_list_box.activate(int(user_names.index(names_in)))
                                    left_list_box.delete(ACTIVE)  # replace the new str

                                    right_list_box.delete(item)  # remove the added name

                                    top.destroy()
                                    break
                                elif total < 0:

                                    answer1 = f"{-total}"
                                    sym = "="

                                    replace_username = right_username + " = " + answer1

                                    right_list_box.insert(END, replace_username)

                                    # DATABASE
                                    check_user(right_username, sym, answer1)

                                    delete_user = "DELETE FROM costumer WHERE username = ?"
                                    main_cursor.execute(delete_user, [(right_username)])
                                    main_db.commit()

                                    left_list_box.activate(int(user_names.index(names_in)))
                                    left_list_box.delete(ACTIVE)  # replace the new str

                                    right_list_box.delete(item)  # remove the added name

                                    top.destroy()
                                    break
                                else:
                                    cur_day = day.get()
                                    cur_month = month.get()
                                    cur_year = year.get()
                                    complete_date1 = f"{cur_day}/{cur_month}/{cur_year}"

                                    answer2 = f"({total})"
                                    sym = "="

                                    replace_username = complete_date1 + " " + f"{right_username}" + " = " + answer2

                                    left_list_box.insert(END, replace_username)

                                    # DATABASE
                                    main_user_name(complete_date1, right_username, sym, answer2)

                                    delete_user = "DELETE FROM users WHERE username = ?"
                                    user_cursor.execute(delete_user, [(right_username)])
                                    user_db.commit()

                                    left_list_box.activate(int(user_names.index(names_in)))
                                    left_list_box.delete(ACTIVE)  # replace the new str

                                    right_list_box.delete(item)  # remove the added name

                                    top.destroy()
                                    break

                            elif right_user_amount.find("(") == 0:
                                total = int(trim_amount_right) - int(left_user_amount)

                                if total == 0:

                                    cur_day = day.get()
                                    cur_month = month.get()
                                    cur_year = year.get()
                                    complete_date1 = f"{cur_day}/{cur_month}/{cur_year}"

                                    answer = f"{total}"
                                    sym = "="

                                    # DATABASE
                                    main_user_name(complete_date1, right_username, sym, answer)

                                    delete_user = "DELETE FROM customer WHERE amount = 0"
                                    main_cursor.execute(delete_user)
                                    main_db.commit()

                                    delete_user = "DELETE FROM users WHERE username = ?"
                                    user_cursor.execute(delete_user, [(right_username)])
                                    user_db.commit()

                                    left_list_box.activate(int(user_names.index(names_in)))
                                    left_list_box.delete(ACTIVE)  # replace the new str

                                    right_list_box.delete(item)  # remove the added name

                                    top.destroy()
                                    break

                                elif total < 0:
                                    cur_day = day.get()
                                    cur_month = month.get()
                                    cur_year = year.get()
                                    complete_date1 = f"{cur_day}/{cur_month}/{cur_year}"

                                    answer3 = f"{-total}"
                                    sym = "="

                                    replace_username = complete_date1 + " " + f"{right_username}" + " = " + answer3

                                    left_list_box.insert(END, replace_username)

                                    left_list_box.activate(int(user_names.index(names_in)))
                                    left_list_box.delete(ACTIVE)  # replace the new str

                                    right_list_box.delete(item)  # remove the added name

                                    # DATABASE
                                    main_user_name(complete_date1, right_username, sym, answer3)

                                    delete_user = "DELETE FROM users WHERE username = ?"
                                    user_cursor.execute(delete_user, [(right_username)])
                                    user_db.commit()

                                    top.destroy()
                                    break

                                else:
                                    cur_day = day.get()
                                    cur_month = month.get()
                                    cur_year = year.get()
                                    complete_date1 = f"{cur_day}/{cur_month}/{cur_year}"

                                    answer4 = f"({total})"
                                    sym = "="

                                    replace_username = complete_date1 + " " + f"{right_username}" + " = " + answer4

                                    left_list_box.insert(END, replace_username)

                                    left_list_box.activate(int(user_names.index(names_in)))
                                    left_list_box.delete(ACTIVE)  # replace the new str

                                    right_list_box.delete(item)  # remove the added name

                                    # DATABASE
                                    main_user_name(complete_date1, right_username, sym, answer4)

                                    delete_user = "DELETE FROM users WHERE username = ?"
                                    user_cursor.execute(delete_user, [(right_username)])
                                    user_db.commit()

                                    top.destroy()
                                    break

                            else:
                                cur_day = day.get()
                                cur_month = month.get()
                                cur_year = year.get()
                                complete_date1 = f"{cur_day}/{cur_month}/{cur_year}"

                                total = int(right_user_amount) + int(left_user_amount)

                                answer5 = f"{total}"
                                sym = "="

                                replace_username = complete_date1 + " " + f"{right_username}" + " = " + answer5

                                left_list_box.activate(int(user_names.index(names_in)))
                                left_list_box.delete(ACTIVE)  # replace the new str

                                left_list_box.insert(END, replace_username)

                                right_list_box.delete(item)  # remove the added name

                                # DATABASE
                                main_user_name(complete_date1, right_username, sym, answer5)

                                delete_user = "DELETE FROM users WHERE username = ?"
                                user_cursor.execute(delete_user, [(right_username)])
                                user_db.commit()

                                top.destroy()
                                break

                    else:

                        cur_day = day.get()
                        cur_month = month.get()
                        cur_year = year.get()
                        complete_date1 = f"{cur_day}/{cur_month}/{cur_year}"

                        left_list_box.insert(END, complete_date1 + " " + f"{get_item}")
                        right_list_box.delete(item)  # remove the added name
                        right_search_list.delete(0, END)  # delete the listbox item

                        # DATABASE
                        user_list = list(get_item.split(" "))
                        name = user_list[0]
                        sym = user_list[1]
                        amount = user_list[2]

                        main_user_name(complete_date1, name, sym, str(amount))

                        delete_user = "DELETE FROM users WHERE username = ?"
                        user_cursor.execute(delete_user, [(name)])
                        user_db.commit()

                        top.destroy()
                        break

        add_to = Button(top, text="Confirm", command=add_to)

        day.place(x=50, y=50)
        month.place(x=100, y=50)
        year.place(x=150, y=50)
        add_to.place(x=95, y=90)

        top.mainloop()


def add_user_amount():
    items = map(int, right_list_box.curselection())

    for item in items:

        get_user = right_list_box.get(item)
        user = check_tuple(get_user)
        get_name = user.split(" ")[0]

        # print(get_user)
        # print(get_name)

        # TOP LEVEL WINDOWS
        top = Toplevel(window, relief=RAISED)
        top.title("ADD CASH")
        top.geometry("250x150")
        top.resizable(width=False, height=False)
        top.iconbitmap("ICON/SC.ico")
        top.grab_set()  # Disable The Parent Windows
        center(top)

        # WIDGETS
        user_name_in_ = Label(top, text=get_name)
        user_amount1 = Spinbox(top, width=5, justify=CENTER, from_=1, to=10000)

        def paid():

            # GETTER
            user1 = check_tuple(get_user)
            get_amount = user1.split(" ")[2]
            amount = user_amount1.get()

            if get_amount.find("(") == 0:

                get_number = get_amount.strip("(").strip(")")
                total = int(amount) + int(get_number)

                paid_amount = f"({total})"
                sym = "="
                new_str = f"{get_name}" + " = " + paid_amount

                right_list_box.insert(END, new_str)
                right_list_box.delete(item)

                # DATABASE ENTRY
                check_user(get_name, sym, paid_amount)

                top.destroy()

            else:

                total = int(get_amount) - int(amount)

                if total == 0:
                    # DATABASE
                    paid_amount = f"{total}"
                    sym = "="

                    check_user(get_name, sym, paid_amount)

                    delete_user = "DELETE FROM users WHERE amount = 0"
                    user_cursor.execute(delete_user)
                    user_db.commit()

                    right_list_box.delete(item)
                    top.destroy()

                elif total < 0:

                    paid_amount = f"({-total})"
                    sym = "="
                    new_str = f"{get_name}" + " = " + paid_amount

                    right_list_box.insert(END, new_str)

                    right_list_box.delete(item)

                    # DATABASE ENTRY
                    check_user(get_name, sym, paid_amount)

                    top.destroy()
                else:

                    paid_amount = f"{total}"
                    sym = ""
                    new_str = f"{get_name}" + " = " + paid_amount

                    right_list_box.insert(END, new_str)

                    right_list_box.delete(item)

                    # DATABASE ENTRY
                    check_user(get_name, sym, paid_amount)

                    top.destroy()

        def not_paid():

            # GETTERS
            user1 = check_tuple(get_user)
            get_amount = user1.split(" ")[2]
            amount = user_amount1.get()

            if get_amount.find("(") != 0:

                total = int(amount) + int(get_amount)

                paid_amount = f"{total}"
                sym = "="
                new_str = f"{get_name}" + " = " + paid_amount

                right_list_box.insert(END, new_str)

                right_list_box.delete(item)

                # DATABASE ENTRY
                check_user(get_name, sym, paid_amount)

                top.destroy()

            else:

                get_number = get_amount.strip("(").strip(")")
                total = int(get_number) - int(amount)

                if total == 0:
                    # DATABASE
                    paid_amount = f"{total}"
                    sym = "="

                    check_user(get_name, sym, paid_amount)

                    delete_user = "DELETE FROM users WHERE amount = 0"
                    user_cursor.execute(delete_user)
                    user_db.commit()

                    right_list_box.delete(item)
                    top.destroy()

                elif total < 0:

                    paid_amount = f"{-total}"
                    sym = "="
                    new_str = f"{get_name}" + " = " + paid_amount

                    right_list_box.insert(END, new_str)

                    right_list_box.delete(item)

                    # DATABASE ENTRY
                    check_user(get_name, sym, paid_amount)

                    top.destroy()
                else:

                    paid_amount = f"({total})"
                    sym = "="
                    new_str = f"{get_name}" + " = " + paid_amount

                    right_list_box.insert(END, new_str)

                    right_list_box.delete(item)

                    # DATABASE ENTRY
                    check_user(get_name, sym, paid_amount)

                    top.destroy()

        paid_btn = Button(top, text="PAID", bg="green", command=paid)
        not_paid_btn = Button(top, text="NOT PAID", bg="red", command=not_paid)

        # WIDGETS POSITION
        user_name_in_.place(x=65, y=50)
        user_amount1.place(x=155, y=50)
        paid_btn.place(x=65, y=75)
        not_paid_btn.place(x=125, y=75)
        top.mainloop()


def user_amount():
    left_list = left_list_box.get(0, END)
    for user in left_list:
        nameuser = check_tuple(user)

        amount = nameuser.split(" ")[3]
        if amount.find("(") == 0:
            name = nameuser.split(" ")

            name.pop(0)
            username = name[0]
            sym = "="
            amount = name[2]

            # print(name)

            right_list_box.insert(END, name)

            # DATABASE ENTRY
            check_user(username, sym, amount)

            delete_user = "DELETE FROM customer WHERE username =?"
            main_cursor.execute(delete_user, [(username)])
            main_db.commit()

            left_list_box.activate(int(left_list.index(user)))
            left_list_box.delete(ACTIVE)  # delete


# DISPLAY DATABASE
user_cursor.execute("SELECT * FROM users")
for names in user_cursor.fetchall():
    # print(names)
    user_name = list(names)
    user_name.pop(0)
    right_list_box.insert(END, user_name)

main_cursor.execute("SELECT * FROM customer")
for names in main_cursor.fetchall():
    # print(names)
    user_name = list(names)
    user_name.pop(0)
    left_list_box.insert(END, user_name)

bank_cursor.execute("SELECT * FROM bank_users")
for names in bank_cursor.fetchall():
    # print(names)
    user_name = list(names)
    user_name.pop(0)
    right_list_bank.insert(END, user_name)

center(window)

# POSITION RELATED
user_input.place(x=325, y=30)
password.place(x=300, y=620)
left_list_box.place(x=0, y=0)
right_search_list.place(x=300, y=150)
right_list_box.place(x=300, y=350)
right_list_bank.place(x=300, y=515)

new_user = Button(window, text="ADD & SEARCH", command=add).place(x=345, y=70)
search_user = Button(window, text="SEARCH", command=search).place(x=455, y=70)
add_main = Button(window, text="ADD TO MAIN", command=add_to_main).place(x=300, y=650)
add_amount = Button(window, text="ADD AMOUNT", command=add_user_amount).place(x=480, y=610)
remove = Button(window, text="REMOVE", command=remove).place(x=480, y=650)
user_amount = Button(window, text="ADD", command=user_amount).place(x=200, y=665)
window.mainloop()
