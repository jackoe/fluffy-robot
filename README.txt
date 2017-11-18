Jack Wines & Tegan Wilson
Natural Language Processing
Blake Howald

Python3 libraries used:
networkx
plotly
tabulate
beautifulsoup4

To run the program, ensure that algorithm.py, kanji_hiragana.txt,
katakana_dict.txt, and edict2 are in the same directory. Type:

    python3 algorithm.py

into the command line to run.

Files:
algorithm.py - our main file: takes in a set of training data and a set of text
  data, calculates the pronunciation of each sentence, finds the minimum edit
  distance between the calculated reading and the actual reading, and outputs
  the average and median edit distance and the top and bottom 5 sentences
scrape_news.py - takes in a set of news urls and pulls test data pairs: sentence
  with kanji, and sentence without kanji, and records them in kanji_hiragana.txt
urls.txt - the set of news urls that we pulled test data from
kanji_hiragana.txt - the test data we pulled from news urls
katakana_dict.txt - a katakana to hiragana map we created to map each katakana
  character to its associated hiragana character (kept the output all in
  hiragana for consistency)
edict2 - the Japanese to English dictionary that we used as our training data
