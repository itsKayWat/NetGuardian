@echo off
NET SESSION >nul 2>&1
if %errorLevel% neq 0 (
    echo Requesting administrative privileges...
    powershell -Command "Start-Process '%~dpnx0' -Verb RunAs"
    exit /b
)

:: Set timestamp for output folder
set "timestamp=%date:~-4%-%date:~4,2%-%date:~7,2%_%time:~0,2%-%time:~3,2%"
set "output_folder=Security_Audit_%timestamp%"

:: Create output directory
mkdir "%output_folder%"

echo Collecting security logs with elevated privileges...

:: System Event Logs with forced elevation
powershell -Command "& {wevtutil epl Security '%output_folder%\Security.evtx'}"
powershell -Command "& {wevtutil epl System '%output_folder%\System.evtx'}"
powershell -Command "& {wevtutil epl Application '%output_folder%\Application.evtx'}"

:: Command history
doskey /history > "%output_folder%\cmd_history.txt"

:: Network connections and listening ports
netstat -ano > "%output_folder%\network_connections.txt"
netstat -b > "%output_folder%\network_processes.txt"

:: Currently running processes
tasklist /v > "%output_folder%\running_processes.txt"

:: Chrome history (requires user profile name)
set "chrome_history=%LOCALAPPDATA%\Google\Chrome\User Data\Default\History"
if exist "%chrome_history%" (
    :: Create a copy since the file might be locked
    copy "%chrome_history%" "%output_folder%\chrome_history.db"
)

:: Recent files accessed
dir /a /s /t:a "%USERPROFILE%\Recent" > "%output_folder%\recent_files.txt"

:: PowerShell command history
if exist "%USERPROFILE%\AppData\Roaming\Microsoft\Windows\PowerShell\PSReadline\ConsoleHost_history.txt" (
    copy "%USERPROFILE%\AppData\Roaming\Microsoft\Windows\PowerShell\PSReadline\ConsoleHost_history.txt" "%output_folder%\powershell_history.txt"
)

echo Log collection complete. Files saved to %output_folder%
pause