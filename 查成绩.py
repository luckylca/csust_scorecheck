import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QLineEdit, QPushButton, QLabel, QHBoxLayout
from PyQt5.QtCore import QUrl
from PyQt5.QtWebEngineWidgets import QWebEngineView
import requests


class WebBrowserApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        # 设置窗口标题和大小
        self.setWindowTitle('长理成绩查询')
        self.setGeometry(100, 100, 1200, 800)

        # 主布局
        main_layout = QVBoxLayout()

        # 输入框和确认按钮
        input_layout = QHBoxLayout()

        self.cookie_label = QLabel("请输入你的完整Cookie字符串：")
        input_layout.addWidget(self.cookie_label)

        self.cookie_entry = QLineEdit(self)
        input_layout.addWidget(self.cookie_entry)

        self.confirm_button = QPushButton("确认", self)
        self.confirm_button.clicked.connect(self.fetch_and_display_webpage)
        input_layout.addWidget(self.confirm_button)

        main_layout.addLayout(input_layout)

        # 创建QWebEngineView用于显示网页
        self.browser = QWebEngineView(self)
        main_layout.addWidget(self.browser)

        # 设置主窗口的中心部件
        container = QWidget()
        container.setLayout(main_layout)
        self.setCentralWidget(container)

    def fetch_and_display_webpage(self):
        # 获取用户输入的Cookie字符串
        custom_cookie_input = self.cookie_entry.text()

        # 定义POST请求的数据
        post_data = {
            'kksj': '',  # 考试时间
            'kcxz': '',  # 课程性质
            'kcmc': '',  # 课程名称
            'xsfs': 'all',  # 显示方式
            'fxkc': '2'  # 非选课程
        }

        # 请求头信息（包括Cookie）
        headers = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'zh-CN,zh;q=0.9',
            'Cache-Control': 'max-age=0',
            'Connection': 'keep-alive',
            'Content-Type': 'application/x-www-form-urlencoded',
            'Host': 'xk.csust.edu.cn',
            'Origin': 'http://xk.csust.edu.cn',
            'Referer': 'http://xk.csust.edu.cn/jsxsd/kscj/cjcx_query',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36',
            'Cookie': custom_cookie_input  # 将Cookie字符串直接添加到请求头中
        }

        url = "http://xk.csust.edu.cn/jsxsd/kscj/cjcx_list"

        try:
            # 发送POST请求
            response = requests.post(url, headers=headers, data=post_data)

            # 检查响应内容
            if response.status_code == 200:
                html_content = response.text
                self.display_webpage(html_content)
            else:
                self.display_webpage(f"请求失败，状态码: {response.status_code}\n{response.text}")

        except Exception as e:
            self.display_webpage(f"请求失败: {e}")

    def display_webpage(self, content):
        # 使用data URL scheme将HTML内容嵌入到QWebEngineView中
        base_url = QUrl("about:blank")
        self.browser.setHtml(content, base_url)


def main():
    app = QApplication(sys.argv)
    browser = WebBrowserApp()
    browser.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()