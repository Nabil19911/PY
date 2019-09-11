from tkinter import *
from tkinter import messagebox
import datetime

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
right_list_box = Listbox(window, width=40, height=15)

# LABEL
available_credit_text = Label(window, text="CREDIT").place(x=405, y=125)
complete_date = Label(window, text=date).place(x=400, y=325)


# FUNCTIONS OF BUTTONS
def remove():
    items = map(int, right_list_box.curselection())
    for item in items:
        right_list_box.delete(item)

    items = map(int, right_search_list.curselection())
    for item in items:
        right_search_list.delete(item)


def search():
    # Getter
    left_list = left_list_box.get(0, END)
    right_search = right_search_list.get(0, END)
    user_entry = user_input.get()

    for user in left_list:
        user_name = user.split(" ")[1]

        if len(right_search) == 0:
            if user_name == user_entry.upper():
                right_search_list.insert(END, user)
        else:
            for users in right_search:
                users_name = users.split(" ")[1]
                if user_name != users_name:
                    if user_name == user_entry.upper():
                        right_search_list.insert(END, user)
                        break
                    break


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

        # WIDGETS
        user_name = Label(top, text=user_entry)
        user_amount1 = Spinbox(top, width=5, justify=CENTER, from_=1, to=10000)

        def paid():

            # GETTERS
            amount = user_amount1.get()
            if len(right_list) == 0:
                user_output = f"{user_entry} = ({amount})"
                right_list_box.insert(END, user_output)
                top.destroy()
            else:
                for users in right_list:

                    user = users

                    if user.split(" ")[0] == user_entry:

                        if user.split(" ")[2].find("(") == 0:
                            num = user.split(" ")[2].strip("(").strip(")")
                            answer = int(num) + int(amount)
                            new_str = f"{user_entry} = ({answer})"
                            right_list_box.activate(int(right_list.index(users)))
                            right_list_box.delete(ACTIVE)
                            right_list_box.insert(END, new_str)
                            top.destroy()
                        else:
                            num = user.split(" ")[2]
                            answer = int(num) - int(amount)
                            if answer == 0:
                                right_list_box.activate(int(right_list.index(users)))
                                right_list_box.delete(ACTIVE)
                                top.destroy()
                            elif answer < 0:
                                new_str = f"{user_entry} = ({-answer})"
                                right_list_box.activate(int(right_list.index(users)))
                                right_list_box.delete(ACTIVE)
                                right_list_box.insert(END, new_str)
                                top.destroy()
                            else:
                                new_str = f"{user_entry} = {answer}"
                                right_list_box.activate(int(right_list.index(users)))
                                right_list_box.delete(ACTIVE)
                                right_list_box.insert(END, new_str)
                                top.destroy()

                        break

                else:
                    user_output = f"{user_entry} = ({amount})"
                    right_list_box.insert(END, user_output)
                    top.destroy()

        def not_paid():

            # GETTERS
            amount = user_amount1.get()
            if len(right_list) == 0:
                user_output = f"{user_entry} = {amount}"
                right_list_box.insert(END, user_output)
                top.destroy()
            else:
                for users in right_list:

                    user = users

                    if user.split(" ")[0] == user_entry:

                        if user.split(" ")[2].find("(") == 0:
                            num = user.split(" ")[2].strip("(").strip(")")
                            answer = int(num) - int(amount)
                            if answer == 0:
                                right_list_box.activate(int(right_list.index(users)))
                                right_list_box.delete(ACTIVE)
                                top.destroy()
                            elif answer < 0:
                                new_str = f"{user_entry} = {-answer}"
                                right_list_box.activate(int(right_list.index(users)))
                                right_list_box.delete(ACTIVE)
                                right_list_box.insert(END, new_str)
                                top.destroy()
                            else:
                                new_str = f"{user_entry} = ({answer})"
                                right_list_box.activate(int(right_list.index(users)))
                                right_list_box.delete(ACTIVE)
                                right_list_box.insert(END, new_str)
                                top.destroy()
                        else:
                            num = user.split(" ")[2].strip("(").strip(")")
                            answer = int(num) + int(amount)
                            new_str = f"{user_entry} = {answer}"
                            right_list_box.activate(int(right_list.index(users)))
                            right_list_box.delete(ACTIVE)
                            right_list_box.insert(END, new_str)
                            top.destroy()
                        break

                else:
                    user_output = f"{user_entry} = {amount}"
                    right_list_box.insert(END, user_output)
                    top.destroy()

        def banked():

            # GETTERS
            amount = user_amount1.get()

            if len(right_list) == 0:
                user_output = f"{user_entry} = [Banked {amount}]"
                right_list_box.insert(END, user_output)
                top.destroy()
            else:
                for users in right_list:
                    username = users.split(" ")[0]
                    user_amount2 = users.split(" ")[3].strip("]")
                    if username == user_entry:
                        total = int(amount) + int(user_amount2)
                        user_output = f"{user_entry} = [Banked {total}]"
                        right_list_box.insert(END, user_output)
                        right_list_box.activate(int(right_list.index(users)))
                        right_list_box.delete(ACTIVE)
                        top.destroy()
                        break
                else:
                    user_output = f"{user_entry} = [Banked {amount}]"
                    right_list_box.insert(END, user_output)
                    # right_list_box.selection_set(right_list.index(users))
                    top.destroy()

        paid_btn = Button(top, text="PAID", bg="green", command=paid)
        not_paid_btn = Button(top, text="NOT PAID", bg="red", command=not_paid)
        banked = Button(top, text="BANKED", bg="#7B68EE", command=banked)

        # WIDGETS POSITION
        user_name.place(x=65, y=50)
        user_amount1.place(x=155, y=50)
        paid_btn.place(x=65, y=75)
        not_paid_btn.place(x=125, y=75)
        banked.place(x=95, y=110)
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

        # WIDGETS
        day = Spinbox(top, width=5, justify=CENTER, from_=1, to=31)
        month = Spinbox(top, width=5, justify=CENTER, from_=1, to=12)
        year = Spinbox(top, width=5, justify=CENTER, from_=2015, to=2050)

        def add_to():

            # Get The Index Position Of The Selected
            items = map(int, right_list_box.curselection())

            # Get All The Items In Left Listbox
            user_names = left_list_box.get(0, END)

            right_search_list.delete(0, END)  # delete the credit listbox item

            for item in items:

                get_item = right_list_box.get(item)

                if len(user_names) == 0:

                    cur_day = day.get()
                    cur_month = month.get()
                    cur_year = year.get()
                    complete_date1 = f"{cur_day}/{cur_month}/{cur_year}"

                    left_list_box.insert(END, f"({complete_date1}) {get_item}")
                    right_list_box.delete(item)  # remove the added name
                    top.destroy()
                else:

                    # user_name coming from left listbox
                    for names in user_names:

                        right_username = get_item.split(" ")[0]
                        left_username = names.split(" ")[1]

                        if right_username == left_username:

                            right_user_amount = get_item.split(" ")[2]
                            left_user_amount = names.split(" ")[3]

                            trim_amount_right = right_user_amount.strip("(").strip(")")
                            trim_amount_left = left_user_amount.strip("(").strip(")")

                            if right_user_amount.find("(") == 0 and left_user_amount.find("(") == 0:
                                cur_day = day.get()
                                cur_month = month.get()
                                cur_year = year.get()
                                complete_date1 = f"{cur_day}/{cur_month}/{cur_year}"

                                total = int(trim_amount_right) + int(trim_amount_left)

                                replace_username = f"({complete_date1}) {right_username} = ({total})"

                                right_list_box.insert(END, replace_username)

                                left_list_box.activate(int(user_names.index(names)))
                                left_list_box.delete(ACTIVE)  # replace the new str

                                right_list_box.delete(item)  # remove the added name
                                top.destroy()
                                break

                            elif left_user_amount.find("(") == 0:
                                total = int(trim_amount_left) - int(right_user_amount)

                                if total == 0:
                                    left_list_box.activate(int(user_names.index(names)))
                                    left_list_box.delete(ACTIVE)  # replace the new str

                                    right_list_box.delete(item)  # remove the added name
                                    top.destroy()
                                    break
                                elif total < 0:
                                    cur_day = day.get()
                                    cur_month = month.get()
                                    cur_year = year.get()
                                    complete_date1 = f"{cur_day}/{cur_month}/{cur_year}"

                                    replace_username = f"({complete_date1}) {right_username} = {-total}"

                                    right_list_box.insert(END, replace_username)

                                    left_list_box.activate(int(user_names.index(names)))
                                    left_list_box.delete(ACTIVE)  # replace the new str

                                    right_list_box.delete(item)  # remove the added name
                                    top.destroy()
                                    break
                                else:
                                    cur_day = day.get()
                                    cur_month = month.get()
                                    cur_year = year.get()
                                    complete_date1 = f"{cur_day}/{cur_month}/{cur_year}"

                                    replace_username = f"({complete_date1}) {right_username} = ({total})"

                                    left_list_box.insert(END, replace_username)

                                    left_list_box.activate(int(user_names.index(names)))
                                    left_list_box.delete(ACTIVE)  # replace the new str

                                    right_list_box.delete(item)  # remove the added name
                                    top.destroy()
                                    break

                            elif right_user_amount.find("(") == 0:
                                total = int(trim_amount_right) - int(left_user_amount)

                                if total == 0:
                                    left_list_box.activate(int(user_names.index(names)))
                                    left_list_box.delete(ACTIVE)  # replace the new str

                                    right_list_box.delete(item)  # remove the added name
                                    top.destroy()
                                    break

                                elif total < 0:
                                    cur_day = day.get()
                                    cur_month = month.get()
                                    cur_year = year.get()
                                    complete_date1 = f"{cur_day}/{cur_month}/{cur_year}"

                                    replace_username = f"({complete_date1}) {right_username} = {-total}"

                                    left_list_box.insert(END, replace_username)

                                    left_list_box.activate(int(user_names.index(names)))
                                    left_list_box.delete(ACTIVE)  # replace the new str

                                    right_list_box.delete(item)  # remove the added name
                                    top.destroy()
                                    break

                                else:
                                    cur_day = day.get()
                                    cur_month = month.get()
                                    cur_year = year.get()
                                    complete_date1 = f"{cur_day}/{cur_month}/{cur_year}"

                                    replace_username = f"({complete_date1}) {right_username} = ({total})"

                                    left_list_box.insert(END, replace_username)

                                    left_list_box.activate(int(user_names.index(names)))
                                    left_list_box.delete(ACTIVE)  # replace the new str

                                    right_list_box.delete(item)  # remove the added name
                                    top.destroy()
                                    break

                            else:
                                cur_day = day.get()
                                cur_month = month.get()
                                cur_year = year.get()
                                complete_date1 = f"{cur_day}/{cur_month}/{cur_year}"

                                total = int(right_user_amount) + int(left_user_amount)

                                replace_username = f"({complete_date1}) {right_username} = {total}"

                                left_list_box.activate(int(user_names.index(names)))
                                left_list_box.delete(ACTIVE)  # replace the new str

                                left_list_box.insert(END, replace_username)

                                right_list_box.delete(item)  # remove the added name
                                top.destroy()
                                break

                    else:

                        cur_day = day.get()
                        cur_month = month.get()
                        cur_year = year.get()
                        complete_date1 = f"{cur_day}/{cur_month}/{cur_year}"

                        left_list_box.insert(END, f"({complete_date1}) {get_item}")
                        right_list_box.delete(item)  # remove the added name
                        right_search_list.delete(0, END)  # delete the listbox item
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
        get_name = get_user.split(" ")[0]

        print(get_user)
        print(get_name)

        # TOP LEVEL WINDOWS
        top = Toplevel(window, relief=RAISED)
        top.title("ADD CASH")
        top.geometry("250x150")
        top.resizable(width=False, height=False)
        top.iconbitmap("ICON/SC.ico")
        top.grab_set()  # Disable The Parent Windows

        # WIDGETS
        user_name = Label(top, text=get_name)
        user_amount1 = Spinbox(top, width=5, justify=CENTER, from_=1, to=10000)

        def paid():

            # GETTER
            get_amount = get_user.split(" ")[2]
            amount = user_amount1.get()

            if get_amount.find("(") == 0:

                get_number = get_amount.strip("(").strip(")")
                total = int(amount) + int(get_number)

                new_str = f"{get_name} = ({total})"
                right_list_box.insert(END, new_str)
                right_list_box.delete(item)
                top.destroy()

            else:

                total = int(get_amount) - int(amount)

                if total == 0:
                    right_list_box.delete(item)
                    top.destroy()
                elif total < 0:
                    new_str = f"{get_name} = ({-total})"
                    right_list_box.insert(END, new_str)
                    right_list_box.delete(item)
                    top.destroy()
                else:
                    new_str = f"{get_name} = {total}"
                    right_list_box.insert(END, new_str)
                    right_list_box.delete(item)
                    top.destroy()

        def not_paid():

            # GETTERS
            get_amount = get_user.split(" ")[2]
            amount = user_amount1.get()

            if get_amount.find("(") != 0:

                total = int(amount) + int(get_amount)

                new_str = f"{get_name} = {total}"
                right_list_box.insert(END, new_str)
                right_list_box.delete(item)
                top.destroy()

            else:

                get_number = get_amount.strip("(").strip(")")
                total = int(get_number) - int(amount)

                if total == 0:
                    right_list_box.delete(item)
                    top.destroy()
                elif total < 0:
                    new_str = f"{get_name} = {-total}"
                    right_list_box.insert(END, new_str)
                    right_list_box.delete(item)
                    top.destroy()
                else:
                    new_str = f"{get_name} = ({total})"
                    right_list_box.insert(END, new_str)
                    right_list_box.delete(item)
                    top.destroy()

        paid_btn = Button(top, text="PAID", bg="green", command=paid)
        not_paid_btn = Button(top, text="NOT PAID", bg="red", command=not_paid)

        # WIDGETS POSITION
        user_name.place(x=65, y=50)
        user_amount1.place(x=155, y=50)
        paid_btn.place(x=65, y=75)
        not_paid_btn.place(x=125, y=75)
        top.mainloop()


def user_amount():
    left_list = left_list_box.get(0, END)
    for user in left_list:
        amount = user.split(" ")[3]
        if amount.find("(") == 0:
            name = user.split(" ")
            name.pop(0)
            right_list_box.insert(END, name)

            left_list_box.activate(int(left_list.index(user)))
            left_list_box.delete(ACTIVE)  # delete


# POSITION RELATED
user_input.place(x=325, y=30)
password.place(x=300, y=620)
left_list_box.place(x=0, y=0)
right_search_list.place(x=300, y=150)
right_list_box.place(x=300, y=350)

new_user = Button(window, text="ADD & SEARCH", command=add).place(x=345, y=70)
search_user = Button(window, text="SEARCH", command=search).place(x=455, y=70)
add_main = Button(window, text="ADD TO MAIN", command=add_to_main).place(x=300, y=650)
add_amount = Button(window, text="ADD AMOUNT", command=add_user_amount).place(x=480, y=600)
remove = Button(window, text="REMOVE", command=remove).place(x=480, y=650)
user_amount = Button(window, text="ADD", command=user_amount).place(x=200, y=665)
window.mainloop()
