import socket

host_name = socket.gethostname()
print(socket.gethostbyname(host_name))