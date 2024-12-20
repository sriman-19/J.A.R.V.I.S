import subprocess
import os

def run_scripts():
    """Executes Main.py, activates the virtual environment, and executes Brain.py."""

    try:
        # Execute Main.py
        main_result = subprocess.run(["python", "Main.py"], cwd="D:\\JARVIS\\JARVIS_ATTEMPT_3", capture_output=True, text=True, check=True)
        print(f"Main.py output:\n{main_result.stdout}")

        # Activate the virtual environment and execute Brain.py

        # For Windows (adjust if your activate script is named differently)
        activate_script = ".venv\\Scripts\\activate"
        brain_script = "python Brain.py"  # Execute Brain.py after activation

        # Combine the activation and Brain.py execution into a single command using cmd.exe. 
        # This is a more robust way to handle activation on Windows, especially within subprocess.
        command = f"{activate_script} && {brain_script}"


        brain_result = subprocess.run(command, cwd="D:\\JARVIS\\JARVIS_ATTEMPT_3", shell=True,  # Use shell=True cautiously (see below)
                                      capture_output=True, text=True)
                                      
        if brain_result.returncode == 0:
            print(f"Brain.py output:\n{brain_result.stdout}")
        else:
            print(f"Error executing Brain.py:\n{brain_result.stderr}")



    except subprocess.CalledProcessError as e:
        print(f"Error: {e}")  # Print detailed error information including stdout/stderr if any
    except FileNotFoundError:
        print("Error: Main.py, Brain.py, or the activate script not found.")



if __name__ == "__main__":
    run_scripts()