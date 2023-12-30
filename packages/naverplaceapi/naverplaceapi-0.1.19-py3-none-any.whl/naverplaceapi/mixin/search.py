import json
import urllib
import urllib.parse
import urllib.request


class SearchMixin:
    CLIENT_ID = "ak4jckPbdjMcrMmFDSgv"
    CLIENT_SECRET = "Ye3VCcl2in"

    def search(self,
               keyword: str, page_size: int = 5,
               client_id: str = CLIENT_ID, client_secret: str = CLIENT_SECRET,
               proxies=None):
        encoded_keyword = urllib.parse.quote(keyword)
        url = f"https://openapi.naver.com/v1/search/local.json?query={encoded_keyword}&display={page_size}"

        request = urllib.request.Request(url)
        request.add_header("X-Naver-Client-Id", client_id)
        request.add_header("X-Naver-Client-Secret", client_secret)
        response = urllib.request.urlopen(request)
        rescode = response.getcode()

        result_list = []
        if rescode == 200:
            response_body = response.read()
            results = json.loads(response_body)['items']

            for result in results:
                result['title'] = result['title'].replace('<b>', '').replace('</b>', '')
                result_list.append(result)
        return result_list
