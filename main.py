import socket
from concurrent.futures import ThreadPoolExecutor

ports = []
ip = input("Enter your router IP adress: ")
counter = 0

def is_valid_IP(ip):
    try:
        socket.inet_aton(ip)
        return True
    except socket.error:
        return False

if not is_valid_IP(ip):
    print("Invalid IP adress!")
    exit(1)

def is_open(port):
    global counter
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(0.5) # Timeout for faster scanning
    try:
        s.connect((ip, int(port)))
        s.shutdown(2)
        return True
    except:
        counter += 1
        percentage = round((counter / 9999) * 100)
        progress = "■" * (percentage // 5) + "□" * (20 - (percentage // 5))
        print(f"|{progress}| {percentage}%", end="\r")
        return False
    finally:
        s.close()


with ThreadPoolExecutor(max_workers=100) as execute:
    results = list(execute.map(is_open, range(10000)))
    # If port is open the it will be stored in a list
    ports = [i for i, open in enumerate(results) if open]

print(f"\nOpen ports: {ports}")