import hashlib

sta = '1250000.0'
end = '15000000.0'
msg = "25d55ad283aa400af464c76d713c07ad"

for i in range(int(sta.split(".")[0]), int(end.split(".")[0])):
    # encrypted_msg = hashlib.md5(str(i).zfill(5).encode()).hexdigest()
    encrypted_msg = hashlib.md5(str(i).encode()).hexdigest()
    if encrypted_msg == str(msg):
        print("found!", str(i))
        ANSWER = str(i)
ANSWER = 0
