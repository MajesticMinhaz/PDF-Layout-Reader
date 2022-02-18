"""
===========================================================================================================
                                File        main.py ( Full project code here included )
                                Author      MD. MINHAZ
                                Email       mdm047767@gmail.com
                                Hire Me     https://pph.me/mdminhaz2003/
                                Repo Link   https://github.com/mdminhaz2003/PDF-Layout-Reader/ (Private Repo)
                                Location    Dhaka, Bangladesh
                                Date        18-02-2022 at 4:56 PM
===========================================================================================================
"""
from tkinter import *
from tkinter.ttk import *
from typing import Union, Optional, Dict, Tuple, Any
from tkinter import messagebox


# Basic Widget Class
class Widget:
    def __init__(self, master, frame_text: str):
        self.frame = LabelFrame(master=master, text=frame_text, padding=10)
        self.frame.grid(row=0, column=0, padx=10, pady=10)

    # Button Widget
    def button(self, text: str, command, row: int, col: int, width: int = 30) -> Union[Button, Button]:
        btn = Button(master=self.frame, text=text, padding=5, width=width, command=command)
        btn.grid(row=row, column=col, padx=5, pady=5)
        return btn

    # Entry Widget
    def edit_text(self, label_text: str, row: int, width: int = 65, show=None) -> Entry:
        Label(master=self.frame, text=label_text).grid(row=row, column=0, padx=5, pady=5)
        edit_text_value = Entry(master=self.frame, width=width, show=show)
        edit_text_value.grid(row=row, column=1, padx=5, pady=5, columnspan=2)
        return edit_text_value

    # Checkbutton Widget
    def check_button(
            self,
            check_button_text: str,
            variable_name: IntVar,
            command, row: int,
            col: int
    ) -> Union[Checkbutton, Checkbutton]:
        check_btn = Checkbutton(master=self.frame, text=check_button_text, variable=variable_name, command=command)
        check_btn.grid(row=row, column=col, padx=20, pady=20, columnspan=1)
        return check_btn

    # Label widget
    def label(self, label_text: str, row: int, col: int) -> Union[Label, Label]:
        label = Label(master=self.frame, text=label_text)
        label.grid(row=row, column=col, padx=5, pady=5)
        return label


# Error Message Dialog Box Function
def err_message_dialog(filed_name: str, empty: True) -> None:
    if empty:
        messagebox.showwarning("Empty Field", f"{filed_name} can't be empty !")
    elif not empty:
        messagebox.showwarning("Invalid Input", f"{filed_name} should be whole number.")
    else:
        messagebox.showwarning("Wrong !", "Something went wrong !")


# Get Edit text field value Function
def field_value(field_name: Entry) -> str:
    return field_name.get()


# Delete Edit Text field value Function
def delete_field_value(field_name: Entry) -> None:
    return field_name.delete(0, "end")


# Check Empty Edit Text field Function
def is_empty(field_name: Entry) -> bool:
    return False if len(field_value(field_name=field_name)) > 0 else True


# Get Checkbutton status code using this Function.
def check_btn_status(btn_variable: IntVar) -> int:
    return btn_variable.get()


# Set Edit Text Config (disabled or enabled)
def set_config(field_name: Entry, config: str) -> Optional[Dict[str, Tuple[str, str, str, Any, Any]]]:
    return field_name.config(state=config)


def check_button_function(btn_variable: IntVar, *fields: Entry) -> None:
    btn_status = check_btn_status(btn_variable=btn_variable)
    if btn_status == 0:
        for x in fields:
            delete_field_value(field_name=x)
            set_config(field_name=x, config="disabled")
    else:
        for x in fields:
            delete_field_value(field_name=x)
            set_config(field_name=x, config="enabled")


if __name__ == "__main__":
    root = Tk()
    root.title("QR Invoice APP")
    root.resizable(False, False)
    root.mainloop()
    