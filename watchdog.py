import subprocess
import time

def start_script(script_path, arguments):    # 启动脚本
    process = subprocess.Popen(["python", script_path] + arguments)
    return process

def check_process(process):    # 检查进程是否仍然运行
    return process.poll() is None

def restart_script(script_path, arguments):    # 重启脚本
    process = start_script(script_path, arguments)
    return process

def watchprocess(username, password):
    script_path = "processscript.py"
    arguments = [username,password]  # 根据你的脚本参数调整这个列表
    process = start_script(script_path, arguments)

    while True:
        if not check_process(process):
            print("Process has stopped, restarting...")
            process = restart_script(script_path, arguments)
        else:
            print("Process is running.")

        # 每隔一段时间检查一次
        time.sleep(5)
