mport socket

HOST = '0.0.0.0'
PORT =  8000

def handle_request(request):
	headers =  request.split()
	filename = headers[1]
	if filename == '/':
        	filename = '/index.html'

	try:
		if not filename.endswith(".html"):
			filename += ".html"
		f = open(filename[1:])
		content = f.read()
		f.close()
		
		response = 'HTTP/1.1 200 OK\n\n' + content

	except FileNotFoundError:
		response = 'HTTP/1.1 404 NOT FOUND\n\nFile Not Found'

	return response

	


server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server_sock.bind((HOST, PORT))
server_sock.listen(1)

print(f'HTTP SERVER Starting on port {PORT} on IP {HOST}')
while True:
	client_conn, client_addr = server_sock.accept()

	try: 
		request = client_conn.recv(1024).decode()
		print(request)
		filename = request.split()[1]
		f = open(filename[1:])
		content = f.read()
		f.close()
		
		response = 'HTTP/1.1 200 OK\r\n\r\n' + content

	except IOError:
		response = 'HTTP/1.1 404 NOT FOUND\r\n\r\nFile Not Found'

	client_conn.sendall(response.encode())
	client_conn.close()

server_sock.close()
