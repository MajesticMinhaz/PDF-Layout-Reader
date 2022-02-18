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


# Language Choice Screen UI part her designed
def language_choice() -> None:
    widget = Widget(master=root, frame_text="Select a Language :")
    widget.button(
        text="Arabic",
        command=lambda: functional_screen(
            frame_text='حدد اختيارا :',
            create_statement_text='إنشاء البيانات',
            create_setting_file_text='إنشاء ملف الإعداد',
            close_window_text='أغلق النافذة',
            language='Arabic'
        ),
        row=0,
        col=0
    )
    widget.button(
        text="English",
        command=lambda: functional_screen(
            frame_text='Select an option :',
            create_statement_text='Create Statements',
            create_setting_file_text='Create Setting File',
            close_window_text='Close Window',
            language='English'
        ),
        row=1,
        col=0
    )
    widget.button(
        text="Quit",
        command=root.quit,
        row=2,
        col=0
    )


# Functional Screen Function
def functional_screen(
        frame_text: str,
        create_statement_text: str,
        create_setting_file_text: str,
        close_window_text: str,
        language: str
) -> None:
    def functional_screen_ui(enter_admin_password_text: str, submit_text: str) -> None:
        functional_screen_window = Toplevel(master=root)
        functional_screen_window.resizable(False, False)
        widget = Widget(master=functional_screen_window, frame_text=frame_text)
        widget.button(
            text=create_statement_text,
            command=create_statement,
            row=0,
            col=0
        )
        widget.button(
            text=create_setting_file_text,
            command=lambda: admin_login_screen(
                enter_admin_password_text=enter_admin_password_text,
                submit_text=submit_text,
                close_window_text=close_window_text,
                language=language
            ),
            row=1,
            col=0
        )
        widget.button(text=close_window_text, command=functional_screen_window.destroy, row=2, col=0)

    if language == "Arabic":
        functional_screen_ui(enter_admin_password_text='أدخل كلمة مرور المسؤول :', submit_text='إرسال')
    else:
        functional_screen_ui(enter_admin_password_text="Enter Admin Password", submit_text="Submit")


if __name__ == "__main__":
    root = Tk()
    root.title("QR Invoice APP")
    root.resizable(False, False)
    root.mainloop()
