# -*- coding: utf-8 -*-

import win32service
import win32api
import win32serviceutil
import win32event
import servicemanager
#import winerror
#import subprocess
#import shlex
import sys
import os
import psutil


class KennySrv(win32serviceutil.ServiceFramework):

    _svc_name_ = 'KennySrv'
    _svc_display_name_ = 'Kenny.ME Service'
    _svc_description_ = 'Enables you to access your pc anytime, anywhere.'

    def __init__(self, args):
        win32serviceutil.ServiceFramework.__init__(self, args)
        self.hWaitStop = win32event.CreateEvent(None, 0, 0, None)

    def log(self, msg):
        servicemanager.LogInfoMsg(str(msg))

    def sleep(self, sec):
        win32api.Sleep(sec * 1000, True)

    def SvcStop(self):
        self.ReportServiceStatus(win32service.SERVICE_STOP_PENDING)
        self.log('stopping')
        self.my_stop()
        self.log('stopped')
        win32event.SetEvent(self.stop_event)
        self.ReportServiceStatus(win32service.SERVICE_STOPPED)

    def SvcDoRun(self):

        self.ReportServiceStatus(win32service.SERVICE_START_PENDING)
        try:
            self.ReportServiceStatus(win32service.SERVICE_RUNNING)
            self.log('start')
            self.my_start()
            self.log('wait')
            win32event.WaitForSingleObject(self.stop_event, win32event.INFINITE)
            self.log('done')
        except Exception, x:
            self.log('Exception : %s' % x)
            self.SvcStop()

    # to be overridden
    def my_start(self):
        self.runflag = True
        while self.runflag:
            self.sleep(5)
            self.log("I'm alive ...")
    # to be overridden

    def my_stop(self):
        self.runflag = False
        self.log("I'm done")


def module_path():
    encoding = sys.getfilesystemencoding()
    if hasattr(sys, 'frozen'):
        return os.path.dirname(unicode(sys.executable, encoding))
    return os.path.dirname(unicode(__file__, encoding))


def terminate_proc_tree(pid, including_parent=True):
    parent = psutil.Process(pid)
    for child in parent.children(recursive=True):
        child.terminate()
    if including_parent:
        parent.terminate()


def ctrlHandler(ctrlType):
    return True

if __name__ == '__main__':
    if len(sys.argv) == 1:
        servicemanager.Initialize()
        servicemanager.PrepareToHostSingle(KennySrv)
        servicemanager.StartServiceCtrlDispatcher()
    else:
        win32serviceutil.HandleCommandLine(KennySrv)

    """
    if len(sys.argv) == 1:
        servicemanager.Initialize()
        servicemanager.PrepareToHostSingle(AragogService)
        servicemanager.StartServiceCtrlDispatcher()
    else:
        win32api.SetConsoleCtrlHandler(ctrlHandler, True)
        win32serviceutil.HandleCommandLine(AragogService)
    """
