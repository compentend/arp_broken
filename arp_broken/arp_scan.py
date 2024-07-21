# coding = UTF-8
from arp import *
import time

nic = "ens33"

attack_ip = "192.168.139.128"
attack_mac = "00:0C:29:92:A9:49"
victim_ip = "192.168.139.129"
victim_mac = "00-0C-29-42-5A-03"
gateway_ip = "192.168.139.2"
gateway_mac = "00-50-56-fb-97-d4"
fake_mac = "11:11:11:11:11:11"
invalid_mac = "ff:ff:ff:ff:ff:ff"

def recv(s):
	while True:
		flow = s.recvfrom(65536)
		packet = flow[0]
		
		if check_arp(packet) is False:
			continue
		opcode = packet[14:][6:8]
		bytes_ip = packet[14:][14:18]
		ip = convert_bytes_ip(bytes_ip)
		if opcode == ARP_RESPONSE:

			print("%s alive" %(ip))
def send(s):

	targets = [attack_ip[0:attack_ip.rindex(".")+1]+ str(i) for i in range(1,255)]
	for target in targets:
		arp_packet = construct_arp_comment(attack_ip,attack_mac,target,invalid_mac,ARP_REQUEST )

	s.send(arp_packet)


def main():
	s = init_socket(nic)

	recv_th = threading.Thread(target = recv , args = (s,))
	recv_th.start()

	send(s)	
	
if __name__=="__main__":
	main()
