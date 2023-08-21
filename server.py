import socket
import http.client
import json


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

    # Получаем значение статуса из GET параметра 'status'
    status = 'OK'
    status_code = '200 '
    if '/?status=' in request:
        status_code = request.split('/?status=')[1].split()[0]
        try:
            if status_code.isdigit():
                status = http.client.responses[int(status_code)]
            elif status_code.isalpha():
                status = http.client.responses[str(status_code)]
        except BaseException:
            status_code = '200'
            json_body = collecting_json(headers, method, status, status_code)
            response = collecting_response(json_body, status, status_code)
            client_socket.send(response.encode())
            client_socket.close()
            return

    json_body = collecting_json(headers, method, status, status_code)

    response = collecting_response(json_body, status, status_code)

    # Отправляем ответ
    client_socket.send(response.encode())


def collecting_response(json_body, status, status_code):
    # Формируем ответ сервера
    response = f'HTTP/1.1 {status_code} {status}\r\n'
    response += 'Content-Type: application/json\r\n'
    response += f'Content-Length: {len(json_body)}\r\n'
    response += '\r\n'
    response += json_body
    return response


def collecting_json(headers, method, status, status_code):
    # Формируем JSON body
    json_body = {
        'headers': headers,
        'method': method,
        'status': status_code + ' ' + status
    }
    json_body = json.dumps(json_body)
    return json_body


def run_server():
    # Создаем сокет
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Устанавливаем опцию SO_REUSEADDR, чтобы можно было повторно использовать адрес сервера
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    # Привязываем серверный сокет к адресу и порту
    server_socket.bind(('localhost', 8787))
    server_socket.listen(1)

    print('Server is running....')

    while True:
        client_socket, client_address = server_socket.accept()
        handle_request(client_socket)


run_server()