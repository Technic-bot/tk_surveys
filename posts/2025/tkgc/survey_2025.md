# Twokinds Group Chat survey 2025

Hello and welcome to another edition of our now traditional yearly survey!

I am Tec and you may have heard of me before, I adore using data to understand and visualize things i like and communities i partake in. As such i have been doing these survey to get a feel about how our little corner of the internet works and looks. 

As usual we will start with some demographic information to know who we are and then follow up with some common questions about the comic an its characters. But this year i deciided to bite the bullet and do some free form questions which proved to be interesting. I have a background in STEM so doing these types of non numeric questions is out of my area of expertise. But it was fun either way.

You may notice this is also hosted on gitihub. It is non standard for this but posting on imgur is no longer an option since they delete posts from time to time, github will likely not and is easier to share!

Anyhow with introductions out of the way we can start with this year results.

## Demographics

As usual some basic demographic data on who we are and where we are in life and in planet Earth will let the graphs do the talking here.
[Age](../graphs/2025/tkgc/tkgc_age_dist_condensed.png)
[Gender](../graphs/2025/tkgc/tkgc_gender_pie.png)
[Sex](../graphs/2025/tkgc/tkgc_sex_pie.png)
[Origin](../graphs/2025/tkgc/tkgc_origin_catbar.png)
[Education](../graphs/2025/tkgc/tkgc_edu_catbar.png)
[Job](../graphs/2025/tkgc/tkgc_job_catbar.png)
[Surveys Taken](../graphs/2025/tkgc/tkgc_surveys_taken_hist.png)

## Twokinds questions

Our second traditional set of questions on topic regarding for favorites of the comics and not so favorites. Only outlier this year is asking how you got into twokinds
[Favorite Character](../graphs/2025/tkgc/tkgc_fav_char_catbar.png)
[Least Favorite Character](../graphs/2025/tkgc/tkgc_unfav_char_catbar.png)
[Favorite Race](../graphs/2025/tkgc/tkgc_fav_race_catbar.png)
[Time following Twokinds](../graphs/2025/tkgc/tkgc_follow_hist.png)
[What got you into Twokinds?](../graphs/2025/tkgc/tkgc_intro.png)
[How long have you been in this community](../graphs/2025/tkgc/tkgc_current_community_stay_hist.png)
[Partake in other Communities?](../graphs/2025/tkgc/tkgc_other_communities_pie.png)
[Do you consider yourself a furry?](../graphs/2025/tkgc/tkgc_furry_pie.png)
[Favorite Chapter](../graphs/2025/tkgc/tkgc_fav_chap_numbar.png)
[Least Favorite Chapter](../graphs/2025/tkgc/tkgc_unfav_chap_numbar.png)
[Are you a patron?](../graphs/2025/tkgc/tkgc_patreon_ord.png)
[What patreon tier would you like?](../graphs/2025/tkgc/tkgc_desired_patreon_ord.png)
[Do you own Merchandise?](../graphs/2025/tkgc/tkgc_merch.png)
[Do you follow Tom's Picarto](../graphs/2025/tkgc/tkgc_picarto_pie.png)
[Have you commisioned twokinds fanart?](../graphs/2025/tkgc/tkgc_commision_pie.png)
[Have you ever made twokinds fanart?](../graphs/2025/tkgc/tkgc_fan_art_pie.png)
[Sunday sketches](../graphs/2025/tkgc/tkgc_sundays_ord.png)

## Free form questions

Ok this is the interesting part. We had around 52 responses and with 8 questions it does become impractical to read every one of them and come with something up myself. And had been waiting for a great excuse to try to do some natural language procession  on something interesting. 

What i wanted to try was at first doing some sentiment analysis to gauge the general attitude in the responses, classifying them into positive negative or neutral for this i used a text classification model based on hugging face transformers in particular i tried with [this multilingia sentiment analysis system]https://huggingface.co/tabularisai/multilingual-sentiment-analysis)

Next i wanted to extract some common themes from the questions in particular i have some background in clusterization algorithms so wanted to try something like that. In this case we take the responses and transform them into a high dimensional vector that distills the content into a hopeuflly continuous and metric high dimensional space, this process is known as embedding. Andthis can be done using the [sentence transformers](https://huggingface.co/sentence-transformers/paraphrase-mpnet-base-v2) framework also by huggingface. Then we can run stuff like [HDBSCAN](https://scikit-learn.org/stable/modules/generated/sklearn.cluster.HDBSCAN.html) to cluster it into semantically similar questions. 

With that it should become easier to steer any manual analysis of the responses. Alas it did not work very well. Sentiment analysis portion had a hard time properly for example the response `I feel with the better publishing schedule we are much more active ` was tagged as negative with very high confidence. 

For embedding analysis it was worse as the clustering did not return anything. HDBSCAN was unable to find any semantic clusters in the responses:

![hdbscan graph][../results/2025/tkgc/embeddings/community_opinion.png]

But in this case i think i could have gotten it to work had i spent enough time choosen the appropiate sentence transformer and tunning HDBscan hyperparamters. But that is way outside the scope of this and honestly i want to publish the results already

Either way you can see all the responses for each question organized here:

### What do you think of Twokinds and its community for this year? 

[Community](../../results/2025/tkgc/sentiments/sentiment_filling.md)

### Fill it the blank: It is not Twokinds until someone _____!

[Fill in](../../results/2025/tkgc/sentiments/sentiment_filling.md)

### How would you introduce someone new to Twokinds? 

[Introduction](../../results/2025/tkgc/sentiments/sentiment_introducing.md)

### What do you like the most about Twokinds?
[Liked most](../../results/2025/tkgc/sentiments/sentiment_most_liked.md)

### How would you describe Twokinds in one word?
[One word](../../results/2025/tkgc/sentiments/sentiment_one_word.md)

