with open('edict2', "r", encoding="euc-jp") as f:
    i = 0
    for line in f:
        i += 1
        if i > 90:
            break
        print(line)
print('done')
