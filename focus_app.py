from time import sleep
from pyautogui import hotkey
from sys import stdout, argv
from threading import Thread
from os import chdir, path, system
from win11toast import toast
import json


def main():

    # clear terminal and prompt for time
    system("cls")
    print("Welcome to \"Focus App\", how long would you like to focus before a break?")
    total_time_min = int(input("Enter time (in minutes): "))
    total_time_sec = int(input("Enter time (in seconds): "))
    print("Timer set!")
    remaining_in_s = (total_time_min * 60) + total_time_sec # convert time to seconds for sleep function
    
    system("cls") # clear terminal

    # create new thread to run countdown to avoid timing discrepencies
    countdown = Thread(target=lambda: track_countdown(remaining_in_s))
    countdown.start() # start the thread (tracking the countdown)

    # sleep for inputted seconds
    sleep(remaining_in_s)
    countdown.join() # join the thread so the screen doesn't clear before the timer has finished
    print("Break time!")
    hotkey("winleft", "d") # minimize all windows

    # send notification on break time
    toast("You are now on break time! - Focus App", "To return reopen the terminal session.")
    system("cls")

    # prompt to restart
    if input("Start again? (Y/n)").upper() == "Y":
        main()
    else:
        print("Exiting...")
        system("cls")

# convert total number of seconds to an f-string that looks pretty
def sec_to_str(sec):
    total_min = sec // 60
    total_hour = total_min // 60
    disp_min = total_min - (total_hour * 60)
    disp_sec = sec - (total_min * 60)
    return f"{"0" if total_hour < 10 else ""}{total_hour}:{"0" if disp_min < 10 else ""}{disp_min}:{"0" if disp_sec < 10 else ""}{disp_sec}s"

# function to keep track of how much time remains concurrently
def track_countdown(r_i_s):
    left = r_i_s
    while left >= 0:
        
        # clear previous line
        stdout.write("\x1b[1A")
        stdout.write("\x1b[2K")

        # print out current time remaining and decrement
        print(f"Time remaining: {sec_to_str(left)}")
        sleep(1)
        left -= 1

# lazy function to install missing modules
def setup():

    # change working directory to location of python script
    abspath = path.abspath(__file__)
    dname = path.dirname(abspath)
    chdir(dname)

    # cheat to install modules because I have a life
    with open("setup.json", "r") as f:
        setup_details = json.load(f)
        if setup_details["fresh"]:
            for mod in setup_details["modules"]:
                print("Attempting to install module with \"python\":", mod)
                system(f"python -m pip install {mod}")
                print("Attempting to install module with \"python3\":", mod)
                system(f"python3 -m pip install {mod}")
            setup_details["fresh"] = False
            with open("setup.json", "w") as f:
                f.write(json.dumps(setup_details))
            
            print("\nAll modules installed!")
            sleep(1)

if __name__ == "__main__":
    setup()
    main()