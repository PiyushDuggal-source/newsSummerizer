from bs4 import BeautifulSoup

html = '''
<tr class="athing" id="41775128">
      <td align="right" valign="top" class="title"><span class="rank">2.</span></td>      <td valign="top" class="votelinks"><center><a id="up_41775128" href="vote?id=41775128&amp;how=up&amp;goto=newest"><div class="votearrow" title="upvote"></div></a></center></td><td class="title"><span class="titleline"><a href="https://requstory.com/" rel="nofollow">Requstory</a><span class="sitebit comhead"> (<a href="from?site=requstory.com"><span class="sitestr">requstory.com</span></a>)</span></span></td></tr>
'''

soup = BeautifulSoup(html, 'html.parser')

# Extract the rank
rank = soup.find('span', class_='rank').get_text()

# Extract the title (link text)
title = soup.find('span', class_='titleline').a.get_text()

# Extract the site name
site = soup.find('span', class_='sitestr').get_text()

# Print the extracted text
print(f"Rank: {rank}")
print(f"Title: {title}")
print(f"Site: {site}")

