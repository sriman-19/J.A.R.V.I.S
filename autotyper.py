import pyautogui
import time
import random

def write_code_online_gdb(filepath="scanned_solution.txt", min_speed=0.02, max_speed=0.08):  # Human-like speed range
    """Reads code from scanned_solution.txt and types it into OnlineGDB with human-like speed variations."""
    try:
        with open(filepath, 'r') as f:
            code = f.read()
    except FileNotFoundError:
        print(f"Error: File '{filepath}' not found. Make sure it's in the same directory as the script.")
        return

    print("You have 5 seconds to switch to the browser window with OnlineGDB.")
    time.sleep(5)


    for i, line in enumerate(code.splitlines()):
        stripped_line = line.lstrip()

        if 'int main()' in stripped_line:
            pyautogui.hotkey('ctrl', 'home')

        for char in stripped_line: # Type character by character
            typing_speed = random.uniform(min_speed, max_speed)  # Vary typing speed for each char
            pyautogui.typewrite(char, interval=typing_speed)  # Type the individual character
           # time.sleep(random.uniform(0.01, 0.05)) # Optionally, small random pauses between characters

        pyautogui.press('enter')
        time.sleep(random.uniform(0.1, 0.3))  # Random pause between lines




def main():
    write_code_online_gdb() # Use default filename and human-like speed


if __name__ == "__main__":
    main()