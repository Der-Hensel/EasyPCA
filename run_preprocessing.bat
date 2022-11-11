ECHO ON
set root=C:\Users\%username%\anaconda3\
call %root%\Scripts\activate.bat %root%

call conda activate ezPCA

call python ezPCA_preprocessing.py

@ECHO ---------------------------------------------------------------------
@ECHO ---------------------------------------------------------------------

pause
