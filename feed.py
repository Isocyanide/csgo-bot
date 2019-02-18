import requests
import pprint
import feedparser
import pickle
from telegram import InlineKeyboardMarkup, InlineKeyboardButton

def feed_in():

	url1 = "https://www.hltv.org/rss/news"

	feed = feedparser.parse(url1)

	feedlist = feed['entries']
	return(feedlist)

def notif(bot, update):
	list1_file = open('list1.db','rb+')

	try:
		list1 = pickle.load(list1_file)
	except:
		list1 = []

	list1_file.close()

	feed = feed_in()

	list1_file = open('list1.db','wb+')

	list2 = feed
	final_list = [i for i in list2 if i not in list1]
	pickle.dump(list2, list1_file)

	list1_file.close()

	feed_list_file = open('feed_list.db','rb+')

	try:
		feed_list = pickle.load(feed_list_file)
	except:
		feed_list = []
	feed_list_file.close()

	for item in final_list:
		title = item['title']
		summary = item['summary']
		link = item['link']

		text = f'<b>{title}</b>\n{summary}'

		inline_button = [[InlineKeyboardButton("More info", url = link)]]
		inline_button_markup = InlineKeyboardMarkup(inline_button)

		for chat_id in feed_list:
			bot.send_message(chat_id = chat_id, text = text, parse_mode = 'html', reply_markup = inline_button_markup)

def start_feed(bot, update):
	feed_list_file = open('feed_list.db','rb+')
	try:
		feed_list = pickle.load(feed_list_file)
	except:
		feed_list = []
	feed_list_file.close()

	msg = update.message
	chat_id = msg.chat_id

	adder = bot.get_chat_member(chat_id = msg.chat_id, user_id = msg.from_user.id)['status']

	if adder in ['creator', 'administrator']:
		if msg.chat_id not in feed_list:
			feed_list.append(msg.chat_id)
			bot.send_message(chat_id = chat_id, text = "Chat succesfully added!",  reply_to_message_id = msg.message_id)
		else:
			bot.send_message(chat_id = chat_id, text = "Your chat is already registered!",  reply_to_message_id = msg.message_id)
	else:
		bot.send_message(chat_id = chat_id, text = "You must be an admin to use this command.",  reply_to_message_id = msg.message_id)

	feed_list_file = open('feed_list.db','wb+')
	pickle.dump(feed_list, feed_list_file)	
	feed_list_file.close()

def stop_feed(bot, update):
	feed_list_file = open('feed_list.db','rb+')
	try:
		feed_list = pickle.load(feed_list_file)
	except:
		feed_list = []
	feed_list_file.close()

	msg = update.message
	chat_id = msg.chat_id

	adder = bot.get_chat_member(chat_id = msg.chat_id, user_id = msg.from_user.id)['status']

	if adder in ['creator', 'administrator']:
		if msg.chat_id in feed_list:
			feed_list.remove(msg.chat_id)
			bot.send_message(chat_id = chat_id, text = "Chat succesfully removed!",  reply_to_message_id = msg.message_id)
		else:
			bot.send_message(chat_id = chat_id, text = "Your chat isn't registered yet!",  reply_to_message_id = msg.message_id)
	else:
		bot.send_message(chat_id = chat_id, text = "You must be an admin to use this command.",  reply_to_message_id = msg.message_id)

	feed_list_file = open('feed_list.db','wb+')
	pickle.dump(feed_list, feed_list_file)
	feed_list_file.close()