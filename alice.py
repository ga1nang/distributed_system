import socket

def get_ip_address():
    try:
        # Connect to an external server to get the local IP address
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
            s.connect(("8.8.8.8", 80))
            ip_address = s.getsockname()[0]
        return ip_address
    except Exception as e:
        return f"Error getting IP address: {e}"

# Get and print the IP address
ip_address = get_ip_address()
print(f"My IP address is: {ip_address}")