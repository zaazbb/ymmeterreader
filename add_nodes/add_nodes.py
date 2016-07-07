
import ctypes


win_main = '浙江宏睿通信技术有限公司互联互通抄表系统'
win_addnode = '[CLASS:#32770]'



dll = ctypes.WinDLL('AutoItX3_x64.dll')
dll.AU3_Init()


if dll.AU3_WinExists(win_main, ''):
    dll.AU3_WinActivate(win_main, '')
    dll.AU3_WinActivate(win_addnode, '')
    #dll.AU3_ControlClick(win_addnode, '',
    #                 '[CLASS:Button; INSTANCE:1]',
    #                 'left', 1, 0, 0)
    dll.AU3_Send('{ENTER}', 0)
    #dll.AU3_Send('{ENTER}{TAB 2}%s{ENTER}' % node, 0)
##    with open('nodes.txt') as f:
##        for line in f:
##            node = line.strip()
##            if not node:
##                continue
##            if dll.AU3_WinExists(win_addnode, '从节点信息管理'):
##                dll.AU3_ControlClick(win_addnode, '从节点信息管理',
##                                     '[CLASS:Button; INSTANCE:1]',
##                                     'left', 1, 5, 5)
##                dll.AU3_Send('{TAB 2}%s{ENTER}' % node, 0)
##            elif dll.AU3_WinExists(win_addnode, '档案确认'):
##                dll.AU3_ControlClick(win_addnode, '',
##                                     '[CLASS:Button; TEXT:手动添加]',
##                                     'left', 1, 0, 0)
##                dll.AU3_Send('{TAB 2}%s{ENTER}' % node, 0)
