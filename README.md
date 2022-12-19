# EasyPCA
Web App for interactive Principal component analysis with feature selection via ANOVA, and interactive Data preprocessing

It all starts with an Excel sheet:
All Apps are build be as intuitive as possible. With the App it is possible to use the advantages of Python without the need to learn the Syntax and since Microsoft office is the most used software for structuring your research data it is just logical to build an interface for Excel. 
Regarding the App it is also possible to use other common datatypes like .csv or .txt. 

In this picture you see a randomized possible dataset with three factors and 14 Parameters. Important...The Excel sheet has to look like this without empty cells,rows, and/or columns.
![Excelsheet_example](https://user-images.githubusercontent.com/109506200/192359614-2ad85830-8602-400e-9704-c2283620ce6a.png)


## Installing the necessary Packages
For this double click on the .exe file and a graphic user interface should appear in the middle of your screen.

![image](https://user-images.githubusercontent.com/109506200/201372190-4f874dbe-dc10-45b5-a62c-d8dbe7df1d6d.png)

click the install button and wait til the process finished.
To start the Application click on the run Buttons and copy the ip address in prefferd browser


## ANOVA for feature selection
To start the ANOVA App press the "Run ANOVA" Button on the GUI and wait for the server connection. 
To upload the data it is possible to drag and drop the Excel file in the box at the top of the site. To operate use the folliwing picture as a guide.

![Bild1](https://user-images.githubusercontent.com/109506200/207357094-3a903ba1-a4f9-4a37-aa62-5d3a114f8d8a.png)

### Output ID
The Output ID are the merged columns of the factors. It is important for the following apps. You can check the output ID by clicking submit without setting alpha.
By setting alpha the non-signifikant features are kicked out of the table. After that you can export the table as a .csv file.

## Preprocessing to have a first evaluation
To start the preprocessing app you click on the "Run preprocessing" button in the GUI. After the server connection is established you can drag and drop your exported csv file or if you want to skip the ANOVA your Excel file in the first box on the top of the website. A metafile is also needed for this app in this metafile factors and metadata is listed as the following suggests

![image](https://user-images.githubusercontent.com/109506200/208409682-8eecef88-beec-464f-984f-1310eff108fe.png)


IMPORTANT: The first columns has to be the Output ID....but with another name (like Sample_ID) 
