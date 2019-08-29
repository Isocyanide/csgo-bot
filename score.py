import requests
from bs4 import BeautifulSoup

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.76 Safari/537.36'}

def points_scraper():
	data = requests.get("https://www.hltv.org/events/4443/starladder-major-2019", headers = headers)

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

