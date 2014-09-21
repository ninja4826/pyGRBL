#Imports
from __future__ import division
from StringIO import StringIO
import serial, time, sys, argparse, os, ftplib

def manual(x, y, z):
	input = raw_input("Enter command. [W/A/S/D/Q/E]").strip()
	
	if input != '':
	
		input_arr = list(input)
		
		for key in input_arr:
		
			if key.upper() == "W":
				y += 1
			elif key.upper() == 'S':
				y -=1
			elif key.upper() == 'D':
				x += 1
			elif key.upper() == 'A':
				x -= 1
			elif key.upper() == 'Q':
				z += 1
			elif key.upper() == 'E':
				z -=1
				
		output = 'G0 X%s Y%s Z%s' % (str(x), str(y), str(z))
				
	elif input == '':
		output = 'esc'
	
	man = [output, x, y, z]
	
	return man
		
def gcode(file, server):
	
	if server != '':
	
		file_exists = False
		r = StringIO()
		
		try:
			ftp = ftplib.FTP(server)
			ftp.login("russ")
		except Exception,e:
			print e
		else:
			filelist = []
			ftp.retrlines('LIST', filelist.append)
		for f in filelist:
			if file in f:
				file_exists = True
		if file_exists:
			ftp.retrbinary('RETR %s' % file, r.write)
			r_string = r.getvalue()
			arr = [s.strip() for s in r_string.splitlines()]
			i = 0
		else:
			print('File %s does not exist on FTP server :(' % file
			
		r.close()
			
		elif server == '':
		
			f = open(file, 'r');
			arr = []
			for line in f:
			arr.append(line.strip())
	
	f.close()
	return arr


parser = argparse.ArgumentParser()
parser.add_argument('device', help='The path to the device to be controlled.')
parser.add_argument('-m', '--mode')
parser.add_argument('-f', '--file', default='')
parser.add_argument('-ftp', default='')

args = parser.parse_args()

device = args.device
mode = args.mode
file = args.file
server = args.ftp

if server == '':
	s = serial.Serial(device, 9600)
	s.write("\r\n\r\n")
	time.sleep(2)
	s.flushInput()

if mode == 'm':

	print "Entering Manual mode..."
	
	x = 0
	y = 0
	z = 0
	while True:
		
		output = manual(x, y, z)
		out = output[0]
		x = output[1]
		y = output[2]
		z = output[3]
		if out != "esc":
			print out
			s.write(out + '\n')
			grbl_out = s.readline()
			print ' : ' + grbl_out.strip()
		
		if out == "esc":
			break
	print "Manual mode exiting..."
	
elif mode == 'g':

	out = gcode(file, server)
	i = 0
	total =0
	progress = 0
	for l in out:
		total += 1
	for line in out:
		i += 1
		line_print = "%s : %s" % (str(i), line)
		print line_print
		progres = (i/total)*100
		print str(progress) + "% done."
		s.write(line + '\n')
		grbl_out = s.readline()
		print ' : ' + grbl_out.strip()
		
		
elif mode == 'c':
	print "Entering Command mode..."
	while True:
	
		cmd = raw_input("CMD : ").strip()
		
		if cmd == 'exit':
			break
		
		s.write(cmd + '\n')
		
		while True:
			grbl_out = s.readline()
			
			print ' : ' + grbl_out.strip()
			
			arr = grbl_out.split()
			
			if arr[0] == 'ok' or arr[0] == 'error:' :
				break
	
	
raw_input("  Press <Enter> to exit and disable grbl.")

s.close()














