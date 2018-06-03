# Python-PTTautologin-mu
多用戶的PTT自動登入程式
## 使用方法
在pttac.txt內輸入帳號密碼，中間以","分隔，每行輸入一組帳號
```
ac1,pw1
ac2,pw2
```
## 可搭配crontab使用
```
0 */8 * * * /usr/bin/python3 /root/pttac.py
```

[修改自PttAutoLoginPost](https://github.com/twtrubiks/PttAutoLoginPost)
