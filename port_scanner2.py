import socket,threading,datetime,os,signal,argparse,sys,time
import tkinter as tk
from tkinter import messagebox

os.system("title Port Scanner by naweedur rahman")
def clear_screen():
    os.system("cls" if os.name == "nt" else "clear")

def check_internet_connection():
    try:
        socket.create_connection(("8.8.8.8", 53))
        return True
    except OSError:
        return False
    
def get_local_ip():
    return socket.gethostbyname(socket.gethostname())

def scan_port(ip, port, result, total_ports, lock):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.settimeout(1)
        result[port] = sock.connect_ex((ip, port))
    with lock:
        percent_complete = (len(result) / total_ports) * 100
        sys.stdout.write(f"\r\tScanning . . . [ {percent_complete:.2f}% ]")
        sys.stdout.flush()

def save_results(ip, min_port, max_port, open_ports, closed_ports):
    current_time = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    total_open_ports = len(open_ports)
    total_closed_ports = len(closed_ports)
    filename = f"results_{ip}_ports_{min_port}-{max_port}_{current_time}.txt"
    with open(filename, "w") as f:
        f.write(f"Port scan results for {ip}\n\n")
        f.write(f"Date Created at: {current_time}\n")
        f.write(f"Total opened ports: {total_open_ports}\n")
        f.write(f"Total closed ports: {total_closed_ports}\n")
        f.write("\nOpen Ports:\n")
        for port in open_ports:
            f.write(f"Port {port}: Open\n")
        f.write("\nClosed Ports:\n")
        for port in closed_ports:
            f.write(f"Port {port}: Closed\n")
    messagebox.showinfo("Scan Completed!", f"Port scan completed. Results saved to:\n\n{os.path.abspath(filename)}")

def port_scan(ip, min_port, max_port):
    open_ports = []
    closed_ports = {}
    threads = []
    lock = threading.Lock()
    total_ports = max_port - min_port + 1
    start_time = time.time()
    for port in range(min_port, max_port + 1):
        thread = threading.Thread(target=scan_port, args=(ip, port, closed_ports, total_ports, lock))
        threads.append(thread)
        thread.start()
    for thread in threads:
        thread.join()
    end_time = time.time()
    duration = end_time - start_time
    open_ports = [port for port, status in closed_ports.items() if status == 0]
    closed_ports = [port for port, status in closed_ports.items() if status != 0]
    save_results(ip, min_port, max_port, open_ports, closed_ports)
    print("\n\n\tScan completed.")
    print(f"\tTotal duration: {duration:.2f} seconds\n")
def signal_handler(sig, frame):
    messagebox.showinfo("Scan Interrupted", "Port scan interrupted.")
    sys.exit(0)
def main():
    parser = argparse.ArgumentParser(description="Python Port Scanner\nBy naweedur rahman")
    parser.add_argument("ip", help="Target IP address")
    parser.add_argument("min_port", type=int, help="Minimum port number")
    parser.add_argument("max_port", type=int, help="Maximum port number")
    args = parser.parse_args()
    clear_screen()
    print("\n\tWelcome to Python Port Scanner!")
    if check_internet_connection():
        print("\n\tInternet connection is available.")
        ip = args.ip
    else:
        print("\n\tInternet connection is not available. Scanning on local host...")
        ip = get_local_ip()
    signal.signal(signal.SIGINT, signal_handler)
    print("\tScanning . . . [ 0% ]", end="", flush=True)
    port_scan(args.ip, args.min_port, args.max_port)
if __name__ == "__main__":
    main()
