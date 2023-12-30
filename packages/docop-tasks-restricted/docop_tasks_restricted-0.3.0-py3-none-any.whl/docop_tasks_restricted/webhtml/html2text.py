"Extract plain text content of the HTML string"

import trafilatura

text = trafilatura.extract(html)
text = text.replace('\n', ' ').replace('¶', ':').replace('\"', "'")

