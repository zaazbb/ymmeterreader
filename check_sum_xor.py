



s = input('pkt:')

d = bytes.fromhex(s)

xor = 0
for i in d:
    xor ^= i
    
print('len=%02X, %02X %02X' % (len(d), sum(d) % 0x100, xor))

input('press any key to exit.')
