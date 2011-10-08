#!/usr/bin/env python

'''
 Known bugs:
  Some programs don't start correctly. (Rare. Occurrences: 1)
   Workaround: Try again; it'll probably work the second time.
 To do:
  High: Fix button placement, window size. Use a counter?
  High: Allow customised program names and gif filenames in buttons
  Med:  Make the grid layout automatic.
  Low:  Fix window size auto-adjusting algorithm
  Low:  Customised program names?
  Low:  Sort by usage?
  Low:  More settings?
'''

# functools.partial() is used to prevent premature call of subprocess.Popen()
# May require Python 2.6+.
from functools import partial

import Tkinter as tk
import os
import subprocess

debug  = True

class Launcher:
    
    def __init__(self, master):
    
        self.master = master
        
        try:
            # Reads settings file, creates list of programs.
            with open("settings", "r") as settingsFile:
                # Carriage returns and line feeds are removed from the file path.
                self.progList = [
                    setting.replace("\r", "").replace("\n", "").split("#")[0].strip()
                    for setting in settingsFile if setting.split("#")[0] != ""]
                if debug: print(self.progList)
        except IOError:
            print("No settings file found...")
            raw_input()
            exit()
        
        # Tkinter window
        self.progNums = len(self.progList)
        self.program = range(self.progNums)
        self.image = range(self.progNums)
        
        self.buttonHeight = 48
        self.buttonWidth = 96
        
        # Button creation for each program
        for i in range(self.progNums):
            if debug:
                print("\nrow={0}".format(str((float(i) if i > 0 else i + 1))))
                print("column={0}".format(str(i * 2 / float(self.progNums))))
                print("progList index: {0}".format(i))
            try:
            
                name = self.progList[i].split(" {0}".format(os.sep))[0].split(os.sep)[-1].split(os.extsep)[0]
                if debug:
                    print("name: {0}".format(name))
                    print("image: Images{0}{1}{2}gif".format(os.sep, name, os.extsep))
                name = "".join(self.progList[i].split(os.extsep)[:-1]).split(os.sep)[-1]
                self.image[i] = tk.PhotoImage(file="Images{0}{1}{2}gif".format(os.sep, name, os.extsep))
                self.program[i] = tk.Button(self.master, compound=tk.TOP,
                    height=self.buttonHeight, width=self.buttonWidth, image=self.image[i],
                    text=name, command=partial(self.runProgram, self.progList[i]))
                    
                # Image garbage collection; leave this line in.
                self.program[i].image = self.image[i]
                # Warning: modulus and division by zero error
                try:
                    self.program[i].grid(row=i % 2, column=i // (self.progNums % 2))
                except ZeroDivisionError:
                    print("ZeroDivisionError")
                    self.program[i].grid(row=(i if i > 1 else 1), column=i // self.progNums)
                
            except:
                print("Unable to create button for {0}".format(self.progList[i]))
    
    def runProgram(self, progPath):
        # Some/most programs need to be launched from their path.
        os.chdir(os.sep.join(progPath.split(os.sep)[:-1]))
        
        subprocess.Popen(progPath)
        exit()

if __name__ == "__main__":
    
    root = tk.Tk()
    root.title("Launcher")
    root.iconbitmap(default="Images{0}Launcher.ico".format(os.sep))
    # Uncomment the next line when the window's auto-resizing is fixed.
    #root.resizable(False, False)
    app = Launcher(root)
    
    # Needs fixing; I can't maths.
    '''
    root.geometry("{0}x{1}".format(
        (app.buttonWidth + 8) * app.progNums / 2,
        (app.buttonHeight + 8) * (app.progNums / 3 if (app.progNums > 3) else 3)
    ))'''
    # For now:
    root.geometry("640x480")
    root.mainloop()
    