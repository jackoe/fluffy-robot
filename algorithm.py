'''
Jack Wines & Tegan Wilson
Natural Language Processing
Blake Howald, 3a
'''

import networkx as nx
import tabulate
import plotly.offline as plot
import plotly.graph_objs as go

def pretty_print(lines):
    for line in lines:
        sent, output, answ, edit_dist = line
        print(sent)
        print(output)
        print(answ)
        print(edit_dist)
        print('-------------')


def output_result_statistics(sent_translation):
    edit_dists = [x[-1] for x in sent_translation]
    print(edit_dists)
    histogram_data = [go.Histogram(x = edit_dists)]
    plot.plot(histogram_data, filename = "histogram")
    print("bottom 5:")
    pretty_print(sent_translation[:5])
    print("top 5:")
    pretty_print(sent_translation[-5:])
    

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

def set_difference(l1, l2):
    s1 = set(l1)
    s2 = set(l2)
    diff = s1.difference(s2)
    return list(diff)

def edit_distance(s1, s2, dp_table):
    if len(s1) == 0 or len(s2) == 0:
        return len(s1) + len(s2)
    if (s1, s2) in dp_table:
        return dp_table[(s1, s2)]
    if s1[0] == s2[0]:
        return edit_distance(s1[1:], s2[1:], dp_table)
    else:
        result = min(edit_distance(s1[1:], s2,    dp_table) + 1,
                     edit_distance(s1, s2[1:],    dp_table) + 1,
                     edit_distance(s1[1:], s2[1:],dp_table) + 2)
        dp_table[(s1, s2)] = result
        return result

def build_sent_graph(sent, train_data):
    # build graph for the test sentence: graph is 9 by len(sent)
    D = nx.DiGraph()

    # assign values to each vertex (actually to each edge leaving the vertex)
    # vertex (i,j) -> i-gram ending at character j
    # if vertex not in graph, adds vertex
    for i in range(1,10):
        for j in range(0,len(sent)):
            if j-i >= -1: # is it possible to find i-gram ending at j
                if sent[j-i+1:j+1] in train_data:
                    value = float(train_data[sent[j-i+1:j+1]][1]) # associated weight
                else:
                    value = 0
                # add edges if value isn't 0
                for l in range(1,10):
                    to_node = 'finish' if j-i<0 else (l,j-i)
                    D.add_edge((i,j), to_node, weight=value)

        D.add_edge('start', (i,len(sent)-1), weight=0)
    return D


def translate(sent, D, train_data):
    Dgraph = nx.DiGraph.copy(D)
    # remove edges coming out of start
    for edge in list(Dgraph.edges('start')):
        Dgraph.remove_edge(edge[0], edge[1])

    # traverse graph to find longest path:
    # Find set of vertices with no incoming edges, S
    S = [v for v in Dgraph.nodes() if len(Dgraph.in_edges(v)) == 0 and v != 'start']
    L = ['start']
    # while S not empty:
    while len(S) > 0:
        # pick v within S
        v = S.pop()
        # take v out of S and place v into L (order solution list)
        L.append(v)
        # for all w st. vw is a directed edge from v to w:
        edges = list(Dgraph.edges(v))
        for e in edges:
            # "delete" vw from the set of edges
            Dgraph.remove_edge(e[0],e[1])
            # if w has no other incoming edges, add w to S
            if len(Dgraph.in_edges(e[1])) == 0:
                S.append(e[1])

    # iterate through L to get path lengths
    backtrack = {}
    for i in range(0,len(L)):
        v = L[i]
        if i == 0:
            backtrack[v] = [0]
        else:
            edges = list(D.in_edges(v))
            backtrack[v] = [float('-inf'), 'start']
            if len(edges) > 0:
                curr_path = backtrack[v][0]
                for e in edges:
                    data = D.get_edge_data(*e)
                    weight = data['weight']
                    u = e[0]
                    path_length = backtrack[u][0] + weight
                    if curr_path < path_length:
                        curr_path = path_length
                        backtrack[v] = [path_length, u]
        if v == 'finish': # in this case we're done
            break

    # backtrack to get max value parse of sentence
    done = False
    curr_v = 'finish'
    path = ['finish']
    while not done:
        if curr_v == 'start':
            done = True
            break
        next_v = backtrack[curr_v][1]
        path.append(next_v)
        curr_v = next_v
    path.reverse()

    # use max path to parse sent and dictionary to get reading
    # do something for kanji that weren't found! (probably leave them be)
    output = ""
    for node in path:
        if not node == 'finish' and not node == 'start':
            i = node[0]
            j = node[1]
            gram = sent[j-i+1:j+1]
            if gram in train_data:
                kana = train_data[gram][0][0]
            else:
                kana = gram
            output = kana + output
    return output

def get_train_data():
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
    return train_data

def main():
    #import training data
    train_data = get_train_data()

    '''parse test sentences:'''
    # import test data
    test_sentences = import_test_data()

    sent_translation = []

    # iterate through test sentences:
    for sent, answ in test_sentences:

        D = build_sent_graph(sent, train_data)
        if(not done_visual):
             nx.drawing.nx_pylab.draw(D)

        output = translate(sent, D, train_data)

        # compare output and answ to determine accuracy
        edit_dist = edit_distance(output,answ,{})
        sent_translation.append((sent,output,answ,edit_dist))

    # print some of the worst offenders for closer examination
    sent_translation.sort(key = lambda x: x[3], reverse = True)
    output_result_statistics(sent_translation)



done_visual = False
if __name__ == "__main__":
    main()
