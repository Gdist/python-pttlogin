import sys,telnetlib,time
def logNprint(text):
    print(text)
    with open("pttac.log","a") as data:
        data.write(str(text)+"\n")

class Ptt(object):
	def __init__(self, host, user, password):
		self._host = host
		self._user = user.encode('big5')
		self._password = password.encode('big5')
		self._telnet = telnetlib.Telnet(host)
		self._content = ''

	@property
	def is_success(self):
		if u"密碼不對" in self._content:
			logNprint("密碼不對或無此帳號。程式結束")
			sys.exit()
		if u"您想刪除其他重複登入" in self._content:
			logNprint("刪除其他重複登入的連線....")
			self._telnet.write(b"y\r\n")
			time.sleep(5)
			self._content = self._telnet.read_very_eager().decode('big5', 'ignore')
		if u"請按任意鍵繼續" in self._content:
			self._telnet.write(b"\r\n")
			time.sleep(2)
		if u"您要刪除以上錯誤嘗試" in self._content:
			logNprint("刪除以上錯誤嘗試...")
			self._telnet.write(b"y\r\n")
			time.sleep(2)
			self._content = self._telnet.read_very_eager().decode('big5', 'ignore')
		if u"您有一篇文章尚未完成" in self._content:
			logNprint('刪除尚未完成的文章....')
			# 放棄尚未編輯完的文章
			self._telnet.write(b"q\r\n")
			time.sleep(2)
			self._content = self._telnet.read_very_eager().decode('big5', 'ignore')
		return True

	@property
	def input_user_password(self):
		if u"請輸入代號" in self._content:
			#logNprint('輸入帳號中...')
			self._telnet.write(self._user + b"\r\n")
			#logNprint('輸入密碼中...')
			self._telnet.write(self._password + b"\r\n")
			time.sleep(2)
			self._content = self._telnet.read_very_eager().decode('big5', 'ignore')
			return self.is_success
		return False

	def is_connect(self):
		self._content = self._telnet.read_very_eager().decode('big5', 'ignore')
		if u"系統過載" in self._content:
			logNprint('系統過載, 請稍後再來')
			sys.exit(0)
		return True

	def login(self):
		if self.input_user_password:
			logNprint("------------------ 登入完成 ------------------")
			return True

		logNprint("沒有可輸入帳號的欄位，網站可能掛了")
		return False

	def logout(self):
		self._telnet.write(b"qqqqqqqqqg\r\ny\r\n")
		time.sleep(1)
		self._telnet.close()
		logNprint("------------------ 登出完成 ------------------")


def main():
	host = 'ptt.cc'
	with open("pttac.txt" , "r") as ac:
		List = [l.strip().split(",") for l in ac ]
	Dic = {}
	for i in List:
		Dic[i[0]] = i[1]

	localtime = time.asctime( time.localtime(time.time()))
	text = "執行時間: "+localtime
	logNprint(text)
	for i in sorted(Dic.keys()):
		user = i
		password = Dic[i]
		ptt = Ptt(host, user, password)
		time.sleep(1)
		if ptt.is_connect():
			logNprint("執行中帳號:%s"%(i))
			if ptt.login():
				ptt.logout()

if __name__ == "__main__":
	main()
