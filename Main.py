import datetime
from email import message
import webbrowser
from idlelib.autocomplete import FILES
import pyaudio
from numpy import tile
import pyttsx3
import speech_recognition
import requests
from bs4 import BeautifulSoup
import os
import pyautogui
from playsound import playsound
import random
from plyer import notification
from pygame import mixer
import speedtest
from spotipy.oauth2 import SpotifyOAuth
import spotipy
import pytesseract
from PIL import Image
import time
import subprocess
import multiprocessing
import threading
import sys
import queue
#from INTRO import play_gif
#play_gif
import cv2
from deepface import DeepFace
from datetime import datetime
engine = pyttsx3.init("sapi5")
voices = engine.getProperty("voices")
engine.setProperty("voice", voices[0].id)
rate = engine.setProperty("rate",170)
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
# Function to start Brain.py and get authorization status
auth_queue=queue.Queue()
def perform_face_recognition():
    cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
    if not cap.isOpened():
        print("Error opening camera", file=sys.stderr)
        return "Error"

    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

    try:
        reference_img = cv2.imread("authorised_pic.jpg")
        if reference_img is None:
            raise FileNotFoundError("authorised_pic.jpg not found")
    except FileNotFoundError as e:
        print(f"Error: {e}", file=sys.stderr)
        return "Error"

    face_match = False
    counter = 0

    while True:
        ret, frame = cap.read()
        if not ret:
            print("Error reading from camera", file=sys.stderr)
            break

        if counter % 30 == 0:
            try:
                if check_face(frame.copy(), reference_img.copy()):  # Pass reference image
                    face_match = True
                    break
            except ValueError as e:
                print(f"DeepFace error: {e}", file=sys.stderr)

        counter += 1

    cap.release()

    return "Authorized" if face_match else "Unauthorized"

def check_face(frame, reference_img):  # Accept reference image as argument
    try:
        verification_result = DeepFace.verify(frame, reference_img, enforce_detection=False)
        return verification_result["verified"]
    except ValueError as e:
        print(f"Error in check_face(): {e}", file=sys.stderr)
        raise

def speak(audio):
    engine.say(audio)
    engine.runAndWait()

def takeCommand():
    r = speech_recognition.Recognizer()
    with speech_recognition.Microphone() as source:
        print("Listening.....")
        r.pause_threshold = 1
        r.energy_threshold = 300
        audio = r.listen(source,0,4)

    try:
        print("Understanding..")
        query  = r.recognize_google(audio,language='en-in')
        print(f"You Said: {query}\n")
    except Exception as e:
        print("Say that again")
        return "None"
    return query
# Add this function after the `takeCommand()` function
def query_gemini_ai(query):
    api_key = "AIzaSyBeac1otD1zowCXeY3Ikt6_YKrF5qw1LlA"
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={api_key}"
    
    headers = {
        'Content-Type': 'application/json'
    }

    data = {
        "contents": [
            {
                "parts": [
                    {"text": query}
                ]
            }
        ]
    }

    response = requests.post(url, headers=headers, json=data)
    if response.status_code == 200:
        result = response.json()
        return result['candidates'][0]['content']['parts'][0]['text']
    else:
        speak("Failed to fetch data from Gemini AI.")
        return None

# Add this function after the `query_gemini_ai()` function
def save_solution_to_file(solution, filename="solution.txt"):
    with open(filename, "w") as file:
        file.write(solution)

# Add this function after the `save_solution_to_file()` function
def read_solution_from_file(filename="solution.txt"):
    if os.path.exists(filename):
        with open(filename, "r") as file:
            return file.read()
    else:
        speak("Solution file not found.")
        return None

# Add this function after the `read_solution_from_file()` function
def display_solution(solution):
    from tkinter import Tk, Label
    window = Tk()
    window.title("Solution")
    window.geometry("400x200")
    label = Label(window, text=solution, font=("Arial", 12))
    label.pack(padx=20, pady=20)
    window.mainloop()

# Function to scan the screen for text and save it to a file
def scan_screen_and_save_text(filename):
    screenshot = pyautogui.screenshot()
    screenshot.save("screen.png")  # Save the screenshot (optional, for debugging)
    img = Image.open("screen.png")
    text = pytesseract.image_to_string(img)  # Extract text using OCR

    # Save the scanned text to the specified file
    with open(filename, "w") as file:
        file.write(text)

    return text

# Main function to handle the scan and query process
def scan_and_query():
    # Scan the screen and save the question to a file
    question_text = scan_screen_and_save_text("scanned_question.txt")
    if question_text:
        speak("Screen scanned and question saved to scanned_question.txt.")
        print("Extracted Question:", question_text)

        speak("In which programming language would you like the solution?")
        programming_language = takeCommand().strip().lower()  # Use the existing takeCommand function to get the programming language

        if programming_language:
            # Query Gemini AI with the scanned question and specified language
            modified_query=f"write only {programming_language} code \n {question_text}"
            speak(f"Asking Gemini AI for the solution in {programming_language}.")

            solution = query_gemini_ai(modified_query)

            if solution:
                speak("The solution is ready.")
                # Save the solution to scanned_solution.txt
                with open("scanned_solution.txt", "w") as file:
                    file.write(solution)
                speak("The solution has been saved in scanned_solution.txt. You can open it now.")
            else:
                speak("Could not retrieve a solution.")
        else:
            speak("No programming language specified.")
    else:
        speak("No question found on the screen.")


def parse_alarm_time(input_time):
    try:
        # Normalize input (convert to uppercase and remove periods)
        normalized_time = input_time.replace(".", "").upper()

        # Convert spoken time to datetime object
        alarm_time = datetime.strptime(normalized_time, "%I:%M %p")
        current_time = datetime.now()

        # If alarm time is earlier today, set it for tomorrow
        if alarm_time.time() <= current_time.time():
            alarm_time = alarm_time.replace(day=current_time.day + 1)
        else:
            alarm_time = alarm_time.replace(day=current_time.day)

        print(f"Alarm set for {alarm_time.strftime('%I:%M %p')}.")
        return alarm_time
    except ValueError:
        print("Invalid time format. Please try again.")
        return None

# Main function to set and trigger the alarm
def set_alarm():
    print("Say the time for the alarm (e.g., '7:30 AM').")
    alarm_input = takeCommand().lower()
    if alarm_input:
        print(f"You said: {alarm_input}")
        alarm_time = parse_alarm_time(alarm_input)
        if alarm_time:
            while True:
                current_time = datetime.now()
                if current_time >= alarm_time:
                    print("Wake up! It's time!")
                    playsound("D:/JARVIS/JARVIS_ATTEMPT_3-continuation/alarm_sound.mp3")  # Ensure you have an alarm sound file named "alarm_sound.mp3"
                    break

                time.sleep(1)


def play_song_spotify_ui(song_name):
    """Plays a song on Spotify using UI automation (less reliable)."""

    try:
        # Check if Spotify is running (using a more cross-platform method)
        spotify_running = False
        for proc in os.popen('tasklist /nh').readlines(): # Windows only check tasklist for process.
            if 'Spotify.exe' in proc:  # Replace with Spotify process name if different
                spotify_running = True
                break

        if not spotify_running:
            spotify_path = "C:/Users/Sriman Reddy/AppData/Local/Microsoft/WindowsApps/Spotify.exe" # Correct the path as per your system
            subprocess.Popen(spotify_path)
            time.sleep(7)  # Give Spotify extra time to fully start (adjust as needed)

        # Activate Spotify window (important for reliability)
        if not spotify_running: #Bring the spotify window to front.
            spotify_window = pyautogui.getWindowsWithTitle("Spotify")[0]
            spotify_window.activate()


        # Focus on search bar (more robust than ctrl+k)
        search_bar_location = pyautogui.locateCenterOnScreen('spotify_search_icon.png', confidence=0.9) # Replace with the actual image of spotify search bar.
        if search_bar_location:
            pyautogui.click(search_bar_location)
            pyautogui.write(song_name, interval=0.1)  # Type with intervals for reliability
            pyautogui.press('enter')
            time.sleep(2)  # Allow time for search and song to start
            pyautogui.press('enter') # Start playing the first result.
            speak(f"Playing '{song_name}' on Spotify (using UI automation)") #Playing command message
        else:
            speak("Could not locate the Spotify search bar.")


    except Exception as e:
        speak(f"An error occurred while playing on Spotify: {e}")



def play_favorite_songs_ui():
    """Plays liked songs on Spotify using UI automation."""
    play_song_spotify_ui("Liked Songs")


def spotify_ui():
    speak("Which song would you like to play on Spotify?")
    song_name = takeCommand().strip()
    play_song_spotify_ui(song_name)
def jarvis_main():
    speak("please wait for verifying your identity...")
    auth_status=perform_face_recognition()
    if auth_status == "Authorized":
        speak("Face recognized, access granted!")
        # ... (Your main Jarvis logic) ...
    elif auth_status == "Unauthorized":
        speak("Face not recognized, access denied!")
    elif auth_status == "Timeout":  # **ADDED: Handle Timeout**
        speak("Face recognition timed out. Please try again.")
    elif auth_status == "Error":  # **ADDED: Handle errors from Brain.py**
        speak("An error occurred during face recognition.")
def run_autotyper():
    """Runs the autotyper.py script."""
    try:
        # Method 1: Using os.system (simpler, less control)
        #os.system("python autotyper.py")

        # Method 2: Using subprocess (more control, recommended)
        subprocess.Popen(["python", "autotyper.py"])

        speak("Autotyper started. Please switch to the target window.")
    except FileNotFoundError:
        speak("Error: autotyper.py not found. Make sure it's in the same directory.")
    except Exception as e:  # Catch other potential errors
        speak(f"An error occurred while starting autotyper: {e}")
if __name__ == "__main__":
    speak("Initializing Jarvis")
    jarvis_main()
    while True:
        query = takeCommand().lower()
        if "wake up" in query:
            from GreetMe import greetMe
            greetMe()

            while True:
                query = takeCommand().lower()
                if "go to sleep" in query:
                    speak("Ok sir , You can call me anytime")
                    break 
                
                #################### JARVIS: THe Trilogy 2.0 #####################
                elif "schedule my day" in query:
                    tasks = [] #Empty list  linkedin
                    
                    speak("Do you want to clear old tasks (Plz speak YES or NO)")
                    query = takeCommand().lower()
                    if "yes" in query:
                        file = open("tasks.txt","w")
                        file.write(f"")
                        file.close()
                        no_tasks = int(input("Enter the no. of tasks :- "))
                        i = 0
                        for i in range(no_tasks):
                            tasks.append(input("Enter the task :- "))
                            file = open("tasks.txt","a")
                            file.write(f"{i}. {tasks[i]}\n")
                            file.close()
                    elif "no" in query:
                        i = 0
                        no_tasks = int(input("Enter the no. of tasks :- "))
                        for i in range(no_tasks):
                            tasks.append(input("Enter the task :- "))
                            file = open("tasks.txt","a")
                            file.write(f"{i}. {tasks[i]}\n")
                            file.close()

                elif "show my schedule" in query:
                    file = open("tasks.txt","r")
                    content = file.read()
                    file.close()
                    mixer.init()
                    mixer.music.load("notification.mp3")
                    mixer.music.play()
                    notification.notify(
                        title = "My schedule :-",
                        message = content,
                        timeout = 15
                    )

                elif "focus mode" in query:
                    a = int(input("Are you sure that you want to enter focus mode :- [1 for YES / 2 for NO "))
                    if (a==1):
                        speak("Entering the focus mode....")
                        os.startfile("D:/JARVIS/JARVIS_ATTEMPT_2/FocusMode.py")
                        exit()

                    
                    else:
                        pass


                


                elif "open" in query:   #EASY METHOD
                    query = query.replace("open","")

                    query = query.replace("jarvis","")
                    pyautogui.press("super")
                    pyautogui.typewrite(query)
                    pyautogui.sleep(2)
                    pyautogui.press("enter")
                elif "internet speed" in query:
                    wifi = speedtest.Speedtest()
                    download_net=print("Download speed:", wifi.download())
                    upload_net=print("Upload speed:", wifi.upload())
                    speak(f"Wifi download speed is {download_net}")
                    speak(f"Wifi Upload speed is {upload_net}")
                    

                elif "ipl score" in query:
                    from plyer import notification  #pip install plyer
                    import requests #pip install requests
                    from bs4 import BeautifulSoup #pip install bs4
                    url = "https://www.cricbuzz.com/"
                    page = requests.get(url)
                    soup = BeautifulSoup(page.text,"html.parser")
                    team1 = soup.find_all(class_ = "cb-ovr-flo cb-hmscg-tm-nm")[0].get_text()
                    team2 = soup.find_all(class_ = "cb-ovr-flo cb-hmscg-tm-nm")[1].get_text()
                    team1_score = soup.find_all(class_ = "cb-ovr-flo")[8].get_text()
                    team2_score = soup.find_all(class_ = "cb-ovr-flo")[10].get_text()

                    print(f"{team1} : {team1_score}")
                    print(f"{team2} : {team2_score}")

                    notification.notify(
                        title = "IPL SCORE :- ",
                        message = f"{team1} : {team1_score}\n {team2} : {team2_score}",
                        timeout = 15
                    )
                
                elif "play a game" in query:
                    from game import game_play
                    game_play()

                elif "screenshot" in query:
                    im = pyautogui.screenshot()
                    im.save("ss.jpg")
                elif "click my photo" in query:
                    pyautogui.press("super")
                    pyautogui.typewrite("camera")
                    pyautogui.press("enter")
                    pyautogui.sleep(2)
                    speak("SMILE")
                    pyautogui.press("enter")

                elif "hello" in query:
                    speak("Hello sir, how are you ?")
                elif "iam fine" in query:
                    speak("that's great, sir")
                elif "how are you" in query:
                    speak("Perfect, sir")
                elif "thank you" in query:
                    speak("you are welcome, sir")
                
           
                elif "pause" in query:
                    pyautogui.press("k")
                    speak("video paused")
                elif "mute" in query:
                    pyautogui.press("m")
                    speak("video muted")
                


                elif "volume up" in query:
                    from keyboard import volumeup
                    speak("Turning volume up,sir")
                    volumeup()
                elif "volume down" in query:
                    from keyboard import volumedown
                    speak("Turning volume down, sir")
                    volumedown()


                elif "google" in query:
                    from SearchNow import searchGoogle
                    searchGoogle(query)
                elif "youtube" in query:
                    from SearchNow import searchYoutube
                    searchYoutube(query)
                elif "wikipedia" in query:
                    from SearchNow import searchWikipedia
                    searchWikipedia(query)

                elif "temperature" in query:
                    search = f"{query}"
                    url = f"https://www.google.com/search?q={search}"
                    r  = requests.get(url)
                    data = BeautifulSoup(r.text,"html.parser")
                    temp = data.find("div", class_ = "BNeawe").text
                    speak(f"current{search} is {temp}")
                elif "weather" in query:
                    search = f"{query}"
                    url = f"https://www.google.com/search?q={search}"
                    r  = requests.get(url)
                    data = BeautifulSoup(r.text,"html.parser")
                    temp = data.find("div", class_ = "BNeawe").text
                    speak(f"current{search} is {temp}")

                elif "song on spotify" in query:
                    spotify_ui()  # Activates the function to ask for and play a songkkk
                elif "play my favorite songs" in query or "play liked songs" in query:  # Options to activate liked songs.
                    play_favorite_songs_ui()
                elif "the time" in query:
                    strTime = datetime.datetime.now().strftime("%H:%M")    
                    speak(f"Sir, the time is {strTime}")
                elif "finally sleep" in query:
                    speak("Going to sleep,sir")
                    exit()

                elif "remember that" in query: 
                    rememberMessage = query.replace("remember that","")
                    rememberMessage = query.replace("jarvis","")
                    speak("You told me to remember that"+rememberMessage)
                    remember = open("Remember.txt","a")
                    remember.write(rememberMessage)
                    remember.close()
                elif "what do you remember" in query:
                    remember = open("Remember.txt","r")
                    speak("You told me to remember that" + remember.read())

                elif "shutdown system" in query:
                    speak("Are You sure you want to shutdown")
                    shutdown = input("Do you wish to shutdown your computer? (yes/no)")
                    if shutdown == "yes":
                        os.system("shutdown /s /t 1")

                    elif shutdown == "no":
                        break
                elif "solve this question" in query:
                    speak("What's the question, please tell me.")
                    user_query = takeCommand().lower()
                    
                    if user_query:
                        response = query_gemini_ai(user_query)
                        if response:
                            # Save response to a text file
                            save_solution_to_file(response)
                                
                            speak("I have the answer. How would you like to see it? (display the answer (or) shall I read the answer?)")
                            answer_method = takeCommand().lower()
                                
                            if "display" in answer_method:
                                solution = read_solution_from_file()
                                if solution:
                                    display_solution(solution)
                            elif "read" in answer_method:
                                speak(response)
                            else:
                                    speak("Sorry, I didn't understand. You can say 'display the solution' or 'read the solution'.")
                        else:
                                speak("Sorry, I couldn't fetch the answer at the moment.")
                    else:
                        speak("apologize,I cant able to solve the question.")

                elif "scan this question" in query:
                    speak("You have 5 seconds to open the screen you want scanned.")
                    time.sleep(5)  # Give the user 5 seconds to open the desired screen manually
                    scan_and_query()
                elif "close the tab" in query:
                    speak("OK")
                    pyautogui.hotkey('alt','f4')
                elif "write a code" in query:
                    speak("What code do you want to write?")
                    code_input = takeCommand().lower()

                    if code_input:
                        response = query_gemini_ai(code_input)
                        if response:
                            # Save response to a text file
                            save_solution_to_file(response)
                            speak("I have wrote a code. How would you like to see it? (display the code (or) shall I read the code?)")
                            code_application = takeCommand().lower()

                            if "display" in code_application:
                                solution = read_solution_from_file()
                                if solution:
                                    display_solution(solution)
                            elif "read" in code_application:
                                speak(response)
                            else:
                                speak(
                                    "Sorry, I didn't understand. You can say 'display the solution' or 'read the solution'.")
                        else:
                            speak("Sorry, I couldn't fetch the answer at the moment.")
                    else:
                        speak("apologize,I cant able to solve the question.")
                elif "now enter the code" in query:
                    run_autotyper()
                elif "who are you" in query:
                    speak("I am Jarvis, your personal assistant")
                elif "set an alarm" in query:
                    set_alarm()


