#! /usr/bin/env python3

import sys
import socket
import json
import struct
import time
from configuration import *
from board import Board
from transposition_table import TranspositionTable
from explorer import *

class Connector:
    def __init__(self, turn, timeout, server_ip):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect((server_ip, PORTS[turn]))

    def send_move(self, move, color):
        letters = 'abcdefghi'
        row_from, column_from, row_to, column_to = move
        initial = letters[column_from] + str(row_from + 1)
        final   = letters[column_to  ] + str(row_to   + 1)
        data = {
                "from":initial,
                "to":final,
                "turn":color.upper(),
                }
        self.send_str(json.dumps(data))

    def send_int(self, integer):
        bytes_sent = self.sock.send(struct.pack('>i', integer))
        return bytes_sent == 4

    def send_str(self, string):
        string = string.encode('utf-8')
        length = len(string)
        if self.send_int(length):
            bytes_sent = self.sock.send(string)
            return bytes_sent == length
        return False

    def recv_int(self):
        size = 4
        header = b''
        while len(header) < size:
            data = self.sock.recv(size - len(header))
            if not data:
                break
            header += data
        return struct.unpack("!i", header)[0]

    def recv_str(self):
        length = self.recv_int()
        return self.sock.recv(length, socket.MSG_WAITALL).decode('utf-8')




TURN_COLOR = {
        "BLACK": False,
        "WHITE": True
        }

openings = {
        "BLACK":[
                 
                ],
        "WHITE":[
                 (4, 5, 3, 5),
                 (5, 4, 5, 5),
                ],
        }


if __name__ == '__main__':
    # arg parsing
    turn = sys.argv[1].lower()
    timeout = int(sys.argv[2])
    server_ip = sys.argv[3]

    # setup tt
    #tt = TranspositionTable(f'/dev/shm/tt_{turn}.sqlite3')
    tt = ''

    conn = Connector(turn, timeout, server_ip)
    conn.send_str(NAME)

    print(f'''Starting game:
    Name: {NAME}
    Turn: {turn}
    Timeout: {timeout}
    Server: {server_ip}
    ''')
    
    turn_number = 0

    while True:
        data = conn.recv_str()
        board = Board(data)
        if board.role == turn.upper():
            print(f' {turn_number} '.center(40,'#'))
            print(board)
            if turn_number < len(openings[board.role]):
                move = openings[board.role][turn_number]
                print(f'{board.role} hardcoded move:', move)
            else:
                print(f' {turn_number} '.center(40,'#'))
                print(board)
                start = time.time()
                move, points = explore(board, 4, -math.inf, math.inf, TURN_COLOR[turn.upper()], tt, THREADS, timeout, start)
                finish = time.time()
                print(board)
                print('Exploring time:', finish - start)
                print('Calculated move:', move)
                print('Points:', points)
                print()
            conn.send_move(move,turn)
            
            new_board = board.move(move,TURN_COLOR[turn.upper()])
            print(new_board)
            print()
            print('#'*40)
            print()

            turn_number += 1

