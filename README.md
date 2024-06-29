# EasyPCA
Web App for interactive Principal component analysis with feature selection via ANOVA, and interactive Data preprocessing

It all starts with an Excel sheet:
All Apps are build be as intuitive as possible. With the App it is possible to use the advantages of Python without the need to learn the Syntax and since Microsoft office is the most used software for structuring your research data it is just logical to build an interface for Excel. 
Regarding the App it is also possible to use other common datatypes like .csv or .txt. 

In this picture you see a randomized possible dataset with three factors and 14 Parameters. Important...The Excel sheet has to look like this without empty cells,rows, and/or columns.
![Excelsheet_example](https://user-images.githubusercontent.com/109506200/192359614-2ad85830-8602-400e-9704-c2283620ce6a.png)


## Installing the necessary Packages
You need to install anaconda as the compiler first. Then click the install batch and wait till the process finished.

## ANOVA for feature selection
To start the ANOVA App double click the ANOVA batch file and wait for the local host connection. 
To upload the data it is possible to drag and drop the Excel file in the box at the top of the site. To operate use the folliwing picture as a guide.

![Bild1](https://user-images.githubusercontent.com/109506200/207357094-3a903ba1-a4f9-4a37-aa62-5d3a114f8d8a.png)

### Output ID
The Output ID are the merged columns of the factors. It is important for the following apps. You can check the output ID by clicking submit without setting alpha.
By setting alpha the non-signifikant features are kicked out of the table. After that you can export the table as a .csv file.

## Preprocessing to have a first evaluation
To start the preprocessing app you double click the preprocessing batch file. After the server connection is established you can drag and drop your exported csv file or if you want to skip the ANOVA your Excel file in the first box on the top of the website. A metafile is also needed for this app in this metafile factors and metadata is listed as the following suggests

![image](https://user-images.githubusercontent.com/109506200/208409682-8eecef88-beec-464f-984f-1310eff108fe.png)


IMPORTANT: The first columns has to be the Output ID....but with another name (like Sample_ID) 

With the Metafile it is possible to color the datapoints according to the  chosen column in order to make a first assumption which of the factors does have an impact on the results. It is comparable to the MatLab Toolbox

### Scaling 
Build into the App is the Autoscaler (or StandardScaler in Python syntax), the RobustScaler, and the MinMaxScaler. By clicking the buttons the scaled data gets plotted and it is possible to export the new scaled data as .csv file. 

![Opera Momentaufnahme_2024-06-28_183254_127 0 0 1](https://github.com/Der-Hensel/EasyPCA/assets/109506200/992f4daf-78ea-4c64-9268-dbca4c064a64)

## EasyPCA

To start the main app you have to doule click the PCA batch file. After drag and dropping the scaled data and metafile you can plot the PCA in two dimensions or three dimensions. With the sliders you can alter which principle component is depicted on whcih axis and with the metafile it is possible to color the data according to the metafile.
## Default Mode of the PCA App
![grafik](https://github.com/Der-Hensel/EasyPCA/assets/109506200/e9dda82a-69b8-4a33-8234-b0eca517eda9)

## Two Dimensional Projection
![grafik](https://github.com/Der-Hensel/EasyPCA/assets/109506200/a9da7272-3c72-4308-88fd-f32914fa146a)
## Three Dimensional Projection
![grafik](https://github.com/Der-Hensel/EasyPCA/assets/109506200/758d353b-12b6-4650-a11d-b586db9f2932)




