import socket

host = '0.0.0.0'
port = 8888 
press = '(Pressione qualquer tecla para voltar ao menu inicial)'
Ctrl_C = 'Você pressionou Ctrl+C para interromper o programa!'

try:
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    server_socket.bind((host, port))

    server_socket.listen(1)
    print(f'Esperando por conexões na porta {port}...')

    while True:
        client_socket, client_address = server_socket.accept()
        print(f'Conexão estabelecida com {client_address}')

        with open('./{}'.format(client_address[0]), 'wb') as file:
            while True:
                data = client_socket.recv(1024)  
                if not data:
                    break  
                file.write(data) 

        print(f'Arquivo recebido!')
        client_socket.close() 
except KeyboardInterrupt:
    print(f'\n{Ctrl_C}')