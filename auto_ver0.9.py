# -*- encoding=utf8 -*-
__author__ = "绫地宁宁"

import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import threading
import time
from airtest.core.api import *
from PIL import Image
from airtest.core.api import device
from airtest.core.error import NoDeviceError
import os
import datetime

# --- Global Configuration and State Variables ---
ST.THRESHOLD = 0.81
REPEAT_TIMES = 10
MODE = 2
MAX_COUNT = 0
script_thread = None
script_running = False
script_paused = False
update_settings = False
root = None  # Declare root globally here
PLATFORM = "APP"  # 新增: 默认平台为APP

# Initialize Airtest
auto_setup(__file__)


def custom_resize_method(w, h, sch_resolution, src_resolution):
    global PLATFORM  # 声明使用全局变量
    try:
        dev_width, dev_height = G.DEVICE.get_current_resolution()
        rs_per_x = dev_width / 1296.0
        rs_per_y = dev_height / 759.0

        # 新增: 当平台为“浏览器”时，禁用缩放
        if PLATFORM == "浏览器":
            rs_per_x = 1.0
            rs_per_y = 1.0

        return int(rs_per_x * w), int(rs_per_y * h)
    except Exception as e:
        print(f"custom_resize_method 发生错误: {e}")
        return int(w), int(h)


ST.RESIZE_METHOD = custom_resize_method


# --- Script Control Functions ---
def start_script():
    global script_thread, script_running, script_paused
    if not script_running:
        script_running = True
        script_paused = False
        start_button.config(state="disabled")
        pause_button.config(text="暂停")
        script_thread = threading.Thread(target=run_automation_logic, daemon=True)
        script_thread.start()
        print("脚本已启动。")
    else:
        print("脚本已经在运行中。")


def toggle_pause():
    global script_paused
    if script_running:
        script_paused = not script_paused
        if script_paused:
            pause_button.config(text="恢复")
            print("脚本已暂停。")
        else:
            pause_button.config(text="暂停")
            print("脚本已恢复。")
    else:
        print("脚本未运行。")


def stop_script():
    global script_running
    if script_running:
        script_running = False
        if script_thread and script_thread.is_alive():
            script_thread.join(timeout=2)
        print("脚本已停止。")
        # Ensure GUI button states are restored after the script stops
        start_button.config(state="normal")
        pause_button.config(text="暂停")
    else:
        print("脚本未运行。")


def apply_settings():
    global REPEAT_TIMES, MODE, ST, update_settings, PLATFORM  # 声明使用全局变量
    try:
        REPEAT_TIMES = int(repeat_times_entry.get())
        MODE = int(mode_entry.get())
        ST.THRESHOLD = float(threshold_entry.get())
        PLATFORM = platform_selector.get()  # 新增: 获取用户选择的平台
        update_settings = True
        print("设置已应用。")
        print(f"当前平台设置: {PLATFORM}")
    except ValueError:
        print("无效输入. 请输入数字.")


def handle_error_and_exit(error_message):
    """
    Displays an error message box and closes the application.
    This function is called from the automation thread and uses root.after to safely
    run GUI updates on the main thread.
    """
    if root:
        root.after(0, lambda: messagebox.showerror("错误", f"脚本发生错误: {error_message}\n日志已生成。"))
        root.after(100, lambda: root.destroy())


# --- Core Automation Logic (runs in a separate thread) ---
def run_automation_logic():
    global REPEAT_TIMES, MODE, ST, MAX_COUNT, script_running, script_paused, update_settings, PLATFORM

    # Create report folder and log directory
    report_folder = f"report_{datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}"
    os.makedirs(report_folder, exist_ok=True)
    logdir = os.path.join(report_folder, "log")

    # Set log directory for this run
    auto_setup(__file__, logdir=logdir)

    try:
        # Connect to device
        try:
            if PLATFORM == "浏览器":
                connect_device("Windows:///?title_re=マブラヴ")
                print("已连接到 Windows 窗口。")
            else:
                dev = device()
                print("已成功连接到设备。")
        except NoDeviceError:
            connect_device("Windows:///?title_re=マブラヴ")
            print("已连接到 Windows 窗口。")
        except Exception as e:
            print(f"发生其他错误: {e}")
            raise  # Re-raise the exception to trigger logging

        # Get window resolution
        screenshot = G.DEVICE.snapshot(quality=100)
        image = Image.fromarray(screenshot)
        width, height = image.size
        std_maker=exists(Template(r"tpl/tpl1757222743287.png", record_pos=(-0.338, -0.267), resolution=(1296, 759)))
        std_x=std_maker[0]
        std_y=std_maker[1]
        print("标致坐标为：",std_x,std_y)
        TOUCH_PLACE_X = width / 2
        TOUCH_PLACE_Y = height / 2
        if PLATFORM=="浏览器":
            TOUCH_PLACE_X=std_x+600
            TOUCH_PLACE_Y=std_y+600
        print("分辨率大小为：", width, height)

        # Main script loop
        while script_running:
            # Check for pause
            while script_paused and script_running:
                time.sleep(10)

            if not script_running:
                break

            # Check for and apply settings at the start of each major loop
            if update_settings:
                update_settings = False
                print("新设置已生效。")

            # --- Your script logic, all 'tpl' paths should be 'tpl/...' ---
            wait(Template(r"tpl/tpl1757222743287.png", record_pos=(-0.338, -0.267), resolution=(1296, 759)), timeout=5)
            touch(Template(r"tpl/tpl1757222863184.png", record_pos=(0.4, 0.181), resolution=(1296, 759)))
            sleep(0.5)
            wait(Template(r"tpl/tpl1757222876809.png", record_pos=(-0.344, -0.266), resolution=(1296, 759)), timeout=5)
            touch(Template(r"tpl/tpl1757222884524.png", record_pos=(0.41, 0.25), resolution=(1296, 759)))
            sleep(0.5)

            for i in range(1, REPEAT_TIMES):
                if MODE == 2:
                    sleep(0.5)
                    wait(Template(r"tpl/tpl1757228998112.png", record_pos=(0.437, -0.24), resolution=(1296, 759)))
                    touch(Template(r"tpl/tpl1757228998112.png", record_pos=(0.437, -0.24), resolution=(1296, 759)))
                    sleep(0.5)
                    wait(Template(r"tpl/tpl1757222933943.png", record_pos=(-0.23, 0.241), resolution=(1296, 759)),
                         timeout=10)
                elif MODE == 1:
                    wait(Template(r"tpl/tpl1757222933943.png", record_pos=(-0.23, 0.241), resolution=(1296, 759)),
                         timeout=120)
                wait(Template(r"tpl/tpl1757222942013.png", record_pos=(0.402, 0.242), resolution=(1296, 759)))
                touch(Template(r"tpl/tpl1757222942013.png", record_pos=(0.402, 0.242), resolution=(1296, 759)))
                sleep(0.5)
                wait(Template(r"tpl/tpl1757222961056.png", record_pos=(0.16, 0.227), resolution=(1296, 759)), timeout=5)
                touch((TOUCH_PLACE_X, TOUCH_PLACE_Y))
                sleep(2)
                if exists(Template(r"tpl/tpl1757229374406.png", record_pos=(0.409, 0.233), resolution=(1296, 759))):
                    touch(Template(r"tpl/tpl1757223305441.png", record_pos=(0.41, 0.234), resolution=(1296, 759)))
                    sleep(0.5)
                elif exists(Template(r"tpl/tpl1757224227568.png", record_pos=(-0.404, 0.135), resolution=(1296, 759))):
                    wait(Template(r"tpl/tpl1757224242520.png", record_pos=(0.398, 0.254), resolution=(1296, 759)),
                         timeout=5)
                    touch(Template(r"tpl/tpl1757224269069.png", record_pos=(0.399, 0.254), resolution=(1296, 759)))
                    sleep(0.5)
                    if exists(Template(r"tpl/tpl1757229374406.png", record_pos=(0.409, 0.233), resolution=(1296, 759))):
                        wait(Template(r"tpl/tpl1757223305441.png", record_pos=(0.41, 0.234), resolution=(1296, 759)),
                             timeout=5)
                        touch(Template(r"tpl/tpl1757223305441.png", record_pos=(0.41, 0.234), resolution=(1296, 759)))
                if exists(Template(r"tpl/tpl1757224532561.png", record_pos=(-0.378, -0.025), resolution=(1296, 759))):
                    wait(Template(r"tpl/tpl1757224242520.png", record_pos=(0.398, 0.254), resolution=(1296, 759)),
                         timeout=5)
                    touch(Template(r"tpl/tpl1757224269069.png", record_pos=(0.399, 0.254), resolution=(1296, 759)))
                    sleep(0.5)
                    if exists(Template(r"tpl/tpl1757229374406.png", record_pos=(0.409, 0.233), resolution=(1296, 759))):
                        wait(Template(r"tpl/tpl1757223305441.png", record_pos=(0.41, 0.234), resolution=(1296, 759)),
                             timeout=5)
                        touch(Template(r"tpl/tpl1757223305441.png", record_pos=(0.41, 0.234), resolution=(1296, 759)))
            if MODE == 2:
                sleep(0.5)
                wait(Template(r"tpl/tpl1757228998112.png", record_pos=(0.437, -0.24), resolution=(1296, 759)))
                touch(Template(r"tpl/tpl1757228998112.png", record_pos=(0.437, -0.24), resolution=(1296, 759)))
                sleep(0.5)
                wait(Template(r"tpl/tpl1757222933943.png", record_pos=(-0.23, 0.241), resolution=(1296, 759)),
                     timeout=10)
            elif MODE == 1:
                wait(Template(r"tpl/tpl1757222933943.png", record_pos=(-0.23, 0.241), resolution=(1296, 759)),
                     timeout=120)
            wait(Template(r"tpl/tpl1757222942013.png", record_pos=(0.402, 0.242), resolution=(1296, 759)))
            touch(Template(r"tpl/tpl1757222942013.png", record_pos=(0.402, 0.242), resolution=(1296, 759)))
            sleep(0.5)
            wait(Template(r"tpl/tpl1757224892007.png", record_pos=(-0.395, -0.17), resolution=(1296, 759)), timeout=5)
            touch(Template(r"tpl/tpl1757231260597.png", record_pos=(0.397, 0.247), resolution=(1296, 759)))
            sleep(0.5)
            wait(Template(r"tpl/tpl1757224970612.png", record_pos=(-0.327, -0.256), resolution=(1296, 759)))
            touch(Template(r"tpl/tpl1757224998053.png", record_pos=(-0.436, -0.034), resolution=(1296, 759)))
            sleep(0.5)
            SECTION_RECORDER = 1
            while True:
                if exists(Template(r"tpl/tpl1757225058518.png", record_pos=(-0.035, -0.006), resolution=(1296, 759))):
                    touch(Template(r"tpl/tpl1757225058518.png", record_pos=(-0.035, -0.006), resolution=(1296, 759)))
                    continue
                elif exists(Template(r"tpl/tpl1757229090368.png", record_pos=(-0.035, -0.11), resolution=(1296, 759))):
                    touch(Template(r"tpl/tpl1757229090368.png", record_pos=(-0.035, -0.11), resolution=(1296, 759)))
                    sleep(0.5)
                    continue
                elif exists(Template(r"tpl/tpl1757225140378.png", record_pos=(-0.036, 0.007), resolution=(1296, 759))):
                    break
                elif SECTION_RECORDER == 1:
                    touch(Template(r"tpl/tpl1757225424358.png", record_pos=(-0.188, -0.185), resolution=(1296, 759)))
                    sleep(0.5)
                    SECTION_RECORDER = 2
                    MAX_COUNT = 1
                    continue
                elif SECTION_RECORDER == 2:
                    touch(Template(r"tpl/tpl1757225626392.png", record_pos=(-0.068, -0.184), resolution=(1296, 759)))
                    sleep(0.5)
                    SECTION_RECORDER = 3
                    MAX_COUNT = 2
                    continue
                elif SECTION_RECORDER == 3:
                    touch(Template(r"tpl/tpl1757225658002.png", record_pos=(-0.435, 0.1), resolution=(1296, 759)))
                    sleep(0.5)
                    SECTION_RECORDER = 4
                    MAX_COUNT = 3
                    continue
                elif SECTION_RECORDER == 4:
                    touch(Template(r"tpl/tpl1757225716944.png", record_pos=(-0.188, -0.184), resolution=(1296, 759)))
                    sleep(0.5)
                    SECTION_RECORDER = 5
                    MAX_COUNT = 4
                    continue
                elif SECTION_RECORDER == 5:
                    touch(Template(r"tpl/tpl1757225754121.png", record_pos=(-0.307, -0.184), resolution=(1296, 759)))
                    sleep(0.5)
                    SECTION_RECORDER = 6
                    MAX_COUNT = 5
                    continue
                elif SECTION_RECORDER == 6:
                    MAX_COUNT = 6
                    break
            if MAX_COUNT != 6:
                touch(Template(r"tpl/tpl1757225830519.png", record_pos=(0.407, 0.237), resolution=(1296, 759)))
                sleep(0.5)
            elif MAX_COUNT == 6:
                break
    except Exception as e:
        log("脚本运行时发生错误: " + str(e))
        print("脚本已停止。")
        handle_error_and_exit(str(e))
    finally:
        # Ensure GUI button states are restored after the script stops
        if root and root.winfo_exists():
            root.after(0, lambda: start_button.config(state="normal"))
            root.after(0, lambda: pause_button.config(text="暂停"))


# --- Main Program Entry Point ---
if __name__ == '__main__':
    # Initialize the GUI
    root = tk.Tk()
    root.title("Airtest Script Control")

    mainframe = ttk.Frame(root, padding="20 20 20 20")
    mainframe.grid(column=0, row=0, sticky=(tk.W, tk.E, tk.N, tk.S))
    root.columnconfigure(0, weight=1)
    root.rowconfigure(0, weight=1)

    # Repeat Times
    ttk.Label(mainframe, text="重复次数 (REPEAT_TIMES):").grid(column=1, row=1, sticky=tk.W)
    repeat_times_entry = ttk.Entry(mainframe, width=7)
    repeat_times_entry.grid(column=2, row=1, sticky=(tk.W, tk.E))
    repeat_times_entry.insert(0, "10")
    # Apply settings button
    apply_button = ttk.Button(mainframe, text="应用设置", command=lambda: apply_settings())
    apply_button.grid(column=3, row=1, sticky=tk.E)

    # Mode
    ttk.Label(mainframe, text="模式 (MODE, 1=推图, 2=扫荡):").grid(column=1, row=2, sticky=tk.W)
    mode_entry = ttk.Entry(mainframe, width=7)
    mode_entry.grid(column=2, row=2, sticky=(tk.W, tk.E))
    mode_entry.insert(0, "2")

    # Threshold
    ttk.Label(mainframe, text="置信度 (ST.THRESHOLD):").grid(column=1, row=3, sticky=tk.W)
    threshold_entry = ttk.Entry(mainframe, width=7)
    threshold_entry.grid(column=2, row=3, sticky=(tk.W, tk.E))
    threshold_entry.insert(0, "0.87")

    # Platform Selector
    ttk.Label(mainframe, text="平台选择:").grid(column=1, row=4, sticky=tk.W)
    platform_selector = ttk.Combobox(mainframe, width=15, state="readonly")
    platform_selector['values'] = ("APP", "浏览器")
    platform_selector.current(0)  # Set default to "APP"
    platform_selector.grid(column=2, row=4, sticky=(tk.W, tk.E))

    # Start, Pause, Stop buttons
    start_button = ttk.Button(mainframe, text="开始脚本", command=lambda: start_script())
    start_button.grid(column=1, row=5, sticky=tk.W)

    pause_button = ttk.Button(mainframe, text="暂停", command=lambda: toggle_pause())
    pause_button.grid(column=2, row=5, sticky=tk.W)

    stop_button = ttk.Button(mainframe, text="停止", command=lambda: stop_script())
    stop_button.grid(column=3, row=5, sticky=tk.W)

    for child in mainframe.winfo_children():
        child.grid_configure(padx=5, pady=5)

    root.mainloop()