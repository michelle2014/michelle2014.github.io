:) helpers.py exists
:) can import helpers.py 
:( detects no lines in common
    expected 0 matches, not 1
:( detects one line in common
    expected "{'Line 3'}", not "{'8'}"
:( detects multiple lines in common
    expected 2 matches, not 1
:( handles duplicate lines in common
    expected 2 matches, not 1
:) handles no sentences in common
:) handles one sentence in common
:( handles multiple sentences in common
    expected 2 matches, not 1
:( handles sentences with different punctuation
    expected 1 matches, not 0
:( handles sentences with punctuation mid-sentence
    expected 2 matches, not 0
:( handles duplicate sentences in common
    expected 2 matches, not 1
:) handles no substrings in common
:( handles one substring in common
    expected 1 matches, not 0
:( handles multiple substrings in common
    expected 4 matches, not 0
:( handles substrings when strings are identical
    expected 4 matches, not 2
:( handles substring length longer than string length
    expected 0 matches, not 1
:( handles duplicate substrings in common
    expected 4 matches, not 0
:( handles substrings containing nonalpha chars
    expected 3 matches, not 1


from nltk.tokenize import sent_tokenize
import nltk
import difflib


def lines(a, b):
    """Return lines in both a and b"""

    # split a and b from newline and store in two lists
    sent_a = a.split('\n')
    sent_b = b.split('\n')

    # convert both list into set
    sa = set(sent_a)
    sb = set(sent_b)

    # define a new set to put those same sentences in
    highlights = sa & sb

    # return sentence list to be highlighted
    return highlights


def sentences(a, b):
    """Return sentences in both a and b"""

    # https://stackoverflow.com/questions/37605710/tokenize-a-paragraph-into-sentence-and-then-into-words-in-nltk
    # remove any newlinein a and b
    a = a.replace('\n', '')
    b = b.replace('\n', '')

    # this gives us a list of sentences
    sent_a = nltk.sent_tokenize(a)
    sent_b = nltk.sent_tokenize(b)

    # https://docs.python.org/3/tutorial/datastructures.html
    # convert both list into set
    sa = set(sent_a)
    sb = set(sent_b)

    # define a new set to put those same sentences in
    highlights = sa & sb

    # return sentence list to be highlighted
    return highlights

# define a function to split into substrings


def substrings_split(str, n):

    # define a substrings list
    substrings = []

    # loop through and append to substrings list
    for i in range(len(str) - n + 1):
        substrings.append(str[i:i + n])

    # return list for next use
    return substrings


def substrings(a, b, n):
    """Return substrings of length n in both a and b"""

    # call substrings split function
    sent_a = substrings_split(a, n)
    sent_b = substrings_split(b, n)

    # convert both list into set
    sa = set(sent_a)
    sb = set(sent_b)

    # define a new set to put those same sentences in
    highlights = sa & sb

    # return sentence list to be highlighted
    return highlights





	# check for duplicates
    # https://thispointer.com/python-3-ways-to-check-if-there-are-duplicates-in-a-list/
    # https://www.w3schools.com/python/python_howto_remove_duplicates.asp











a = '"Goodbye," said the fox. "Here is my secret. It is quite simple: One sees clearly only with the heart. Anything essential is invisible to the eyes."'
b = '"Goodbye," said the fox. "And now here is my secret, a very simple secret: It is only with the heart that one can see rightly; what is essential is invisible to the eye."'


for sentence in sent_b:
    tokenized_text_a = nltk.word_tokenize(sentence)


for sentence in sent_b:
    tokenized_text_b = nltk.word_tokenize(sentence)
	

# iterate over length of sentences and compare
    if len_a > len_b:
        for i in range(len_a):
            s = difflib.SequenceMatcher(None, sent_a[i], sent_b[i])
            if s.ratio() == 1.0:
                return sent_a[i]

    if len_a < len_b:
        for i in range(len_b):
            s = difflib.SequenceMatcher(None, sent_a[i], sent_b[i])
            if s.ratio() == 1.0:
                return sent_a[i]
				

x = 'only I had promised to spend Sunday with a girl. Raymond promptly replied that she could come, too. In fact, his friends wife would be very pleased not to be the only woman in a party of men.'
chunks, chunk_size = len(x), len(x)/4
[ x[i:i+chunk_size] for i in range(0, chunks, chunk_size) ]
print(x)