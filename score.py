import requests
from bs4 import BeautifulSoup

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.76 Safari/537.36'}
'''
data = requests.get("http://esportlivescore.com/e_444767-g2-vs-tyloo-iem-katowice-2019-main-qualifier.html", headers = headers)

soup = BeautifulSoup(data.content, features="html.parser")

team_list = []

teams = soup.find_all('div', class_= 'team-info__team')
for team in teams:
	team_list.append(team.find('h2').text)
score_1 = soup.find('span', class_= 'team_1_overall_score_1').text
score_2 = soup.find('span', class_= 'team_2_overall_score_1').text

score_1 = f"{score_1} : {team_list[0]}"
score_2 = f"{score_2} : {team_list[1]}"
#print(soup.find_all('div', class_= 'teamName'))
'''

def points_scraper():
	data = requests.get("https://www.hltv.org/events/3883/iem-katowice-2019", headers = headers)

	soup = BeautifulSoup(data.content, features="html.parser")

	team_k = []

	table = soup.find('table', class_="table")
	team_list = table.find_all('div', class_ = "text-ellipsis")
	for team in team_list:
		team_name = team.text
		team_k.append(team_name)

	points = soup.find_all('td', class_ = "points")
	text = f'<b>Points table:</b>\n'
	for l in range(0, len(team_k)):
		text += (f'<b>{team_k[l]}</b> <i>{points[l].text}</i>\n')
	return text

def points(bot, update):
	text = points_scraper()
	bot.send_message(chat_id = update.message.chat_id, text = text, parse_mode = 'html', reply_to_message_id = update.message.message_id)

