#Using Python to create windows service
#Template 

	import win32serviceutil
	import win32event
	import servicemanager
	
	class MyService(win32serviceutil.ServiceFramework):
		_svc_name_ = 'KennySrv'
    	_svc_display_name_ = 'Kenny Test Service'
    	_svc_description_ = 'Test Kenny Service'

		def __init__(self, args):
        	win32serviceutil.ServiceFramework.__init__(self, args)
        	self.hWaitStop = win32event.CreateEvent(None, 0, 0, None)
		
		def SvcDoRun(self):
			self.ReportServiceStatus(win32service.SERVICE_START_PENDING) 
			self.ReportServiceStatus(win32service.SERVICE_RUNNING)
			...
			win32event.WaitForSingleObject(self.stop_event, win32event.INFINITE)
		
		def SvcStop(self):
			self.ReportServiceStatus(win32service.SERVICE_STOP_PENDING)
			...
			win32event.SetEvent(self.stop_event)
        	self.ReportServiceStatus(win32service.SERVICE_STOPPED)

Using the win32serviceutil.ServiceFramewok and implement above these function.
Note that the keyword **\_svc_name\_**, **\_svc_display_name\_** and **_svc_description\_** is the windwos service keyword. To explain below

* \_svc_name\_ : It's a name for Windows Service Name, this name could be the same name of the Class Name, or could not, for example, the Class Name is MyService, the svc_name could be the same (MyService) or other name (KennySrv). The important thing is, when load the service into the windows, we must be to use the srv_name, not class name!
* \_svc_display_name\_ : When service is loaded, Windows service manager will show this **display name**
* \_svc_description_ : It's just a description and will be put the note.

##Test Method 
### Pythonic way
When you write down the code which name is MyService.py for example, you cane use the pythonic way to test, the instruction list below.

1. python MyService.py install (install the service to windows)
2. net start KennySrv (if the \_srv_name\_ is KennySrv)
3. All of the message will be output to Event viewer, You can open the start menu and type the **evnetvwr** to open this application. (Windows Logs --> Application)
4. net stop KennySrv (stop the service from windows)
5. python MyService.py remove  (remove the servie from windows service register list)

### Executable way
If your python script has been converted to executable file(using pyinstaller or py2exe), then you can just do the same thing but no python keyword

1. MyService.exe install
2. net start KennySrv
3. net stop KennySrv
4. MyService.exe remove

### Debug mode
You can open the debug mode like this
* python MyService.py debug, or
* MyService.exe debug
All of the messages will be output to console screen.

## Issue
If you use net command to start the service but the servies can't run successfully, restart again, it will be ok.

### Net tool and sc tool
* NET COMMAND: The net use command is a Command Prompt command that's used to connect to, remove, and configure connections to shared resources, like mapped drives and network printers.
* SC COMMAND: Service Control - Create, Start, Stop, Query or Delete any Windows SERVICE. The command options for SC are case sensitive. 

### Using SC to create, start, stop and delete service 
Using the sc command to create service, the instruction is below
#### To create the service
`sc create [_srv_name_] binpath= "The full path of your executable file full"`

for example: 

`sc create KennySrv binpath= "C:\abc\def\MyService.exe"`

#### To start the service
`sc start [_srv_name_]`

for example

`sc start KennySrv`

#### To stop the service

`sc stop [_srv_name_]`

for example

`sc stop KennySrv`

#### To delete the service

`sc delete [_srv_name_]`

for example

`sc delete KennySrv`


### Mix the net and sc

When you install the service by executable file (like MyServie.exe install), you can remove(delete) this service by sc, just use sc delete command :)

Important Note: the option **binpath=** or other options of sc must be followed by the one space character(blank), if you have not this, the sc command will show syntax error message.

For example

* Wrong way: `binpath="C:\abc\def\MyService.exe"`
* Right way: `binpath= "C:\abc\def\MyService.exe"`
