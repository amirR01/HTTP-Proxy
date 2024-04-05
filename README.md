# HTTP-Proxy
A simple HTTP proxy server written in Python.

## Usage
1. Clone the repository
2. Run the server using `python3 main.py`
3. Configure your browser to use the proxy server at `localhost:12345`
4. Enjoy!

## Note 
- You can change the address and port of the proxy server in the `main.py` file in the `main` function.
- If you use `CONNECT` command before sending the requests the proxy will stablish a connection with the server and will forward the requests to the server.
```
curl -x localhost:12345 CONNECT destination
```