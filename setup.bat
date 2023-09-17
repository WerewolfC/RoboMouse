
@setlocal enableextensions enabledelayedexpansion
@echo off
echo:
echo 1 - Setting up current working folder
FOR /f %%i IN ('cd') DO set cwd=%%i
echo [INFO]- Working folder set to: %cwd%
echo:
echo 2 - Setting up python virtual enviroment
FOR /f "delims=" %%G IN ('where python') DO (
    set py=%%G
    set pythonVersion=Python311
    if not "!py:%pythonVersion%=!"== "%py%" (
        goto INSTALLVENV
    ) ELSE (
            echo [ERROR]- Python 3.1x is missing
            goto FAILEDSCRIPT
    )
)

:INSTALLVENV
echo [INFO]- Python was found %py%
echo [INFO]- Creating virtual enviroment
%py -m venv .venv
IF %ERRORLEVEL% EQU 0 (
    echo [INFO]- Virtual enviroment created
) ELSE (
    echo [ERROR]- Failed to create virtual enviroment
    goto FAILEDSCRIPT
)
echo:
echo 3 - Setting up pip requirements
set scriptFolder=\.venv\Scripts\
set scriptPath=%cwd%%scriptFolder%
cd %scriptPath%
call activate.bat
IF %ERRORLEVEL% EQU 0 (
    echo [INFO]- Virtual enviroment active
) ELSE (
    echo [ERROR]- Virtual enviroment inactive
    goto FAILEDSCRIPT
)

python -m pip install --upgrade pip
IF %ERRORLEVEL% EQU 0 (
    echo [INFO]- Pip updated succesfully
) ELSE (
    echo [ERROR]- Pip update failed
    goto FAILEDSCRIPT
)

echo [INFO]- Existing packages:
python -m pip list
cd %cwd%
python -m pip install -r pip_requirements.txt
IF %ERRORLEVEL% EQU 0 (
    echo [INFO]- Pip packages installed succesfully
) ELSE (
    echo [ERROR]- Pip packages update failed
    goto FAILEDSCRIPT
)
echo [INFO]- Current Pip packages:
python -m pip list

echo:
echo 4 - Setting up launch application file
set pythonExe=pythonw.exe
set appExe=app.py
set launcher=launcher.bat
echo @echo off > %launcher%
echo start "" %scriptPath%%pythonExe% %cwd%\%appExe% >> %launcher%
echo [INFO]- %launcher% file has been created - use it to launch the app!
echo:
echo **************** Setup finished !!! ***************
goto:ENDSCRIPT


:FAILEDSCRIPT
echo [ERROR]- Setup procedure not finished due to missing requirements!!!
goto ENDSCRIPT
:ENDSCRIPT
echo:
pause
endlocal
