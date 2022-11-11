echo ON
set root=C:\Users\%username%\anaconda3\
call %root%\Scripts\activate.bat %root%
@rem call conda env list
dir

call conda install nb_conda_kernels --yes
call conda create --name ezPCA --yes
call conda activate ezPCA
call conda install ipykernel --yes
call conda install -c anaconda numpy --yes
call conda install -c anaconda pandas --yes
call conda install -c conda-forge dash --yes
call conda install -c conda-forge dash-core-components --yes
call conda install -c conda-forge dash-html-components --yes
call conda install -c conda-forge dash-renderer --yes
call conda install -c conda-forge jupyter-dash --yes
call conda install -c plotly plotly --yes
call conda install -c anaconda scikit-learn --yes
call conda install -c conda-forge statsmodels --yes
call conda install -c anaconda xlrd --yes
call conda install -c anaconda openpyxl --yes
call conda install pip --yes
call pip install dash-draggable


@ECHO ------------------------------------------------
@ECHO ----------------------DONE----------------------
@ECHO ------------------------------------------------
pause
