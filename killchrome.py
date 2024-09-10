import psutil
import time

def kill_chrome_processes():
    for proc in psutil.process_iter(attrs=['pid', 'name']):
        try:
            # Check if the process name contains "chrome"
            if "chrome" in proc.info['name'].lower():
                print(f"Terminating Chrome process with PID {proc.info['pid']}")
                proc.terminate()
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass

if __name__ == "__main__":
    while True:
        kill_chrome_processes()
        time.sleep(120)  # Sleep for 60 seconds (1 minute)
