# r/Twokinds survey 2025

Hello and welcome to another edition of our now traditional yearly survey!

I am Tec and you may have heard of me before, I adore using data to understand and visualize things i like and communities i partake in. As such i have been doing these survey to get a feel about how our little corner of the internet works and looks. 

As usual we will start with some demographic information to know who we are and then follow up with some common questions about the comic an its characters. But this year i deciided to bite the bullet and do some free form questions which proved to be interesting. I have a background in STEM so doing these types of non numeric questions is out of my area of expertise. But it was fun either way.

You may notice this is also hosted on gitihub. It is non standard for this but posting on imgur is no longer an option since they delete posts from time to time, github will likely not and is easier to share and fix!

Anyhow with introductions out of the way we can start with this year results.

## Demographics

As usual some basic demographic data on who we are and where we are in life and in planet Earth will let the graphs do the talking here.
![Age](../../../graphs/2025/subreddit/subreddit_age_dist_condensed.png)
![Gender](../../../graphs/2025/subreddit/subreddit_gender_pie.png)
![Sex](../../../graphs/2025/subreddit/subreddit_sex_pie.png)
![Origin](../../../graphs/2025/subreddit/subreddit_origin_catbar.png)
![Education](../../../graphs/2025/subreddit/subreddit_edu_catbar.png)
![Job](../../../graphs/2025/subreddit/subreddit_job_catbar.png)
![Surveys Taken](../../../graphs/2025/subreddit/subreddit_surveys_taken_hist.png)

## Twokinds questions

Our second traditional set of questions on topic regarding for favorites of the comics and not so favorites. Only outlier this year is asking how you got into twokinds and how many surveys you had filled before.

I did provide an 'other' field in some questions and some people gave quite the long comment there, left it on the graphs since i think it is a bit funny and is a bit annoying to remove

![Favorite Character](../../../graphs/2025/subreddit/subreddit_fav_char_catbar.png)
![Least Favorite Character](../../../graphs/2025/subreddit/subreddit_unfav_char_catbar.png)
![Favorite Race](../../../graphs/2025/subreddit/subreddit_fav_race_catbar.png)
![Time following Twokinds](../../../graphs/2025/subreddit/subreddit_follow_hist.png)
![What got you into Twokinds?](../../../graphs/2025/subreddit/subreddit_intro.png)
![How long have you been in this community](../../../graphs/2025/subreddit/subreddit_current_community_stay_hist.png)
![Partake in other Communities?](../../../graphs/2025/subreddit/subreddit_other_communities_pie.png)
![Do you consider yourself a furry?](../../../graphs/2025/subreddit/subreddit_furry_pie.png)
![Favorite Chapter](../../../graphs/2025/subreddit/subreddit_fav_chap_numbar.png)
![Least Favorite Chapter](../../../graphs/2025/subreddit/subreddit_unfav_chap_numbar.png)
![Are you a patron?](../../../graphs/2025/subreddit/subreddit_patreon_ord.png)
![What patreon tier would you like?](../../../graphs/2025/subreddit/subreddit_desired_patreon_ord.png)
![Do you own Merchandise?](../../../graphs/2025/subreddit/subreddit_merch.png)
![Do you follow Tom's Picarto](../../../graphs/2025/subreddit/subreddit_picarto_pie.png)
![Have you commisioned twokinds fanart?](../../../graphs/2025/subreddit/subreddit_commision_pie.png)
![Have you ever made twokinds fanart?](../../../graphs/2025/subreddit/subreddit_fan_art_pie.png)
![Sunday sketches](../../../graphs/2025/subreddit/subreddit_sundays_ord.png)

## Free form questions

Ok this is the interesting part. We had around 111 responses and with 6 questions it does become impractical to read every one of them and come with something up myself. And had been waiting for a great excuse to try to do some natural language procession on something interesting. 

What i wanted to try was at first doing some sentiment analysis to gauge the general attitude in the responses, classifying them into positive negative or neutral. For this i used a text classification system based on hugging face transformers. In particular i tried with [this multilingual sentiment analysis system](https://huggingface.co/tabularisai/multilingual-sentiment-analysis)

Next i wanted to extract some common themes from the questions. I have some background in clusterization algorithms so wanted to try something like that. In this case we take the responses and transform them into a high dimensional vector that distills the content into a hopeuflly continuous and metric high dimensional space, this process is known as embedding. This can be done using the [sentence transformers](https://huggingface.co/sentence-transformers/paraphrase-mpnet-base-v2) framework also by huggingface. Then we can run stuff like [HDBSCAN](https://scikit-learn.org/stable/modules/generated/sklearn.cluster.HDBSCAN.html) to cluster it into semantically similar questions. 

With that it should become easier to steer any manual analysis of the responses. Alas it did not work very well. Sentiment analysis portion had a hard time properly tagging stuff. For example the response `I see a lot more community made content` was tagged as negative with very high confidence. 

For embedding analysis it was worse as the clustering did not return anything. HDBSCAN was unable to find any semantic clusters in the responses:

![hdbscan graph](../../../results/2025/subreddit/embeddings/community_opinion.png)

If you are wondering i used [UMAP](https://umap-learn.readthedocs.io/en/latest/), the to project the vectors into something I could graph.

In a working case every point would be assigned a cluster or noise label, but it did not. I think i could have gotten it to work had i spent enough time choosing the appropiate sentence transformer and tunning HDBscan hyperparameters specially with this number of responses. But that is way outside the scope of this and honestly i want to publish the results already

Either way you can see all the responses for each question organized here (these are links) plus some of my own thoughts on the responses. And if you want to check the results for sentiment analysis and embedding you can find the csvs with the classification on [this folder](../../../results/2025/subreddit/sentiments/) and likewise you can see the embedding graphs [over here](../../../results/2025/subreddit/embeddings/).



### [What do you think of Twokinds and its community for this year?](../../../results/2025/subreddit/sentiments/sentiment_community_opinion.md)
Most people seem to agree twokinds and the comminity have been `great` so far. Some going with `Its been wonderful and very kind.. get it? Ahaha` which i agree. A couple do point out we are sometimes `Horny, but dedicated` and we have the usual mentions about Tom being a bit off with his schedule but better than last year: `Much better than last year. Community can't thrive if content is slow or nonexistent.` and how this is a boon for the community.

### [Fill it the blank: It is not Twokinds until someone _____!](../../../results/2025/subreddit/sentiments/sentiment_filling.md)
Most responders agreed that we are not in Twokinds until we someone `changes species and/or gender` or is otherwise transformed or `Genderbends`. And of course it cannot be Twokinds until someone `gets naked` and a couple mentions about people being down for some characters.

### [How would you introduce someone new to Twokinds?](../../../results/2025/subreddit/sentiments/sentiment_introducing.md)
So most people seem to consider to simply drop a new reader to chapter one and let them handle it themselves `I would tell them about the comic and an overview, show them a link to chapter one, and warn them it’s rough at first but you can see the artist evolving visibly over time.` while of course mentioning the quality does improve over time. incidentally a lot of people also would try to add their mini summary `I'd show them some of the character art and tell them about the story.` show them some non comic art first: `Probably through one of the coloured picarto artworks, then direct them to the comic if they're interested.` and a common idea was mentioning Tom was Markiplier brother: `Tell them Markiplier's brother has been making the comic for a long time and show a brief comparison between how it looks now to how it started`. For the record i do think Tom early art is worse than today but still charming and better than the average 15 year old at the time

### [What do you like the most about Twokinds?](../../../results/2025/subreddit/sentiments/sentiment_most_liked.md)
Of course a lot of people here love `The art` the most but a common thread is also `the characters`. And lots of people also mention how they love the characterization perhaps even more than their looks as this comment so succintly puts it: `Hot furry man, hot furry women, hot humans.... Personality and surprisingly good characteristic development. And characters you will love them for a lot of reasons. not from looks, but who they are, and what they are.` Shoutout to this response too `I love the theme of characters having dual backgrounds and how the world and its different inhabitants view and treat them. Internalized hatred is a theme explored in the comic.` which shows one of the main themes of the comic. As i have always said the comic strenght is in its characterization.

### [How would you describe Twokinds in one word?](../../../results/2025/subreddit/sentiments/sentiment_one_word.md)
Seems most people have high regard for the comic being described as `interesting`, ` great` and `Oneofakind` which i agree there is not quite something else like Twokinds out there. And a couple mentions of poeple caling it `Risqué` and `horny`

### [What keeps you coming back to Twokinds and its community?](../../../results/2025/subreddit/sentiments/sentiment_retention.md)
Seems what keeps most people around is the `New Sketches and pages` so the `Art` but a couple of people also mentioned they like the community we have fostered and they have made friends here like so `I have made friends from this community that I talk to on a daily basis. I moderate a TK fan community. I love seeing the evolution of Tom's artistry throughout the comic, and I'm captivated by the story and its characters.` and some people just have been enjoying it here so long why would they leave: `I've been 10 years at this, I definitely can't stop now :)`
