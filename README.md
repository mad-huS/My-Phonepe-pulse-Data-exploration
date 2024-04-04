# Phonepe-pulse-Data-exploration
![image](https://github.com/mad-huS/My-Phonepe-pulse-Data-exploration/assets/156919023/988deef5-2a3b-4b36-bc12-617b65981cdc)
Hello everyone! I'm excited to introduce you to my latest project - an application designed to explore PhonePe Pulse data.

## What is PhonePe pulse?

PhonePe Pulse is a first-of-its-kind product in India that showcases data about more than ₹. 2000+ crore transactions by consumers. It provides data-driven insights and trends from the Indian digital payments industry based on PhonePe transaction data across India. This dataset contains data from PhonePe Pulse, covering the years 2018-2022 across all quarters. It provides insights into digital payment trends and patterns in India during this time period.

# Lets get into the project!

## 1. Importing the required libraries
  First, Analyse all the data whcih is cloned from the github repository. Next import all the requried libraries for the project.
  
  ![image](https://github.com/mad-huS/My-Phonepe-pulse-Data-exploration/assets/156919023/d04f73ff-c074-4fbb-a3a7-408e39ae9ba8)

  you can use the below syntax to clone the repository from github,
  
  from git.repo.base import Repo
  
  Repo.clone_from("GitHub Clone URL","Path to get the cloned files")

## 2. Data Extraction:
  Extract the available data from the json file and convert it to the DataFrame, so that it can be easily uploaded in a sql database. 
  For this, I have used a nested for loop to extract all the data available.

  ![image](https://github.com/mad-huS/My-Phonepe-pulse-Data-exploration/assets/156919023/023c9c1b-8bac-4362-bfac-eb31af157ece)

## 3. Uploading the data into MySql:
  After extracting the data, establish a connection with the sql data base, here I have used MySql workbench.
  Create tables with the column names as per the Data frame we have created. Then, Insert the values from dataframe into the specified columns.
  
  ![image](https://github.com/mad-huS/My-Phonepe-pulse-Data-exploration/assets/156919023/5c7b0eec-adf0-4f6d-9e3b-ffa1e164e04b)

  creating table and inserting values....
  
  ![image](https://github.com/mad-huS/My-Phonepe-pulse-Data-exploration/assets/156919023/fdf9f7e4-9f06-49e2-b57d-f686b2ee08ac)

## 4. Again extract the data from mysql database and convert it into a data frame.
  By establishing a same connection to the database, we can convert the table available in the mysql database into Dataframes.

  ![image](https://github.com/mad-huS/My-Phonepe-pulse-Data-exploration/assets/156919023/5758ee16-0fe3-4729-9871-ca455d21c151)

## 5. Use plotly express to analyse the data:
    Go through the data available, we can analyse and visualize it using plotly express.

## 6. Work on Streamlit to run the application:
  Install the streamlit package, Design the app as per your requriements.



  

  


