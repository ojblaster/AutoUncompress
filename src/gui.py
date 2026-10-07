import customtkinter as ctk
from PIL import Image, ImageTk
import ctypes
import webbrowser
import os

try:
    myappid = 'ChromeAutoRoute' 
    ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)
except: pass

#App init
ctk.set_appearance_mode("dark")
app = ctk.CTk()
app.geometry("1200x800")
app.title("Chrome AutoRoute")
app.minsize(800, 500)

#Customization
version = "1.0.0"
githubLink = "https://github.com/ojblaster/AutoUncompress"

bgColor = "#2C2C2C"
buttonColor = "#3F3F3F"
buttonHoverColor = "#4B4B4B"
black = "#000000"
redColor = "#F10000"
redHoverColor = "#CE0000"

fontL = ctk.CTkFont(family="Inter", weight="bold", size=25, slant="italic")
fontN = ctk.CTkFont(family="Inter", weight="bold", size=25)

#Images
src = os.path.dirname(os.path.abspath(__file__))
root = os.path.dirname(src)
assets = os.path.join(root, "assets")

iconImage = ctk.CTkImage(light_image=Image.open(f"{assets}\\icon.png"), dark_image=Image.open(f"{assets}\\icon.png"), size=(45, 45))
githubImage = ctk.CTkImage(light_image=Image.open(f"{assets}\\github.png"), dark_image=Image.open(f"{assets}\\github.png"), size=(45,45))

app.iconbitmap(f"{assets}\\icon.ico")

#Top banner
banner = ctk.CTkFrame(app, bg_color=buttonColor, height=50, corner_radius=0)
banner.pack_propagate(False)
banner.pack(side="top", fill="x")

icon = ctk.CTkLabel(banner, image=iconImage, text="")
icon.pack(side="left")

seperator = ctk.CTkFrame(app, fg_color=black, height=5, corner_radius=0)
seperator.pack(side="top", fill="both")

title = ctk.CTkLabel(banner, text=f"Chrome AutoRoute V{version} ", font=fontL)
title.pack(side="left", padx=10)

githubButton = ctk.CTkButton(banner, image=githubImage, text="", command=lambda: webbrowser.open(githubLink), width=0, fg_color=bgColor, hover_color=bgColor)
githubButton.pack(side="right", padx=5)

#App Functions and Variables
mainPage = ctk.CTkFrame(app, fg_color="blue", corner_radius=0)

pageDirectory = []
def openPage(frame):
    if not pageDirectory:
        pageDirectory.append(frame)
    elif frame != pageDirectory:
        currentPage = pageDirectory[-1]
        if not frame in pageDirectory:
            pageDirectory.append(frame)
        elif frame in pageDirectory:
            items = items[:items.index(target) + 1]
        
        frame.pack(side="top", fill="both", expand="True")

openPage(mainPage)
app.mainloop()