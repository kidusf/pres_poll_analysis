# Poll Analysis
This project analysizes the polls during the 2020 election season. Note that the data set from this repository is from the 538 dataset repository and I do not claim ownership 
of this dataset.

The dataset is included in the github repository. The program will read in the dataset when run and give the following prompt:

![Prompt](https://github.com/kidusf/pres_poll_analysis/blob/main/Output.PNG)

NOTE: all of the polls are averaged by each day for the plots and the bar plots average all of the state's data

When Option 1 is selected, it will prompt the user for a state and give a statistical summary. An example graph is shown below for the state of Colorado:

![Colorado](https://github.com/kidusf/pres_poll_analysis/blob/main/StateGraph.PNG)


![Summary](https://github.com/kidusf/pres_poll_analysis/blob/main/Colorado%20Summary.PNG)

When Option 2 is selected, it will plot the National Data and give a statistical summary:

![National](https://github.com/kidusf/pres_poll_analysis/blob/main/FilteredNational.PNG)


![Sum](https://github.com/kidusf/pres_poll_analysis/blob/main/National.PNG)

When Option 3 is selected, it will plot all of the state margins in a bar plot and it will categorize states by tilt, lean, likely, and safe states

![Margins](https://github.com/kidusf/pres_poll_analysis/blob/main/MarginsPlot.PNG)


![Category](https://github.com/kidusf/pres_poll_analysis/blob/main/MarginsCategory.PNG)

When Option 4 is selected, it will predict who will win based on the state margins and electoral votes each state had

![Predict](https://github.com/kidusf/pres_poll_analysis/blob/main/PredictedPlot.PNG)



When Option 5 is selected, it will exit the program. This repository is likely to be modified to support web browsers
