#!/usr/bin/env python3

import base64
import socket
import sys

def run(host, port):
  data = base64.b64encode(sys.stdin.buffer.read())
  with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((host, port))
    s.sendall(data)
  print('Received', repr(data))


if __name__ == '__main__':
  if len(sys.argv) != 3:
    print('Usage: {} <server> <port>'.format(sys.argv[0]))
  run(sys.argv[1], int(sys.argv[2]))
