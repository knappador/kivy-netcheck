kivy-netcheck
=============

Check and prompt for network connection as necessary.  Conditional import for Android support and can be debugged on desktop.

#### Features
If there is no connection, the module can be configured to ask the user if they want to open settings and then **take them to network settings** to give them a chance to get a connection before **doing your network activity after the app resumes if the user was able to connect**.  Uses P4A/PyJNIus and includes sample app.

#### Install
Pre-built application in ```/bin```
adb install -r /bin/NetcheckTesting-0.1-debug-unaligned.apk

#### Build
Copy the netcheck.sh to a P4A dist then run:
```netcheck.sh my/path/to/app/```
If it doesn't work, edit netcheck.sh to configure P4A to build this.  Need PyJNIus in your dist. 

#### Debuggable
```.netcheck/main.py``` To see some toggle switches for turning on and off the fake results during debugging.

#### Docs
Public API.

Should be py3k compatible.  Not tested.  Contact me for support.
