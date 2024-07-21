# coding = UTF-8
import socket
import struct

def convert_port(port):
	"""covert port to bytes port

	Args:
		port(int): port

	Returns:
		bytes: bytes port
	"""
	return struct.pack("!H",port)

def convert_bytes_port(bytes_port):

	return struct.unpack("!H",bytes_port)[0]

def convert_ip(ip):
	return struct.pack("!4B", *[int(i) for i in ip.split(".")])

def convert_bytes_ip(bytes_ip):


	return socket.inet_ntoa(bytes_ip)

def convert_mac(mac):
	if "-" in mac:
		mac = mac.replace("-",":")
	mac = mac.lower()
	mac_parts = mac.split(":")
	if len(mac_parts)!=6:
		raise ValueError("Invalid MAC address format")
	return struct.pack("!6B", *[int(i, 16) for i in mac_parts])


def main():
   print(convert_ip("192.168.139.2"))	

if __name__ =="__main__":
	 main()
