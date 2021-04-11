from selenium import webdriver
from file_function import print_debug
from init_function import connect, init_verif, get_driver
from GUI import GUI, Login

open("./file/DEBUG.txt", "w", encoding="utf-8").close()

driver = get_driver()
init_verif(driver)

if "login" not in open(".\\file\\log.txt","r", encoding="utf-8").read():
    Login(driver).root.mainloop()
else:
    connect(driver)

gui = GUI(driver)
gui.Menu_1(gui.BG1)
gui.root.mainloop()

try:
    driver.close()
except:
    pass