# ezPCA
Web App for interactive Principal component analysis with feature selection via ANOVA, and interactive Data preprocessing

It all starts with an Excel sheet:
All Apps are build be as intuitive as possible. With the App it is possible to use the advantages of Python without the need to learn the Syntax and since Microsoft office is the most used software for structuring your research data it is just logical to build an interface for Excel. 
Regarding the App it is also possible to use other common datatypes like .csv or .txt. 

In this picture you see a randomized possible dataset with three factors and 14 Parameters. Important...The Excel sheet has to look like this without empty cells,rows, and/or columns.
![Excelsheet_example](https://user-images.githubusercontent.com/109506200/192359614-2ad85830-8602-400e-9704-c2283620ce6a.png)


## The ANOVA App
When you start the App, either from the conda environment or by double-clicking on the batch file run_ANOVA.bat you need to type the ip-address shown on the command prompt in your browser 

![cmd_run](https://user-images.githubusercontent.com/109506200/193014412-c1958e9a-0d82-4aef-b1d9-d8c9959ff8ab.png)


You should be able to see the following picture 

![ANOVA_start](https://user-images.githubusercontent.com/109506200/192362057-45695382-4a9e-49d7-aea3-65d436975539.png)

in the dashed box it is possible to either drag and drop or select your excel sheet from a directory. The maximum of factors for now is three, but in fututre updates this will change to a more elegant solution. With the 'Set ID' Input box you merge the number of factors into one column and generate an standardized sample id based on the factors. With the second Inputbox it is possible to perform a one-way (Just factor1), two-way (Factor 1 & 2), or three-anova (factor 1,2$3) (for now). Future updates are planned. You can check if you set the right amount of factors by clicking on submit without entering a significance level.
On the left side of the screen the ANOVA-Output were sum of squared, degrees of freedom, F-value and p-value are shown. By setting a significance value unsifnificant feature will be eliminated and kicked out of the dataframe. The new Dataframe can be exported as a .csv data file (since I don't want to show the real data here, you have to trust me on that one ;))



## The Preprocessing App

