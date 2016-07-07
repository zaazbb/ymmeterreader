
start_flag = 'readback===\r\n'.encode()
end_flag = '===readbackok\r\n'.encode()

with open('untitleapp3.txt', 'rb') as f, open('app-3.bin', 'wb') as fo:
    d = f.read()
    start = d.index(start_flag)
    print(hex(start))
    end = d.rindex(end_flag)
    print(hex(end))
    fo.write(d[start+len(start_flag):end])
    
