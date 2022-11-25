import re

regex = 'design\s*pattern'
text = 'design     patterns'

result = re.findall(regex, text, re.IGNORECASE)
print(result)