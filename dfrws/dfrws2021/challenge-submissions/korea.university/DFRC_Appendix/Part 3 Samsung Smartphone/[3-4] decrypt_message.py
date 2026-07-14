import sqlite3
import base64
from unittest import result
import zlib
from Crypto.Cipher import AES

key = b"rb5CuefkDLyb9T"

def main():
    conn = sqlite3.connect("mmssms.db")
    cursor = conn.cursor()

    cursor.execute("SELECT type, address, date(strftime('%Y-%m-%d %H:%M:%S.', \"date\"/1000, 'unixepoch') || (\"date\"%1000), \"+2 hours\") as _date,\
        datetime(strftime('%Y-%m-%d %H:%M:%S.', \"date\"/1000, 'unixepoch') || (\"date\"%1000), \"+2 hours\") as date,\
        body FROM sms")
    
    results = []
    for row in cursor.fetchall():
        if row[4][0:3] == "HHY":
            row = list(row)
            decoded_str = base64.b64decode(row[4][3:].encode("utf-8"))
            aes = AES.new(key+bytes(row[2].encode("ascii")), AES.MODE_ECB)
            row[4] = aes.decrypt(decoded_str)
            if row[0] == 1:
                row[0] = "SEND"
            else:
                row[0] = "RECEIVE"
            results.append([row[0], row[1], row[3], row[4]])
            
    if len(results) > 0:
        cursor.execute("CREATE TABLE IF NOT EXISTS dec_sms \
            (type text, address text, date datetime, body text)")
        
        sql = "INSERT INTO dec_sms(type, address, date, body) VALUES (?, ?, ?, ?)"
        unpad = lambda s: s[0:-ord(s[-1])]
        for result in results:
            result[3] = unpad(result[3].decode("utf-8"))
            cursor.execute(sql, (result[0], result[1], result[2], result[3]))
        conn.commit()
    
    conn.close()

if __name__ == '__main__':
    main()