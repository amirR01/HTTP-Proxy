import socket
import threading

def handle_connection(client_socket):
    request = client_socket.recv(4096)
    if not request:
        return
    
    host,port = extract_host_port_from_request(request)

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.connect((host, port))

    if request.startswith(b'CONNECT'):
        client_socket.send(b'HTTP/1.1 200 Connection established\r\n\r\n')
    else:
        modified_request = modify_http_request(request)
        server_socket.send(modified_request)

    threading.Thread(target=forward_data, args=(client_socket, server_socket)).start()
    threading.Thread(target=forward_data, args=(server_socket, client_socket)).start()
    

def extract_host_port_from_request(request):
    lines = request.split(b'\r\n')
    first_line_parts = lines[0].decode('utf-8').split(' ')

    if first_line_parts[0] == 'CONNECT':
        host_port_parts = first_line_parts[1].split(':')
        host = host_port_parts[0]
        port = int(host_port_parts[1]) if len(host_port_parts) > 1 else 443
    else:
        url = first_line_parts[1]
        if url.startswith('http://'):
            url = url[len('http://'):]
        
        parts = url.split('/')
        domain_parts = parts[0].split(':')
        host = domain_parts[0]
        port = int(domain_parts[1]) if len(domain_parts) > 1 else 80

    return host, port

def modify_http_request(request):
    request_lines = request.split(b'\r\n')
    
    first_line_parts = request_lines[0].decode('utf-8').split(' ')
    if len(first_line_parts) > 1 and first_line_parts[1].startswith('http'):
        url_parts = first_line_parts[1].split('/')
        modified_url = '/' + '/'.join(url_parts[3:])
        
        request_lines[0] = ' '.join([first_line_parts[0], modified_url, first_line_parts[2]]).encode('utf-8')
    
    modified_request = b'\r\n'.join(request_lines)
    return modified_request

def forward_data(source, destination):
    while True:
        data = source.recv(4096)
        if not data:
            break
        destination.sendall(data)

    source.close()
    destination.close()

def start_proxy():
    proxy = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    proxy.bind(('127.0.0.1', 12345))
    proxy.listen(5)
    print("Listening on port 12345")

    while True:
        client_socket, addr = proxy.accept()
        
        client_handler = threading.Thread(target=handle_connection, args=(client_socket,))
        client_handler.start()

if __name__ == "__main__":
    start_proxy()