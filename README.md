# JARVIS: Personal AI Assistant

JARVIS is an advanced personal assistant designed to automate tasks, provide information, and enhance productivity. This project integrates various functionalities like face recognition, voice commands, and task management to create a smart virtual assistant.

## Features

### Core Functionalities
1. **Face Recognition:**
   - Ensures secure access by verifying user identity using face recognition.
   - Unauthorized access prompts a warning, while authorized access allows full functionality.

2. **Voice Commands:**
   - Enables interaction using natural language for tasks like web searches, task scheduling, and controlling media.

3. **Task Automation:**
   - Open applications, search the web, manage schedules, and more with simple voice commands.

4. **Screen Scanning and AI Assistance:**
   - Scans the screen for text using OCR and queries AI models like Gemini for solutions or code generation.

5. **Spotify Control:**
   - Automate song selection and playback on Spotify.

6. **Internet Speed Test:**
   - Measures upload and download speeds with a voice-activated command.

7. **Alarm and Schedule Management:**
   - Set alarms and maintain a daily task schedule.

8. **Question Solver and Code Writer:**
   - Scan, solve questions, and generate programming code using AI.

9. **Autotyper:**
   - Simulates human-like typing for programming and text input.

10. **Fun and Utility Commands:**
    - Play games, take screenshots, capture photos, and interact conversationally.

### Security Features
- Periodic face scanning every 30 seconds for unauthorized users.
- Warning messages upon detecting unauthorized users.

---

## Installation and Setup

### Prerequisites
- Python 3.x installed on your system.
- Required Python libraries:
  - `pyttsx3`, `speech_recognition`, `pyautogui`, `pytesseract`, `opencv-python`, `DeepFace`, `plyer`, `pygame`, `spotipy`, `requests`, `beautifulsoup4`, and `pillow`.

### Setup Instructions
1. **Clone the Repository:**
   ```bash
   git clone https://github.com/your-username/jarvis.git
   cd jarvis
   ```

2. **Install Dependencies:**
   Install all required libraries using pip:
   ```bash
   pip install -r requirements.txt
   ```

3. **Setup Tesseract OCR:**
   - Download and install Tesseract OCR from [Tesseract OCR](https://github.com/tesseract-ocr/tesseract).
   - Update the path to the Tesseract executable in the code:
     ```python
     pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
     ```

4. **Configure AI Keys:**
   - Replace placeholders in the code (e.g., Gemini API key) with your actual API keys.

5. **Run the Application:**
   Execute the main script:
   ```bash
   python Main.py
   ```

---

## File Details

### 1. `Main.py`
- Core functionality of JARVIS, including face recognition, voice commands, task management, and AI integration.

### 2. `execute.py`
- Automates the execution of multiple scripts, including virtual environment activation and subsequent script execution.

### 3. `autotyper.py`
- Simulates human-like typing for entering code or text into platforms like OnlineGDB.

---

## How to Use JARVIS

1. **Start JARVIS:**
   Run `Main.py` and follow voice instructions for interaction.

2. **Trigger Features:**
   Use wake words like "Wake up, JARVIS" to activate listening for commands.

3. **Voice Commands Examples:**
   - "Set an alarm for 7:30 AM."
   - "Open YouTube."
   - "What's the internet speed?"
   - "Play my favorite songs."

4. **Security:**
   JARVIS will periodically check for authorized users through face recognition and notify upon detecting unauthorized access.

---

## Command List

### General Commands
- **"Wake up, JARVIS"** - Activates JARVIS for listening to commands.
- **"Go to sleep"** - Deactivates JARVIS temporarily.

### Task Management
- **"Schedule my day"** - Create a list of tasks for the day.
- **"Show my schedule"** - Displays the tasks scheduled for the day.

### Internet and System Control
- **"Open [application name]"** - Opens any installed application (e.g., Chrome, Notepad).
- **"Internet speed"** - Checks the current internet speed.

### Entertainment
- **"Play a song on Spotify"** - Plays a specific song on Spotify.
- **"Play my favorite songs"** or **"Play liked songs"** - Plays your liked songs on Spotify.
- **"Pause"** - Pauses a currently playing video or song.
- **"Mute"** - Mutes audio in a video or song.
- **"Volume up"** or **"Volume down"** - Adjusts the system volume.

### Alarms and Notifications
- **"Set an alarm for [time]"** - Sets an alarm at the specified time.
- **"Show notifications"** - Displays recent notifications.

### AI Assistance and Code Generation
- **"Solve this question"** - Queries Gemini AI to solve a verbally described question.
- **"Scan this question"** - Scans the screen for a question and queries Gemini AI for a solution.
- **"Write a code"** - Asks Gemini AI to generate a code based on your verbal input.
- **"Now enter the code"** - Activates the Autotyper to type code into an editor like OnlineGDB.

### Face Recognition and Security
- **"Who are you?"** - Introduces JARVIS.
- **"Wake up JARVIS"** - Activates face recognition and other functionalities.

### Information Retrieval
- **"Google [query]"** - Searches the query on Google.
- **"YouTube [query]"** - Searches and plays videos on YouTube.
- **"Wikipedia [query]"** - Retrieves a summary of the query from Wikipedia.
- **"What’s the temperature/weather?"** - Provides current weather details.

### Utility Commands
- **"Take a screenshot"** - Captures the screen and saves the image.
- **"Click my photo"** - Opens the camera and takes a photo.
- **"Shutdown system"** - Shuts down the computer after confirmation.

### Fun and Games
- **"Play a game"** - Launches a game integrated into JARVIS.

### Time Management
- **"What is the time?"** - Announces the current time.

### Custom Reminders
- **"Remember that [message]"** - Saves a note for later.
- **"What do you remember?"** - Recalls saved notes.

### Tab Control
- **"Close the tab"** - Closes the active window or browser tab.

---

## Future Enhancements
- Expand compatibility with additional AI APIs.
- Implement real-time feedback for commands.
