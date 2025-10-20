
query = 'a?t'
sample = [
        'snack',
        'act',
        'pack',
        'axt'
    ]


'''
For wildcard matching, we know a word matches if characters in both words:
    1. equal (ex. b = b, c = c)
    2. query has ? (? = all characters, ? = a, ? =b, ...)

Matching can be made by iterating through each character at the same index for both words and checking for differences.
We can also reduce checking by first checking if the lengths differ (ex. app?le could never equal to bee)

Algorithm will work by:
    1. iterating through each word
    2. check if length is the same 
    3. check if each character are equal by match characters or ?
    4. remove from matches if not equal, otherwise keep
    5. return matches
'''
matches = []
for word in sample:
    # different length of both words implies that these words will not match
    if len(query) == len(word): 
        # append the word first, if a difference is found remove
        matches.append(word) 
        for i in range(len(query)): 
            if query[i] != word[i] and query[i] != '?': 
                matches.pop()
                break

print(matches)


