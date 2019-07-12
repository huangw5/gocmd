#!/usr/bin/env python3

import argparse
import base64
import socket
import subprocess
import io

parser = argparse.ArgumentParser()
parser.add_argument(
    '--port', type=int, help='The port to listen to', default=4444, nargs='?')
parser.add_argument(
    '--host', type=str, help='The host to listen to', default='127.0.0.1', nargs='?')
args = parser.parse_args()

args = parser.parse_args()


def run():
  with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((args.host, args.port))
    print('Listening on {}:{}...'.format(args.host, args.port))
    s.listen()
    while True:
      conn, addr = s.accept()
      with conn:
        buf = io.StringIO()
        print('Connected by', addr)
        while True:
          data = str(conn.recv(1024), 'utf-8')
          buf.write(data)
          if '\n' in data or len(data) == 0:
            break
        script = base64.b64decode(buf.getvalue())
        print(u'Script:\n{}'.format(script))
        proc = subprocess.run(['bash', '-c', script],
                              stdout=subprocess.PIPE,
                              stderr=subprocess.STDOUT)
        print(u'Output:\n{}'.format(proc.stdout.decode('utf-8')))
        conn.send(proc.stdout)


if __name__ == '__main__':
  run()
