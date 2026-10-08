import customtkinter as ctk
from PIL import Image, ImageTk
import ctypes
import webbrowser
import os
from configManager import loadConfig

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

config = loadConfig()
domains = config.get("rules", {})

#Customization
version = "1.0.0"
githubLink = "https://github.com/ojblaster/AutoUncompress"

bgColor = "#2C2C2C"
buttonColor = "#3F3F3F"
buttonHoverColor = "#4B4B4B"
redColor = "#F10000"
redHoverColor = "#CE0000"

fontL = ctk.CTkFont(family="Inter", weight="bold", size=25, slant="italic")
fontN = ctk.CTkFont(family="Inter", weight="bold", size=25)
fontS = ctk.CTkFont(family="Inter", weight="bold", size=15)

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

icon = ctk.CTkLabel(banner, image=iconImage, text="", corner_radius=5)
icon.pack(side="left", padx = (5,0))

seperator = ctk.CTkFrame(app, fg_color="Black", height=5, corner_radius=0)
seperator.pack(side="top", fill="both")

title = ctk.CTkLabel(banner, text=f"Chrome AutoRoute V{version} ", font=fontL)
title.pack(side="left", padx=10)

githubButton = ctk.CTkButton(banner, image=githubImage, text="", command=lambda: webbrowser.open(githubLink), width=0, fg_color=bgColor, hover_color=bgColor)
githubButton.pack(side="right", padx=5, pady=2)

pathFrame = ctk.CTkScrollableFrame(app, bg_color=buttonColor, height=35, corner_radius=0, orientation="horizontal")
pathFrame.pack(side="top", fill="x")
seperator1 = ctk.CTkFrame(app, fg_color="Black", height=5, corner_radius=0)
seperator1.pack(side="top", fill="both")

#App Functions and Variables
mainPage = ctk.CTkFrame(app, fg_color="transparent", corner_radius=0); mainPage.name = "Main Page"
urlRulesButton = ctk.CTkButton(mainPage, font=fontN, command=lambda: openPage(urlRules), fg_color=buttonColor, hover_color=buttonHoverColor, text="URL Rules", border_width=3, border_color="Black"); urlRulesButton.pack(fill = "both", padx=10, pady=10, expand=True)

urlRules = ctk.CTkScrollableFrame(app, fg_color="transparent", corner_radius=0); urlRules.name = "URL Rules"
def loadURLRules():
    for name, details in domains.items():
        domainSpecific = ctk.CTkFrame(app, fg_color="transparent", corner_radius=0); domainSpecific.name = name
        domainButton = ctk.CTkButton(urlRules, font=fontN, command=lambda p=domainSpecific: openPage(p), fg_color=buttonColor, hover_color=buttonHoverColor, text=name, border_width=3, border_color="Black"); domainButton.pack(fill = "both", padx=10, pady=10)
        
        domainTitle = ctk.CTkLabel(domainSpecific, text=name, font=fontL); domainTitle.pack(side="top", pady = 5, padx = 5)
        seperator2 = ctk.CTkFrame(domainSpecific, fg_color="White", height=4, corner_radius=2); seperator2.pack(side="top", fill="x", padx=10)
        unzipButton = ctk.CTkCheckBox(domainSpecific, text="Unzip any .zip files?", font=fontN, fg_color=redColor, hover_color=redHoverColor); unzipButton.pack(pady=5, side="top")

pageDirectory = []
def updateDirectory():
    for child in pathFrame.winfo_children():
        child.destroy()
    for page in pageDirectory:
        pageButton = ctk.CTkButton(pathFrame, font=fontN, text=page.name, width=0, command=lambda p=page:openPage(p), fg_color="transparent", hover=False)
        pageButton.pack(side="left", padx=5)
        pathSeperator = ctk.CTkLabel(pathFrame, text=">", font=fontS)
        pathSeperator.pack(side="left")        

def openPage(frame):
    global pageDirectory

    if not pageDirectory:
        pageDirectory.append(frame)
        print("start of dir")

        frame.pack(side="top", fill="both", expand="True")
        updateDirectory()
    elif frame != pageDirectory[-1]:
        currentPage = pageDirectory[-1]
        if not frame in pageDirectory:
            print("new page")
            pageDirectory.append(frame)

            frame.pack(side="top", fill="both", expand="True")
            updateDirectory()
        elif frame in pageDirectory:
            print("return page")
            pageDirectory = pageDirectory[:pageDirectory.index(frame) + 1]
        currentPage.pack_forget()

        frame.pack(side="top", fill="both", expand="True")
        updateDirectory()
    else: print("already on page")

openPage(mainPage)
loadURLRules()
print(domains)
app.mainloop()