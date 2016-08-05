import logging
log = logging.getLogger(__name__)

import requests
import requests.exceptions
import plugins.streams


def make_twitch_stream(data):
	channel_data = data.get('channel', {})
	channel = channel_data.get('name', '').lower()
	title = channel_data.get('status', '')
	game = data.get('game')

	return plugins.streams.Stream(channel, 'twitch.tv/' + channel, title, game)


def get_twitch_data(channels):
	url = 'https://api.twitch.tv/kraken/streams'
	query_params = {'channel': ','.join(channels)}
	response = requests.get(url, query_params)
	response.raise_for_status()

	return response.json()


def get_online_streams(urls):
	"""From a collection of URLs, get the ones that are live on twitch.tv."""
	channels = plugins.streams.filter_urls(urls, 'twitch.tv')

	if not channels:
		return []

	data = get_twitch_data(channels)
	streams = data.get('streams', [])
	log.debug('%s online twitch.tv streams', len(streams))

	return [make_twitch_stream(stream) for stream in streams]
