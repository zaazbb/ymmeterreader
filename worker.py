
#import sys
import time
from datetime import datetime
import traceback

import serial
#from crcmod import predefined

from packet import PacketParser


testdata = [
#'41 CD 01 FF FF 00 00 00 00 00 00 11 11 11 11 11 11 7C 00 00 00 00 00 00 11 11 11 11 11 11 11 01 01 04 11 11 11 11 11 11 03 FF FF 00 00 01 00 01 00 66 55 00 00 00 00 00 00 00 00 00', 
#'43 CD 01 FF FF FF FF FF FF FF FF 11 11 11 11 11 11 F0 96 6E 01 F5 FD FF FF FF 26 E0 FA FF FF FF 7F FF FE FF FF FF FF FF FF FF FF FF FF FF FF DF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF 3F 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00', 
'41 CD 71 82 78 01 00 50 54 10 00 06 05 04 03 02 01 3C 01 00 50 54 10 00 06 05 04 03 02 01 41 0B 06 22 00 00 68 06 05 04 03 02 01 68 91 14 32 38 33 37 33 33 33 33 33 33 33 33 33 33 33 33 33 33 33 33 8E 16 00 00', 
]


def worker(conn, port):
    try:
        ser = serial.Serial(port, 38400, timeout=0)
    except:
        #conn.send(['err', "can't open %s" % port])
        conn.send(['err', traceback.format_exc()])
    buf = bytearray()
    
    flog = open('pkt.log',  'w')
    #f = open('pkt.bin', 'wb')
    
    frame_index = 0
        
    while True:
        if ser.in_waiting:
            try:
                #buf.extend(ser.read(ser.in_waiting))
                b = ser.read(ser.in_waiting)
                #f.write(b)
                #f.flush()
                buf.extend(b)
            except:
                conn.send(['err', traceback.format_exc()])
            #buf.extend(ser.read())
            #print(ser.read(ser.in_waiting))
            print('+++ ', ' '.join('%02X'%ii for ii in buf),  file=flog, flush=True)
            i = buf.find(b'\xFE\xFE\xFE\xFE')
            if i != -1:
                # from wl, no crc.
                if len(buf) > i+4 and len(buf)>= i + buf[i+4] + 5:
                    t = datetime.now().strftime('%H:%M:%S %f')
                    try:
                        pktstr = ' '.join('%02X'%ii for ii in buf[i+8: i+buf[i+4]+5])
                        print('--- ', pktstr,  file=flog, flush=True)
                        #print(pktstr)
                        baseinfo, extinfo = PacketParser(buf[i+8: i+buf[i+4]+5])
                        baseinfo[0:0] = [str(t), 'plc' if buf[i+5] == 0xFF else '%02i-%i'%divmod(buf[i+5], 2)]
                        conn.send(['pkt', baseinfo, extinfo, pktstr])
                    except:
                        #conn.send(['err', 'parsePktError:' + pktstr])
                        #print('-'.join('%02X'%ii for ii in buf[i: i+buf[i+4]+5]),  file=flog, flush=True)
                        errinfo = traceback.format_exc()
                        conn.send(['err', errinfo])
                        print(errinfo,  file=flog, flush=True)
                        print(pktstr)
                    del buf[: i+buf[i+4]+5]
        if conn.poll():
            msg = conn.recv()
            if msg[0] == 'send':
                pkt = bytearray(b'\xFE\xFE\xFE\xFE\x00\x00\x01\x00')
                msg[2][2] = frame_index
                pkt.extend(msg[2])
                pkt[4] = len(msg[2]) + 3
                pkt[5] = msg[1]
                pkt[7] = pkt[4] ^ pkt[5] ^ pkt[6]
                # crc
                #pkt.extend(predefined.mkCrcFun('x-25')(pkt[4:]).to_bytes(2, 'little'))
                try:
                    ser.write(pkt)
                    frame_index += 1
                    if frame_index == 256:
                        frame_index = 0
                except:
                    conn.send(['err', traceback.format_exc()])     
            elif msg[0] == 'setchnlgrp':
                pkt = bytearray(b'\xFE\xFE\xFE\xFE\x03\x0E\x01\x1B')
                pkt[5] = msg[1]
                pkt[7] = pkt[4] ^ pkt[5] ^ pkt[6]
                ser.write(pkt)
                #print('workgroup set to ',  msg[1])
            elif msg[0] == 'parsepkt':
                try:
                    pktstr = ' '.join('%02X'%i for i in msg[1])
                    baseinfo, extinfo = PacketParser(msg[1])
                    baseinfo[0:0] = [msg[0], '']
                    conn.send(['pkt', baseinfo, extinfo, pktstr])
                except:
                    conn.send(['err', traceback.format_exc()])
            #print(' '.join('%02X'%i for i in pkt))

        time.sleep(0.01)


#    for i in testdata:
#        time.sleep(0.5)
#        d = bytearray.fromhex(i)
#        print(' '.join('%02X'%ii for ii in d))
#        t = datetime.now().strftime('%H:%M:%S %f')
#        baseinfo, extinfo = PacketParser(d)
#        baseinfo.insert(0, str(t))
#        conn.send(['pkt', baseinfo, extinfo, ' '.join('%02X'%ii for ii in d)])
#    
#    rxded = [0, 0]
#
#    while True:
#        if conn.poll():
#            payload = conn.recv()
#            if payload[17:17+2] == b'\xF0\x06':
#                addr = payload[5:5+6]
#                addr.reverse()
#                d = None
#                if addr == b'\x11' * 6:
#                    if rxded[0] == 0:
#                        rxded[0] = 1
#                        d = bytearray.fromhex('43 CD 01 FF FF FF FF FF FF FF FF 11 11 11 11 11 11 F0 96 6E 01 F5 FD FF FF FF 26 E0 FA FF FF FF 7F FF FE FF FF FF FF FF FF FF FF FF FF FF FF DF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF 3F 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00')
#                    else:
#                        rxded[0] = 1
#                elif addr == bytes.fromhex('000003100063'):
#                    if rxded[1] == 0:
#                        rxded[1] = 1
#                        d = bytearray.fromhex('43 CD 01 FF FF FF FF FF FF FF FF 63 00 10 03 00 00 F0 96 6E 01 FF FF FF F0 0F FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF 3F 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00')
#                if d:
#                    t = datetime.now().strftime('%H:%M:%S %f')
#                    baseinfo, extinfo = PacketParser(d)
#                    baseinfo.insert(0, str(t))
#                    conn.send(['pkt', baseinfo, extinfo, ' '.join('%02X'%ii for ii in d)])
#        time.sleep(0.01)
