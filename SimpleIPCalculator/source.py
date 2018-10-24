import socket
import sys
import ipaddress
import re
import json
from socket import inet_ntoa
from struct import pack
def change_to_int(adres):
	a,b,c,d = adres.split(".")
	a = int(a)
	b = int(b)
	c = int(c)
	d = int(d)
	ip = [a,b,c,d]
	return ip
def format_validator (adres):
	match = re.search(r'^\d{1,}.\d{1,}.\d{1,}.\d{1,}/\d{1,}$', adres)
	if(match):
		return True
	else:
		return False
		
def address_validator (adres, maska):
	zwracane = True
	adres = change_to_int(adres)
	maska = int(maska)
	if(adres[0] >=0 and adres[0] <=255 and adres[1]>=0 and adres[1]<=255 and adres[2]>=0 and adres[2]<=255 and adres[3]>=0\
	and adres[3]<=255 and maska >=0 and maska <=32):
		return True
	else:
		return False
		
def cidr_mask(cidr):
	cidr = int(cidr)
	mask = (0xffffffff >> (32 - cidr)) << (32 - cidr)
	return (str( (0xff000000 & mask) >> 24)   + '.' +
          str( (0x00ff0000 & mask) >> 16)   + '.' +
          str( (0x0000ff00 & mask) >> 8)    + '.' +
          str( (0x000000ff & mask)))
		
def adres_sieci(adres,cidr):
	maska = cidr_mask(cidr)
	adres = change_to_int(adres)
	maska = change_to_int(maska)
	x = [adres[0]&maska[0], adres[1]&maska[1], adres[2]&maska[2], adres[3]&maska[3]]
	return ("{}.{}.{}.{}/{}".format(x[0],x[1],x[2],x[3],cidr))
	
def klasa_sieci(adres):
	a = adres.split(".")
	a = int(a[0])
	
	if(a >= 1 and a <= 127):
		return "A"
	elif (a >=128 and a<=191):
		return "B"
	elif (a >=192 and a<=223):
		return "C"
	elif (a >=224 and a<=239):
		return "D"
	else:
		return "E"
	
def binary_address(adres):
	adres = change_to_int(adres)
	return ("{}.{}.{}.{}".format(bin(adres[0])[2:].zfill(8),bin(adres[1])[2:].zfill(8),bin(adres[2])[2:].zfill(8),bin(adres[3])[2:].zfill(8)))

def broadcast_address(adres, maska):
	
	adres = change_to_int(adres)
	maska = change_to_int(maska)
	broadcast = [int(bin(a | ~b), 2) & 0xff for a, b in zip(adres, maska)]
	return ("{}.{}.{}.{}".format(broadcast[0],broadcast[1],broadcast[2],broadcast[3]))
	
def host_min(adres): 	#adres sieci
	
	host_min, maska = adres.split("/")
	host_min = host_min.split(".")
	host_min[3] = str(int(host_min[3])+1)
	
	return ("{}.{}.{}.{}".format(host_min[0],host_min[1],host_min[2],host_min[3]))

def host_max(adres):	#adres broadcast
	host_min = adres.split(".")
	host_min[3] = str(int(host_min[3])-1)
	return ("{}.{}.{}.{}".format(host_min[0],host_min[1],host_min[2],host_min[3]))
	
def host_length(maska):
	liczba =  pow(2, 32-int(maska)) -2
	if(liczba < 0):
		liczba = 0
	return liczba
	
warunek = True
if (len(sys.argv) > 1):
	calosc = sys.argv[1]
	if (format_validator(calosc)):
		adres, maska = calosc.split("/")			
		if not (address_validator(adres, maska)):
			warunek = False
	else:
		warunek = False
else:
	adres = socket.gethostbyname(socket.gethostname())
	adres = ipaddress.ip_network(adres)
	adres,maska = str(adres).split("/")

if(warunek):

	maska_dziesietnie = cidr_mask(maska)
	adres_sieci = adres_sieci(adres,maska)
	klasa_sieci = klasa_sieci(adres)
	maska_binarnie = binary_address(maska_dziesietnie)
	broadcast_address = broadcast_address(adres,maska_dziesietnie)
	broadcast_address_binarnie = binary_address(broadcast_address)
	host_min = host_min(adres_sieci)
	host_min_binarnie = binary_address(host_min)
	host_max = host_max(broadcast_address)
	host_max_binarnie = binary_address(host_max)
	host_length = host_length(maska)
	host_length_binarnie = bin(int(host_length))[2:].zfill(8)
	if(int(maska) > 30):
		host_min = "brak"
		host_min_binarnie ="brak"
		host_max = "brak"
		host_max_binarnie = "brak"
		host_length = "punkt-punkt"
		host_length_binarnie = "punkt-punkt"
	if(int(maska) == 32):
		adres_sieci = "brak"
		klasa_sieci = "brak"
		broadcast_address = "brak"
		broadcast_address_binarnie = "brak"
		host_length = "to jest pojedynczy host, nie siec"
		host_length_binarnie = "to jest pojedyczny host, nie siec"
	print("Adres sieci: {0} ".format(adres_sieci))
	print("Klasa sieci: {0}  ".format(klasa_sieci))
	print("Maska binarnie: {0}  ".format(maska_binarnie))
	print("Maska dziesietnie: {0}  ".format(maska_dziesietnie))
	print("Broadcast binarnie: {0}  ".format(broadcast_address_binarnie))
	print("Broadcast dziesietnie: {0}  ".format(broadcast_address))
	print("Host min binarnie: {0}  ".format(host_min_binarnie))
	print("Host min dziesietnie: {0}  ".format(host_min))
	print("Host max binarnie: {0}  ".format(host_max_binarnie))
	print("Host max dziesietnie: {0}  ".format(host_max))
	print("Ilosc hostow binarnie: {0}  ".format(host_length_binarnie))
	print("Ilosc hostow dziesietnie: {0}  ".format(host_length))
	data = {}
	data['adres'] = []
	data['adres'].append({
		'adres sieci' : adres_sieci,
		'klasa sieci' : klasa_sieci,
		'maska sieci binarnie' : maska_binarnie,
		'maska sieci dziesietnie' : maska_dziesietnie,
		'adres broadcast binarnie' : broadcast_address_binarnie,
		'adres broadcast dziesietnie' : broadcast_address,
		'min adres hosta binarnie' : host_min_binarnie,
		'min adres hosta dziesietnie' : host_min,
		'max adres hosta binarnie' : host_max_binarnie,
		'max adres hosta dziesietnie' : host_max,
		'ilosc hostow binarnie' : host_length_binarnie,
		'ilosc hostow dziesietnie' : host_length
	})
	with open('data.json', 'w') as outfile:
	
		json.dump(data, outfile)
else:
	print("Wprowadzono niepoprawny adres")
