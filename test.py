import re 

candidate = '12/12/14'

regex = re.compile(r'\d{2}/\d{2}/\d{2}')
matchobj = regex.search(candidate)
print(matchobj)