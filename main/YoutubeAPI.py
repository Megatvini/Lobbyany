import json
from urlparse import urlparse
import urllib
import urllib2


class YoutubeAPI:
    youtube_key = "AIzaSyDOa1aEANwXp_TF8O57FmyT_Idu7vb7PWA"

    apis = {
        'videos.list': 'https://www.googleapis.com/youtube/v3/videos',
        'search.list': 'https://www.googleapis.com/youtube/v3/search',
        'channels.list': 'https://www.googleapis.com/youtube/v3/channels',
        'playlists.list': 'https://www.googleapis.com/youtube/v3/playlists',
        'playlistItems.list': 'https://www.googleapis.com/youtube/v3/playlistItems',
        'activities': 'https://www.googleapis.com/youtube/v3/activities',
    }

    page_info = {}

    def search(self, q, max_results=10):

        params = {
            'q': q,
            'part': 'id, snippet',
            'maxResults': max_results
        }

        return self.search_advanced(params)

    def search_videos(self, q, max_results=10, order=None):

        params = {
            'q': q,
            'type': 'video',
            'part': 'id, snippet',
            'maxResults': max_results
        }
        if order is not None:
            params['order'] = order

        return self.search_advanced(params)

    def search_channel_videos(self, q, channel_id, max_results=10, order=None):

        params = {
            'q': q,
            'type': 'video',
            'channelId': channel_id,
            'part': 'id, snippet',
            'maxResults': max_results
        }
        if order is not None:
            params['order'] = order

        return self.search_advanced(params)

    def search_advanced(self, params, page_info=False):

        api_url = self.get_api('search.list')
        if params is None or 'q' not in params:
            raise ValueError('at least the Search query must be supplied')

        api_data = self.api_get(api_url, params)
        if page_info:
            return {
                'results': self.decode_list(api_data),
                'info': self.page_info
            }
        else:
            return self.decode_list(api_data)

    def get_api(self, name):
        return self.apis[name]


    def decode_list(self, api_data):

        res_obj = json.loads(api_data)
        if 'error' in res_obj:
            msg = "Error " + res_obj['error']['code'] + " " + res_obj['error']['message']
            if res_obj['error']['errors'][0]:
                msg = msg + " : " + res_obj['error']['errors'][0]['reason']
            raise Exception(msg)
        else:
            self.page_info = {
                'resultsPerPage': res_obj['pageInfo']['resultsPerPage'],
                'totalResults': res_obj['pageInfo']['totalResults'],
                'kind': res_obj['kind'],
                'etag': res_obj['etag'],
                'prevPageToken': None,
                'nextPageToken': None
            }
            if 'prevPageToken' in res_obj:
                self.page_info['prevPageToken'] = res_obj['prevPageToken']
            if 'nextPageToken' in res_obj:
                self.page_info['nextPageToken'] = res_obj['nextPageToken']

            items_array = res_obj['items']
            if isinstance(items_array, dict) or len(items_array) == 0:
                return False
            else:
                return items_array

    def api_get(self, url, params):
        params['key'] = self.youtube_key

        f = urllib2.urlopen(url + "?" + urllib.urlencode(params))
        data = f.read()
        f.close()

        return data

    def getMp3DownloadLink(self, youtubeVideoId):
        return "http://www.youtubeinmp3.com/fetch/?video=http://www.youtube.com/watch?v=" + youtubeVideoId


    def getVideoSearchSuggestions(self, query, maxSuggestions):
        res = self.search(query, maxSuggestions)
        if (len(res) == 0):
            return []
        else:
            return map(lambda x: x['snippet']['title'], res)

    def getVideoId(self, query):
        res = self.search(query)
        if (not res):
            return ''
        return res[0]['id']['videoId']

    def parseToSeconds(self, param):
        a = param.replace("P", " ").replace("T", " ").replace("M", " ").replace("S", " ")
        spl = a.split()
        res = int(spl[0])*60 + int(spl[1])
        return res



    def getVideoDuration(self, videoId):
        link = "https://www.googleapis.com/youtube/v3/videos"
        params = {"key": self.youtube_key, "part": "contentDetails", "id": "9bZkp7q19f0"}
        f = urllib2.urlopen(link + "?" + urllib.urlencode(params))
        data = f.read()
        f.close()
        obj = json.JSONDecoder().decode(data)
        a = obj["items"]
        b = a[0]
        c = b["contentDetails"]
        d = c["duration"]
        print(data)
        return self.parseToSeconds(d)




    def _parse_url_path(self, url):

        array = urlparse(url)
        return array['path']

    def _parse_url_query(self, url):

        array = urlparse(url)
        query = array['query']
        query_parts = query.split('&')
        params = {}
        for param in query_parts:
            item = param.split('=')
            if not item[1]:
                params[item[0]] = ''
            else:
                params[item[0]] = item[1]

        return params

#youtube = YoutubeAPI()


# print(youtube.getMp3DownloadLink(youtube.getVideoId("icejfish")))
# print(youtube.getVideoSearchSuggestions("batman", 10))

