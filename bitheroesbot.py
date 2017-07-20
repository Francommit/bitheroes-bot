import pyautogui, time, webbrowser, os, sys, random, copy, datetime, requests
from retrying import retry

# Initialize globals
logText = "Log File: \n \n"
familiarCounter = 0


def main():

    try:
        loadGame()

        i = 0
        questsToDo = 20

        while i < questsToDo:
	        beginQuest("z5","z5_d3","normal")
	        i += 1

        # TO-DO: Get the raid pictures in the correct resolution.
        # beginRaid("r2","normal")

    except Exception as e:
        logMessages(str(e))
        
    finally:
        shutDownPc()

def energyCalculator():
    totalEnergy = 204
    minutesTillEnergyRegeneration =4


def checkPatch():
    if checkForImageIterations("news"):
        logMessages('New patch is here. Closing popup.')
        clickButtonIterations("doNotShowThisAgain")
        clickButtonIterations("newsClose")
    else:
        logMessages('No new patch.')


def shutDownPc():
    time.sleep(10)
    os.system('shutdown -s')

def loadGame():
    time.sleep(2)

    os.system("start \"\" http://www.kongregate.com/games/Juppiomenz/bit-heroes?acomplete=bit+heroes")
    waitUntilLoaded()
    checkPatch()
    logMessages("BitHeroes bot started.")


def beginQuest(zonelevel,dungeonlevel,difficulty):
    clickButtonIterations("quest",4)
    setZone(zonelevel)
    startDungeon(dungeonlevel,difficulty)
    checkDungeonStatus()


@retry(stop_max_attempt_number=100)
def waitUntilLoaded():
    i = 0

    while i < 4:
        region = pyautogui.locateCenterOnScreen(imPath("quest"+str(i)+".png"))

        if region is None:
            logMessages("Still loading...")
            i +=1
        else:
            logMessages("Game loaded!")
            return

        time.sleep(1)
    
    raise Exception("Still not loaded.")


def logMessages(message):
    global logText
    print(str(datetime.datetime.now()) + " " + message)
    logText += str(datetime.datetime.now()) + " " + message + "\n"



@retry(stop_max_attempt_number=1000)
def checkDungeonStatus():
    global familiarCounter
    i = 0

    while i < 3:

        try:
            questCompleted = pyautogui.locateCenterOnScreen(imPath("yes"+str(i)+".png"))
            persuadeFamiliar = pyautogui.locateCenterOnScreen(imPath("persuade"+str(i)+".png"))
            defeatedState = pyautogui.locateCenterOnScreen(imPath("defeat"+str(i)+".png"))
        except Exception as e:
            logMessages("we broked fam" + str(e))

        if questCompleted is None:
            i +=1
        else:
            logMessages("Quest finished.")
            clickButtonIterations("yes")
            time.sleep(5)
            pyautogui.press("esc")
            return

        if persuadeFamiliar is None:
            logMessages("Iterator "+ str(i) +" Familiar count:" + str(familiarCounter))
        else:
            familiarCounter += 1
            logMessages("Found a god damn familiar!")
            clickButtonIterations("persuade")
            clickButtonIterations("confirmYes")

        if defeatedState is not None:
            logMessages("u ded ningga")
            clickButtonIterations("defeat")
            clickButtonIterations("close")

        time.sleep(1)

    raise Exception("Still not cleared.")


def setZone(zone):
    availableZones = ["z3","z4","z5","z1","z2"]
    totalZonesFromStartingZone = 3

    i = 0

    logMessages("Trying to set the zone to " + str(zone))

    while i < totalZonesFromStartingZone:
        if checkForImageIterations(zone,4):
            logMessages("Zone is selected as " + str(zone))
            return
        else:
            i += 1
            logMessages("Moving to the next quest zone.")
            clickButtonIterations('zoneRight')


def startDungeon(dungeon,difficulty):
    clickButtonIterations(dungeon)
    clickButtonIterations(difficulty)
    clickButtonIterations("accept")


def beginRaid(raidlevel,difficulty):
    clickButtonIterations("raid")
    selectRaid(raidlevel)
    clickButtonIterations(difficulty)
    clickButtonIterations("accept")
    checkDungeonStatus()


def selectRaid(raidlevel):
    setRaidLevel(raidlevel)
    # To-Do: Need to get three Summon images
    clickButtonIterations("summon")


def setRaidLevel(raidlevel):
    availableRaids = ["r1","r2","r3"]

    for raidSelected in availableRaids:

        time.sleep(0.5)
        logMessages("Checking if raid is set to " + raidlevel)
        region = pyautogui.locateOnScreen(imPath(raidlevel+".png"))

        if region is None:
            clickButtonIterations("change_raid")
        else:
            logMessages("Raid set to " + raidlevel)
            return


def checkForImageIterations(imagename,iteratorNumber = 3):
    i = 0

    while i < iteratorNumber:
        logMessages("Finding " + imagename + str(i)+" image...")
        region = pyautogui.locateCenterOnScreen(imPath(imagename+str(i)+".png"))

        if region is None:
            logMessages("Could not find " + imagename + " on screen. Is the game visible?")
            i +=1
        else:
            logMessages("Found " + imagename + " button at : " + str(region))
            time.sleep(1)
            return True

        time.sleep(1)

    return False


@retry(stop_max_attempt_number=5)
def clickButtonIterations(buttonname,iteratorNumber = 3):
    i = 0

    while i < iteratorNumber:
        region = pyautogui.locateCenterOnScreen(imPath(buttonname+str(i)+".png"))

        if region is None:
            logMessages("Looking for: " + buttonname + str(i))
            i +=1
        else:
            pyautogui.click(region, duration=0.25)
            logMessages("Found: "+ buttonname + str(i))
            return

        time.sleep(1)

    raise Exception("Could not locate button")


def imPath(filename):
    return os.path.join('images', filename)

if __name__ == "__main__":
    main()