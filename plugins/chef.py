from lib import utils

outputs = []


def process_message(data):
    if data.get('text', '').split()[0] == '!chef':
        text = data.get('text').split()
        channel = data.get('channel')

        
        # Setup plugin
        admin_channel, botname, icon_emoji = utils.setup_bot(config)
        message_attrs = {'icon_emoji': icon_emoji, 'username': botname}
        
        
        user = data.get('user')
        username = utils.get_user_name(user, slack_client)
        
        
        if len(text) > 1:
            command = text[1]
            args = text[2:]
        else:
            text = ("%s - to chef type "
                    "`!chef <command>`" % username)
            outputs.append([channel, text, message_attrs])
            return
        
        text = "User:%s\nCommand:%s\nArgs:%s" % (username, command, args)
        
        logging.info(text)
        print(text)
        outputs.append([channel, text, message_attrs])
