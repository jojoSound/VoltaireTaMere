import json
from tkinter import Tk, Toplevel, Label, PhotoImage, Button
import webbrowser
from selenium import webdriver
from selenium.webdriver.chrome.options import Options as chrome_options
from selenium.webdriver.firefox.options import Options as firefox_options
from selenium.webdriver.opera.options import Options as opera_options
from file_function import print_debug, found_data

class pop_up:
    def __init__(self, cmd, parent=None):
        self.cmd = cmd
        self.size = cmd.get("size")
        self.txt = cmd.get("text")
        if self.txt:
            self.txt = self.txt.replace("\\n","\n")
        self.title = cmd.get("title")
        self.link = cmd.get("link")
        self.lock = cmd.get("lock")
        if parent:
            self.root = Toplevel(parent)
        else:
            self.root = Tk()
            self.root.iconphoto(True, PhotoImage(file = "asset\\VoltaireTaMere_icon[PNG].png"))
        self.root.title(self.title)
        self.root.resizable(False, False)
        self.root.geometry(self.size)
        self.root.configure(bg='#23272A')

        Label(self.root, text=self.txt, bg='#23272A', fg='#ffffff', font=('Helvetica', '10',"bold")).pack()

        Button(self.root,
                        text="  OK  ",
                        command=lambda: [self.open_link(), self.root.destroy(), self.stop()],  
                        bg="#a2d417",
                        fg="#ffffff",
                        activebackground  ="#a2d417",
                        bd=0).pack()
    
    def open_link(self):
        if self.link != None:
            webbrowser.open_new(self.link)

    def stop(self):
        if self.lock:
            exit()

def connect(driver):
    try:
        driver.find_element_by_id("btn_home_sortir").click()
    except:
        pass
    driver.get("https://www.projet-voltaire.fr/voltaire/com.woonoz.gwt.woonoz.Voltaire/Voltaire.html?returnUrl=www.projet-voltaire.fr/choix-parcours/&applicationCode=pv")
    
    if found_data("./file/options.txt", "auto_login"):
        logIn= found_data(".\\file\\log.txt", "login")
        mdp = found_data(".\\file\\log.txt", "mdp")
        
        driver.find_element_by_id("user_pseudonym").send_keys(logIn)
        driver.find_element_by_id("user_password").send_keys(mdp)
        driver.find_element_by_id("login-btn").click()
        
def get_driver():
    try:
        driver = webdriver.Chrome()
    except:
        print_debug("[DRIVER] don't detect Chrome","yellow")
        try:
            driver = webdriver.Opera()
        except:
            print_debug("[DRIVER] don't detect Opera","yellow")
            try:
                driver = webdriver.Firefox() 
            except:
                print_debug("[DRIVER] Failed to detect driver","red")
                pop_up(json.loads('{"text":"aucun moteur\\n de recherche detecté \\n(chrome, opera ou firefox)", "title":"VoltaireTaMere", "link":"https://www.google.com/intl/fr_fr/chrome/", "lock":true, "size":"180x90"}')).root.mainloop()
                exit()

    driver.implicitly_wait(1)
    return driver

def init_verif(driver, parent=None):
    driver.get("https://sites.google.com/view/voltairetamere/init")
    cmd = json.loads(driver.find_element_by_class_name("yaqOZd").text)
    driver.get("https://sites.google.com/view/voltairetamere/load")
    print(cmd.get("version"), found_data("./file/version.txt", "version"))
    if cmd.get("version") != found_data("./file/version.txt", "version"):
        pp_cmd = {"text":"VoltaireTaMere doit être\\n mis à jour", "title":"VoltaireTaMere", "link":"https://sites.google.com/view/voltairetamere/accueil", "lock":True, "size":"180x70"}
        pop_up(pp_cmd, parent).root.mainloop()
        exit()
    
    if cmd.get("title"):
        pop_up(cmd).root.mainloop()
        if cmd.get("lock"):
            exit()
