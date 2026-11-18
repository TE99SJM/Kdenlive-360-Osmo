@echo off
setlocal
set "osmoDir=%LOCALAPPDATA%\kdenlive\scripts\osmo360-native"
if not exist "%~dp0app\osmo360-editor.exe" (
  echo Extract the entire Windows ZIP before running this installer.
  pause
  exit /b 1
)
robocopy "%~dp0app" "%osmoDir%" /E /R:2 /W:1 /NFL /NDL /NJH /NJS /NP
if errorlevel 8 goto failed
start "" /wait "%osmoDir%\osmo360-editor.exe" --install --data-dir "%LOCALAPPDATA%\kdenlive"
if errorlevel 1 goto failed
echo Installed for the current user. Restart Kdenlive to use Osmo 360 Editor.
pause
exit /b 0
:failed
echo Installation failed. Close the Osmo editor and check that the destination is writable.
pause
exit /b 1
