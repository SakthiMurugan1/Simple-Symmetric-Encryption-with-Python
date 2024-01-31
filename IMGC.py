from tkinter import *
import tkinter.filedialog as tkFileDialog
import tkinter.messagebox as tkMessageBox
from tkinter.filedialog import askopenfilename
from PIL import Image
from Crypto.Cipher import AES
import random
import os

def encrypt(filename, key):
    chunk_size = 64*1024
    if (len(key)>32):
        key = key[:len(s)-(len(s)-32)]
    elif (len(key)<32):
        key = key + '\0' * (32-len(key))
    output_file = filename+".enc"
    file_size = str(os.path.getsize(filename)).zfill(16)
    with open(filename, 'rb') as inputfile:
        with open(output_file, 'wb') as outf:
            while True:
                chunk = inputfile.read(chunk_size)
                if len(chunk) == 0:
                    break
                elif len(chunk) % 16 != 0:
                   chunk += ' '*(16 - len(chunk)%16)
                IV=''
                for i in range(16):
                    IV += chr(random.randint(65, 91))
                encryptor = AES.new(key, AES.MODE_CBC, IV)
                outf.write(str.encode(IV))
                outf.write(encryptor.encrypt(chunk))                       
    enc_success(output_file)
    
def decrypt(filename, key):
    chunk_size = 64*1024
    if (len(key)>32):
        key = key[:len(s)-(len(s)-32)]
    elif (len(key)<32):
        key = key + '\0' * (32-len(key))
    output_file = filename[:-4]
    IV = ''
    with open(filename, 'rb') as inf:
        with open(output_file, 'wb') as outf:
            while True:
                IV = ''
                IV = inf.read(16)
                if len(IV)!=16:
                    break
                decryptor = AES.new(key, AES.MODE_CBC, IV)
                chunk = inf.read(chunk_size)
                if len(chunk)==0:
                    break
                outf.write(decryptor.decrypt(chunk))
    dec_success(output_file)
  
def enc_success(imagename):
    tkMessageBox.showinfo("Success","Encrypted Image: " + imagename)

def dec_success(imagename):
    tkMessageBox.showinfo("Success","Decrypted Image: " + imagename)
    img = Image.open(imagename)
    img.show()
   
def key_alert():
    tkMessageBox.showinfo("Key Alert","Please enter a key.")
   
def image_open():
    enc_key = keyfield.get()
    if enc_key == "":
        key_alert()
    else:
        filename = askopenfilename()
        encrypt(filename,enc_key)

def cipher_open():
    dec_key = keyfield.get()
    if dec_key == "":
        key_alert()
    else:
        filename = askopenfilename()
        decrypt(filename,dec_key)

class App:
    def __init__(self, master):
        global keyfield
        title = "Image Transfer Security"
        msgtitle = Message(master, text =title)
        msgtitle.config(font=('arial', 17, 'bold'), width=200)
        msgtitle.pack()
        
        keylabel = Label(master, text="Enter Encrypt/Decrypt Key:")
        keylabel.pack()
        keyfield = Entry(master, width=20)
        keyfield.pack()
    
        self.encrypt = Button(master, text="Encrypt", fg="black",
                              command=image_open, width=25,height=3)
        self.encrypt.pack(side=LEFT)
        self.decrypt = Button(master,text="Decrypt", fg="black",
                             command=cipher_open, width=25,height=3)
        self.decrypt.pack(side=RIGHT)

IMGC = Tk()
IMGC.wm_title("Image Encryption")
app = App(IMGC)
IMGC.mainloop()
