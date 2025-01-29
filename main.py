import sys
import base64
import requests
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QLineEdit, QPushButton, QLabel, QHBoxLayout
from PyQt5.QtCore import QUrl
from PyQt5.QtWebEngineWidgets import QWebEngineView


# 获取初始Cookies和登录以获取完整Cookies的函数
def get_cookies(username, password):
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

        # 准备登录数据
        encoded_username = base64.b64encode(username.encode()).decode()
        encoded_password = base64.b64encode(password.encode()).decode()
        payload = {
            "userAccount": username,
            "userPassword": "",
            "encoded": f"{encoded_username}%%%{encoded_password}"
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
        login_url = "http://xk.csust.edu.cn/jsxsd/xk/LoginToXk"
        response_login = requests.post(login_url, headers=post_headers, data=payload, allow_redirects=False)

        if response_login.status_code == 302:
            new_cookies = "; ".join([f"{cookie.name}={cookie.value}" for cookie in response_login.cookies])
            return f"{initial_cookies}; {new_cookies}"
        else:
            print("Login request did not result in a redirect")
            return None
    else:
        print(f"Failed to get initial cookies, status code: {response_initial.status_code}")
        return None


class WebBrowserApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        # 初始化UI组件
        self.setWindowTitle('长理成绩查询')
        self.setGeometry(100, 100, 1200, 800)

        main_layout = QVBoxLayout()

        input_layout = QHBoxLayout()
        self.username_label = QLabel("请输入你的学号：")
        self.password_label = QLabel("请输入你的密码：")
        input_layout.addWidget(self.username_label)
        self.username_entry = QLineEdit(self)
        input_layout.addWidget(self.username_entry)
        input_layout.addWidget(self.password_label)
        self.password_entry = QLineEdit(self)
        input_layout.addWidget(self.password_entry)

        self.confirm_button = QPushButton("确认", self)
        self.confirm_button.clicked.connect(self.fetch_and_display_webpage)
        input_layout.addWidget(self.confirm_button)

        main_layout.addLayout(input_layout)

        self.browser = QWebEngineView(self)
        main_layout.addWidget(self.browser)

        container = QWidget()
        container.setLayout(main_layout)
        self.setCentralWidget(container)

    def fetch_and_display_webpage(self):
        username = self.username_entry.text()
        password = self.password_entry.text()
        cookies = get_cookies(username, password)
        if cookies:
            post_data = {'xsfs': 'all', 'fxkc': '2'}  # 示例POST数据
            headers_query = {
                "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
                "Accept-Encoding": "gzip, deflate",
                "Accept-Language": "zh-CN,zh;q=0.9",
                "Cache-Control": "max-age=0",
                "Connection": "keep-alive",
                "Content-Type": "application/x-www-form-urlencoded",
                "Cookie": cookies,
                "Host": "xk.csust.edu.cn",
                "Origin": "http://xk.csust.edu.cn",
                "Referer": "http://xk.csust.edu.cn/jsxsd/kscj/cjcx_query",
                "Upgrade-Insecure-Requests": "1",
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36"
            }
            url = "http://xk.csust.edu.cn/jsxsd/kscj/cjcx_list"
            try:
                response = requests.post(url, headers=headers_query, data=post_data)
                if response.status_code == 200:
                    html_content = response.text
                    self.display_webpage(html_content)
                else:
                    self.display_webpage(f"请求失败，状态码: {response.status_code}\n{response.text}")
            except Exception as e:
                self.display_webpage(f"请求失败: {e}")
        else:
            self.display_webpage("未能成功获取Cookies，请检查您的用户名和密码。")

    def display_webpage(self, content):
        base_url = QUrl("about:blank")
        self.browser.setHtml(content, base_url)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    browser = WebBrowserApp()
    browser.show()
    sys.exit(app.exec_())