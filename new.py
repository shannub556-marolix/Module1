import time
import webbrowser
import pyautogui as pgt


def Dropdown(n):
    time.sleep(1)
    for i in range(n):
        pgt.press("down")
    pgt.press("Enter")
    time.sleep(1)
    return


webbrowser.open('https://docs.google.com/forms/d/e/1FAIpQLSf0R5A-5ANJzxMbYL7JytYPRYbe4vYMyU_TvxX5cSXz1KEE6A/viewform')
time.sleep(4)
pgt.press("tab")
pgt.press("tab")
pgt.write("shannub556.marolix@gmail.com")
pgt.press("tab")
Dropdown(2)
pgt.press("tab")
pgt.press("down")
pgt.press("Enter")
time.sleep(1)
pgt.press("tab")
Dropdown(19)
pgt.press("tab")
Dropdown(43)
pgt.press("tab")
pgt.press("Enter")