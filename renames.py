raw_cols = (
    "Marca temporal",
    "Age",
    "Gender Identity",
    "Sexual Orientation",
    "Where are you from? (place of birth)",
    "Education",
    "Employment",
    "Favorite character",
    "Least Favorite Character",
    "Favorite race",
    "How long have you been following the comic? (in years)",
    #"How long have you been part of r/Twokinds? (in years)",
    "How long have you been part of TKGC? (in years)",
    "Do you participate in other Twokinds fan communities (Discord, forums, etc)?",
    "In general, how long have you been a part of Twokinds fan communities? (In years)",
    "Do you identify as a furry or a member of the furry fandom?",
    "Favorite chapter of the comic?",
    "Least Favorite chapter of the comic?",
    "If you are a patron of Thomas Fischbach's Patreon, what tier are you subscribed to?",
    "If money were not an issue would you subscribe to Tom patreon. If so which tier?",
    "How do you feel about the Sunday Sketches Tom does weekly?",
    "How do you feel about colored sketches Tom does at the end each month?",
    "Do you own any official Twokinds merchandise?",
    "Do you follow Tom on Picarto?",
    "Have you ever commissioned Twokinds-related art from artists other than Thomas Fischbach?",
    "Have you ever made Twokinds fan art? (Drawings, Fanfiction, DIY, etc)",
)

cols = ["time", "age", "gender", "sex", "origin", "edu", "job"]
cols += ["fav_char", "unfav_char", "fav_race"]
cols += ["follow", "current_community_stay", "other_communities", "other_community_stay"]
cols += ["furry"]
cols += ["fav_chap", "unfav_chap", "patreon", "desired_patreon"]
cols += ["sundays", "colors", "merch", "picarto", "commision", "fan_art"]

col_remap = dict(zip(raw_cols, cols))

extra_maps = {
  'Do you participate in other Twokinds fan communities (Discord server, reddit, forums, etc)?' : 'other_comms',
  "How long have you been part of this subreddit? (in years)" : "reddit"
  }

col_remap.update(extra_maps)

gender_renames = {"Male": "Cisgender Male"}
orig_renames = {
    "Latin America and the Caribbean": "Latin America",
    "Oceania (Australia, New Zealand, Pacific Islands)": "Oceania",
}

char_renames = {
    "Madelyn (Maddie)": "Madelyn",
    "Mrs Nibbly": "Nibbly",
    "Don’t have one": "None",
    "I don't know": 'None'
}


