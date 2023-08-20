import socket
import http.client


def handle_request(client_socket):
    # Принимаем запрос от клиента
    request = client_socket.recv(1024).decode()

    # Парсим запрос для получения метода и заголовков
    try:
        method = request.split()[0]
        headers = request.split('\r\n')[1:-2]  # Пропускаем первую строку(метод) и последние две пустые строки
    except IndexError:
        # Если запрос не соответствует формату, возвращаем ошибку 400 Bad Request
        response = 'HTTP/1.1 400 Bad Request\r\n\r\n'
        client_socket.send(response.encode())
        client_socket.close()
        return

    def run_server():
        # Создаем сокет
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # Устанавливаем опцию SO_REUSEADDR, чтобы можно было повторно использовать адрес сервера
        server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        # Привязываем серверный сокет к адресу и порту
        server_socket.bind(('localhost', 8787))
        server_socket.listen(1)

        print('Server is running...')

        client_socket, client_address = server_socket.accept()
        handle_request(client_socket)

    run_server()