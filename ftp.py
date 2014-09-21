
from StringIO import StringIO
import ftplib

server = '192.168.1.30'
file = 'asdf.txt'
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
	for l in arr:
		i += 1
		print str(i)
		print l
else:
	print ':('
	
r.close()