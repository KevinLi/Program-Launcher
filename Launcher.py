#!/usr/bin/env python

# Known bugs:
#  Some programs don't start correctly. (Rare. Occurrences: 1)
#   Workaround: Try again; it'll probably work the second time.
# To do:
#  Med:  Make the grid layout automatic.
#  Low:  Fix window size auto-adjusting algorithm
#  Low:  Customised program names?
#  Low:  Sort by usage?
#  Low:  More settings?

# functools.partial() is used to prevent premature call of subprocess.Popen()
# May require Python 2.6+.
from functools import partial

import Tkinter as tk
import os
import subprocess

class Launcher:
    
    def __init__(self, master):
        try:
            # Reads settings file, creates list of programs.
            with open("settings", "r") as settingsFile:
                # replace() used to remove carriage return and line feed from the file path.
                self.progList = [
                    setting.replace("\r", "").replace("\n", "").split("#")[0].strip()
                    for setting in settingsFile if setting.split("#")[0] != ""]
        except IOError:
            print("No settings file found...")
            raw_input()
            exit()
        
        # Tkinter window
        self.progNums = len(self.progList)
        self.program = range(self.progNums)
        self.image = range(self.progNums)
        
        self.master = master
        
        self.buttonHeight = 48
        self.buttonWidth = 96
        
        # Quit button. Actually, we don't even need one.
        # self.exit = tk.Button(self.master, text="QUIT", fg="red", command=self.master.quit)
        # self.exit.grid(row=self.progNums - 1, column=self.progNums + 1)
        
        # Button creation for each program
        for i in range(self.progNums):
            try:
                
                name = self.progList[i].split(" {0}".format(os.sep))[0].split(os.sep)[-1].split(os.extsep)[0]
                self.image[i] = tk.PhotoImage(file="Images{0}{1}{2}gif".format(os.sep, name, os.extsep))
                self.program[i] = tk.Button(self.master, compound=tk.TOP,
                    height=self.buttonHeight, width=self.buttonWidth, image=self.image[i],
                    text=name, command=partial(self.runProgram, self.progList[i]))
                
                # Image garbage collection; leave this line in.
                self.program[i].image = self.image[i]
                
                self.program[i].grid(row=i % 3, column=int(i / 3))
            except:
                pass
    
    def runProgram(self, progPath):
        
        # Some/most programs need to be launched from their path.
        # Changes directory to the program's path before running it.
        os.chdir(os.sep.join(progPath.split(os.sep)[:-1]))
        
        subprocess.Popen(progPath)
        
        # Launcher exits.
        exit()

if __name__ == "__main__":
    
    root = tk.Tk()
    root.title("Launcher")
    root.iconbitmap(default="Images{0}Launcher.ico".format(os.sep))
    #root.resizable(False, False)
    app = Launcher(root)
    
    # Needs fixing; I can't maths.
    root.geometry("{0}x{1}".format(
        app.buttonWidth * app.progNums / 3 + app.buttonHeight,
        app.buttonHeight * app.progNums / 4 + app.buttonWidth
    ))
    
    root.mainloop()

