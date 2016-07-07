
#import os.path


def mk_upg02(src, flen, sver, crc):
    template = '43 CD 01 FF FF FF FF FF FF FF FF 33 21 10 03 00 00 F0 02 01 00 01 00 02 6E 01 88 77 1D 4D 95 28 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00'
    pkt = bytearray.fromhex(template)
    i = 11
    srcaddr = bytearray.fromhex(src)
    srcaddr.reverse()
    pkt[i:i+6] = srcaddr
    i += 6
    i += 7
    pkt[i:i+2] = flen.to_bytes(2, 'little')
    i += 2
    sver &= 0xFFFF
    pkt[i:i+2] = sver.to_bytes(2, 'little')
    i += 2
    pkt[i:i+4] = crc.to_bytes(4, 'little')
    return pkt

def _chk_xor(d):
    xor = 0
    for i in d:
        xor ^= i
    return xor

def mk_upg04(src, flen, crc, index, d):
    template = '43 CD 01 FF FF FF FF FF FF FF FF 33 21 10 03 00 00 F0 04 01 00 6E 01 1D 4D 95 28 01 00 80'
    pkt = bytearray.fromhex(template)
    i = 11
    srcaddr = bytearray.fromhex(src)
    srcaddr.reverse()
    pkt[i:i+6] = srcaddr
    i += 6
    i += 4
    pkt[i:i+2] = flen.to_bytes(2, 'little')
    i += 2
    pkt[i:i+4] = crc.to_bytes(4, 'little')
    i += 4
    pkt[i:i+2] = index.to_bytes(2, 'little')
    pkt.extend(d)
    pkt.append(sum(d) % 0x100)
    pkt.append(_chk_xor(d))
##    with open('upgdat.txt', 'a') as f:
##        f.write('index=%i\n'%index)
##        f.write(' '.join('%02X'%i for i in d))
##        f.write('\n')
    return pkt

def mk_bpsts(dst, src):
    template = '63 CD 01 FF FF 11 11 22 22 33 33 FF FF FF FF FF FF F0 06'
    pkt = bytearray.fromhex(template)
    i = 5
    srcaddr = bytearray.fromhex(dst)
    srcaddr.reverse()
    pkt[i:i+6] = srcaddr
    i += 6
    srcaddr = bytearray.fromhex(src)
    srcaddr.reverse()
    pkt[i:i+6] = srcaddr
    i += 6
    return pkt   

def get_app_code(fcb):
    with open(fcb, 'rb') as f:
        d = f.read()
#        if os.path.splitext(fcb)[1] == '.bin':
#            return d[:0xb700]
        # 0 - reserve, 1 - ht8550, 3 - ht8910/ht8912.
        if d[8] != 3:
            print('fcb is not for ht8912')
            return
        # 0 - download file, 1 - iap file.
        if d[12] != 0:
            print('fcb is not a download file')
            return
        i = 32
        while i < len(d):
            
            length = int.from_bytes(d[i:i+2], 'little')
            i += 2
            addr = int.from_bytes(d[i:i+3], 'little')
            i += 3
            # 0 - global addr, 1 - int_flash addr, 2 - ext_flash addr.
            addrtype = d[i]
            i += 1
            i += 10
            #print(hex(length))
            #print(hex(addr))
            #print(addrtype)
            if addrtype == 1 and addr == 0x10000:
                return d[i:i+length]
            else:
                i += length
                
def mk_chng2txm(dst, src):
    template = '63 CD 01 FF FF 11 11 22 22 33 33 FF FF FF FF FF FF F0 03 01 00 01 FF FF FF FF FF FF 02 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00'
    pkt = bytearray.fromhex(template)
    i = 5
    dstaddr = bytearray.fromhex(dst)
    dstaddr.reverse()
    pkt[i:i+6] = dstaddr
    i += 6
    srcaddr = bytearray.fromhex(src)
    srcaddr.reverse()
    pkt[i:i+6] = srcaddr
    return pkt
    
def mk_rdsncfg(dst, src):
    template = '41 CD 01 FF FF 11 11 22 22 33 33 00 00 00 00 00 00 7C 11 11 22 22 33 33 00 00 00 00 00 00 11 01 01 04'
    pkt = bytearray.fromhex(template)
    i = 5
    dstaddr = bytearray.fromhex(dst)
    dstaddr.reverse()
    pkt[i:i+6] = dstaddr
    i += 6
    srcaddr = bytearray.fromhex(src)
    srcaddr.reverse()
    pkt[i:i+6] = srcaddr
    i += 6
    # nwk control
    i += 1
    pkt[i:i+6] = dstaddr
    i += 6
    pkt[i:i+6] = srcaddr
    i += 6
    return pkt
    
def mk_readback(dst, src):
    template = '63 CD 01 FF FF 11 11 22 22 33 33 FF FF FF FF FF FF F0 07'
    pkt = bytearray.fromhex(template)
    i = 5
    dstaddr = bytearray.fromhex(dst)
    dstaddr.reverse()
    pkt[i:i+6] = dstaddr
    i += 6
    srcaddr = bytearray.fromhex(src)
    srcaddr.reverse()
    pkt[i:i+6] = srcaddr
    return pkt
    

if __name__ == '__main__':
    d = get_app_code(r'D:\work\repository\YM001\trunk\software\proj\app\obj\app_with_boot.fcb')
    print(' '.join('%02X'%i for i in d[:128]))
    print(' '.join('%02X'%i for i in d[-256:-128]))
    print(' '.join('%02X'%i for i in d[-128:]))
