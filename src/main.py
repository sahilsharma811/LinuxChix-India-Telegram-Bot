from telegram.ext import Updater,CommandHandler
from telegram import ChatAction
from datetime import datetime, timedelta
from pytz import timezone
from time import sleep
import logging,requests,pytz,re,ast

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',level=logging.INFO)

updater=Updater(token='Telegram Bot Token')

dispatcher=updater.dispatcher

meetupApi={'sign':'true','key':'Meetup API Key'}

utc = pytz.utc

def start(bot, update, args):
        bot.sendChatAction(chat_id=update.message.chat_id, action=ChatAction.TYPING)
        sleep(0.2)
        bot.sendMessage(chat_id=update.message.chat_id,text='''
Hi! Welcome to the LinuxChix Bot.
Use /help to get /help''')

def motto(bot, update):
        bot.sendChatAction(chat_id=update.message.chat_id, action=ChatAction.TYPING)
        sleep(0.2)
        bot.sendMessage(chat_id=update.message.chat_id,text='Be Polite! Be Helpful.')

def websiteLink(bot, update):
        bot.sendChatAction(chat_id=update.message.chat_id, action=ChatAction.TYPING)
        sleep(0.2)
        bot.sendMessage(chat_id=update.message.chat_id,text='http://india.linuxchix.org/')

def meetupPageLink(bot, update):
        bot.sendChatAction(chat_id=update.message.chat_id, action=ChatAction.TYPING)
        sleep(0.2)
        bot.sendMessage(chat_id=update.message.chat_id,text='https://www.meetup.com/LinuxChix-India-Meetup/')

def nextMeetupDetails(bot, update):
        bot.sendChatAction(chat_id=update.message.chat_id, action=ChatAction.TYPING)
        sleep(0.2)
        r=requests.get('https://api.meetup.com/LinuxChix-India-Meetup/events', params=meetupApi)
        event_link=r.json()[0]['link']
        date_time=r.json()[0]['time']//1000
        utc_dt = utc.localize(datetime.utcfromtimestamp(date_time))
        indian_tz = timezone('Asia/Kolkata')
        date_time=utc_dt.astimezone(indian_tz)
        date_time=date_time.strftime('%Y-%m-%d %H:%M:%S %Z%z')
        if 'venue' in r.json()[0]:
                venue=r.json()[0]['venue']['address_1']
                bot.sendLocation(chat_id=update.message.chat_id, latitude=r.json()[0]['venue']['lat'],longitude=r.json()[0]['venue']['lon'])
        else:
                venue='Venue is still to be decided'
        bot.sendMessage(chat_id=update.message.chat_id, text='''
Next Meetup
Date/Time : %s
Venue : %s
Event Page : %s
'''%(date_time, venue, event_link))

def nextMeetupSchedule(bot, update):
        bot.sendChatAction(chat_id=update.message.chat_id, action=ChatAction.TYPING)
        sleep(0.2)
        r=requests.get('https://api.meetup.com/LinuxChix-India-Meetup/events', params=meetupApi)
        bot.sendMessage(chat_id=update.message.chat_id, text='''
Next Meetup Schedule
%s
'''%(re.sub('</a>','',re.sub('<a href="','',re.sub('<br/>',' ',re.sub('<p>',' ',re.sub('</p>','\n',r.json()[0]['description'])))))),parse_mode='HTML')


def facebookLink(bot, update):
        bot.sendChatAction(chat_id=update.message.chat_id, action=ChatAction.TYPING)
        sleep(0.2)
        bot.sendMessage(chat_id=update.message.chat_id, text='https://www.facebook.com/linuxchixin')

def twitterLink(bot, update):
        bot.sendChatAction(chat_id=update.message.chat_id, action=ChatAction.TYPING)
        sleep(0.2)
        bot.sendMessage(chat_id=update.message.chat_id,text='https://twitter.com/linuxchixin')

def githubLink(bot, update):
        bot.sendChatAction(chat_id=update.message.chat_id, action=ChatAction.TYPING)
        sleep(0.2)
        bot.sendMessage(chat_id=update.message.chat_id, text='https://github.com/linuxchixin')

def developer(bot,update):
        bot.sendChatAction(chat_id=update.message.chat_id, action=ChatAction.TYPING)
        sleep(0.2)
        bot.sendMessage(chat_id=update.message.chat_id, text='https://github.com/sahilsharma811/')

def codeRepository(bot,update):
        bot.sendChatAction(chat_id=update.message.chat_id, action=ChatAction.TYPING)
        sleep(0.2)
        bot.sendMessage(chat_id=update.message.chat_id, text='To contribute or create an issue for the bot, go to: ' + 
                'https://github.com/sahilsharma811/LinuxChix-India-Telegram-Bot')        

def help(bot, update):
        bot.sendChatAction(chat_id=update.message.chat_id, action=ChatAction.TYPING)
        sleep(0.2)
        bot.sendMessage(chat_id=update.message.chat_id, text='''
Use one of the following commands
/motto - to see motto of LinuxChix group
/website - to goto LinuxChix Website
/meetuppage - to get a link to LinuxChix Meetup page
/nextmeetup - to get info about next Meetup
/nextmeetupschedule - to get schedule of next Meetup
/facebook - to get a link to LinuxChix Facebook page
/twitter - to get LinuxChix Twitter link
/github - to get a link to LinuxChix Github page
/repository - to see the source code and contribute to the bot.
''')

dispatcher.add_handler(CommandHandler('start', start, pass_args=True))
dispatcher.add_handler(CommandHandler('website', websiteLink))
dispatcher.add_handler(CommandHandler('motto', motto))
dispatcher.add_handler(CommandHandler('twitter', twitterLink))
dispatcher.add_handler(CommandHandler('meetuppage', meetupPageLink))
dispatcher.add_handler(CommandHandler('nextmeetup', nextMeetupDetails))
dispatcher.add_handler(CommandHandler('nextmeetupschedule', nextMeetupSchedule))
dispatcher.add_handler(CommandHandler('facebook', facebookLink))
dispatcher.add_handler(CommandHandler('github', githubLink))
dispatcher.add_handler(CommandHandler('developer', developer))
dispatcher.add_handler(CommandHandler('help', help))
dispatcher.add_handler(CommandHandler('repository', codeRepository))

updater.start_polling()