import socket
import json


def socket_server(listen_port, connect_number, process_func, debug=False):

    # 创建一个TCP socket对象
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # 绑定IP地址和端口号
    server_address = ('localhost', 6666)
    server_socket.bind(server_address)

    # 监听连接请求
    server_socket.listen(10)
    print('等待连接...')

    while True:
        # 接受客户端连接请求并建立连接
        client_socket, client_address = server_socket.accept()
        print(f'连接来自 {client_address}')

        # 接收查询请求
        query = client_socket.recv(1024).decode()
        print(f'收到查询：{query}')

        # 在dataframe中查找并返回一行或多行数据
        result = process_func(query)

        # 返回查询结果给客户端，以JSON格式返回
        response_json = json.dumps(result)
        # print(response_json)
        client_socket.sendall(response_json.encode())

        # 关闭客户端连接和服务器socket对象

        client_socket.close()
        server_socket.close()
