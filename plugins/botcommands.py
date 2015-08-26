from lib import utils

outputs = []


def process_message(data):
    if data.get('text', '').split()[0] == '!botcommands':

        admin_channel, botname, icon_emoji = utils.setup_bot(config)
        message_attrs = {'icon_emoji': icon_emoji, 'username': botname}

        user = data.get('user')
        username = utils.get_user_name(user, slack_client)
        
        bot_commands = utils.get_plugins()
        if bot_commands['ok']:
            text = "bot commands foo"
        else:
            text = ("Failed to get commands %s"
                    " - %s" % (username,
                                       bot_commands.get('error', 'Unknown error!')))
        logging.info(text)
        print(text)
        outputs.append([channel, text, message_attrs])
