import time
from TeacherAccount.models import AccountSystem
import base64
from Crypto.Cipher import AES

BLOCK_SIZE = 16  # Bytes
KEY = 'luckyluckylucky0'
VI = '0102030405060708'

#  补位
pad = lambda s: s + (BLOCK_SIZE - len(s) % BLOCK_SIZE) * \
                chr(BLOCK_SIZE - len(s) % BLOCK_SIZE)
unpad = lambda s: s[:-ord(s[len(s) - 1:])]

def EncodeTicket(account_name): # 返回ticket
    now_time = time.time()
    plain_text = str(now_time) + '$' + account_name
    plain_text = pad(plain_text)
    cipher = AES.new(KEY.encode('utf8'), AES.MODE_CBC, VI.encode('utf8'))
    cipher_text = cipher.encrypt(plain_text.encode('utf8'))
    cipher_text = base64.b64encode(cipher_text)
    cipher_text = cipher_text.decode('utf8')
    return cipher_text

def DecodeTicket(ticket): # 返回account_name
    cipher_text = ticket.encode('utf8')
    cipher_text = base64.decodebytes(cipher_text)
    cipher = AES.new(KEY.encode('utf8'), AES.MODE_CBC, VI.encode('utf8'))
    plain_text = cipher.decrypt(cipher_text)
    plain_text = unpad(plain_text)
    plain_text = plain_text.decode('utf8')

    index = 0
    for ch in plain_text:
        index = index + 1
        if ch == '$':
            break
    ticket_time = (float)(plain_text[:(index - 1)])
    now_time = time.time()
    if ticket_time + 60 * 60 * 24 < now_time: # ticket有效期 1天
        return ''
    return plain_text[index:]

def CheckTicket(ticket):
    account_id = DecodeTicket(ticket)
    account_count = AccountSystem.objects.filter(id=int(account_id)).count()
    if (account_count != 1):
        return ''
    return AccountSystem.objects.filter(id=int(account_id)).values()[0]['username']

def GetUserNameById(id):
    try:
        username = AccountSystem.objects.filter(id=id).values()[0]['username']
        return username
    except Exception:
        return '获取老师用户名失败'


