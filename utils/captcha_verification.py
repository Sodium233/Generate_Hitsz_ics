import requests
import config

def choose_message_verification(session):
    data = {
        'isMultifactor': 'true',
        'reAuthType': '3',
        'service': 'http://jw.hitsz.edu.cn/casLogin',
    }

    response = session.post(
        'https://ids.hit.edu.cn/authserver/reAuthCheck/changeReAuthType.do',
        cookies=session.cookies,
        headers=session.headers,
        data=data,
    )
    data = {
        'userName': config.USERNAME,
        'authCodeTypeName': 'reAuthDynamicCodeType',
    }
    # 发送请求获取验证码
    response = session.post(
        'https://ids.hit.edu.cn/authserver/dynamicCode/getDynamicCodeByReauth.do',
        cookies=session.cookies,
        headers=session.headers,
        data=data,
    )

    if(response.status_code != 200):
        print("请求失败，请检查网络连接或稍后再试")
        return 0
    elif("验证码已发送至手机" in response.text):
        print("验证码已发送至手机")
    elif("您已重复发送，请45秒后再试试" in response.text):
        print("验证码发送过于频繁，请稍后再试")
        return 0
    
    code = input("请输入收到的验证码：")
    data = {
        'service': 'http://jw.hitsz.edu.cn/casLogin',
        'reAuthType': '3',
        'isMultifactor': 'true',
        'password': '',
        'dynamicCode': code,
        'uuid': '',
        'answer1': '',
        'answer2': '',
        'otpCode': '',
        'skipTmpReAuth': 'true',
    }

    response = session.post(
        'https://ids.hit.edu.cn/authserver/reAuthCheck/reAuthSubmit.do',
        cookies=session.cookies,
        headers=session.headers,
        data=data,
    )

    if("认证成功" in response.text):
        print("认证成功")
        return 1
    else:
        return 0

def choose_hit_verification(session):
    data = {
        'isMultifactor': 'true',
        'reAuthType': '13',
        'service': 'http://jw.hitsz.edu.cn/casLogin',
    }

    response = session.post(
        'https://ids.hit.edu.cn/authserver/reAuthCheck/changeReAuthType.do',
        cookies=session.cookies,
        headers=session.headers,
        data=data,
    )
    
    data = {
        'userName': config.USERNAME,
        'authCodeTypeName': 'reAuthWeLinkDynamicCodeType',
    }

    # 发送请求获取验证码
    response = session.post(
        'https://ids.hit.edu.cn/authserver/dynamicCode/getDynamicCodeByReauth.do',
        cookies=session.cookies,
        headers=session.headers,
        data=data,
    )

    if(response.status_code != 200):
        print("请求失败，请检查网络连接或稍后再试")
        return 0
    elif("验证码已发送至手机" in response.text):
        print("验证码已发送至手机")
    elif("您已重复发送" in response.text):
        print("验证码发送过于频繁，请稍后再试")
        return 0
    
    code = input("请输入收到的验证码：")
    
    data = {
        'service': 'http://jw.hitsz.edu.cn/casLogin',
        'reAuthType': '13',
        'isMultifactor': 'true',
        'password': '',
        'dynamicCode': code,
        'uuid': '',
        'answer1': '',
        'answer2': '',
        'otpCode': '',
        'skipTmpReAuth': 'true',
    }

    response = session.post(
        'https://ids.hit.edu.cn/authserver/reAuthCheck/reAuthSubmit.do',
        cookies=session.cookies,
        headers=session.headers,
        data=data,
    )
    
    if ("认证成功" in response.text):
        print("认证成功")
        return 1
    else:
        return 0