import math

import requests
from djangoProject.settings import API_KEY, API_URL, SEARCH_METHOD, LIMIT, PAGE, SEARCH_FORMAT


def search_music(track_name, artist_name=None, page_id=None, track_id=None):
    result_url = f'{API_URL}?method={SEARCH_METHOD}&track={track_name}&api_key={API_KEY}&limit={LIMIT}&format={SEARCH_FORMAT}'
    if page_id:
        result_url += f'&page={page_id}'
    if artist_name:
        result_url += f'&artist={artist_name}'

    r = requests.get(result_url)
    if track_id:
        result_search = r.json()['results']['trackmatches']['track'][track_id]
        return result_search

    result_search = r.json()['results']['trackmatches']['track']
    total_results = int(r.json()['results']['opensearch:totalResults'])
    data = []
    result_json = {
        'total_results': total_results,
        'pages': math.ceil(total_results / LIMIT),
        'current_page': PAGE,
        'result': data,
    }
    if page_id:
        result_json.update({'current_page': page_id})
    count = 0
    for result in result_search:
        data.append({
            'track_id': count,
            'listeners': int(result['listeners']),
            'track_name': result['name'],
            'artist': result['artist'],
            'url': result['url'],
        })
        count += 1
    return result_json
