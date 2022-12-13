ECHO ON
set root=C:\Users\%username%\anaconda3\
call %root%\Scripts\activate.bat %root%
start ""  http://127.0.0.1:8080/
call conda activate ezPCA

call python ezPCA_preprocessing.py

@ECHO ---------------------------------------------------------------------
@ECHO ---------------------------------------------------------------------

pause
