import socket
import requests
import time
import threading
from queue import Queue
import ipaddress
from colorama import Fore, Style
import pyfiglet
from datetime import datetime
import webbrowser
import subprocess

socket.setdefaulttimeout(0.25)
lock = threading.Lock()

def get_public_ip():
    try:
        response = requests.get('https://api.ipify.org')
        if response.status_code == 200:
            return response.text
        else:
            return "Unknown"
    except:
        return "Unknown"

def get_country(ip):
    try:
        response = requests.get(f'http://ip-api.com/json/{ip}')
        if response.status_code == 200:
            data = response.json()
            return data.get('country', 'Unknown')
        else:
            return "Unknown"
    except:
        return "Unknown"

def scan(ip, port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        con = sock.connect((ip, port))
        with lock:
            if port == 8080:
                print(f"Port {port} is open on {ip}:{port} {Fore.RED}HTTP{Style.RESET_ALL}")
            else:
                print(f"Port {port} is open on {ip}")
        con.close()
    except:
        pass

def execute(queue):
    while True:
        ip, port = queue.get()
        scan(ip, port)
        queue.task_done()

def generate_ip_range(start_ip, end_ip):
    start = int(ipaddress.IPv4Address(start_ip))
    end = int(ipaddress.IPv4Address(end_ip))
    for ip_int in range(start, end + 1):
        yield str(ipaddress.IPv4Address(ip_int))

def print_logo():
    # Define ANSI escape codes for colors
    green_code = "\033[32m"  # Green
    yellow_code = "\033[33m"  # Yellow
    reset_code = "\033[0m"   # Reset

    logo = pyfiglet.figlet_format("W8Team", font="slant")
    # Add full square border around logo
    logo_lines = logo.split('\n')
    logo_width = len(logo_lines[0])
    bordered_logo = f"{green_code}+{'-' * (logo_width + 2)}+{reset_code}\n"
    for idx, line in enumerate(logo_lines):
        if idx == 0:
            bordered_logo += f"{green_code}| {line}{' ' * (logo_width - len(line))} {yellow_code}{get_public_ip()} - {get_country(get_public_ip())} - {datetime.now().strftime('%Y-%m-%d %I:%M:%S %p')} |{reset_code}\n"
        else:
            bordered_logo += f"{green_code}| {line}{' ' * (logo_width - len(line))}{' ' * (logo_width - len(line))} |{reset_code}\n"
    bordered_logo += f"{green_code}+{'-' * (logo_width + 2)}+{reset_code}\n"
    # Print bordered logo
    print(bordered_logo)

def run_tool():
    password = "0011"
    entered_password = input("Enter password: ")
    if entered_password != password:
        print("Incorrect password.")
        print("Opening Telegram channel link in Chrome browser...")
        subprocess.run(["termux-open-url", "https://t.me/W8TeamSB"])
        return

    print_logo()  # Display the W8Team logo quickly
    start_ip = input('Start IP Address: ')
    end_ip = input('End IP Address: ')

    queue = Queue()
    start_time = time.time()

    for x in range(100):
        thread = threading.Thread(target=execute, args=(queue,))
        thread.daemon = True
        thread.start()

    for ip in generate_ip_range(start_ip, end_ip):
        queue.put((ip, 80))
        queue.put((ip, 8080))

    queue.join()

    # Calculate and display time taken
    elapsed_time = time.time() - start_time
    print(f'Time taken: {elapsed_time:.2f} seconds')

if __name__ == "__main__":
    run_tool()
