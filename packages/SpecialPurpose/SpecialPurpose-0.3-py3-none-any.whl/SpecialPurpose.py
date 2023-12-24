import string 
import pyfiglet
def clean(x):
    result=[]
    for i in list(x) :
        if i not in string.punctuation and i != '\n':
            result.append(i)
    return "".join(result)

def welcome():
    welcome = pyfiglet.figlet_format("Welcome to MonieCrypt",font="slant")
    print(welcome)

def readFile():
    while True:
        try:
            infile = input("Enter the input filename : ")
            file = open(infile,"r")
            break
        except:
            print(f"{infile} doesnt exist in this directory ! ")
    return infile


def writeFile(text):
    outFile = input("Enter output filename : ")
    file = open(outFile,"w")
    print(text,file=file)
    return outFile


def keyORanalysis():
    while True:
        key_present = input("Do you have a key ? (Yes/No)")
        if key_present.lower()=="yes":
            return True
        elif key_present.lower()=="no":
            print("We are doing frequency analysis.")
            return False
        else:
            print("Try again")
def getKey():
    key = input("Enter key : ")
    key = clean(key)
    return key


def prep_cipher_text(file):
    ciphered = list(map(clean,file.read().split()))
    return " ".join(ciphered)


def oldEnc():
    pass

def newEnc():
    key = getKey()
    
def oldDec():
    pass

def newDec():
    pass

