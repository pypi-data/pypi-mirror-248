# 从sa读取数据

import pandas as pd
import requests


class SA:
    def __init__(self, root_url, JSON_HEADERS, FORM_HEADERS, project_id, user, token, *args, **kwargs):
        self.JSON_HEADERS = JSON_HEADERS
        self.FORM_HEADERS = FORM_HEADERS
        self.root_url = root_url
        self.project_id = project_id
        self.user = user
        self.token = token

    def get_sql_data(self, sql):
        """获得sql原始数据"""
        report_url = f'{self.root_url}/api/sql/query?token={self.token}&project={self.project_id}'
        body = {
            "q": sql,
            "format": 'csv'
        }
        rep = requests.post(report_url, headers=self.FORM_HEADERS, data=body, verify=True)
        return rep

    def sparse_data(self, raw_text):
        text_lines = raw_text.split('\n')
        text_list = [line.split('\t') for line in text_lines]
        df = pd.DataFrame(text_list[1:-1], columns=text_list[0])  # 第一行是标题，最后一行是空行
        return df
