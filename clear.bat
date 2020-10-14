for /F "delims=" %%a in ('dir /s/b *.ipynb') do nbstripout "%%a"

pause