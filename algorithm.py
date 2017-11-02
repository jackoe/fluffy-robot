'''
Jack Wines & Tegan Wilson
Natural Language Processing
Blake Howald, 3a
'''
def import_test_data():
    kanji_hiragana = []
    with open('kanji_hiragana.txt') as f:
        new_sentence = True
        kanji = ""
        hiragana = ""
        for line in f:
            line = line[:-1]
            if new_sentence:
                kanji = line
                new_sentence = False
            else:
                hiragana = line
                kanji_hiragana.append((kanji, hiragana))
                new_sentence = True
    return kanji_hiragana[:-1]

def parse_line(line):
    split_line = line.split(' ')
    kanji = split_line[0].split(';')
    katakana = split_line[1][1:-1].split(';')
    return kanji, katakana

def main():

    # '''create dictionary:'''
    # create a katakana to hiragana map (dictionary):
    kana_dict = {}
    # with open('katakana_dict.txt', "r", encoding="euc-jp") as f:
    #     for line in f:
    #         new_data = line.split()
    #         kana_dict[new_data[0]] = new_data[1]

    # open edict file and put data into a dictionary
    i = 0
    # key = n-gram, value = length of n-gram + (.01*len-1)
    train_data = {}
    with open('edict2', "r", encoding="euc-jp") as f:
        for line in f:
            kanji_l, hiragana_l = parse_line(line.replace('(P)', ''))
            for kanji in kanji_l:
                train_data[kanji] = hiragana_l

    '''parse test sentences:'''
    # import test data
    test_sentences = import_test_data()


    # iterate through test sentences:

        # build graph for the test sentence

        # assign values to each vertex (or edges if necessary)

        # traverse graph to find longest path:

            # Find set of vertices with no incoming edges, S

            # while S not empty:

            # pick v within S

            # take v out of S and place v into L (order solution list)

            # for all w st. vw is a directed edge from v to w:

                # "delete" vw from the set of edges

                # if w has no other incoming edges, add w to S

        # backtrack to get max value parse of sentence

        # use max value parse and dictionary to get reading
        # do something for kanji that aren't found!

    # examine output v. answer to determine accuracy

    # print some of the worst offenders for closer examination


if __name__ == "__main__":
    main()
