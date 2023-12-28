# -*- coding: utf-8 -*-
# author:Tiper(邱鹏)
# 文件所属项目:QDC SMS SDK
# 文件描述:QuanmSMS SDK (泉鸣开放平台sms接口SDK)，包含执行短信业务所需的方法
# ♥Python版本要求：Python3及以上（可自行修改兼容Python2）♥
# 官网：dev.quanmwl.com
# 更新日期:2023-11-13【更改配置方式】

import random
import hashlib
import requests


class SDK:
    def __init__(self, openID='', apiKey='', apiHttp='http'):
        # 请开发者修改下列三行配置信息
        self.open_id = openID   # 开发者ID
        self.api_key = apiKey   # 能力列表的apiKey
        self.def_model_id = 0    # 默认情况下使用的模板ID,供外部使用
        self.sdk_version = '1.0.0'  # sdk版本号【非必要不要修改】
        if openID == '' or apiKey == '' :
            print('[SMS_SDK]ArgerError!openID or apiKey is null!console:https://dev.quanmwl.com/console')
            return
        if apiHttp != 'http' and apiHttp != 'https':
            print('[SMS_SDK]ArgerError!apiHttp:The specified value is not supported!(you can use: "http" or "https")')
            return

        # 因备用通道现仅在特殊情况开放【默认关闭】
        # 故自动节点功能默认关闭，不建议普通用户或在未和平台确认的情况下开启自动节点功能
        self.api_http = apiHttp  # 【默认，api支持https，如有需要请修改初始化参数：apiHttp】
        self.api_host = 'dev.quanmwl.com'  # Api Host【默认,非必要无需修改】
        self.api_gateway = self.api_http + '://' + self.api_host  # 【默认,非必要无需修改】

        self.try_next = 0  # 失败容错及刷间隔【默认，非必要无需修改】
        self.standby_number = 0  # 备用线路计数器

        # 更多状态：https://quanmwl.yuque.com/docs/share/9fbd5429-6575-403d-8a3d-7081b2977eda?#8sz4 《平台状态码处理指引》

    def sign(self, _tel, model_id, model_args):
        # type:(str, str, str) -> str
        """
        签名方法
        :param _tel: 接收者手机号
        :param model_id: 短信模板ID
        :param model_args: 短信模板变量参数字典
        :return:
        """
        hl = hashlib.md5()
        server_sign_data = f"{self.open_id}{self.api_key}{_tel}{model_id}{model_args}"
        hl.update(server_sign_data.encode("utf-8"))
        return hl.hexdigest()

    def send(self, tel, model_id, model_args):
        # type:(str, int, dict) -> tuple[bool, str]
        """
        发送短信
        :param tel: 接收者手机号
        :param model_id: 短信模板ID
        :param model_args: 短信模板变量参数字典
        :return:
        """
        headers = {
            'User-Agent': 'QuanmOpenApi_Python_SDK-Sms_' + self.sdk_version,  # 非必要，但推荐传入用于兼容性统计
        }

        data = {
            'openID': self.open_id,
            'tel': tel,
            'sign': self.sign(tel, str(model_id), str(model_args).replace(' ', '')),
            'model_id': model_id,
            'model_args': f'{model_args}'
        }
        try:
            response = requests.post(f'{self.api_gateway}/v1/sms', headers=headers, data=data)
            # http_status = response.status_code  几乎可以不依赖http状态码，如有需要请自行修改
        except:
            return False, 'Server Error\nTip: You can check if the connection to dev.quanmwl.com is smooth (the gateway you configured is: ' + self.api_gateway +' )If the configuration is correct and the network is unobstructed, please upgrade your SDK', None
        _mess = 'Not Find'
        if response is None or '<!DOCTYPE html>' in response.text:
            print("[SMS_SDK]Requests Fail")

            return False, _mess, None
        else:
            try:
                redata = eval(response.text)
            except Exception as e:
                return False, f"解析错误:{e}", None
            else:
                _mess = redata['mess']

            http_state = response.status_code
            if http_state != 200 and 'state' not in redata:
                return False, _mess, None

            api_state = redata['state']

            if api_state == '200':
                return True, _mess, api_state
            else:
                return False, _mess, api_state


if __name__ == '__main__':
    sms = SDK()  # 实例化SDK【提示：该操作仅需进行一次！】
    # 这里演示了一个简单的验证码功能
    check_code = random.randint(100000, 999999)  # 生成验证码
    results, info = sms.send('接受者的手机号', sms.def_model_id, {'code': check_code})  # 发送
    print(info)
