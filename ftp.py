
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
	
print r.getvalue()
