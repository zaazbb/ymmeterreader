
from collections import OrderedDict
from ctypes import Structure, c_ushort, c_ubyte, c_uint

#from crcmod import predefined


SHR = b'\xFE' * 4


class MacFCD(Structure):
    _fields_ = [('FTD',         c_ushort, 3),
                ('secureEn',    c_ushort, 1),
                ('frmHangup',   c_ushort, 1),
                ('ackReq',      c_ushort, 1),
                ('panIdCompr',  c_ushort, 1),
                ('reserve',     c_ushort, 1),
                ('frmIdxcompr', c_ushort, 1),
                ('extInfoInd',  c_ushort, 1),
                ('dstAddrMode', c_ushort, 2),
                ('frmVer',      c_ushort, 2),
                ('srcAddrMode', c_ushort, 2)]
                
class TimeslotLevel(Structure):
    _fields_ = [('timeSlot',    c_ushort,  10), 
                    ('level',   c_ushort,  4), 
                    ('reserve',  c_ushort,  2)]

mac_ftype = ('mBeacon', 'mData', 'mAck', 'mCmd',
               'mReserve', 'mReserve', 'mReserve', 'mReserve')

AddrLen = 0, 0, 2, 6


class NwkFCD(Structure):
    _fields_ = [('FTD',         c_ubyte, 2),
                ('dstAddrMode', c_ubyte, 2),
                ('srcAddrMode', c_ubyte, 2),
                ('reserve',     c_ubyte, 1),
                ('routeInd',    c_ubyte, 1)]

class NwkRouteInfo(Structure):
    _fields_ = [('number',      c_uint, 5),
                ('index',       c_uint, 5),
                ('addrMode0',   c_uint, 2),
                ('addrMode1',   c_uint, 2),
                ('addrMode2',   c_uint, 2),
                ('addrMode3',   c_uint, 2),
                ('addrMode4',   c_uint, 2),
                ('addrMode5',   c_uint, 2),
                ('reserve',     c_uint, 2)]
                
class NwkCfgSnOpt(Structure):
    _fields_ = [('timeSlot', c_ubyte, 1), 
                    ('level', c_ubyte, 1), 
                    ('chnlGrp', c_ubyte, 1), 
                    ('shortAddr', c_ubyte, 1), 
                    ('panId', c_ubyte, 1), 
                    ('relayLst', c_ubyte, 1), 
                    ('reserve', c_ubyte, 1), 
                    ('offline', c_ubyte, 1)]

nwk_ftype = 'nData', 'nCmd', 'nReserve', 'nReserve'
nwk_ctype = {1:'ncJoinNwkReq', 2:'ncJoinNwkResp', 3:'ncRouteErr', 
    0x10:'ncFiGather',  0x11:'ncFiGatherResp',  0x12:'ncCfgSn', 0x13:'ncCfgSnResp', 
    0x16:'ncFreeNdRdy'}
    

class ApsFCD(Structure):
    _fields_ = [('FTD',         c_ubyte, 3),
                ('OEI',         c_ubyte, 1),
                ('reserve',     c_ubyte, 4)]

aps_ftype = ('aAckNack',  'aCmd', 'aRoute', 'aReport', 
               'aReserve', 'aReserve', 'aReserve', 'aReserve')
aps_ctype = ('acCfgUart', 'acSetChnlGrp', 'acSetRssi', 
    'acSetTsmtPower', 'acRdNdCfg', 'acDevReboot', 'acSoftUpgrade', 'acBcastTiming')

aps_baudrate = 'auto', '1200', '2400', '4800',  '9600', '19200'
ApsTsmtPower = {0:'16dBm', 1:'10dBm', 2:'4dBm', 3:'-2dBm'}


def reverse_hex(addr):
    addr.reverse()
    return addr.hex().upper()
    
def bitrate(dat, bitn):
    bits = 0
    for b in dat:
        for i in range(8):
            if (b>>i) & 1:
                bits += 1
    return '%.2f%%' % (bits*100/bitn)
    

def PacketParser(pkt):
#    print(' '.join('%02X' % i for i in pkt))
#    if len(pkt) < 6 or pkt[0] != len(pkt) - 3:
#        return None, 'packet length < 6'
#    if pkt[3] != pkt[0] ^ pkt[1] ^ pkt[2]:
#        return None, 'PHR check error'
#    if predefined.mkCrcFun('x-25')(pkt) != int.from_bytes(pkt[-2:], 'little'):
#        return None, 'crc error'
    #pktdict = {'phy': {'infoChnlIdx': pkt[1], 'stdInd': pkt[2]}}

    i = 0
    
    # parse mac.
    macfcd = MacFCD.from_buffer(pkt[i:i+2])
    #pktdict['mac'] = {'frmType': macfcd.FTD,
    #                  'frmHangup': macfcd.frmHangup,
    #                  'ackReq': macfcd.ackReq,
    #                  'frmVer': macfcd.frmVer}
    baseinfo = [mac_ftype[macfcd.FTD], str(macfcd.ackReq)]
    cmdinfo = OrderedDict()
    i += 2
    if macfcd.frmIdxcompr:
        #pktdict['mac']['frmIdx'] = pkt[i]
        baseinfo.append(str(pkt[i]))
        i += 1
    else:
        baseinfo.append('')
    if macfcd.panIdCompr:
        #pktdict['mac']['panId'] = int.from_bytes(pkt[i:i+2], 'little')
        baseinfo.append(reverse_hex(pkt[i:i+2]))
        i += 2
    else:
        baseinfo.append('')
    n = AddrLen[macfcd.dstAddrMode]
    #pktdict['mac']['dstAddr'] = pkt[i:i+n]
    baseinfo.append(reverse_hex(pkt[i:i+n]))
    i += n
    n = AddrLen[macfcd.srcAddrMode]
    #pktdict['mac']['srcAddr'] = pkt[i:i+n]
    baseinfo.append(reverse_hex(pkt[i:i+n]))
    i += n
    if macfcd.extInfoInd:
        extlen = pkt[i]
        i += 1
        #pktdict['mac']['extInfo'] = pkt[i:i+extlen]
        i += extlen

    if macfcd.FTD == 0:
        # beacon.
        cmdinfo = mac_beacon(pkt[i:])
    elif macfcd.FTD == 2:
        # ack.
        pass
    elif macfcd.FTD == 3:
        # command
        if pkt[i] == 1:
            # network maintain req.
            baseinfo[0] = 'mcNwkMntnReq'
            i += 1
            cmdinfo = nwk_nwk_maintain_req(pkt[i:])
        elif pkt[i] == 2:
            # network maintain resp.
            baseinfo[0] = 'mcNwkMntnResp'
            i += 1
            cmdinfo = nwk_nwk_maintain_resp(pkt[i:])
        elif pkt[i] == 0xF0:
            # ym upgrade.
            #baseinfo[0] = 'mcUpgrade'
            i += 1
            if pkt[i] == 1:
                baseinfo[0] = 'mcUpgRst'
                i += 1
                cmdinfo['vendId'] = reverse_hex(pkt[i:i+2])
                i += 2
                cmdinfo['resetTo'] = 'app' if pkt[i] == 2 else 'boot'
                i += 1
                cmdinfo['checkCode'] = ' '.join(['%02X'%i for i in pkt[i:i+16]])
            elif pkt[i] == 0x91:
                baseinfo[0] = 'mcUpgRstAck'
                i += 1
                cmdinfo['ackCode'] = '%02X' % pkt[i]
            elif pkt[i] == 2:
                baseinfo[0] = 'mcUpgRxm'
                i += 1
                cmdinfo['vendId'] = reverse_hex(pkt[i:i+2])
                i += 2
                cmdinfo['hVer'] = reverse_hex(pkt[i:i+2])
                i += 2
                cmdinfo['fileType'] = str(pkt[i])
                i += 1
                cmdinfo['fileLen'] = str(int.from_bytes(pkt[i:i+2], 'little'))
                i += 2
                cmdinfo['sVer'] = reverse_hex(pkt[i:i+2])
                i += 2
                cmdinfo['crc'] = reverse_hex(pkt[i:i+4])
                i += 4
                cmdinfo['checkCode'] = ' '.join(['%02X'%i for i in pkt[i:i+16]])
            elif pkt[i] == 0x92:
                baseinfo[0] = 'mcUpgRxmAck'
                i += 1
                cmdinfo['ackCode'] = '%02X' % pkt[i]
            elif pkt[i] == 3:
                baseinfo[0] = 'mcUpgTxm'
                i += 1
                cmdinfo['vendId'] = reverse_hex(pkt[i:i+2])
                i += 2
                cmdinfo['upgMode'] = 'bcast' if pkt[i] else 'unicast'
                i += 1
                cmdinfo['dstAddr'] = reverse_hex(pkt[i:i+6])
                i += 6
                cmdinfo['fileType'] = {1:'dsp', 2:'app'}.get(pkt[i], '???')
                i += 1
                cmdinfo['checkCode'] = ' '.join(['%02X'%i for i in pkt[i:i+16]])
            elif pkt[i] == 0x93:
                baseinfo[0] = 'mcUpgTxmAck'
                i += 1
                cmdinfo['ackCode'] = '%02X' % pkt[i]
            elif pkt[i] == 4:
                baseinfo[0] = 'mcUpgPkt'
                i += 1
                cmdinfo['vendId'] = reverse_hex(pkt[i:i+2])
                i += 2
                cmdinfo['pktNum'] = str(int.from_bytes(pkt[i:i+2], 'little'))
                i += 2
                cmdinfo['crc'] = reverse_hex(pkt[i:i+4])
                i += 4
                cmdinfo['pktIdx'] = str(int.from_bytes(pkt[i:i+2], 'little'))
                i += 2
                cmdinfo['pktLen'] = str(pkt[i])
            elif pkt[i] == 0x94:
                baseinfo[0] = 'mcUpgTxmAck'
                i += 1
                cmdinfo['ackCode'] = '%02X' % pkt[i]
                i += 1
                cmdinfo['curFrm'] = str(int.from_bytes(pkt[i:i+2], 'little'))
            elif pkt[i] == 5:
                baseinfo[0] = 'mcUpgSts'
            elif pkt[i] == 0x95:
                baseinfo[0] = 'mcUpgTxmAck'
                i += 1
                cmdinfo['vendId'] = reverse_hex(pkt[i:i+2])
                i += 2
                cmdinfo['hVer'] = reverse_hex(pkt[i:i+2])
                i += 2
                cmdinfo['dspVer'] = reverse_hex(pkt[i:i+2])
                i += 2
                cmdinfo['appVer'] = reverse_hex(pkt[i:i+2])
                i += 2
                cmdinfo['devSn'] = ' '.join(['%02X'%i for i in pkt[i:i+8]])
                i += 8
                cmdinfo['lAddr'] = reverse_hex(pkt[i:i+6])
                i += 6
                cmdinfo['sAddr'] = reverse_hex(pkt[i:i+2])
                i += 2
                cmdinfo['panId'] = reverse_hex(pkt[i:i+2])
                i += 2
                cmdinfo['runMode'] = '%02X' % pkt[i]
            elif pkt[i] == 6:
                baseinfo[0] = 'mcUpgBpSts'
            elif pkt[i] == 0x96:
                baseinfo[0] = 'mcUpgBpStsAck'
                i += 1
                n = int.from_bytes(pkt[i:i+2], 'little')
                cmdinfo['pktnum'] = str(n)
                i += 2
                if n == 0:
                    cmdinfo['upgRate'] = '??'
                else:
                    cmdinfo['upgRate'] = bitrate(pkt[i:i+64], n)
                cmdinfo['bpFlag'] = pkt[i:i+64].hex().upper()
            else:
                baseinfo[0] = 'mcUpg???'
        elif pkt[i] == 0xF1:
            # remote debug.
            baseinfo[0] = 'mcRdbg'
            i += 1
            cmdinfo['dir'] = 'up' if pkt[i]&0x80 else 'down'
            cmdinfo['index'] = str(pkt[i] & 0x7F)
            i += 1
            cmdinfo['cmd'] = str(pkt[i])
            i += 1
            cmdinfo['len'] = str(pkt[i])
            i += 1
            cmdinfo['dat'] = ' '.join('%02X'%ii for ii in pkt[i:-2])
        else:
            baseinfo[0] = 'mcReserve'
    elif macfcd.FTD == 1:
        # data.
        # parse nwk.
        nwkfcd = NwkFCD.from_buffer(pkt[i:i+1])
        #pktdict['nwk'] = {'frmType': nwkfcd.FTD}
        baseinfo[0] = nwk_ftype[nwkfcd.FTD]
        i += 1
        n = AddrLen[nwkfcd.dstAddrMode]
        #pktdict['nwk']['dstAddr'] = pkt[i:i+n]
        baseinfo.append(reverse_hex(pkt[i:i+n]))
        i += n
        n = AddrLen[nwkfcd.srcAddrMode]
        #pktdict['nwk']['srcAddr'] = pkt[i:i+n]
        baseinfo.append(reverse_hex(pkt[i:i+n]))
        i += n
        #pktdict['nwk']['radius'] = pkt[i] & 0x0F
        #pktdict['nwk']['frmIdx'] = pkt[i] >> 4
        baseinfo.append(str(pkt[i] >> 4))
        baseinfo.append(str(pkt[i] & 0x0F))
        i += 1
        if nwkfcd.routeInd:
            routeinfo = NwkRouteInfo.from_buffer(pkt[i:i+4])
            #pktdict['nwk']['relayIdx'] = routeinfo.index
            routeaddrs = []
            i += 3
            #pktdict['nwk']['relayLst'] = []
            for ii in range(routeinfo.number):
                n = AddrLen[getattr(routeinfo, 'addrMode%i' % ii)]
                #pktdict['nwk']['relayLst'].append(pkt[i:i+n])
                routeaddrs.append(reverse_hex(pkt[i:i+n]).lstrip('0'))
                i += n
            baseinfo.append('-'.join(routeaddrs))
        else:
            baseinfo.append('')
                
        if nwkfcd.FTD == 1:
            # command.
            baseinfo[0] = nwk_ctype.get(pkt[i], 'ncReserve')
            if pkt[i] == 1:
                # joinNwkReq
                i += 1
                cmdinfo['cmdOpt'] = '%02X'%pkt[i]
            elif pkt[i] == 2:
                # joinNwkResp
                i += 1
                cmdinfo = nwk_join_nwk_resp(pkt[i:])
            elif pkt[i] == 3:
                # routeErr
                i += 1
                cmdinfo['errCode'] = 'noResp' if pkt[i] == 1 else '--'
                i += 1
                n = AddrLen[nwkfcd.dstAddrMode]
                cmdinfo['failAddr'] = reverse_hex(pkt[i:i+n])
            elif pkt[i] == 0x10:
                # fiGatherCmd
                i += 1
                cmdinfo['pgIdx'] = str(pkt[i] & 0x0F)
            elif pkt[i] == 0x11:
                # fiGatherResp
                i += 1
                cmdinfo['pgIdx'] = str(pkt[i] & 0x0F)
                cmdinfo['totPg'] = str(pkt[i] >> 4)
                i += 1
                n = pkt[i]
                i += 1
                neighbors = []
                for ii in range(n):
                    neighbors.append('%s:%02X' % (reverse_hex(pkt[i:i+6]),  pkt[i+6]))
                    i += 7
                cmdinfo['neighbors'] = '\n'.join(neighbors)
            elif pkt[i] == 0x12:
                # cfgSn
                i += 1
                cmdinfo = nwk_cfg_sn(pkt[i:])
            elif pkt[i] == 0x13:
                # cfgSnResp
                i += 1
                cmdinfo['cmdOpt'] = str(pkt[i])
                i += 1
                cmdinfo['hVer'] =  reverse_hex(pkt[i:i+2])
                i += 2
                cmdinfo['sVer'] =   reverse_hex(pkt[i:i+3])
            elif pkt[i] == 0x16:
                # fNdRdy
                i += 1
                cmdinfo['cmdOpt'] = str(pkt[i])
                i += 1
                tslotlv = TimeslotLevel.from_buffer(pkt[i:i+2])
                cmdinfo['timeSlot'] = str(tslotlv.timeSlot)
                cmdinfo['level'] =str( tslotlv.level)
        elif nwkfcd.FTD == 0:
            # data.
            # parse aps.
            apsfcd = ApsFCD.from_buffer(pkt[i:i+1])
            i += 1
            #pktdict['aps'] = {'frmType': apsfcd.FTD, 'frmIdx': pkt[i]}
            baseinfo.append(str(pkt[i]))
            baseinfo[0] = aps_ftype[apsfcd.FTD]
            i += 1
            if apsfcd.OEI:
                extlen = pkt[i]
                i += 1
                #pktdict['aps']['vendId'] = pkt[i:i+2]
                #i += 2
                #pktdict['aps']['extData'] = pkt[i:i+extlen]
                i += extlen
            #pktdict['aps']['DUI'] = pkt[i]
            #baseinfo.append(str(pkt[i]))
            if apsfcd.FTD == 0:
                # ack/nack.
                baseinfo.append('Ack' if pkt[i] else 'Nack')
                pass
            elif apsfcd.FTD == 1:
                # command.
                baseinfo[0] = aps_ctype[pkt[i]] if pkt[i] < len(aps_ctype) else 'acReserve'
                if pkt[i] == 0:
                    # cfgUart
                    i += 1
                    if pkt[i] > len(aps_baudrate):
                        cmdinfo['baudrate'] = '--'
                    else:
                        cmdinfo['baudrate'] = aps_baudrate[pkt[i]]
                        
                    i += 1
                    if pkt[i] == 0:
                        cmdinfo['parity'] = 'none'
                    elif pkt[i] == 1:
                        cmdinfo['parity'] = 'odd'
                    elif pkt[i] == 2:
                        cmdinfo['parity'] = 'even'
                    else:
                        cmdinfo['parity'] = 'invalid'
                elif pkt[i] == 1:
                    # setChnlGrp
                    i += 1
                    cmdinfo['chnlGrp'] = str(pkt[i])
                elif pkt[i] == 2:
                    # setRssi
                    i += 1
                    cmdinfo['rssi'] = str(pkt[i])
                elif pkt[i] == 3:
                    # setTsmtPower
                    i += 1
                    cmdinfo['tsmtPower'] = ApsTsmtPower.get(pkt[i], '--')
                elif pkt[i] == 4:
                    # rdNodeCfg
                    i += 1
                    if i < len(pkt):
                        cmdinfo = aps_read_node_config(pkt[i:])
                        baseinfo[0] += 'Up'
                    else:
                        baseinfo[0] += 'Dn'
                elif pkt[i] == 5:
                    # devReboot
                    pass
                elif pkt[i] == 6:
                    # softUpgrade
                    i += 1
                    cmdinfo['vendId'] = pkt[i:i+2].hex().upper()
                    i += 2
                    cmdinfo['devType'] = str(pkt[i])
                    i += 1
                    cmdinfo['totPkt'] = str(int.from_bytes(pkt[i:i+2], 'little'))
                    i += 2
                    cmdinfo['curPkt'] = str(int.from_bytes(pkt[i:i+2], 'little'))
                elif pkt[i] == 7:
                    # bcastTiming
                    i += 1
                    cmdinfo['bcastFrmIdx'] = str(pkt[i])
                    i += 1
                    tslotlv = TimeslotLevel.from_buffer(pkt[i:i+2])
                    cmdinfo['timeSlot'] = str(tslotlv.timeSlot)
                    cmdinfo['level'] = str(tslotlv.level)
                    i += 2
                    cmdinfo['maxDly'] = str(int.from_bytes(pkt[i:i+4], 'little'))
                baseinfo.append(baseinfo[0])
            elif apsfcd.FTD == 2:
                # data route.
                # aRoute
                if pkt[i] > len(aps_baudrate):
                    cmdinfo['baudrate'] = '--'
                else:
                    cmdinfo['baudrate'] = aps_baudrate[pkt[i]]
                baseinfo.append('baud' + cmdinfo['baudrate'])
                i += 1
                cmdinfo['data'] = ' '.join('%02X'%ii for ii in pkt[i:])
            elif apsfcd.FTD == 3:
                # report.
                # aReport
                if pkt[i] == 0:
                    cmdinfo['reportType'] = 'evtReprot'
                    i += 1
                    if pkt[i] == 0:
                        cmdinfo['reportInfo'] = 'meterEvt'
                    elif pkt[i] == 1:
                        cmdinfo['reportInfo'] = 'snEvt'
                    else:
                        cmdinfo['reportInfo'] = '--'
                else:
                    cmdinfo['reportType'] = '--'
                baseinfo.append(cmdinfo['reportType'])
            else:
                baseinfo.append(str(pkt[i]))
    #return pktdict
    return baseinfo, cmdinfo
    

def mac_beacon(p):
    i = 0
    info = {}
    info['tsmtRndDly'] = str(p[i])
    i += 1
    info['beaconRound'] = str(p[i])
    i += 1
    tslotlv = TimeslotLevel.from_buffer(p[i:i+2])
    info['timeSlot'] = str(tslotlv.timeSlot)
    info['level'] = str(tslotlv.level)
    i += 2
    info['beaconInd'] = str(p[i])
    i += 1
    info['nwkCapacity'] =  str(int.from_bytes(p[i:i+2], 'little'))
    i += 2
    info['fiThreshold'] = str(p[i])
    i += 1
    info['cnPanId'] =  reverse_hex(p[i:i+2])
    i += 2
    info['cnAddr'] = reverse_hex(p[i:i+6])
    return info
    
def nwk_nwk_maintain_req(p):
    i = 0
    info = {}
    pathn = p[i] & 0x0F
    info['pathNodeNum'] = str(pathn)
    info['pathIdx'] = str(p[i] >> 4)
    i += 1
    # len(p) = 1+x*pathn+pathn-1
    # x = len(p)/pathn - 1
    n = len(p)//pathn - 1
    routers = []
    fipowers = []
    for ii in range(pathn):
        routers.append(reverse_hex(p[i:i+n]))
        i += n
    for ii in range(pathn-1):
        fipowers.append(str(p[i]))
        i += 1
    info['routers'] = '\n'.join(routers)
    info['fiPowers'] = '-'.join(fipowers)
    return info

def nwk_nwk_maintain_resp(p):
    i = 0
    info = {}
    pathn = p[i] & 0x0F
    info['pathNodeNum'] = str(pathn)
    info['pathIdx'] = str(p[i] >> 4)
    i += 1
    # len(p) = 1+x*pathn+2*pathn-2
    # x = (len(p) + 1)/pathn - 2
    n = (len(p) + 1)//pathn - 2
    routers = []
    dnRssi = []
    upRssi = []
    for ii in range(pathn):
        routers.append(reverse_hex(p[i:i+n]))
        i += n
    for ii in range(pathn-1):
        dnRssi.append(str(p[i]))
        i += 1
    for ii in range(pathn-1):
        upRssi.append(str(p[i]))
        i += 1
    info['routers'] = '\n'.join(routers)
    info['dnRssi'] = '-'.join(dnRssi)
    info['upRssi'] = '-'.join(upRssi)
    return info
    
def nwk_join_nwk_resp(p):
    i = 0
    info = {}
    info['cmdOpt'] = '%02X'%p[i]
    i += 1
    info['panId'] = reverse_hex(p[i:i+2])
    i += 2
    info['cnAddr'] = reverse_hex(p[i:i+6])
    i += 6
    tslotlv = TimeslotLevel.from_buffer(p[i:i+2])
    info['timeSlot'] = str(tslotlv.timeSlot)
    info['level'] = str(tslotlv.level)
    i += 2
    info['rssi'] = str(p[i])
    i += 1
    n = p[i]
    info['relayNum'] = str(p[i])
    i += 1
    relays = []
    for ii in range(n):
        relays.append(reverse_hex(p[i:i+2]))
        i += 2
    info['relays'] = '-'.join(relays)
    return info
    
def nwk_cfg_sn(p):
    i = 0
    info = {}
    opt = NwkCfgSnOpt.from_buffer(p[i:i+1])
    i += 1
    info['offline'] = str(opt.offline)
    if opt.chnlGrp:
        info['chnlGrp'] = str(p[i])
        i += 1
    if opt.timeSlot or opt.level:
        tslotlv = TimeslotLevel.from_buffer(p[i:i+2])
    if opt.timeSlot:
        info['timeSlot'] = str(tslotlv.timeSlot)
    if opt.level:
        info['level'] = str(tslotlv.level)
    i += 2
    if opt.shortAddr:
        info['shortAddr'] =  reverse_hex(p[i:i+2])
        i += 2
    if opt.panId:
        info['panId'] =  reverse_hex(p[i:i+2])
        i += 2
    if opt.relayLst:
        n = p[i]
        info['relayNum'] = str(n)
        i += 1
        relayLst = []
        for ii in range(n):
            nn = p[i]
            i += 1
            relays = []
            for iii in range(nn):
                relays.append(reverse_hex(p[i:i+2]))
                i += 2
            relayLst.append('-'.join(relays))
        info['relayLst'] = ','.join(relayLst) 
    return info
    
def aps_read_node_config(p):
    i = 0
    info = {}
    info['factoryAddr'] = reverse_hex(p[i:i+6])
    i += 6
    info['nodeType'] = str(p[i])
    i += 1
    info['panId'] = reverse_hex(p[i:i+2])
    i += 2
    info['shortAddr'] = reverse_hex(p[i:i+2])
    i += 2
    info['vendId'] = reverse_hex(p[i:i+2])
    i += 2
    info['hVer'] = reverse_hex(p[i:i+2])
    i += 2
    info['sVer'] = reverse_hex(p[i:i+3])
    i += 3
    info['tsmtPower'] = ApsTsmtPower.get(p[i], '--')
    i += 1
    info['rssi'] = str(p[i])
    i += 1
    info['chnlGrp'] = str(p[i])
    i += 1
    tslotlv = TimeslotLevel.from_buffer(p[i:i+2])
    info['timeSlot'] = str(tslotlv.timeSlot)
    info['level'] = str(tslotlv.level)
    i += 2
    info['nwkCapacity'] = str(int.from_bytes(p[i:i+2], 'little'))
    i += 2
    n = p[i]
    info['relayNum'] = str(n)
    i += 1
    relayLst = []
    for ii in range(n):
        nn = p[i]
        i += 1
        relays = []
        for iii in range(nn):
            relays.append(reverse_hex(p[i:i+2]))
            i += 2
        relayLst.append('-'.join(relays))
    info['relayLst'] = ','.join(relayLst) 
    return info
    
    
if __name__ == '__main__':
    d = bytearray.fromhex(
        '24 00 01 25 40 CD 01 FF FF FF FF FF FF FF FF 06 05 04 03 02 '
        '01 00 01 1A 04 02 00 23 5F DA 3D AA AA AA AA AA AA 1B EA')
    print(PacketParser(d))
