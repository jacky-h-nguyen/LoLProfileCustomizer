import tkinter as tk
from tkinter import ttk
from tkinter import *
from lcu_driver import Connector # pip install lcu-driver

global IconID
global unownedIconID
global backgroundID

root = tk.Tk()
root.title("LoL Profile Customizer")
tabControl = ttk.Notebook(root) #creating multiple tabs

tab1 = ttk.Frame(tabControl) #tabs 1 to 4
tab2 = ttk.Frame(tabControl)
tab3 = ttk.Frame(tabControl)
tab4 = ttk.Frame(tabControl)

tabControl.add(tab1, text='Icons') #label for tabs
tabControl.add(tab4, text='Unowned Icons')
tabControl.add(tab2, text='Profile Background')
tabControl.add(tab3, text='Chat Rank')
tabControl.pack(expand=1, fill="both")

def changeIcon(): #method that connects lcu driver to client and changes summoner icon based on inputted icon ID
    x1 = iconInput.get()
    connector = Connector()
    global IconID
    IconID = x1
    async def setIcon(connection):
        await connection.request('put', '/lol-summoner/v1/current-summoner/icon',data={'profileIconId': IconID})

    @connector.ready  # when LCU API is ready to be used
    async def connect(connection):
        await setIcon(connection)

    connector.start()

def changeUnownedIcon(): #method that connects lcu driver to client and changes summoner icon based on inputted icon ID, even if the icon is unowned
    x1 = unownedIconInput.get()
    connector = Connector()
    global unownedIconID
    unownedIconID = x1
    async def setIcon(connection):
        await connection.request('put', '/lol-chat/v1/me/',data={"icon": unownedIconID})

    @connector.ready  # when LCU API is ready to be used
    async def connect(connection):
        await setIcon(connection)

    connector.start()

label2 = Label(tab1, text="Enter Icon ID: ", font=('helvetica', 14)).pack()
iconInput = tk.Entry(tab1)
iconInput.pack()
button1 = Button(tab1, text='Change Icon', command=changeIcon, bg='brown', fg='white', font=('helvetica', 9, 'bold')).pack()

label2 = Label(tab4, text="Enter Icon ID: ", font=('helvetica', 14)).pack()
unownedIconInput = tk.Entry(tab4)
unownedIconInput.pack()
button1 = Button(tab4, text='Change to Unowned Icon', command=changeUnownedIcon, bg='brown', fg='white', font=('helvetica', 9, 'bold')).pack()

def changeBG(): #method that connects lcu driver to client and changes profile background based on inputted skin ID
    x1 = backgroundInput.get()
    connector = Connector()
    global backgroundID
    backgroundID = x1
    async def setBackground(connection):
        await connection.request('post', '/lol-summoner/v1/current-summoner/summoner-profile',data={"key": "backgroundSkinId", "value": backgroundID})
    @connector.ready  #when LCU API is ready to be used
    async def connect(connection):
        await setBackground(connection)
    connector.start()

label2 = Label(tab2, text="Enter Background ID: ", font=('helvetica', 14)).pack()
backgroundInput = Entry(tab2)
backgroundInput.pack()
button1 = Button(tab2, text='Change Background', command=changeBG, bg='brown', fg='white', font=('helvetica', 9, 'bold')).pack()
Label(tab2, text=" ", font=('helvetica', 14)).pack()

label3 = Label(tab3, text="Change Chat Rank: ", font=('helvetica', 14)).pack(side=TOP)
GameModeList = ["ranked_tft", "ranked_solo_5x5", "ranked_flex_sr", "ranked_flex_tt"]
RankList = ["Challenger", "Grandmaster", "Master", "Diamond", "Platinum", "Gold", "Silver", "Bronze", "Iron"]
DivisonList = ["I", "II", "III", "IV"]
variable0 = StringVar(root)
variable = StringVar(root)
variable2 = StringVar(root)
variable0.set(GameModeList[1])
variable.set(RankList[0])
variable2.set(DivisonList[0])
opt0 = OptionMenu(tab3, variable0, *GameModeList)
opt0.pack()
opt = OptionMenu(tab3, variable, *RankList)
opt.pack()
opt2 = OptionMenu(tab3, variable2, *DivisonList)
opt2.pack()
Label(tab3, text=" ", font=('helvetica', 14)).pack(side=TOP)

def changeRank(*args): #method that changes chat rank display
    connector = Connector()
    async def setRank(connection):
        await connection.request('put', '/lol-chat/v1/me',data={"lol": {"rankedLeagueTier": variable.get(), "rankedLeagueDivision": variable2.get(), "rankedLeagueQueue": variable0.get()}})
    @connector.ready  #when LCU API is ready to be used
    async def connect(connection):
        await setRank(connection)
    connector.start()

variable0.trace('w', changeRank)
variable.trace('w', changeRank)
variable2.trace('w', changeRank)

root.mainloop()