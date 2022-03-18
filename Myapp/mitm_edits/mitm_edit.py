import json
import time

from mitmproxy import http
import django
import os, sys

sys.path.append("E:\PycharmProjects\GD1mock")
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "GD1mock.settings")
django.setup()
from Myapp.models import *


def request(flow):
    # '在请求发送到服务器之前进行干预的脚本'
    # 拦截模式
    project_id = os.path.basename(__file__).split('_')[0]
    mocks = DB_mock.objects.filter(project_id=project_id, state=True)
    for m in mocks:
        if m.catch_url in flow.request.url:  # 中了这个 mock 单元
            if m.model == 'lj':
                flow.response = http.Response.make(
                    m.state_code,
                    m.mock_response_body_lj,
                    json.loads(m.response_headers)
                )
            break


def response(flow):
    # '在请求从服务器返回后进行干预的脚本'
    # 放行模式
    project_id = os.path.basename(__file__).split('_')[0]
    mocks = DB_mock.objects.filter(project_id=project_id, state=True)
    for m in mocks:
        if m.catch_url in flow.request.url:  # 中了这个 mock 单元
            if m.model == 'fx':
                all_updatas = m.mock_response_body.split('\n')
                for u in all_updatas:
                    if '=>' in u:  # 是普通替换规则
                        try:
                            json.loads(flow.response.text)
                            flow.response.text = json.dumps(json.loads(flow.response.text), ensure_ascii=False)
                        except:
                            ...
                        flow.response.text = flow.response.text.replace(u.split('=>')[0].rstrip(),
                                                                        u.split('=>')[1].lstrip())
                    elif '=' in u:  # 是 json 路径替换规则
                        try:
                            old = json.loads(flow.response.text)
                        except:
                            continue
                        key = u.split('=')[0].rstrip()
                        value = eval(u.split('=')[1].lstrip())
                        tmp_cmd = ''
                        for i in key.split('.'):
                            try:
                                int(i)
                                tmp_cmd += '[%s]' % i
                            except:
                                tmp_cmd += '[%s]' % repr(i)
                        end_cmd = "old" + tmp_cmd + "=value"
                        try:
                            exec(end_cmd)
                        except:
                            continue
                        flow.response.text = json.dumps(old)
                    else:  # 不符合规则的
                        ...
            break
