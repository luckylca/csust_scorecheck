import requests

# 第一步：获取初始Cookie
initial_url = "http://xk.csust.edu.cn/jsxsd/"
headers_initial = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
    "Accept-Encoding": "gzip, deflate",
    "Accept-Language": "zh-CN,zh;q=0.9",
    "Cache-Control": "max-age=0",
    "Connection": "keep-alive",
    "Host": "xk.csust.edu.cn",
    "Referer": "http://xk.csust.edu.cn/jsxsd/xk/LoginToXk?method=exit&tktime=1738033988000",
    "Upgrade-Insecure-Requests": "1",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36"
}

response_initial = requests.get(initial_url, headers=headers_initial)
if response_initial.status_code == 200:
    initial_cookies = "; ".join([f"{cookie.name}={cookie.value}" for cookie in response_initial.cookies])
    print(f"Initial Cookies: {initial_cookies}")
else:
    print(f"Failed to get initial cookies, status code: {response_initial.status_code}")
    exit(1)

# 第二步：使用获取到的Cookie构造并发送POST请求
login_url = "http://xk.csust.edu.cn/jsxsd/xk/LoginToXk"

# 使用你提供的载荷源代码
payload = {
    "userAccount": "202405010132",
    "userPassword": "",
    "encoded": "MjAyNDA1MDEwMTMy%%%QEx1Q2syNjEyMjQ="
}

post_headers = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
    "Accept-Encoding": "gzip, deflate",
    "Accept-Language": "zh-CN,zh;q=0.9",
    "Cache-Control": "max-age=0",
    "Connection": "keep-alive",
    "Content-Type": "application/x-www-form-urlencoded",
    "Cookie": initial_cookies,
    "Host": "xk.csust.edu.cn",
    "Origin": "http://xk.csust.edu.cn",
    "Referer": "http://xk.csust.edu.cn/jsxsd/",
    "Upgrade-Insecure-Requests": "1",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36"
}

response_login = requests.post(login_url, headers=post_headers, data=payload, allow_redirects=False)

# 检查是否是重定向响应
if response_login.status_code == 302:
    new_cookies = "; ".join([f"{cookie.name}={cookie.value}" for cookie in response_login.cookies])
    print(f"New Cookies from Login Request: {new_cookies}")

    # 拼接两个Cookie字符串，并确保每个Cookie之间有空格
    combined_cookies = f"{initial_cookies}; {new_cookies}"
    print(f"Combined Cookies: {combined_cookies}")
else:
    print(f"Login request did not result in a redirect, status code: {response_login.status_code}")