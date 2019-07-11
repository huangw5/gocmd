#!/usr/bin/env python3

import base64
import socket
import subprocess
import io

HOST = ''
PORT = 50007


def run():
  with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    print('Listening on port {}'.format(PORT))
    s.listen()
    while True:
      conn, addr = s.accept()
      with conn:
        buf = io.StringIO()
        print('Connected by', addr)
        while True:
          data = str(conn.recv(1024), 'utf-8')
          buf.write(data)
          if '\n' in data:
            break
        script = base64.b64decode(buf.getvalue())
        proc = subprocess.run(['bash', '-c', script],
                              stdout=subprocess.PIPE,
                              stderr=subprocess.STDOUT)
        print('Output:\n{}'.format(proc.stdout.decode('utf-8')))
        conn.send(proc.stdout)


def main(argv):
  if len(argv) > 1:
    raise app.UsageError('Too many command-line arguments.')


if __name__ == '__main__':
  run()