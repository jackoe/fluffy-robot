'''
Jack Wines & Tegan Wilson
Natural Language Processing
Blake Howald, 3a
'''

def main():

    '''create dictionary:'''
    # create a katakana to hiragana map (dictionary):
    kana_dict = {}
    with open('katakana_dict.txt', "r", encoding="euc-jp") as f:
        for line in if:
            new_data = line.split()
            kana_dict[new_data[0]] = new_data[1]

    # open edict file and put data into a dictionary
    # key = n-gram, value = length of n-gram + (.01*len-1)
    with open('edict2', "r", encoding="euc-jp") as f:
        for line in if:

            pass


    '''parse test sentences:'''

    # import test data

    # iterate through test sentences:

        # build graph for the test sentence

        # assign values to each vertex (or edges if necessary)

        # traverse graph to find longest path (or shortest if needed?)

        # backtrack to get max value parse of sentence

        # use max value parse and dictionary to get reading
        # do something for kanji that aren't found!

    # examine output v. answer to determine accuracy

    # print some of the worst offenders for closer examination


if __name__ == "__main__":
    main()
