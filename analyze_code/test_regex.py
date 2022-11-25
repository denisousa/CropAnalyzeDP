import re
from patterns_name import patterns

patterns_join = '|'.join(patterns)
regex_all_patterns_join = f'({patterns_join})'
text = 'factory_____AAmethod bla bla bla'

result = re.findall(regex_all_patterns_join, text, re.IGNORECASE)
print(result, text)