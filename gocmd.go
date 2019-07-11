package main

import (
	"bufio"
	"encoding/base64"
	"flag"
	"fmt"
	"io"
	"log"
	"net"
	"os"
	"os/exec"
)

var (
	port = flag.Int("port", 4444, "The port to listen")
	bash = flag.String("bash", "bash", "The script interpreter")
)

func handleConnection(conn net.Conn) {
	defer conn.Close()
	log.Printf("Connection from %v\n", conn.RemoteAddr().String())
	scanner := bufio.NewScanner(conn)
	if !scanner.Scan() {
		return
	}
	data, err := base64.StdEncoding.DecodeString(scanner.Text())
	if err != nil {
		log.Printf("Failed to decode: %v\n", err)
		return
	}
	input := string(data)
	log.Printf("The input is %s\n", input)
	mw := io.MultiWriter(os.Stdout, conn)
	cmd := exec.Command(*bash, "-c", input)
	cmd.Stderr = mw
	cmd.Stdout = mw
	if err := cmd.Run(); err != nil {
		log.Printf("Failed to execute: %v\n", err)
	}
}

func main() {
	flag.Parse()
	ln, err := net.Listen("tcp", fmt.Sprintf(":%d", *port))
	if err != nil {
		log.Fatalf("Failed to listen on port %v: %v\n", *port, err)
	}
	log.Printf("Listening on port %v...\n", *port)
	for {
		conn, err := ln.Accept()
		if err != nil {
			log.Printf("Failed to accept: %v\n", err)
		}
		go handleConnection(conn)
	}
}
