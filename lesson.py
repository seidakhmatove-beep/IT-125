 = ('h', 6.13, 'C', 'e', 'T', True, 'k', 'e', 3, 'e', 1, 'g')
letters = []
numders = []


for i in data_tuple:
    if type (1) == str:
        lettdata_tupleers.append(i)
else:
    numders.append(i)
    
numders.remove(6.13)
numders.sort()


if True in numders:
    numders.remove(True)
    letters.append(True)
    
index_3 = numders.index(3)
index_1 = numders.index(1)

numders.insert(index_3 + 1, 2)

numders.sort()

letters.reverse()

for i in range(len(letters)):
    if letters[i] == 'e':
        letters[i] == 'z'
    elif letters[i] == 'k':
        letters[i] = 'o'
        
        
word_letters = ['C','o','g','t','z']
letters = word_letters

letters_tuple = tuple(letters)
letters_tuple = tuple(numders)

print("Letters:", letters_tuple)
print("Numbers:", numders_tuple)



