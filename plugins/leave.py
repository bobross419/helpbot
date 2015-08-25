from lib import utils

outputs = []


def process_message(data):
    if data.get('text', '').split()[0] == '!leave':
        text = data.get('text').split()
        channel = data.get('channel')

        # Setup plugin
        admin_channel, botname, icon_emoji = utils.setup_bot(config)
        message_attrs = {'icon_emoji': icon_emoji, 'username': botname}

        # Only allow !leave from admin_channel
        admin_channel_id = utils.get_channel_id_by_name(admin_channel,
                                                        slack_client)
        if admin_channel_id not in channel:
            return

        user = data.get('user')
        username = utils.get_user_name(user, slack_client)
        if len(text) > 1:
            leave_channel = text[1].strip('#')
        else:
            text = ("%s - to leave a channel or private group type "
                    "`!leave <channel/group>`" % username)
            outputs.append([channel, text, message_attrs])
            return
        leave_channel_id = utils.get_channel_id_by_name(leave_channel,
                                                         slack_client)
        leave = utils.kick_user(user, leave_channel_id, slack_client)
        if leave['ok']:
            text = "%s left channel %s." % (username, leave_channel)
        else:
            text = ("Failed to leave %s to %s"
                    " channel - %s" % (username, leave_channel,
                                       leave.get('error', 'Unknown error!')))
        logging.info(text)
        print(text)
        outputs.append([channel, text, message_attrs])
