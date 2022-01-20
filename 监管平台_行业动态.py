import re
import json
import time

from requests import Session

from utils import init_log, DBClass, get_settings, get_database, request, get_md5, aes_cbc
from settings import headers, index_url, content_url

logger = init_log('my')
DATABASE, TABLE = get_database()
DOMAIN, RUN_INTERVAL = get_settings()
headers['Host'] = re.search('//(.*?)(/|$)', DOMAIN).group(1)
headers['Origin'] = DOMAIN
DB = DBClass(DATABASE, 'sqlserver')


class EvaluationNews(object):

    def __init__(self):
        self.session = Session()

    def parser(self, table: list):
        for li in table:
            try:
                uid = str(li.get('ID')).replace('%', '%25')
                obj = {
                    'title': li.get('TITLE'),
                    'release_time': li.get('TM'),
                    'url': content_url.format(uid),
                    'uid': uid,
                }
                pk = DB.select_condition(TABLE, 'id', [['uid', '=', obj.get('uid')]])
                if pk:
                    DB.update_many(TABLE, [obj], [{'id': pk[0][0]}])
                else:
                    DB.insert_many(TABLE, [obj])
            except Exception as e:
                pass

    def get_index(self, page: str) -> int:
        print('开始扫描 行业动态 页数={}'.format(page))
        logger.info('开始扫描 行业动态 页数={}'.format(page))
        try:
            data = {
                "pageNo": page,
                "pageSize": 10,
                "ptype": "jd",
                "timeType": "0",
                "total": 0,
                "ts": int(time.time() * 1000),
                "type": "1001",
            }
            data_str = 'E9498112A6CD42E0A4B2939CEBBC94CB' + ''.join([li + str(data.get(li)) for li in data])
            headers['portal-sign'] = get_md5(data_str)
            response, status_code = request(self.session, DOMAIN + index_url, 'post', headers=headers, json=data)
            data = aes_cbc.decrypt(response.json().get('Data'))
            data = json.loads(data)
            page_total = data.get('PageTotal')
            table = data.get('Table')
            self.parser(table)
            return page_total
        except Exception as e:
            print(e)
            logger.error('开始扫描 行业动态 页数={} 错误={}'.format(page, str(e)))

    def run(self):
        try:
            page = 1
            while True:
                page_total = self.get_index(page)
                if page < page_total:
                    page += 1
                else:
                    break
        except Exception as e:
            print(e)


def main():
    if RUN_INTERVAL:
        while True:
            try:
                EvaluationNews().run()
            except Exception as e:
                print(e)
            finally:
                time.sleep(60 * 60 * int(RUN_INTERVAL))
    else:
        EvaluationNews().run()


if __name__ == '__main__':
    main()
