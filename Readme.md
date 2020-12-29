# pwd-manager

> command line password manager written in python

The password manager stores all your passwords in an encrypted `.pwdm` file in your HOME directory. The file is encrypted using a [Fernet algorithm](https://cryptography.io/en/latest/fernet.html?highlight=fernet#using-passwords-with-fernet) with your master password.

## Installation

1. clone this repository
2. cd into it
3. install with pip: `pip install .`

to verify the installation, try:

```shell
pwd-man --help
```

this should show all available commands:

```shell
usage: pwd-man [-h] {create,get,list,reset,delete,change_password} ...

Manage passwords for all your services

positional arguments:
  {create,get,list,reset,delete,change_password}
    create              creates a password for a service
    get                 copies password from service to your clipboard
    list                lists all services
    reset               resets all passwords - cannot be undone
    delete              deletes a service
    change_password     change your master password

optional arguments:
  -h, --help            show this help message and exit
```


## Features

+ all passwords stay on your machine
+ generate a random password if none provided
+ store an optional username with your password
+ copy the password to your clipboard
+ change your master password whenever you like




