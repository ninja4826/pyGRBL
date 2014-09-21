#Imports
from __future__ import division
import serial, time, sys, argparse, tty
	
def test(x, y, z):

	fd = sys.stdin.fileno()
	old_settings = termios.tcgetattr(fd)
	try:
		tty.setraw(sys.stdin.fileno())
		ch = sys.stdin.read(1)
	finally:
		termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
		
	key = ch
		
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

def manual(x, y, z):
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
	
if mode == 't':

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
		if out == "esc":
			break
	print "Manual mode exiting..."

elif mode == 'g':
	out = gcode(file)
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





















