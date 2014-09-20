#Imports
import serial
import time
import sys
import argparse

def manual(x, y, z):
	print 'Entering Manual mode'
	key = raw_input("Enter command. [W/A/S/D/Q/E]").strip()
	key.upper()
	if key.upper() == "W":
		output = 'G0 X%s Y%s Z%s' % (str(x), str(y + 1), str(z))
		y += 1
	elif key.upper() == 'S':
		output = 'G0 X%s Y%s Z%s' % (str(x), str(y - 1), str(z))
		y -=1
	elif key.upper() == 'D':
		output = 'G0 X%s Y%s Z%s' % (str(x + 1), str(y), str(z))
		x += 1
	elif key.upper() == 'A':
		output = 'G0 X%s Y%s Z%s' % (str(x - 1), str(y), str(z))
		x -= 1
	elif key.upper() == 'Q':
		output = 'G0 X%s Y%s Z%s' % (str(x), str(y), str(z + 1))
		z += 1
	elif key.upper() == 'E':
		output = 'G0 X%s Y%s Z%s' % (str(x), str(y), str(z - 1))
		z -=1
	elif key.upper() == '':
		output = "esc"
	
	man = [output, x, y, z]
	
	return man
		
def gcode(file):

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

args = parser.parse_args()

device = args.device
mode = args.mode
file = args.file

s = serial.Serial(device, 9600)
s.write("\r\n\r\n")
time.sleep(2)
s.flushInput()

if mode == 'm':
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
	out = gcode(file)
	
	for line in out:
		print line
		s.write(line + '\n')
		grbl_out = s.readline()
		print ' : ' + grbl_out.strip()
raw_input("  Press <Enter> to exit and disable grbl.")

s.close()