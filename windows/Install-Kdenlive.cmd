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
set "oldOsmo=%LOCALAPPDATA%\kdenlive\scripts\osmo360"
if exist "%oldOsmo%\editor.py" if exist "%oldOsmo%\engine.py" (
  choice /c YN /m "Archive the previous Python add-on files"
  if not errorlevel 2 if errorlevel 1 call :archiveOld
)
echo Installed for the current user. Restart Kdenlive to use Osmo 360 Editor.
pause
exit /b 0
:failed
echo Installation failed. Close the Osmo editor and check that the destination is writable.
pause
exit /b 1

:archiveOld
set "archive=%LOCALAPPDATA%\kdenlive\backups\osmo360-python"
if not exist "%archive%" mkdir "%archive%"
if not exist "%archive%\" (
  echo Could not create the backup folder. The native add-on is registered.
  exit /b 0
)
for %%F in (editor.py media.py camera.py engine.py lensmaps.py spherical.py LICENSE-PanoForge) do (
  if exist "%oldOsmo%\%%F" if not exist "%archive%\%%F" move /-Y "%oldOsmo%\%%F" "%archive%\%%F" >nul
)
echo Previous add-on files are backed up in "%archive%".
exit /b 0
