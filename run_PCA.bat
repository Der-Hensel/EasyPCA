ECHO ON
set root=C:\Users\%username%\anaconda3\
call %root%\Scripts\activate.bat %root%
start ""  http://127.0.0.1:8050/
call conda activate ezPCA

call python ezPCA_PCA_v1.py

@ECHO ---------------------------------------------------------------------
@ECHO ---------------------------------------------------------------------

pause

