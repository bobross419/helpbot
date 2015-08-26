import arrow
import json
import sys


def _extract_id(name, items):
    for item in items:
        if item['name'] == name:
            return item['id']
    return None


def format_helps(helps):
    text = []
    for halp in helps:
        halp = json.loads(halp)
        channel = halp.keys()[0]
        user = halp[channel]['user']
        ts = arrow.get(halp[channel]['timestamp'])
        t = ":fire: @%s needs halp in %s - %s" % (user, channel, ts.humanize())
        text.append(t)
    return text


def format_prs(prs):
    text = []
    for pr in prs:
        pr = json.loads(pr)
        link = pr.keys()[0]
        user = pr[link]['user']
        ts = arrow.get(pr[link]['timestamp'])
        t = ":warning: @%s needs this PR reviewed: %s - %s" % (user, link,
                                                               ts.humanize())
        text.append(t)
    return text


def get_channels(slack_client):
    return json.loads(slack_client.api_call('channels.list'))


def get_channel_id_by_name(channel, slack_client):
    groups = get_groups(slack_client)
    match = _extract_id(channel, groups.get('groups', []))
    if not match:
        channels = get_channels(slack_client)
        match = _extract_id(channel, channels.get('channels', []))
    return match


def get_channel_name(channel, slack_client):
    if channel.startswith('G'):
        apicall = 'groups.info'
        channel_type = 'group'
    else:
        apicall = 'channels.info'
        channel_type = 'channel'
    cdata = json.loads(slack_client.api_call(apicall, channel=channel))
    return cdata[channel_type]['name']


def get_groups(slack_client):
    return json.loads(slack_client.api_call('groups.list'))


def get_user_name(user, slack_client):
    udata = json.loads(slack_client.api_call('users.info', user=user))
    return udata['user']['name']


def invite_user(user, channel, slack_client):
    if channel.startswith('G'):
        apicall = 'groups.invite'
    else:
        apicall = 'channels.invite'
    resp = slack_client.api_call(apicall, user=user, channel=channel)

    return json.loads(resp)


def get_plugins():
    #plugins = { 'ok': True, 'plugins': [ 'foo', 'bar' ] }
    modules = bot.bot_plugins
    plugins = {'ok': True, 'plugins': modules }
    return plugins


def setup_bot(config):
    admin_channel = config.get('admin_channel')
    botname = config.get('botname')
    icon_emoji = config.get('icon_emoji')

    return admin_channel, botname, icon_emoji
