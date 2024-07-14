from selenium import webdriver
from selenium.webdriver.edge.service import Service
from selenium.webdriver.edge.options import Options
from selenium.webdriver.common.by import By
import time
import os
import argparse
from functools import wraps 
import builtins
import logging

# 重定义print函数使其写入日志
original_print = builtins.print
def new_print(*args, **kwargs):
    # 调用原始的print函数，同时记录日志
    original_print(*args, **kwargs)
    logging.info(" ".join(str(arg) for arg in args))
# 替换内置的print函数
builtins.print = new_print

def islogin(func):
    @wraps(func)
    def wrapper(self, *args, **kwargs):
        # 检查是否已登录
        self.driver.get('https://tsbt.chinamde.cn/')
        self.wait(2)
        loginelement = self.driver.find_elements(By.XPATH, '//*[@id="zz-index-2022"]/div/div[2]/div/div[2]/a[2]')
        if loginelement[0].get_attribute('class') == 'name':
            print('已登录')
            self.wait(2)
            return func(self, *args, **kwargs)
        else:
            print('未登录，跳转至登录页面')
            self.login()
            self.wait(2)
            return func(self, *args, **kwargs)
    return wrapper

class CoursePlayer:
    def __init__(self, user_data_dir, driver_path, username, password):
        self.user_data_dir = user_data_dir
        self.driver_path = driver_path
        self.username = username
        self.password = password
        self.driver = self.initialize_driver()

    def initialize_driver(self):
        options = Options()
        options.use_chromium = True
        options.add_argument(f"user-data-dir={self.user_data_dir}")

        service = Service(self.driver_path)
        driver = webdriver.Edge(service=service, options=options)
        return driver

    def play_video(self, elements):
        for element in elements:
            percent_span = element.find_element(By.CLASS_NAME, 'class_percent')
            chapteritem_cont = element.find_element(By.CLASS_NAME, 'chapteritem_cont')
            self.current_video_name = chapteritem_cont.text
            print(percent_span.text + self.current_video_name)
            if percent_span.text != '100%':
                link = element.find_element(By.TAG_NAME, 'a')
                self.driver.execute_script("arguments[0].click();", link)
                self.wait(2)
                self.handle_video_playback()
                return 

    #判断播放器有无iframe标签
    def handle_video_playback(self):
        iframes = self.driver.find_elements(By.TAG_NAME, 'iframe')
        if iframes:
            self.driver.switch_to.frame(iframes[0])  # 切换到iframe
            self.play_or_resume_iframe_video()
            self.driver.switch_to.default_content()  # 切换回默认内容
        else:
            self.play_or_resume_inline_video()

    def play_or_resume_iframe_video(self):
        # 尝试点击播放按钮，如果失败则点击重播按钮
        try:
            play_button = self.driver.find_element(By.XPATH, '//*[@id="playbtn"]')
            play_button.click()
        except:
            replay_button = self.driver.find_element(By.XPATH, '//*[@id="replaybtn"]')
            replay_button.click()
        video = self.driver.find_element(By.TAG_NAME, 'video')
        self.monitor_video_status(video, True)

    def play_or_resume_inline_video(self):
        video = self.driver.find_element(By.TAG_NAME, 'video')
        play_button = self.driver.find_element(By.XPATH, '//*[@id="player"]/div/div/div[7]')
        play_button.click()
        self.monitor_video_status(video, False)

    def monitor_video_status(self, video, iframes):
        playstat = True
        while playstat:
            duration = float(video.get_attribute('duration'))
            ended = video.get_attribute('ended') == 'true'
            paused = video.get_attribute('paused') == 'true'
            current_time = float(video.get_attribute('currentTime'))

            print()
            print(f"正在播放视频: {self.current_video_name}")
            print(f"当前时间: {current_time}")
            print(f"视频总时长: {duration}")
            print(f"视频是否播放结束: {ended}")
            print(f"视频是否暂停: {paused}")
            print()

            if ended or current_time >= duration:
                playstat = False
            elif paused:
                self.resume_video(iframes)

            self.wait(1)



    def resume_video(self, iframes):
        self.handle_video_playback()

    def get_course_list(self):
        course_list = self.driver.find_elements(By.CLASS_NAME, 'kechenglb')
        if not course_list:
            print("没有课程，程序退出")
            return False
        else:
            print("还有课程，开始刷课")
            course_list[0].click()
            return True

    def get_list(self):
        li = self.driver.find_element(By.XPATH, '/html/body/div[5]/div/div[2]/div[2]')
        charptli = li.find_elements(By.CLASS_NAME, 'chapter-li')
        for chapter in charptli:
            self.driver.execute_script("arguments[0].className = 'chapter-li active';", chapter)

        elements = li.find_elements(By.CLASS_NAME, 'nor')
        print('获得课程目录')
        self.play_video(elements)

    def wait(self, seconds):
        time.sleep(seconds)

    @islogin
    def run(self):
        while True:
            self.driver.get('https://tsbt.chinamde.cn/p_mycourse.html')
            self.wait(2)
            if not self.get_course_list():
                break
            self.wait(2)
            self.get_list()
            self.get_list()  #保证第一个视频也能检测是否100%

        self.wait(5)
        self.driver.quit()

    def login(self):
        self.driver.get('https://tsbt.chinamde.cn/login.html')
        self.wait(2)
        self.driver.find_elements(By.XPATH, '//*[@id="zz-index"]/div[2]/div/section/div/div/div[2]/div[1]/div[5]/input')
        self.driver.find_element(By.ID, 'name').send_keys(self.username)
        self.driver.find_element(By.ID, 'password').send_keys(self.password)
        self.driver.find_element(By.XPATH, '//*[@id="zz-index"]/div[2]/div/section/div/div/div[2]/div[1]/div[5]/input').click()
        return 

def runscript(username, password):
    # 定义目录和驱动路径
    user_directory_name = 'user'
    webdriver_file_name = 'msedgedriver.exe'
    webdriver_dir_name = 'webdrive'

    # 获取当前工作目录
    current_working_directory = os.getcwd()

    # 构建完整的webdriver路径
    webdriver_path = os.path.join(current_working_directory, webdriver_dir_name, webdriver_file_name)

    # 构建用户数据目录
    user_data_directory = os.path.join(current_working_directory, user_directory_name, username)

    # 创建课程播放器实例并运行
    course_player = CoursePlayer(user_data_directory, webdriver_path, username, password)
    course_player.run()



if __name__ == "__main__":
    # 设置命令行参数解析器
    parser = argparse.ArgumentParser(description="课程播放器自动化脚本")
    parser.add_argument("username", help="登录账号")
    parser.add_argument("password", help="登录密码")
    args = parser.parse_args()

    # 创建课程播放器实例并运行
    runscript(args.username, args.password)
    
    