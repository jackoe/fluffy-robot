'''
Jack Wines & Tegan Wilson
Natural Language Processing
Blake Howald, 3a
'''

import networkx as nx

def import_test_data():
    kanji_hiragana = []
    with open('kanji_hiragana.txt',"r") as f:
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
    line = line.replace('(P)', '')
    split_line = line.split(' ')
    kanji = split_line[0].split(';')

    hiragana = split_line[1]
    if hiragana[:2] == '/(':
        return None
    elif hiragana[0] == '[' and hiragana[-1] == ']':
        hiragana = hiragana[1:-1]
    else:
        print('err', hiragana, line)
    hiragana = hiragana.split(';')
    return kanji, hiragana

def main():

    # '''create dictionary:'''
    # create a katakana/hiragana to hiragana map (dictionary):
    train_data = {}
    with open('katakana_dict.txt', "r") as f:
        for line in f:
            new_data = line.split()
            train_data[new_data[0]] = [new_data[1],1]
            train_data[new_data[1]] = [new_data[1],1]

    # open edict file and put data into a dictionary
    # key = the kanji n-gram
    # value = [assiciated pronunciation, value = length of n-gram + (.01*len-1)]
    with open('edict2', "r", encoding="euc-jp") as f:
        i = 0
        for line in f:
            parsed_line = parse_line(line)
            if parsed_line == None:
                continue
            kanji_l, hiragana_l = parsed_line
            for kanji in kanji_l:
                value = len(kanji) + (len(kanji)-1) * .01
                train_data[kanji] = [hiragana_l, value]

    '''parse test sentences:'''
    # import test data
    test_sentences = import_test_data()
    k = 0

    # iterate through test sentences:
    for test_sent in test_sentences:
        k += 1
        if k > 1:
            break

        sent = test_sent[0]
        answ = test_sent[1]

        # build graph for the test sentence: graph is 9 by len(sent)
        D = nx.DiGraph()

        # assign values to each vertex (actually to each edge leaving the vertex)
        # vertex (i,j) -> i-gram ending at character j
        # if vertex not in graph, adds vertex
        for i in range(1,10):
            for j in range(0,len(sent)):
                if j-i >= 0: # is it possible to find i-gram ending at j
                    if sent[j-i:j+1] in train_data:
                        value = train_data[sent[j-i:j+1]][1] # associated weight
                    else:
                        value = 0
                    # add edges if value isn't 0
                    if value > 0:
                        for l in range(1,10):
                            to_node = 'finish' if i == 1 else (l,j-i)
                            D.add_edge((i,j), to_node, weight=value)
            
            D.add_edge('start', (i,len(sent)), weight=0)

        # traverse graph to find longest path:
        # Find set of vertices with no incoming edges, S
        S = [v for v in D.nodes() if len(v.in_edges()) == 0]
        L = [start]
        Dgraph = nx.copy(D)
        # while S not empty:
        while len(S) > 0:
            # pick v within S
            v = S.pop()
            # take v out of S and place v into L (order solution list)
            L.append(v)
            # for all w st. vw is a directed edge from v to w:
            edges = Dgraph.edges(v)
            for v, w in edges:
                # "delete" vw from the set of edges
                D.remove_edge(v,w)
                # if w has no other incoming edges, add w to S
                if len(w.in_edges()) == 0:
                    S.append(w)

        # iterate through L to get path lengths

        # backtrack to get max value parse of sentence

        # use max value parse and dictionary to get reading
        # do something for kanji that aren't found!

    # examine output v. answer to determine accuracy

    # print some of the worst offenders for closer examination


if __name__ == "__main__":
    main()
