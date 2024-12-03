# Learning-model-project

# Overview

In this Project we were interested in looking at school learning environments, specifically between remote settings and in person settings.
We found a large DataSet consisting of 956k rows that illustrated class room counts and learning modalities(Remote, In Person, or Hybrid) within all
school districts in the United States between the years 2021 and 2022. For our predicitions outcome we were looking to predict in the future there 
would be a shift for more remote learning modality settings in America. In this Repo there will be a brief explanation of how we got our results and
any future improvements we would advise or like to perform in the future. 

# DataSet and Storage

We found our DataSet from a governmental website that had perfomed analysis of their own for the year 2021 to 2022. Downbelow is a snapshot of the site
we downloaded our Data from.

![image](https://github.com/user-attachments/assets/adef4e00-c56b-4b87-b7eb-fbe6eaebdd27)

Once we had chosen and collected our DataSet we had decided to store the DataSet initially into MongoDB but were advised to instead choose SQL since there
is more customization and SQL is more reliable than MongoDB. Once stored we created our Tables and exported the DataSet as a CSV file and started to work
on our code within GoogleCollab for the remainder of this project

# GoogleCollab

Within GoogleCollab we went through the usual process of looking at our Data itself, in order to acertain which columns we needed and could which to remove.
We also removed any NaN values within our DataSet and some rows that had BI as the "state" for certain rows, we discovered BI was a "between states" form of
classification which we decided to avoid since there were only a few of them and it was unecessary for results. 

![image](https://github.com/user-attachments/assets/9752a911-34ae-460d-8908-8f4b06bb8b7a)

Afterwards we decided to start the process of analysing our DataSet and evaluating which model to choose for our large DataSet. We decided to use RandomForrest
since it's a well liked and enjoyable model, especially with such a large set of Data as ours. Throughout the process we had to encode our columns and change 
specific structures of certain columns in order to process the Data. For our model we decided to primarily focus on the individual modalities (remote, hybrid, in
person) along with the student counts, in order to acess any patterns within student counts of certain modalities in order to predict any increases in the future.
During the process we discovered a method with classweight in order to ease the function of training our model as well, so we decided to implement the function
in order to improve the accuracy as much as possible.

![image](https://github.com/user-attachments/assets/10fe08aa-20c2-4271-b943-1898b164fcfc)

After going through the setup and training our model we regrettably didn't succeed in obtaining a good accuracy score for our project. We are not sure if there was
an issue with the scaling of the data, but we believe with more time and knowledge we could increase the accuracy score and improve the model for bettwe pattern 
recognition and generalization. We also did try using a sample of the Data in order to improve the time of the individual epochs of the training, however it only 
improved the model slightly.

![image](https://github.com/user-attachments/assets/2f64f9b1-29c0-4d70-87f5-58f307f9813b)

Originally we planned on having graphical representations of future predicitions but however the code was not functioning correctly and would need further debugging
in order to apply to this project, so we chose to just display the training model and the process of the model itself instead. 

# Tableau

Tableau was chosen to help illustrate what exists within the DataSet itself currently. We wanted to clearly illustrate how the records span across the states themselves
and how the varied within a year. These graphs are included on the public profile of the project mate who created these graphs, there profile will be linked here:https://public.tableau.com/app/profile/marilu.montalvo/vizzes

Below are screenshots of some of the Graphs themselves.

![image](https://github.com/user-attachments/assets/4fdb26c3-1fae-4379-8b30-12e08014396a)
![image](https://github.com/user-attachments/assets/6896a0d7-eae2-4aca-9541-ddbb7a694d1c)


![image](https://github.com/user-attachments/assets/c57471b2-71a5-4830-a02a-a740d8d1acf9)
![image](https://github.com/user-attachments/assets/6daa1550-4d82-4172-8cc6-9bd16b31e87e)


![image](https://github.com/user-attachments/assets/70b0c52f-adaa-458b-a181-8e530629fedb)


# Conclusion / Future thoughts

At the end of this Project we realize that there is much to be worked upon and impoved however the best project is always one that can be improved and improved.
Some take aways we believe from this project are that In-Person learning settings appear to be more dominate in the majority of the United States, which means 
our DataSet was heavily learning towards In-Person over the other two modalities, to fix this we think we could fuse Hybrid and Remote together since we primarily
want to observe any remote classroom settings against pure In-person settings. We believe for future research we should include other countries in the world 
in order to have a more global array of data to truly determine the more dominate learning modality, along with maybe including graduation rates for future questions.




