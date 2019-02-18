import requests
from bs4 import BeautifulSoup
import pprint 
from datetime import datetime

pp = pprint.PrettyPrinter(indent=4)

def upcoming_matches():
	final_dict = {}

	headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.76 Safari/537.36'}
	data = requests.get("https://www.hltv.org/matches?event=3884", headers = headers)

	soup = BeautifulSoup(data.content, features="html.parser")
	
	matches = soup.find_all('a', class_= "a-reset block upcoming-match standard-box")

	for match1 in list(matches):
		local_dict = {}
		try:
			team_list = match1.find_all('div', class_ = "team")
			local_dict['versus'] = f"{team_list[0].text} vs {team_list[1].text}"
		except:
			break

		time1 = match1.find('div', class_= "time").get("data-unix")
		time1 = ((int(time1))/1000)+19800
		date = datetime.utcfromtimestamp(time1).strftime('%Y-%m-%d %H:%M:%S').split(" ")
		year = date[0]
		local_dict['time'] = (date[1])[:5]

		local_dict['event'] = match1.find('span', class_="event-name").text
		
		if year in final_dict.keys():
			final_dict[year].append(local_dict)
		else:
			final_dict[year] = []
			final_dict[year].append(local_dict)

	text = f""

	for year in final_dict.keys():
		text += f"\n\n<b>{year}</b>\n"

		list_of_mathces = final_dict[year]
		for match in list_of_mathces:
			text += f"\n<b>{match['time']} : {match['event']}</b>\n<i>{match['versus']}</i> "

	if text:
		return text
	else:
		return "No upcoming matches."

def matches(bot, update):
	text = upcoming_matches()
	bot.send_message(chat_id = update.message.chat_id, text = text, parse_mode = 'html', reply_to_message_id = update.message.message_id)
