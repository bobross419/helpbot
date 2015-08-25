from lib import utils
from lib import helps

outputs = []


def process_message(data):
    if data.get('text', '').split()[0] == '!preview':
        text = data.get('text').split()
        channel = data.get('channel')

        # Setup plugin
        admin_channel, botname, icon_emoji = utils.setup_bot(config)
        message_attrs = {'icon_emoji': icon_emoji, 'username': botname}

        # Only allow !preview from admin_channel
        admin_channel_id = utils.get_channel_id_by_name(admin_channel,
                                                        slack_client)
        if admin_channel_id not in channel:
            return
        
	user = data.get('user')
        username = utils.get_user_name(user, slack_client)
        if len(text) > 1:
            preview_channel = text[1].strip('#')
        else:
            text = ("%s - to preview a channel or private group type "
                    "`!preview <channel/group>`" % username)
            outputs.append([channel, text, message_attrs])
            return
        preview_channel_id = utils.get_channel_id_by_name(preview_channel,
                                                         slack_client)
	# Hardcoded for now
	records = config.get('messages') 
        preview = utils.preview_channel(preview_channel_id, records, slack_client)
	
        if preview['ok']:
	    preview_text = utils.format_history(preview['messages'], slack_client)
	    preview_text = '\n'.join(preview_text)
            text = "%s previewed channel %s:\n```%s```" % (username, preview_channel, preview_text)
        else:
            text = ("%s failed to preview %s"
                    " channel - %s" % (username, preview_channel,
                                       preview.get('error', 'Unknown error!')))
        logging.info(text)
        print(text)
        outputs.append([channel, text, message_attrs])
