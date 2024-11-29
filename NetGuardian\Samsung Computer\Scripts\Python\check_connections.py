@echo off
echo Removing suspicious port forwarding rules...

:: Remove all port proxy settings
netsh interface portproxy reset

:: Display current settings to verify removal
netsh interface portproxy show all

:: Block the specific port that was being forwarded
netsh advfirewall firewall add rule name="Block_41951" dir=in action=block protocol=TCP localport=41951
netsh advfirewall firewall add rule name="Block_41951_Out" dir=out action=block protocol=TCP remoteport=41951