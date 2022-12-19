 
#notactualcode

from tkinter import *
import random
import time
from tkinter import ttk
from tkinter import messagebox
import sqlite3

def system():
    root = Tk()
    root.geometry("1700x800")
    root.title("Coffee Shop Management")

# Topframe
topframe = Frame(bg="floral white", width=1600, height=50)
topframe.pack(side=TOP)

# Leftframe
leftframe = Frame(width=900, height=700)
leftframe.pack(side=LEFT)

# rightframe
rightframe = Frame(width=400, height=700)
rightframe.pack(side=RIGHT)
