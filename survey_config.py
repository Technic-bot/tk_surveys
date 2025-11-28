survey = [   
    {   "raw": "Marca temporal",
        "name": "time",
        "type": None},
    {   'name': 'age',
        'raw': 'Age',
        'title': 'Age Distribution',
        'type': None, # Handled separately
        'label': 'years'},
    {   'name': 'gender',
        'raw': 'Gender Identity',
        'title': 'Gender Distribution',
        'type': 'pie'},
    {   'name': 'sex',
        'raw': 'Sexual Orientation',
        'title': 'Sexual Orientation',
        'type': 'pie'},
    {   'name': 'origin',
        'raw': 'Where are you from? (place of birth)',
        'title': 'Place of origin',
        'type': 'bar_cat'},
    {   'name': 'edu',
        'raw': 'Education',
        'title': 'Educational level',
        'type': 'bar_cat'},
    {   'name': 'job',
        'raw': 'Employment',
        'title': 'Employment status',
        'type': 'bar_cat'},
    {   'name': 'fav_char',
        'raw': 'Favorite character',
        'title': 'Favorite Character',
        'type': 'bar_cat'},
    {   'name': 'unfav_char',
        'raw': 'Least Favorite Character',
        'title': 'Least Favorite Character',
        'type': 'bar_cat'},
    {   'name': 'fav_race',
        'raw': 'Favorite race',
        'title': 'Favorite Race',
        'type': 'bar_cat'},
    {   'name': 'follow',
        'raw': 'How long have you been following the comic? (in years)',
        'title': 'Time following Twokinds',
        'type': 'histogram',
        'label': 'years'},
    {   'name': 'intro',
        'raw': "What got you into Twokinds?",
        'title': "What got you into Twokinds?",
        'type': None # Handled separately
    },
    {   'name': 'current_community_stay',
        'raw': 'How long have you been part of this community? (in years)',
        'title': 'Time in this community',
        'type': 'histogram',
        'label': 'years'},
    {   'name': 'other_communities',
        'raw': 'Do you participate in other Twokinds fan communities (Discord, '
               'forums, etc)?',
        'title': 'Are you part of other Twokinds communities?',
        'type': 'pie'},
    {   'name': 'furry',
        'raw': 'Do you identify as a furry or a member of the furry fandom?',
        'title': 'Do you consider yourself a furry?',
        'type': 'pie'},
    {   'name': 'fav_chap',
        'raw': 'Favorite chapter of the comic?',
        'title': 'Favorite Chapter',
        'type': 'bar_num',
        'label': 'chapter'},
    {   'name': 'unfav_chap',
        'raw': 'Least Favorite chapter of the comic?',
        'title': 'Least Favorite Chapter',
        'type': 'bar_num',
        'label': 'chapter'},
    {   'name': 'patreon',
        'raw': "If you are a patron of Thomas Fischbach's Patreon, what tier "
               'are you subscribed to?',
        'title': 'Are you a Patreon',
        'type': 'bar_order_keys'},
    {   'name': 'desired_patreon',
        'raw': 'If money were not an issue would you subscribe to Tom patreon. '
               'If so which tier?',
        'title': 'Which Patreon tier would you subscribe if money was not an '
                 'issue?',
        'type': 'bar_order_keys'},
    {   'name': 'sundays',
        'raw': 'How do you feel about the Sunday Sketches Tom does weekly?',
        'title': 'How do you feel about Sunday Sketches?',
        'type': 'bar_order_keys'},
    {   'name': 'merch',
        'raw': 'Do you own any official Twokinds merchandise?',
        'type': None 
    },
    {   'name': 'picarto',
        'raw': 'Do you follow Tom on Picarto?',
        'title': 'Do you follow Tom on Picarto?',
        'type': 'pie'},
    {   'name': 'fan_art',
        'raw': 'Have you ever made Twokinds fan art? (Drawings, Fanfiction, '
               'DIY, etc)',
        'title': 'Have you ever made Twokinds fan art?',
        'type': 'pie'},
    {   'name': 'commision',
        'raw': 'Have you ever commissioned Twokinds-related art from artists '
               'other than Thomas Fischbach?',
        'title': 'Have you ever commisioned Twokinds art?',
        'type': 'pie'},
    {   'name': 'surveys_taken',
        'raw': 'How many of my surveys have you taken including this?',
        'title': "Prior Participation",
        'type': 'histogram',
        'label': 'number' },
    # Sentiment analysis questions
    { 
        'raw': "What do you like the most about Twokinds?",
        'name' : 'most_liked',
        'type': 'sentiment' 
    },
    { 
        'raw': "What keeps you coming back to Twokinds and its community?",
        'name': 'retention',
        'type': 'sentiment' 
    },
    {   
        'raw': "How would you describe Twokinds in one word?",
        'name' : "one_word",
        'type': 'sentiment' 
    },
    {
        'raw': "How would you introduce someone new to Twokinds?",
        'name': 'introducing',
        'type': 'sentiment' 
    },
    {
        'raw': "What do you think of Twokinds and its community for this year?",
        'name': 'community_opinion',
        'type': 'sentiment' 
    },
    {
        'raw': "Fill it the blank: It is not Twokinds until someone _____!",
        'name': 'filling',
        'type': 'sentiment' 
    },
    { 
        'raw': "What other questions would you like to see next time?",
        'name': "questions",
        'type': 'sentiment' 
    }
        
]

gender_renames = {"Male": "Cisgender Male"}

orig_renames = {
    "Latin America and the Caribbean": "Latin America",
    "Oceania (Australia, New Zealand, Pacific Islands)": "Oceania",
}

char_renames = {
    "Madelyn (Maddie)": "Madelyn",
    "Mrs Nibbly": "Nibbly",
    "Don't have one": "None",
    "I don't know": 'None',
    "Every bad character is made specifically to be hated. I can't find a poorly written character.": "None",
    "No se, todos me caen bien ": 'None'
}
