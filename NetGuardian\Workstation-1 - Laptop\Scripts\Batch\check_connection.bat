@echo off
NET SESSION >nul 2>&1
if %errorLevel% neq 0 (
    echo Requesting administrative privileges...
    powershell -Command "Start-Process '%~dpnx0' -Verb RunAs"
    exit /b
)

echo Checking network connections with elevated privileges...
set "timestamp=%date:~-4%-%date:~4,2%-%date:~7,2%_%time:~0,2%-%time:~3,2%"
set "log_file=connection_check_%timestamp%.log"

echo =========================================== >> %log_file%
echo Network Connection Check - %date% %time% >> %log_file%
echo =========================================== >> %log_file%

echo Checking current connections...
netstat -ano >> %log_file%

echo Checking active port forwarding rules...
netsh interface portproxy show all >> %log_file%

echo Checking listening ports...
netstat -an | find "LISTENING" >> %log_file%

echo Checking running processes with network connections...
netstat -b >> %log_file%

echo Checking DNS cache...
ipconfig /displaydns >> %log_file%

echo Checking routing table...
route print >> %log_file%

echo Connection check complete. Results saved to %log_file%
echo Please check %log_file% for detailed information.

pause