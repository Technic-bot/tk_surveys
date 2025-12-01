# Twokinds Group Chat survey 2025

Hello and welcome to another edition of our now traditional yearly survey!

I am Tec and you may have heard of me before, I adore using data to understand and visualize things i like and communities i partake in. As such i have been doing these survey to get a feel about how our little corner of the internet works and looks. 

As usual we will start with some demographic information to know who we are and then follow up with some common questions about the comic an its characters. But this year i deciided to bite the bullet and do some free form questions which proved to be interesting. I have a background in STEM so doing these types of non numeric questions is out of my area of expertise. But it was fun either way.

You may notice this is also hosted on gitihub. It is non standard for this but posting on imgur is no longer an option since they delete posts from time to time, github will likely not and is easier to share!

Anyhow with introductions out of the way we can start with this year results.

## Demographics

As usual some basic demographic data on who we are and where we are in life and in planet Earth will let the graphs do the talking here.
![Age](../../../graphs/2025/tkgc/tkgc_age_dist_condensed.png)
![Gender](../../../graphs/2025/tkgc/tkgc_gender_pie.png)
![Sex](../../../graphs/2025/tkgc/tkgc_sex_pie.png)
![Origin](../../../graphs/2025/tkgc/tkgc_origin_catbar.png)
![Education](../../../graphs/2025/tkgc/tkgc_edu_catbar.png)
![Job](../../../graphs/2025/tkgc/tkgc_job_catbar.png)
![Surveys Taken](../../../graphs/2025/tkgc/tkgc_surveys_taken_hist.png)

## Twokinds questions

Our second traditional set of questions on topic regarding for favorites of the comics and not so favorites. Only outlier this year is asking how you got into twokinds

I did provide an 'other' field in some questions and some people gave quite the long comment there, left it on the graphs since i think it is a bit funny and is a bit annoying to remove

![Favorite Character](../../../graphs/2025/tkgc/tkgc_fav_char_catbar.png)
![Least Favorite Character](../../../graphs/2025/tkgc/tkgc_unfav_char_catbar.png)
![Favorite Race](../../../graphs/2025/tkgc/tkgc_fav_race_catbar.png)
![Time following Twokinds](../../../graphs/2025/tkgc/tkgc_follow_hist.png)
![What got you into Twokinds?](../../../graphs/2025/tkgc/tkgc_intro.png)
![How long have you been in this community](../../../graphs/2025/tkgc/tkgc_current_community_stay_hist.png)
![Partake in other Communities?](../../../graphs/2025/tkgc/tkgc_other_communities_pie.png)
![Do you consider yourself a furry?](../../../graphs/2025/tkgc/tkgc_furry_pie.png)
![Favorite Chapter](../../../graphs/2025/tkgc/tkgc_fav_chap_numbar.png)
![Least Favorite Chapter](../../../graphs/2025/tkgc/tkgc_unfav_chap_numbar.png)
![Are you a patron?](../../../graphs/2025/tkgc/tkgc_patreon_ord.png)
![What patreon tier would you like?](../../../graphs/2025/tkgc/tkgc_desired_patreon_ord.png)
![Do you own Merchandise?](../../../graphs/2025/tkgc/tkgc_merch.png)
![Do you follow Tom's Picarto](../../../graphs/2025/tkgc/tkgc_picarto_pie.png)
![Have you commisioned twokinds fanart?](../../../graphs/2025/tkgc/tkgc_commision_pie.png)
![Have you ever made twokinds fanart?](../../../graphs/2025/tkgc/tkgc_fan_art_pie.png)
![Sunday sketches](../../../graphs/2025/tkgc/tkgc_sundays_ord.png)

## Free form questions

Ok this is the interesting part. We had around 52 responses and with 8 questions it does become impractical to read every one of them and come with something up myself. And had been waiting for a great excuse to try to do some natural language procession on something interesting. 

What i wanted to try was at first doing some sentiment analysis to gauge the general attitude in the responses, classifying them into positive negative or neutral for this i used a text classification model based on hugging face transformers in particular i tried with [this multilingual sentiment analysis system](https://huggingface.co/tabularisai/multilingual-sentiment-analysis)

Next i wanted to extract some common themes from the questions in particular i have some background in clusterization algorithms so wanted to try something like that. In this case we take the responses and transform them into a high dimensional vector that distills the content into a hopeuflly continuous and metric high dimensional space, this process is known as embedding. Andthis can be done using the [sentence transformers](https://huggingface.co/sentence-transformers/paraphrase-mpnet-base-v2) framework also by huggingface. Then we can run stuff like [HDBSCAN](https://scikit-learn.org/stable/modules/generated/sklearn.cluster.HDBSCAN.html) to cluster it into semantically similar questions. 

With that it should become easier to steer any manual analysis of the responses. Alas it did not work very well. Sentiment analysis portion had a hard time properly for example the response `I feel with the better publishing schedule we are much more active ` was tagged as negative with very high confidence. 

For embedding analysis it was worse as the clustering did not return anything. HDBSCAN was unable to find any semantic clusters in the responses:

![hdbscan graph](../../../results/2025/tkgc/embeddings/community_opinion.png)

But in this case i think i could have gotten it to work had i spent enough time choosing the appropiate sentence transformer and tunning HDBscan hyperparameters or had i simply got more responses. But that is way outside the scope of this and honestly i want to publish the results already

Either way you can see all the responses for each question organized here (these are links) plus some of my own thoughts on the responses.

### [What do you think of Twokinds and its community for this year?](../../../results/2025/tkgc/sentiments/sentiment_community_opinion.md)
So in general seems like people are very fond of the server. As this response  `The people in the TKGC community have made me very very happy <3` summarizes. People also seem like that Tom has increased his thoroughput this year as this surveyee poinst out: `The number of pages being posted have picked up and the community has been fun to hang out with.`. There is however some people considering that Tom should work more on the comic (`Tom should lock in on the comic, not sketches.`) and there were a couple comments about the community being a bit hard to navigate. And of course as any survey lots of people were ambivalent.

### [Fill it the blank: It is not Twokinds until someone _____!](../../../results/2025/tkgc/sentiments/sentiment_filling.md)
Unsurprisingly most of you decided that it is not Twokinds until someone `Gets Genderbent` or is transformed one way or the other.

### [How would you introduce someone new to Twokinds?](../../../results/2025/tkgc/sentiments/sentiment_introducing.md)
Most people agreed that the best idea to introduce someone to twokinds is to show them recent sketches or colored art before sending them to page 1: `Id first show them the Sunday sketches before the comic so they understand that the art style won’t stay… rough.` Personally I do find his early style to be charming and honestly better than more than 80% of 15 year olds then and today could make. But also understand some people won't feel like going through his early drawings regardless. And a couple decide to go straight to the money shot `Butts` which honestly points for the honesty.

### [What do you like the most about Twokinds?](../../../results/2025/tkgc/sentiments/sentiment_most_liked.md)
Of course a lot of people like `The art` the most and after all Tom is a visual artist. But a lot of people also commented they like the characterization and how they can connecte with the characters one way or another: `A lot of things, but in general. How it makes me feel, I feel like I am with the characters in the good and the bad moments.` I have always said that the best part of the comics are its characters. What I did not expect was seeing several people commenting on Tom growth as an artist as what they like exemplified by this response: `Evolution of Tom’s work as a writer and artist`

### [How would you describe Twokinds in one word?](../../../results/2025/tkgc/sentiments/sentiment_one_word.md)
There was quite the split here some described twokinds as mostly horni: `Adolescent`, `Softcore`, `Butts` which i disagree but i understand where they are coming from. But a lot of people also find it `interesting` `earnest` and `charming` which to be fair i do think Tom puts all his heart into this.

### [What keeps you coming back to Twokinds and its community?](../../../results/2025/tkgc/sentiments/sentiment_retention.md)
It seems for a lot of people not only they are invested in the comic but they have also found a little corner of the internet to call home here: `Other than how awesome the comic is? The group chat is full of so many awesome furs that I enjoy hanging out with!` and `For the comic, the story. For the community, the incredibly nice people that are part of it.` show it
