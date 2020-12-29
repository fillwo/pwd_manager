import argparse
from pathlib import Path
import os
import json
import string
import random
from .crypter import decrypt, encrypt
from getpass import getpass
import sys
import pyperclip

# ----------------------------- helper functions ----------------------------- #
def save_pwd_file(target_path, pwds, pwd):
    """encrypts & saves pwd object file

    Args:
        target_path (string): target path
        pwds (object): the object to save
        pwd (string): the master password
    """
    encrypted = encrypt(json.dumps(pwds).encode(), pwd.encode())
    with open(target_path, "wb") as cfile:
        cfile.write(encrypted)

def list_all_services(pwds):
    print("Your Services:")
    for key in pwds:
        print(key)

def create_random_password(n = 10):
    letters = string.ascii_letters + string.digits + "!?$&"
    return ''.join(random.SystemRandom().choice(letters) for _ in range(n))


def main():
    # ----------------------- parsing commandline arguments ---------------------- #
    parser = argparse.ArgumentParser(description="Manage passwords for all your services")
    subparsers = parser.add_subparsers(dest="cmd")
    subparsers.required = True

    parser_create = subparsers.add_parser("create", help="creates a password for a service")
    parser_create.add_argument("service", type=str, help="name of the service")
    parser_create.add_argument("-p", "--password", type=str, help="uses user defined password instead of creating one")
    parser_create.add_argument("-u", "--username", type=str, help="save a user name for the service")

    parser_get = subparsers.add_parser("get", help="copies password from service to your clipboard")
    parser_get.add_argument("service", type=str, help="name of the service")

    parser_list = subparsers.add_parser("list", help="lists all services")
    parser_list.add_argument("-v", "--verbose", action="store_true", default=False, help="prints the passwords to console")

    parser_reset = subparsers.add_parser("reset", help="resets all passwords - cannot be undone")
    parser_reset.add_argument("--hard", action="store_true", default=False, help="does not prompt for your master password (in case you forgot it)")

    parser_delete = subparsers.add_parser("delete", help="deletes a service")
    parser_delete.add_argument("service", type=str, help="name of the service")

    subparsers.add_parser("change_password", help="change your master password")

    args = parser.parse_args()
    # print("debug args: {}".format(args))

    # --------------------------- handling the pwd file -------------------------- #
    home_path = str(Path.home())
    pwd_file_path = os.path.join(home_path, ".pwdm")
    file_exists = os.path.exists(pwd_file_path)

    # ----------------- allow hard reset without password prompt ----------------- #
    if args.cmd == "reset" and args.hard:
        os.remove(pwd_file_path)
        print("removed password file: {}".format(pwd_file_path))
        sys.exit()

    # -------------------------- change master password -------------------------- #
    if args.cmd == "change_password":
        if not file_exists:
            print("cannot change password: no password set yet")
            sys.exit()
        old_pwd = getpass("Enter old password:\n")
        with open(pwd_file_path, "rb") as pfile:
            success, decrypted = decrypt(pfile.read(), old_pwd.encode())
            if not success:
                print("wrong password!")
                sys.exit()
            pwds = json.loads(decrypted.decode())
        new_pwd = getpass("Enter new password:\n")
        confirm_new_pwd = getpass("Confirm new password:\n")
        if new_pwd != confirm_new_pwd:
            print("passwords do not match!")
            sys.exit()
        save_pwd_file(pwd_file_path, pwds, new_pwd)
        print("changed password")
        sys.exit()

    # ------------------------------ password prompt ----------------------------- #
    if not file_exists:
        master_pwd = getpass("Enter a strong master password to encrypt your other passwords:\n")
        confirm_pwd = getpass("Confirm password:\n")
        if master_pwd != confirm_pwd:
            print("passwords do not match!")
            sys.exit()
    else:
        master_pwd = getpass("Enter password:\n")

    if file_exists:
        with open(pwd_file_path, "rb") as pfile:
            success, decrypted = decrypt(pfile.read(), master_pwd.encode())
            if not success:
                print("wrong password!")
                sys.exit()
            pwds = json.loads(decrypted.decode())
    else:
        pwds = {}


    # ---------------------------------------------------------------------------- #
    #                              main programm logic                             #
    # ---------------------------------------------------------------------------- #

    # ------------------------------- create entry ------------------------------- #
    if args.cmd == "create":
        if args.service in pwds:
            print("service already exists!")
            sys.exit()

        if args.password:
            password_for_service = args.password
        else:
            password_for_service = create_random_password()
            print("created random password for {}: {}".format(args.service, password_for_service))
            pyperclip.copy(password_for_service)
            print("password has been copied to clipboard")
        
        p_entry = {"pwd": password_for_service}
        if args.username:
            p_entry["username"] = args.username

        pwds[args.service] = p_entry
        save_pwd_file(pwd_file_path, pwds, master_pwd)

    # --------------------------------- get entry -------------------------------- #
    elif args.cmd == "get":
        if args.service not in pwds:
            print("service does not exist!")
            sys.exit()

        entry = pwds[args.service]
        if "username" in entry:
            print("{} (username: {})".format(args.service, entry["username"]))
        else:
            print(args.service)
        pyperclip.copy(entry["pwd"])
        print("password has been copied to clipboard")

    # ----------------------------- reset everything ----------------------------- #
    elif args.cmd == "reset":
        os.remove(pwd_file_path)
        print("removed password file: {}".format(pwd_file_path))

    # ------------------------------- list services ------------------------------ #
    elif args.cmd == "list":
        if len(pwds.keys()) == 0:
            print("No services created yet!")
            sys.exit()
        
        print("Your Services:\n")
        for key, value in pwds.items():
            if "username" in value:
                if args.verbose:
                    print("{} (username: {}) - password: {}".format(key, value["username"], value["pwd"]))
                else:
                    print("{} (username: {})".format(key, value["username"]))
            else:
                if args.verbose:
                    print("{} - password: {}".format(key, value["pwd"]))
                else:
                    print(key)
        
        print("\n")

    # ----------------------------- delete a service ----------------------------- #
    elif args.cmd == "delete":
        if args.service not in pwds:
            print("service does not exist!")
            sys.exit()
        
        del pwds[args.service]
        save_pwd_file(pwd_file_path, pwds, master_pwd)
        print("deleted service {}".format(args.service))
        
    else:
        pass





