# File Structure

All_Senator_Tweets/raw_tweets/: This directory contains all the tweets for each of the 100 senators within the time frame. They are not filtered to include those that talk about healthcare and they include non-English tweets.

All_Senator_Tweets/raw_tweets/clean_senate_tweets.py: `python clean_senate_tweets.py` is the command to run. Used to filter the data and outputs into the cleaned_folder.

All_Senator_Tweets/cleaned_tweets/: contains all the filtered senator tweets used to classify. Also includes Classifier.py, run by `python Classifier.py`, which will classify all the tweets in the directory as pro or anti obamacare. Also includes tweetsToMap.py, which converts the tweets into a US map for visualization.

Classifier.py: This is used to classify the tweets in NewClassifyObamacare.csv as pro, anti, or neutral to Obamacare. Run using `python Classifier.py` and will output the accuracies for each of the models.

GetOldTweets-python-master/: Is the Github repository used to collect the senator tweets.

getRandomSenators.py: Run using `python getRandomSenators.py` and outputs which senators to use for the control group. Outputs into SamplingSenators.txt

language.py: `python language.py` is the command. NewObamacare.csv is the input file and it writes out to NewObamacareEn.csv for English tweets and NewObamacareNotEn.csv for non-English tweets.

Media/: Includes deliverables and pictures used for report

NewClassifyObamacare.csv: The csv used to manually classify the Obamacare tweets. These were collected randomly using a bash command.

NewObamacare.csv: This file contains all the tweets about Obamacare between July 19 to July 25, 2017.

populationMap.py: `python populationMap.py` is how you run the file. It will create a visualization of the population for each of the states in the US, this uses Populations.csv as an input

predictVotes.py: run using `python predictVotes.py`. This uses PredictData.csv as input to create different prediction models to guess the final votes for each of the Senators using twitter data.

RepealHealthCareAct.json: Json file from Congressional records that show how each senator voted as well as their respective state and party.

Senate_Tweets/: Senator tweets for the control group and for the nine that voted against party lines.

Senators.csv: csv file for each senator, their state, and their twitter handle

Senators_twitter: is a list of official twitter handles for Senators

training_stats.py: Gathers the stats for the manually classified tweets. Gets how many were anti, pro, or neutral towards Obamacare.

Tweet_Analysis.py: Script used to get preliminary data on the tweets

USPopulation.csv: A file that is tab separated which contains the state and their respective population. Used for data visualization.

# Python version
I used python 3.5.2 to run this code.

# Classifying Obamacare Tweets
We took 600 random tweets from `NewObamacare.csv` and placed them in the file, `NewClassifyObamacare.csv`. From there
we manually went through each of these tweets and add a column to the end of each of the lines for whether they were
against the idea of Obamacare (-1), for the idea of Obamacare (1), or neutral towards the idea (0). For these tweets,
we also deleted any tweet not in English because this would mess with the sentiment analysis tool. Furthermore, we 
will go about removing non-English tweets while analyzing them.
