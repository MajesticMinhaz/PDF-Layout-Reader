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
import os
from tkinter import *
from tkinter.ttk import *
from typing import Union, Optional, Dict, Tuple, Any
from tkinter import messagebox
from tkinter import filedialog


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
def err_message_dialog(field_name: str, empty: bool = True) -> None:
    if empty:
        messagebox.showwarning("Empty Field", f"{field_name} can't be empty !")
    elif not empty:
        messagebox.showwarning("Invalid Input", f"{field_name} should be whole number.")
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


# File select Edit text function.
def file_select(field_name: Entry, *field: str) -> None:
    delete_field_value(field_name=field_name)
    file_path = filedialog.askopenfilename(
        title=field[0],
        filetypes=[(field[1], field[2])]
    )
    if field[3] == "False":
        field_name.insert(0, os.path.dirname(file_path))
    else:
        field_name.insert(0, file_path)


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


# Admin Login screen for Create setting file
def admin_login_screen(
        enter_admin_password_text: str,
        submit_text: str,
        close_window_text: str,
        language: str
) -> None:
    admin_login_screen_window = Toplevel(root)
    admin_login_screen_window.resizable(False, False)

    widget = Widget(master=admin_login_screen_window, frame_text=enter_admin_password_text)
    user_password = widget.edit_text(label_text=enter_admin_password_text, width=30, row=0, show="*")
    text = widget.label(label_text="", row=1, col=1)

    def checking_password(passwd: Entry):
        if is_empty(passwd):
            text.config(text="Password can\'t be empty")
            delete_field_value(passwd)
        elif len(field_value(passwd)) < 8:
            text.config(text="Length of Password should be at least 8")
            delete_field_value(passwd)
        elif len(field_value(passwd)) == 8 and field_value(passwd) != "12345678":
            text.config(text="Wrong Password ! Try Again !")
            delete_field_value(passwd)
        elif len(field_value(passwd)) == 8 and field_value(passwd) == "12345678":
            text.config(text="Successfully logged in.")
            delete_field_value(passwd)
            admin_login_screen_window.destroy()

            if language == 'Arabic':
                # create_setting_file(
                #     input_valid_information_text='إدخال معلومات صحيحة',
                #     submit_text=submit_text,
                #     close_window_text=close_window_text
                # )
                pass
            else:
                # create_setting_file(
                #     input_valid_information_text="Input Valid Information",
                #     submit_text=submit_text,
                #     close_window_text=close_window_text
                # )
                pass
        else:
            widget.label(label_text="Something went wrong ! Try Again", row=1, col=1)
            passwd.delete(0, 'end')

    widget.button(text=submit_text, command=lambda: checking_password(user_password), row=2, col=0, width=15)
    widget.button(text=close_window_text, command=admin_login_screen_window.destroy, row=2, col=2, width=15)


# Create setting file function here covered
def create_setting_file(
        input_valid_information_text: str,
        submit_text: str,
        close_window_text: str
) -> None:
    setting_screen_window = Toplevel(master=root)
    setting_screen_window.resizable(False, False)

    widget = Widget(master=setting_screen_window, frame_text=input_valid_information_text)

    username = widget.edit_text(label_text="Username", row=0)
    admin_password = widget.edit_text(label_text="Admin Password", row=1, show="*")

    output_file_name = widget.edit_text(label_text="Filename (*.env)", row=2)
    output_file_name.insert(0, "setting.env")
    set_config(field_name=output_file_name, config="disabled")

    company_name = widget.edit_text(label_text="Company Name", row=3)
    qr_location_x = widget.edit_text(label_text="QR Location X (cm)", row=4)
    qr_location_y = widget.edit_text(label_text="QR Location Y (cm)", row=5)
    qr_size = widget.edit_text(label_text="QR Code Size (cm)", row=6)

    # ----------------------------- Only for Local drive folder location -------------------------------
    local_drive_folder_location = widget.edit_text(label_text="Local Drive Folder Location", row=7)
    local_drive_folder_location.insert(0, "Select a file")
    local_drive_folder_location.bind(
        "<Button-1>", lambda a="Select any file", b="Any File", c="*.*", d="False": file_select(
            local_drive_folder_location, a, b, c, d
        )
    )

    # -------------------------------------------------------------------------------------------------
    # ------------------------------------Checkbutton here start-------------------------------------

    google_drive_check_btn_status = IntVar()
    widget.check_button(
        check_button_text="Google Drive Folder",
        variable_name=google_drive_check_btn_status,
        command=lambda: check_button_function(
            google_drive_check_btn_status,
            google_drive_access_token,
            google_drive_folder_id
        ),
        row=8,
        col=0
    )

    # ---------------------------------- Google Drive Checkbutton end here----------------------------------------

    # ---------------------------------- OneDrive Checkbutton here start------------------------------------------

    one_drive_folder_check_btn_status = IntVar()
    widget.check_button(
        check_button_text="OneDrive Folder",
        variable_name=one_drive_folder_check_btn_status,
        command=lambda: check_button_function(
            one_drive_folder_check_btn_status,
            one_drive_folder
        ),
        row=8,
        col=1
    )

    # ---------------------------------- OneDrive Checkbutton end here------------------------------------------

    # ---------------------------------- FTP server Checkbutton here start------------------------------------------

    ftp_server_check_btn_status = IntVar()
    widget.check_button(
        check_button_text="FTP Server",
        variable_name=ftp_server_check_btn_status,
        command=lambda: check_button_function(
            ftp_server_check_btn_status,
            ftp_ip,
            ftp_username,
            ftp_password,
            ftp_folder_location
        ),
        row=8,
        col=2
    )
    # ----------------------------------FTP Server Checkbutton here end------------------------------------------
    # ----------------------------------Checkbutton here end------------------------------------------

    google_drive_access_token = widget.edit_text(label_text="Access Token", row=9)
    google_drive_folder_id = widget.edit_text(label_text="Google Drive Folder ID", row=10)

    one_drive_folder = widget.edit_text(label_text="OneDrive Folder", row=11)

    ftp_ip = widget.edit_text(label_text="FTP IP", row=12)
    ftp_username = widget.edit_text(label_text="FTP Username", row=13)
    ftp_password = widget.edit_text(label_text="FTP Password", row=14, show="*")
    ftp_folder_location = widget.edit_text(label_text="FTP Folder Location", row=15)

    # -------------------------------------------------------------------------------------------------
    # disable all additional fields without local drive field
    set_config(field_name=google_drive_access_token, config="disabled")
    set_config(field_name=google_drive_folder_id, config="disabled")
    set_config(field_name=one_drive_folder, config="disabled")
    set_config(field_name=ftp_ip, config="disabled")
    set_config(field_name=ftp_username, config="disabled")
    set_config(field_name=ftp_password, config="disabled")
    set_config(field_name=ftp_folder_location, config="disabled")

    # -------------------------------------------------------------------------------------------------
    def checking_input_validity() -> None:
        if is_empty(username):
            err_message_dialog("Username")
        elif is_empty(admin_password):
            err_message_dialog('Admin Password')
        elif is_empty(company_name):
            err_message_dialog('Company Name')
        elif is_empty(qr_location_x):
            err_message_dialog("QR Code Location X (cm)")
        elif is_empty(qr_location_y):
            err_message_dialog("QR Code Location Y (cm)")
        elif is_empty(qr_size):
            err_message_dialog("QR code box size (cm)")
        elif is_empty(local_drive_folder_location) or field_value(local_drive_folder_location) == 'Select a file':
            err_message_dialog("Local Drive Folder Location")
        elif check_btn_status(google_drive_check_btn_status) == 1 and is_empty(google_drive_access_token):
            err_message_dialog("Google Drive Access Token")
        elif check_btn_status(google_drive_check_btn_status) == 1 and is_empty(google_drive_folder_id):
            err_message_dialog("Google Drive Folder ID")
        elif check_btn_status(one_drive_folder_check_btn_status) == 1 and is_empty(one_drive_folder):
            err_message_dialog("OneDrive Folder")
        elif check_btn_status(ftp_server_check_btn_status) == 1 and is_empty(ftp_ip):
            err_message_dialog("FTP IP")
        elif check_btn_status(ftp_server_check_btn_status) == 1 and is_empty(ftp_username):
            err_message_dialog("FTP Username")
        elif check_btn_status(ftp_server_check_btn_status) == 1 and is_empty(ftp_password):
            err_message_dialog("FTP Password")
        elif check_btn_status(ftp_server_check_btn_status) == 1 and is_empty(ftp_folder_location):
            err_message_dialog("FTP Folder Location")
        elif field_value(username) != "root2020":
            err_message_dialog("Username", False)
        elif field_value(admin_password) != "12345678":
            err_message_dialog("Admin Password", False)
        elif not field_value(qr_location_x).isdigit():
            err_message_dialog("QR Code Location X (cm)", False)
        elif not field_value(qr_location_y).isdigit():
            err_message_dialog("QR Code Location Y (cm)", False)
        elif not field_value(qr_size).isdigit():
            err_message_dialog("QR Code Size (cm)", False)
        else:
            user_input = {
                "username": field_value(username),
                "password": field_value(admin_password),
                "setting_file_name": field_value(output_file_name),
                "company_name": field_value(company_name),
                "qr_location_x": field_value(qr_location_x),
                "qr_location_y": field_value(qr_location_y),
                "qr_size": field_value(qr_size),
                "local_drive_folder_location": field_value(local_drive_folder_location),
                "google_drive_access_token": field_value(google_drive_access_token),
                "google_drive_folder_id": field_value(google_drive_folder_id),
                "one_drive_folder": field_value(one_drive_folder),
                "ftp_ip": field_value(ftp_ip),
                "ftp_username": field_value(ftp_username),
                "ftp_password": field_value(ftp_password),
                "ftp_folder_location": field_value(ftp_folder_location)
            }

            messagebox.showinfo("Successful !", f"Successfully created setting.env file inside :\n"
                                                f"{field_value(local_drive_folder_location)}")

            # Deleting all value from current screen
            delete_field_value(username)
            delete_field_value(admin_password)
            delete_field_value(company_name)
            delete_field_value(qr_location_x)
            delete_field_value(qr_location_y)
            delete_field_value(qr_size)
            delete_field_value(local_drive_folder_location)
            delete_field_value(google_drive_access_token)
            delete_field_value(google_drive_folder_id)
            delete_field_value(one_drive_folder)
            delete_field_value(ftp_ip)
            delete_field_value(ftp_username)
            delete_field_value(ftp_password)
            delete_field_value(ftp_folder_location)

            write_setting_file_func(values=user_input)

    widget.button(
        text=submit_text,
        command=lambda: checking_input_validity(),
        row=16,
        col=0,
        width=16
    )
    widget.button(text="Log File", command=None, row=16, col=1, width=16)
    widget.button(text=close_window_text, command=setting_screen_window.destroy, row=16, col=2, width=16)


if __name__ == "__main__":
    root = Tk()
    root.title("QR Invoice APP")
    root.resizable(False, False)
    language_choice()
    root.mainloop()
