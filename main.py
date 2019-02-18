import requests
import pprint
from telegram import InlineKeyboardMarkup, InlineKeyboardButton, InlineQueryResultArticle, ParseMode, InputTextMessageContent
from telegram.ext import (Updater, MessageHandler, Filters, CommandHandler, InlineQueryHandler,
						  ConversationHandler, RegexHandler, CallbackQueryHandler)
import logging

pp = pprint.PrettyPrinter(indent=4)

#Bot functions
from feed import notif, start_feed, stop_feed
from upcoming_matches import matches
from score import points

def main():

	logging.basicConfig(level=logging.INFO,
	                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

	updater = Updater(token="TOKEN")

	dispatcher = updater.dispatcher
	j = updater.job_queue

	job = j.run_repeating(notif, interval = 300, first = 0)

	matches_handler = CommandHandler('matches', matches)
	start_feed_handler = CommandHandler('start_feed', start_feed)
	stop_feed_handler = CommandHandler('stop_feed', stop_feed)
	points_handler = CommandHandler('points', points)

	dispatcher.add_handler(matches_handler)
	dispatcher.add_handler(start_feed_handler)
	dispatcher.add_handler(stop_feed_handler)
	dispatcher.add_handler(points_handler)

	updater.start_polling()
	updater.idle()

if __name__ == '__main__':
    main()
