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
import json
import re
import pdftotext
import ntplib
from datetime import datetime
import calendar
import time
from uttlv import TLV
import base64
import qrcode
from reportlab.pdfgen import canvas
from PyPDF2 import PdfFileWriter
from PyPDF2 import PdfFileReader
from tkinter import *
from tkinter.ttk import *
from typing import Union, Optional, Dict, Tuple, Any
from cryptography.fernet import Fernet
from dotenv import load_dotenv
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
                create_setting_file(
                    input_valid_information_text='إدخال معلومات صحيحة',
                    submit_text=submit_text,
                    close_window_text=close_window_text
                )
            else:
                create_setting_file(
                    input_valid_information_text="Input Valid Information",
                    submit_text=submit_text,
                    close_window_text=close_window_text
                )
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


# Write setting file
def write_setting_file_func(
        values: dict
) -> None:
    # creating key
    key = Fernet.generate_key()
    cipher_code = Fernet(key)

    def encryption_func(key_name: str) -> str:
        return cipher_code.encrypt(values[key_name].encode('utf-8')).decode('utf-8')

    # Getting all values from user input
    key = key.decode('utf-8')
    username = encryption_func(key_name="username")
    admin_password = encryption_func(key_name="password")
    setting_file_name = encryption_func(key_name="setting_file_name")
    company_name = encryption_func(key_name="company_name")
    qr_location_x = encryption_func(key_name="qr_location_x")
    qr_location_y = encryption_func(key_name="qr_location_y")
    qr_size = encryption_func(key_name="qr_size")
    local_drive_folder_location = encryption_func(key_name="local_drive_folder_location")
    google_drive_access_token = encryption_func(key_name="google_drive_access_token")
    google_drive_folder_id = encryption_func(key_name="google_drive_folder_id")
    one_drive_folder = encryption_func(key_name="one_drive_folder")
    ftp_ip = encryption_func(key_name="ftp_ip")
    ftp_username = encryption_func(key_name="ftp_username")
    ftp_password = encryption_func(key_name="ftp_password")
    ftp_folder_location = encryption_func(key_name="ftp_folder_location")

    # Creating File template here
    template = f"KEY={key}\nADMIN_USERNAME={username}\nPASSWORD={admin_password}\nFILE_NAME={setting_file_name}\n" \
               f"COMPANY_NAME={company_name}\nQR_LOC_X={qr_location_x}\nQR_LOC_Y={qr_location_y}\nQR_SIZE={qr_size}\n" \
               f"LOCAL_FILE_LOC={local_drive_folder_location}\nGOOGLE_DRIVE_TOKEN={google_drive_access_token}\n" \
               f"GOOGLE_DRIVE_FOLDER_ID={google_drive_folder_id}\nONE_DRIVE_FOLDER={one_drive_folder}\n" \
               f"FTP_IP={ftp_ip}\nFTP_USERNAME={ftp_username}\nFTP_PASSWORD={ftp_password}\n" \
               f"FTP_FOLDER_LOC={ftp_folder_location}\n"

    # Creating setting file path
    path = os.path.join(values["local_drive_folder_location"], "setting.env")

    # write setting file now
    with open(path, 'w') as write:
        write.write(template)
        write.close()

    log_file(
        log_message="Created a new Setting file",
        setting_file_path=f"{values['local_drive_folder_location']}"
    )


# Creating Log file
def log_file(
        log_message: str,
        setting_file_path: str
) -> None:
    setting_file_data = read_setting_file_func(path=setting_file_path)
    log_file_path = os.path.join(setting_file_path, "log_info.json")
    key = setting_file_data["key"].encode('utf-8')
    cipher_code = Fernet(key)
    date_time = datetime.now()

    def date_time_encryption_text_func(key_name: str) -> str:
        return cipher_code.encrypt(date_time.strftime(key_name).encode('utf-8')).decode('utf-8')

    def dict_value_encryption_text_func(key_name: str) -> str:
        return cipher_code.encrypt(setting_file_data[key_name].encode('utf-8')).decode('utf-8')

    data = {
        "key": key.decode("utf-8"),
        "username": dict_value_encryption_text_func("username"),
        "task": cipher_code.encrypt(log_message.encode('utf-8')).decode('utf-8'),
        "company_name": dict_value_encryption_text_func("company_name"),
        "local_drive_folder_loc": dict_value_encryption_text_func("local_drive_folder_location"),
        "date": date_time_encryption_text_func(key_name="%d %B, %Y"),
        "weekday": date_time_encryption_text_func(key_name="%A"),
        "time": date_time_encryption_text_func(key_name="%I:%M:%S %p")
    }

    if os.path.isfile(log_file_path):
        with open(log_file_path, 'r') as read_file:
            convert_to_list = json.loads(read_file.read())
            read_file.close()

        write_text = json.dumps(data)

        # convert list to json
        for item in convert_to_list:
            convert_to_json = json.dumps(item)
            write_text += f',\n{convert_to_json}'

        # text formatting
        final_write_text = f'[{write_text}]'
        print(final_write_text)
        # write log_info.json file
        with open(log_file_path, 'w') as write_file:
            write_file.write(final_write_text)
            write_file.close()
    else:
        write_data = f'[{json.dumps(data)}]'
        print(write_data)
        # write log_info.json file
        with open(log_file_path, 'w') as write_file:
            write_file.write(write_data)
            write_file.close()


# Read setting file
def read_setting_file_func(
        path: str
) -> dict:
    setting_file_absolute_path = os.path.join(path, "setting.env")
    try:
        load_dotenv(setting_file_absolute_path)
        key = os.getenv('KEY').encode('utf-8')
        cipher_code = Fernet(key)

        # decryption shortcut function
        def decryption_func(key_name: str) -> str:
            return cipher_code.decrypt(bytes(os.getenv(key_name), 'utf-8')).decode('utf-8')

        try:
            data = {
                "key": key.decode('utf-8'),
                "username": decryption_func(key_name='ADMIN_USERNAME'),
                "admin_password": decryption_func(key_name='PASSWORD'),
                "file_name": decryption_func(key_name='FILE_NAME'),
                "company_name": decryption_func(key_name='COMPANY_NAME'),
                "qr_loc_x": decryption_func(key_name='QR_LOC_X'),
                "qr_loc_y": decryption_func(key_name='QR_LOC_Y'),
                "qr_size": decryption_func(key_name='QR_SIZE'),
                "local_drive_folder_location": decryption_func(key_name='LOCAL_FILE_LOC'),
                "google_drive_access_token": decryption_func(key_name='GOOGLE_DRIVE_TOKEN'),
                "google_drive_folder_id": decryption_func(key_name='GOOGLE_DRIVE_FOLDER_ID'),
                "one_drive_folder": decryption_func(key_name='ONE_DRIVE_FOLDER'),
                "ftp_ip": decryption_func(key_name='FTP_IP'),
                "ftp_username": decryption_func(key_name='FTP_USERNAME'),
                "ftp_password": decryption_func(key_name='FTP_PASSWORD'),
                "ftp_folder_location": decryption_func(key_name='FTP_FOLDER_LOC')
            }
            return data
        except Exception as e:
            messagebox.showerror("Value Not Found !", "Some value is missing in your setting file.")
            print(e)
            return {}
    except ValueError as e:
        messagebox.showerror("Value Not Found !", "Some Values not found in this setting file.\n"
                                                  "Please Create a new one.")
        print(f"Value Not Found !\n{e}")


# Create Statement button function
def create_statement() -> None:
    create_statement_file_input_window = Toplevel(master=root)
    create_statement_file_input_window.resizable(False, False)
    widget = Widget(master=create_statement_file_input_window, frame_text="Enter Correct Info :")

    setting_file_path = widget.edit_text(label_text="Setting File", row=0)
    setting_file_path.insert(0, "Select setting.env file")
    setting_file_path.bind(
        "<Button-1>", lambda a="Select setting.env file", b="Setting File", c="setting.env", d="False": file_select(
            setting_file_path, a, b, c, d
        )
    )

    pdf_file_path = widget.edit_text(label_text="PDF file", row=1)
    pdf_file_path.insert(0, "Select input PDF file")
    pdf_file_path.bind(
        "<Button-1>", lambda a="Select input PDF file", b="PDF files", c="*.pdf", d="True": file_select(
            pdf_file_path, a, b, c, d
        )
    )

    # def checking_value() -> None:
    #     global pdf_date, pdf_vat_number, hour, minute, second, year, day, month
    #     if is_empty_field(setting_file_path):
    #         err_message_dialog(input_name="setting file's path")
    #     elif is_empty_field(pdf_file_path):
    #         err_message_dialog(input_name="input pdf file's path")
    #     else:
    #         set_config_edit_text(field_name=setting_file_path, config_text="disabled")
    #         set_config_edit_text(field_name=pdf_file_path, config_text="disabled")
    #
    #         # Read PDF file
    #         with open(field_value(pdf_file_path), 'rb') as read_pdf:
    #             pdf_page_obj = pdftotext.PDF(pdf_file=read_pdf)
    #         pdf_all_text = "\n\n".join(pdf_page_obj)
    #         pdf_page_text_list = pdf_all_text.split()
    #         try:
    #             # get date and vat number from pdf file
    #             pdf_date = list(filter(lambda item: date_rag.match(item), pdf_page_text_list))[0]
    #             pdf_vat_number = list(filter(lambda item: vat_num_rag.match(item), pdf_page_text_list))[0]
    #         except ValueError as e:
    #             print('Some value is missing in pdf file.')
    #             print(e)
    #             messagebox.showerror('Invalid Format', 'Your pdf file is Invalid Format.')
    #
    #         ntp_client = ntplib.NTPClient()
    #         try:
    #             response = ntp_client.request('pool.ntp.org')
    #             hour = str(datetime.fromtimestamp(response.tx_time).hour)
    #             minute = str(datetime.fromtimestamp(response.tx_time).minute)
    #             second = str(datetime.fromtimestamp(response.tx_time).second)
    #         except ConnectionError as e:
    #             hour = str(datetime.fromtimestamp(time.time()).hour)
    #             minute = str(datetime.fromtimestamp(time.time()).minute)
    #             second = str(datetime.fromtimestamp(time.time()).second)
    #             print(f'Tried using NTP server but it was not reachable so instead used system time\nError: {e}')
    #
    #         # formatting time
    #         def check_digit(digit: str) -> str:
    #             return f'0{digit}' if len(digit) < 2 else digit
    #
    #         # final time output
    #         hour = check_digit(hour)
    #         minute = check_digit(minute)
    #         second = check_digit(second)
    #
    #         # checking info
    #         date_time = datetime.now()
    #         if pdf_date is not None:
    #             date_data = pdf_date.split(re.findall(r'[\.\/-]', pdf_date)[0])
    #
    #             year = list(filter(lambda a: re.search(r'[0-9]{4}', a), date_data))[0]
    #             day = date_data[0]
    #
    #             try:
    #                 month_list = list(calendar.month_abbr)
    #                 lower_date = pdf_date.lower()
    #                 month_index = str(month_list.index(
    #                     list(filter(lambda a: re.findall(a.lower(), lower_date), month_list[1:]))[0]
    #                 ))
    #                 month_index = check_digit(month_index)
    #             except ValueError:
    #                 month_index = date_data[1]
    #             pdf_date = f'{year}-{month_index}-{day} {hour}:{minute}:{second}'
    #         else:
    #             pdf_date = date_time.strftime(f'%Y-%m-%d {hour}:{minute}:{second}')
    #
    #         setting_data = read_setting_file_func(path=field_value(setting_file_path))
    #
    #         widget.label(label_text=f"Company Name: {setting_data['company_name']}", row=3, col=1)
    #         widget.label(label_text=f"Date: {pdf_date}", row=4, col=1)
    #         widget.label(label_text=f"VAT Number : {pdf_vat_number}", row=5, col=1)
    #         widget.label(label_text=f"QR Location X (cm): {setting_data['qr_loc_x']}", row=6, col=1)
    #         widget.label(label_text=f"QR Location Y (cm): {setting_data['qr_loc_y']}", row=7, col=1)
    #         widget.label(label_text=f"QR Code Size (cm): {setting_data['qr_size']}", row=8, col=1)
    #
    #         vat_amount = widget.edit_text(label_text="VAT", row=9)
    #         total_amount = widget.edit_text(label_text="Total", row=10)
    #
    #         # Prepare QR Code
    #         def prepare_qr_code_text() -> None:
    #             global qr_text
    #             qr_text = TLV()
    #             qr_text[0x01] = setting_data["company_name"].encode('UTF-8')
    #             qr_text[0x02] = pdf_vat_number.encode('UTF-8')
    #             qr_text[0x03] = pdf_date.encode('UTF-8')
    #             qr_text[0x04] = total.encode('UTF-8')
    #             qr_text[0x05] = vat.encode('UTF-8')
    #             print(qr_text)
    #             qr_text = base64.b64encode(qr_text.to_byte_array())
    #             create_qr_code(
    #                 pdf_file_path=field_value(pdf_file_path),
    #                 qr_loc_x=int(setting_data["qr_loc_x"]),
    #                 qr_loc_y=int(setting_data["qr_loc_y"]),
    #                 qr_size=int(setting_data["qr_size"]),
    #                 base_screen=create_statement_file_input_window
    #             )
    #
    #         def checking_vat_and_total() -> None:
    #             global vat, total
    #             if is_empty_field(vat_amount):
    #                 err_message_dialog(input_name="VAT")
    #             elif is_empty_field(total_amount):
    #                 err_message_dialog(input_name="Total")
    #             else:
    #                 vat = field_value(vat_amount)
    #                 total = field_value(total_amount)
    #                 prepare_qr_code_text()
    #
    #         widget.button(
    #             text="Submit",
    #             command=checking_vat_and_total,
    #             row=11,
    #             col=2
    #         )

    widget.button(
        text="Next",
        command=None,
        row=2,
        col=1
    )

    widget.button(
        text="Close Window",
        command=create_statement_file_input_window.destroy,
        row=2,
        col=2
    )


if __name__ == "__main__":
    root = Tk()
    root.title("QR Invoice APP")
    root.resizable(False, False)
    language_choice()
    root.mainloop()
