import pandas as pd
import datetime
import os
import json
import tkinter as tk
from tkinter import messagebox
from ttkbootstrap import *
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import warnings
import seaborn as sns
from PIL import Image, ImageTk
from datetime import datetime
from ttkbootstrap import Style
import random
from datetime import timedelta

warnings.filterwarnings("ignore")

# ----------------------- 颜色相关函数(全局) ----------------------- #
def get_theme_colors():
    # 根据主题选择颜色列表
    if style_keyword == 'minty':
        colors = ["#007AFF", "#34C759", "#FF9500", "#AF52DE", "#FF2D55"]
    elif style_keyword == 'darkly':
        colors = ["#00FFFF", "#FF00FF", "#FFD700", "#FF4500", "#ADFF2F"]
    else:
        colors = ["#FFFFFF", "#CCCCCC", "#AAAAAA"]
    return colors
# ----------------------- 数据相关函数 ----------------------- #
def get_record_days(data):
    # 以年月日组合去重记录天数
    return len(np.unique(["-".join([str(data["year"][i]), str(data["month"][i]), str(data["day"][i])])
                            for i in range(len(data))]))

def create_data(file_name):
    # 创建 UNSWow 数据记录 CSV 模板
    columns = [
        "year", "month", "day", "hour", "minute",
        "WH (Hours)", "SH (Hours)", "EH (Hours)",
        "HS: Shower(+60)", "HS: Toothbrush(+20)", "HS: Tidy Room(+5)",
        "HS: Laundry(+10)", "HS: Late Night(-50)", "HS: Junk Food(-30)",
        "HS (Total)", "CT (0-100)", "Final Score"
    ]
    result = pd.DataFrame({col: [] for col in columns})
    result.to_csv(file_name, index=False)

def add_record_to_data(file_name, new_record):
    # 读取、追加新纪录，再保存
    data = pd.read_csv(file_name)
    data = data.append(new_record, ignore_index=True)
    data.to_csv(file_name, index=False)

def remove_last_row(file_name):
    data = pd.read_csv(file_name)
    if len(data) == 0:
        return data
    data = data.drop(data.index[-1])
    data.to_csv(file_name, index=False)

# 显示消息对话框
def show_message(message):
    messagebox.showinfo("Message", message)

def confirm_remove():
    data = pd.read_csv(file_name)
    if len(data)==0:
        show_message("No records to remove.")
        return
    last_year = str(data["year"].iloc[-1])
    last_month = str(data["month"].iloc[-1])
    last_day = str(data["day"].iloc[-1])
    last_hour = str(data["hour"].iloc[-1])
    last_minute = str(data["minute"].iloc[-1])
    output_date = " ".join(["-".join([last_year, last_month, last_day]),
                            ":".join([last_hour, last_minute])])
    answer = messagebox.askyesno("Confirm Remove",
                                 "Are you sure you want to remove the last row?\n(Date: "+output_date+")")
    if answer:
        remove_last_row(file_name)
        show_message("Last row removed successfully.")

def backup():
    answer = messagebox.askyesno("Confirm Backup", "Are you sure you want to make backup?")
    if answer:
        data = pd.read_csv(file_name)
        backup_name = "backup_" + file_name
        data.to_csv(backup_name, index=False)
        show_message("Backup Complete")

def animate_text():
    # 从文件中读取所有激励语句
    try:
        with open("motivations.txt", "r", encoding="utf-8") as f:
            motivational_lines = [line.strip() for line in f if line.strip()]
    except FileNotFoundError:
        motivational_lines = ["Stay Consistent", "Keep Moving Forward"]  # 备用

    # 随机选择字体大小、颜色和文本内容
    new_size = random.choice([16, 18, 20, 22])
    colors=get_theme_colors()
    new_color = random.choice(colors)
    new_text = random.choice(motivational_lines)

    # 更新 Canvas 上的文字样式和内容
    text_canvas.itemconfig(
        text_item,
        font=("Helvetica", new_size, "bold"),
        fill=new_color,
        text=new_text
    )

    # 递归调用形成动画效果
    root.after(1000, animate_text)  # 每 1 秒更新一次

# ----------------------- 评分计算函数 ----------------------- #
def compute_final_score(WH, SH, EH, hs_raw, CT):
    # 将 WH/SH/EH 标准化到 100 分
    WH_score = min(WH / 5, 1) * 100
    SH_score = min(SH / 5, 1) * 100
    EH_score = min(EH / 1.5, 1) * 100
    # 限制健康总分在 0～100
    HS_score = max(min(hs_raw, 100), 0)
    final_score = 0.15 * WH_score + 0.25 * SH_score + 0.15 * EH_score + 0.10 * HS_score + 0.35 * CT
    return round(WH_score,2), round(SH_score,2), round(EH_score,2), round(HS_score,2), round(final_score,2)

# ----------------------- GUI部分 ----------------------- #
file_name = "records.csv"
if not os.path.exists(file_name):
    create_data(file_name)
data = pd.read_csv(file_name)

root = tk.Tk()
now = datetime.now()
style_keyword = 'minty'
root.iconphoto(True, tk.PhotoImage(file='UNSWow.jpg'))
root.title("UNSWow! v1.0.3")
width = 750
height = 620
root.geometry(f"{width}x{height}")
root.resizable(False, False)
style = Style(theme=style_keyword)
sns.set_style('darkgrid')

# 底部进度条等
flood = Floodgauge(root)
flood.start()
flood.pack(fill="x")

# 设置背景图片和标题
if 5 <= now.hour <= 17:
    style_keyword = 'minty'
    image = Image.open("background_day.jpg")
else:
    style_keyword = 'darkly'
    image = Image.open("background_night.jpg")
style = Style(theme=style_keyword)

image = image.convert('RGBA')
photo = ImageTk.PhotoImage(image)
canvas = Canvas(root, width=950, height=30, bg='SystemTransparent')
canvas.pack(side=tk.BOTTOM)
canvas.create_image(0, 0, anchor=tk.NW, image=photo)

title = Label(root, text="UNSWow!", font=('Helvetica', 60))
title.pack(pady=20)

text_canvas = Canvas(root, width=width, height=30, bg='SystemTransparent', bd=0)
text_canvas.pack()  # 直接添加到主窗口中

# 在新的Canvas中创建动画文本
text_item = text_canvas.create_text(
    width//2, 15,  # 垂直居中于新的Canvas
    text=random.choice(["Stay Consistent", "Keep Moving Forward"]),
    font=("Helvetica", 0, "bold"),
    fill="white"
)

# 启动动画
animate_text()

# ----------------------- 输入记录界面 ----------------------- #
def show_input_fields():
    input_window = tk.Toplevel(root)
    input_window.geometry("550x500")
    input_window.title("Add UNSWow Record")

    # 每日各项指标输入
    label_WH = Label(input_window, text="Enter WH (Working Hours, max 5H):")
    label_WH.pack()
    entry_WH = Entry(input_window, width=40)
    entry_WH.pack(pady=5)

    label_SH = Label(input_window, text="Enter SH (Study Hours, max 5H):")
    label_SH.pack()
    entry_SH = Entry(input_window, width=40)
    entry_SH.pack(pady=5)

    label_EH = Label(input_window, text="Enter EH (Exercise Hours, max 1.5H):")
    label_EH.pack()
    entry_EH = Entry(input_window, width=40)
    entry_EH.pack(pady=5)

    label_CT = Label(input_window, text="Enter CT (Completed Tasks, self-evaluate, in score 0-100):")
    label_CT.pack()
    entry_CT = Entry(input_window, width=40)
    entry_CT.pack(pady=5)
    Label(input_window, text="HS(Health Score):").pack()
    # 健康子项：使用复选框表示是否完成/发生
    check_vars = {}
    health_items = [
        ("HS: Shower(+60)", 60),
        ("HS: Toothbrush(+20)", 20),
        ("HS: Tidy Room(+5)", 5),
        ("HS: Laundry(+10)", 10),
        ("HS: Late Night(-50)", -50),
        ("HS: Junk Food(-30)", -30)
    ]
    for item, score in health_items:
        var = IntVar()
        # 默认选中表示完成，对于扣分项（Late Night, Junk Food）默认为不选
        if score > 0:
            var.set(0)  # 初始不完成
        else:
            var.set(0)
        chk = Checkbutton(input_window, text=item, variable=var)
        chk.pack(anchor='w',padx=70, pady=3)
        check_vars[item] = var

    # 添加复选框：是否为昨天补记
    record_yesterday_var = IntVar()
    record_yesterday_check = Checkbutton(input_window, text="Record for Yesterday?", variable=record_yesterday_var)
    record_yesterday_check.pack(pady=5)

    def record_action():
        try:
            WH = float(entry_WH.get())
            SH = float(entry_SH.get())
            EH = float(entry_EH.get())
            CT = float(entry_CT.get())

            # 计算 HS 各项得分
            hs_raw = 0
            for item, score in health_items:
                if check_vars[item].get() == 1:
                    hs_raw += score
            # 限定健康分在 0~100
            hs_total = max(min(hs_raw, 100), 0)

            # 判断是否补记录
            now_time = datetime.now()
            if record_yesterday_var.get() == 1:
                now_time -= timedelta(days=1)

            # 计算标准化分数及Final Score
            WH_score, SH_score, EH_score, HS_score, final_score = compute_final_score(WH, SH, EH, hs_total, CT)

            # 生成记录字典
            new_record = {
                "year": now_time.year,
                "month": now_time.month,
                "day": now_time.day,
                "hour": now_time.hour,
                "minute": now_time.minute,
                "WH (Hours)": WH,
                "SH (Hours)": SH,
                "EH (Hours)": EH,
                "HS: Shower(+60)": "T" if check_vars["HS: Shower(+60)"].get()==1 else "F",
                "HS: Toothbrush(+20)": "T" if check_vars["HS: Toothbrush(+20)"].get()==1 else "F",
                "HS: Tidy Room(+5)": "T" if check_vars["HS: Tidy Room(+5)"].get()==1 else "F",
                "HS: Laundry(+10)": "T" if check_vars["HS: Laundry(+10)"].get()==1 else "F",
                "HS: Late Night(-50)": "T" if check_vars["HS: Late Night(-50)"].get()==1 else "F",
                "HS: Junk Food(-30)": "T" if check_vars["HS: Junk Food(-30)"].get()==1 else "F",
                "HS (Total)": hs_total,
                "CT (0-100)": CT,
                "Final Score": final_score
            }

            add_record_to_data(file_name, new_record)
            show_message(f"Record added successfully! Your score for today is {final_score:.2f}")
            input_window.destroy()
        except ValueError:
            show_message("Invalid input. Please enter valid numbers.")


    record_button = Button(input_window, text="Record", bootstyle="outline", command=record_action)
    record_button.pack(pady=10)

def show_chart(data):
    if len(list(data.iloc())) == 0:
        show_message("No data recorded.")
        return

    data = pd.read_csv(file_name)
    input_window = tk.Toplevel(root)
    input_window.geometry("800x550")  # 增加窗口尺寸
    input_window.title("UNSWow Chart")

    # 顶部标题
    label_info = tk.Label(input_window, text="UNSWow Metrics Trend", font=('Helvetica', 30))
    label_info.pack(pady=2)

    # 下拉菜单区域
    control_frame = tk.Frame(input_window)
    control_frame.pack(pady=0)

    option_var = tk.StringVar(input_window)
    option_var.set("Daily")  # 默认值

    option_menu = OptionMenu(control_frame, option_var, "Daily", "Monthly", "Yearly", command=lambda _: update_chart())
    option_menu.pack()

    # 图表区域容器（用于居中）
    chart_frame = tk.Frame(input_window)
    chart_frame.pack(fill="both", expand=True)

    fig = plt.Figure(figsize=(10, 6), dpi=100)  # 增加图表尺寸
    fig.subplots_adjust(left=0.01, right=0.99, top=0.99, bottom=0.01)  # 调整布局

    ax = fig.add_subplot(111)

    canvas_fig = FigureCanvasTkAgg(fig, master=chart_frame)
    canvas_widget = canvas_fig.get_tk_widget()
    canvas_widget.pack(expand=True)  # 仅用 expand 而不设置 anchor，默认居中

    def update_chart():
        ax.clear()
        granularity = option_var.get()
        data["date"] = pd.to_datetime(data[["year", "month", "day"]])
        avg_score = data["Final Score"].mean()

        # 绘制均分水平线
        ax.axhline(y=avg_score, color='red', linestyle='--', label=f"Avg Score: {avg_score:.2f}")

        if granularity == "Daily":
            grouped = data.groupby("date")["Final Score"].mean()
            x_labels = grouped.index.strftime("%Y-%m-%d")
        elif granularity == "Monthly":
            grouped = data.resample("M", on="date")["Final Score"].mean()
            x_labels = grouped.index.strftime("%Y-%m")
        elif granularity == "Yearly":
            grouped = data.resample("Y", on="date")["Final Score"].mean()
            x_labels = grouped.index.strftime("%Y")
        else:
            return

        ax.plot(x_labels, grouped.values, marker='o', label="Final Score")
        ax.set_xlabel("Time")
        ax.set_ylabel("Score")
        ax.set_title(f"Final Score Trend ({granularity})")
        ax.legend()
        ax.tick_params(axis='x', rotation=30)
        fig.subplots_adjust(bottom=0.25)  # 再次设置防止刷新时失效
        canvas_fig.draw()

    update_chart()

# ----------------------- 记录过滤功能 ----------------------- #
def get_unique_dates(data):
    years = sorted(data["year"].unique())
    months = sorted(data["month"].unique())
    days = sorted(data["day"].unique())
    return years, months, days

def filter_records(data):
    if len(list(data.iloc())) == 0:
        show_message("No data recorded.")
        return
    data = pd.read_csv(file_name)
    years, months, days = get_unique_dates(data)

    filter_window = tk.Toplevel(root)
    filter_window.title("Filter Records")

    year_var = tk.StringVar(value="None")
    month_var = tk.StringVar(value="None")
    day_var = tk.StringVar(value="None")

    # 过滤条件选择框
    options_frame = tk.Frame(filter_window)
    options_frame.pack(pady=10, fill='x')

    tk.Label(options_frame, text="Select Year:").pack(side='left', padx=5)
    year_menu = tk.OptionMenu(options_frame, year_var, "None", *years)
    year_menu.config(foreground="black")
    year_menu.pack(side='left')

    tk.Label(options_frame, text="Month:").pack(side='left', padx=5)
    month_menu = tk.OptionMenu(options_frame, month_var, "None", *months)
    month_menu.config(foreground="black")
    month_menu.pack(side='left')

    tk.Label(options_frame, text="Day:").pack(side='left', padx=5)
    day_menu = tk.OptionMenu(options_frame, day_var, "None", *days)
    day_menu.config(foreground="black")
    day_menu.pack(side='left')

    # "Show Records" 按钮
    filter_button = Button(filter_window, text="Show Records",
                           command=lambda: show_filtered_records(data, tree, year_var.get(), month_var.get(), day_var.get()))
    filter_button.pack()

    # "Remove Last Row" 按钮
    remove_button = Button(filter_window, text="Remove Last Row", bootstyle="outline", command=confirm_remove)
    remove_button.pack(pady=10)

    # 记录显示区域
    records_frame = tk.Frame(filter_window)
    records_frame.pack(expand=True, fill='both')

    tree = tk.ttk.Treeview(records_frame, columns=('Hour', 'Minute', 'WH', 'SH', 'EH', 'HS_Total', 'CT', 'Final Score'),
                           show='headings')
    tree.heading('Hour', text='Hour')
    tree.heading('Minute', text='Minute')
    tree.heading('WH', text='WH (H)')
    tree.heading('SH', text='SH (H)')
    tree.heading('EH', text='EH (H)')
    tree.heading('HS_Total', text='HS (Total)')
    tree.heading('CT', text='CT')
    tree.heading('Final Score', text='Final Score')

    tree.column('Hour', width=50)
    tree.column('Minute', width=50)
    tree.column('WH', width=80)
    tree.column('SH', width=80)
    tree.column('EH', width=80)
    tree.column('HS_Total', width=80)
    tree.column('CT', width=80)
    tree.column('Final Score', width=100)

    tree.pack(expand=True, fill='both')

    scrollbar = tk.Scrollbar(records_frame, orient='vertical', command=tree.yview)
    tree.configure(yscroll=scrollbar.set)
    scrollbar.pack(side='right', fill='y')

def show_filtered_records(data, tree, year, month, day):
    # 构造布尔掩码
    condition = pd.Series([True] * len(data))
    if year != "None":
        condition &= data['year'] == int(year)
    if month != "None":
        condition &= data['month'] == int(month)
    if day != "None":
        condition &= data['day'] == int(day)

    filtered_data = data[condition]

    if filtered_data.empty:
        show_message("No records match the selected criteria.")
        return

    # 清空树形视图并插入结果
    tree.delete(*tree.get_children())
    for index, row in filtered_data.iterrows():
        tree.insert('', 'end',
                    values=(row['hour'], row['minute'], row['WH (Hours)'], row['SH (Hours)'],
                            row['EH (Hours)'], row['HS (Total)'], row['CT (0-100)'], row['Final Score']))


def show_filtered_records(data, tree, year, month, day):
    # 构造布尔掩码
    condition = pd.Series([True] * len(data))
    if year != "None":
        condition &= data['year'] == int(year)
    if month != "None":
        condition &= data['month'] == int(month)
    if day != "None":
        condition &= data['day'] == int(day)

    filtered_data = data[condition]

    if filtered_data.empty:
        show_message("No records match the selected criteria.")
        return

    # 清空树形视图并插入结果
    tree.delete(*tree.get_children())
    for index, row in filtered_data.iterrows():
        tree.insert('', 'end',
                    values=(row['hour'], row['minute'], row['WH (Hours)'], row['SH (Hours)'],
                            row['EH (Hours)'], row['HS (Total)'], row['CT (0-100)'], row['Final Score']))

# ----------------------- 查看成绩的子界面 ----------------------- #
def show_scores(data):
    input_window = tk.Toplevel(root)
    input_window.geometry("500x730")  # 增加高度以便容纳环状图
    input_window.title("Your Scores")
    score_size = 20
    score_title_size = 28

    # 顶部标题
    label_info = Label(input_window, text="Your UNSWow Scores", font=('Helvetica', score_title_size, "bold"))
    label_info.pack(pady=10)

    # 计算成绩数据
    today = datetime.now().date()
    data["date"] = pd.to_datetime(data[["year", "month", "day"]]).dt.date  # 转换为日期格式

    # 坚持总天数
    total_days = len(data["date"].unique())

    # 总平均成绩
    total_avg_score = data["Final Score"].mean()

    # 最近一周平均成绩
    one_week_ago = today - timedelta(days=7)
    recent_week_data = data[data["date"] >= one_week_ago]
    weekly_avg_score = recent_week_data["Final Score"].mean() if len(recent_week_data) > 0 else 0

    # 当天成绩
    today_data = data[data["date"] == today]
    today_score = today_data["Final Score"].values[0] if len(today_data) > 0 else 0

    score_pad=1
    # 显示成绩信息
    label_total_days = Label(input_window, text=f"Total Days of Consistency: {total_days}", font=('Helvetica', score_size))
    label_total_days.pack(pady=score_pad)

    label_total_avg = Label(input_window, text=f"Total Average Score: {total_avg_score:.2f}", font=('Helvetica', score_size))
    label_total_avg.pack(pady=score_pad)

    label_weekly_avg = Label(input_window, text=f"Average Score in Last Week: {weekly_avg_score:.2f}", font=('Helvetica', score_size))
    label_weekly_avg.pack(pady=score_pad)

    label_today_score = Label(input_window, text=f"Today's Score: {today_score:.2f}", font=('Helvetica', score_size))
    label_today_score.pack(pady=score_pad)

    Label(input_window, text="-"*50, font=('Helvetica', score_size)).pack()

    # 绘制环状图
    # 每个维度的总和
    total_WH = data["WH (Hours)"].sum()
    total_SH = data["SH (Hours)"].sum()
    total_EH = data["EH (Hours)"].sum()
    total_CT = data["CT (0-100)"].sum()
    total_HS = data["HS (Total)"].sum()

    # 数据为每个维度的总和
    categories = ['WH', 'SH', 'EH', 'CT', 'HS']
    values = np.asarray([total_WH, total_SH, total_EH, total_CT, total_HS])

    # 绘制环状图
    fig, ax = plt.subplots(figsize=(2.5, 2.5))

    fig.patch.set_facecolor('none')  # 设置整个图形背景为透明
    ax.patch.set_facecolor('none')   # 设置子图背景为透明

    wedges, _ = ax.pie(values, labels=[""] * len(values), startangle=90,
                       wedgeprops=dict(width=0.45, edgecolor='w'),colors=get_theme_colors())

    # 设置图形的样式
    ax.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
    # 添加legend到图形的右边

    percent=values/np.sum(values)
    ax.legend([c+":"+str(np.round(p*100,1))+"%" for p,c in zip(percent,categories)],
              fontsize=6,
              loc='upper right')

    # 将图形嵌入Tkinter窗口
    canvas = FigureCanvasTkAgg(fig, master=input_window)
    canvas.draw()
    canvas.get_tk_widget().pack()
    Label(input_window, text="-"*50, font=('Helvetica', score_size)).pack()
    with open("evaluations.json", "r", encoding="utf-8") as f:
        evaluations = json.load(f)

    def generate_evaluation(score):
        if score == "N/A":
            return "No data today. Let’s get started!"

        if score > 85:
            return random.choice(evaluations["high_first"])
        elif score > 70:
            return random.choice(evaluations["first"])
        elif score > 60:
            return random.choice(evaluations["two_one"])
        elif score > 50:
            return random.choice(evaluations["two_two"])
        elif score > 40:
            return random.choice(evaluations["third"])
        elif score > 35:
            return random.choice(evaluations["ordinary"])
        else:
            return random.choice(evaluations["fail"])

    evaluation = generate_evaluation(today_score)
    # 显示评价文字
    Label(input_window, text="\nEvaluation:", font=("Helvetica", (score_size + score_title_size) // 2, "bold")).pack()
    Label(input_window, text=evaluation, font=("Helvetica", int(score_size*0.9)), wraplength=360, justify='left').pack(pady=(5, 0))

# ----------------------- 数理分析给出建议的部分 ----------------------- #
def analyze_track(data): # 需要传递 root
    # 创建新窗体
    analysis_window = tk.Toplevel(root)
    analysis_window.geometry("600x380")  # 调整高度以容纳描述
    analysis_window.title("Analysis - Predict Next Day")

    # 标题
    label_info = Label(analysis_window, text="Choose Mathematical Method for Prediction", font=('Helvetica', 20))
    label_info.pack(pady=10)

    methods = ["Linear Regression", "Exponential Smoothing", "Moving Average"]
    method_text = [
        "Linear Regression: Predicts future values by fitting a straight line to the data,\n suitable for data with a linear trend.",
        "Exponential Smoothing: Forecasts by assigning higher weights to recent data for smoothing,\n best for series without clear trends or seasonality.",
        "Moving Average: Predicts by averaging values over a recent window,\n useful for short-term forecasting and trend identification but lags behind trend changes."
    ]

    # 下拉菜单区域
    method_frame = Frame(analysis_window)
    method_frame.pack(pady=10)

    method_var = StringVar(analysis_window)
    method_var.set(methods[0])  # 默认选项

    option_menu = OptionMenu(method_frame, method_var, *methods)
    option_menu.pack()

    # Label to display the method description (created initially)
    description_label = Label(method_frame, text=method_text[0], justify="left")
    description_label.pack(pady=(5, 10))

    def update_description(*args):
        selected_method = method_var.get()
        try:
            index = methods.index(selected_method)
            description_label.config(text=method_text[index])
        except ValueError:
            description_label.config(text="Description not available.")

    # Trace changes to the method_var and call update_description
    method_var.trace_add("write", update_description)

    # 按钮区域
    button_frame = Frame(analysis_window)
    button_frame.pack(pady=20)

    # 执行预测的按钮
    predict_button = Button(button_frame, text="Predict", width=200, command=lambda: predict_next_day(analysis_window,data, method_var.get()))
    predict_button.pack()


def predict_next_day(analysis_window,data, method):
    for widget in analysis_window.winfo_children():
        if isinstance(widget, Label) and widget.cget("text").startswith("Predicted Score"):
            widget.destroy()  # 删除已有的预测结果标签
    # 在这里根据选择的数理方法进行预测
    if method == "Linear Regression":
        predicted_value = linear_regression(data)
    elif method == "Exponential Smoothing":
        predicted_value = exponential_smoothing(data)
    elif method == "Moving Average":
        predicted_value = moving_average(data)

    result_label = Label(analysis_window, text=f"Predicted Score for Next Day: {predicted_value:.2f}\n" \
                                                "You better exceed this number for improvement!🚀", font=('Helvetica', 18))
    result_label.pack(pady=20)

def linear_regression(data):
    x = np.arange(len(data))
    y = data['Final Score'].values  # 假设是分数
    # 简单的线性回归模型（这只是个简单示例，实际应用中可能要使用专业库，如 sklearn）
    slope, intercept = np.polyfit(x, y, 1)
    prediction = slope * (len(data)) + intercept
    return prediction

def exponential_smoothing(data):
    # 指数平滑法
    smoothing_factor = 0.1
    smoothed_values = []
    smoothed_values.append(data['Final Score'].iloc[0])
    for i in range(1, len(data)):
        smoothed_value = smoothing_factor * data['Final Score'].iloc[i] + (1 - smoothing_factor) * smoothed_values[i-1]
        smoothed_values.append(smoothed_value)
    return smoothed_values[-1]  # 返回最后一个预测值

def moving_average(data):
    #简单移动平均法（这里是3天移动平均）
    window_size = 3
    moving_avg = data['Final Score'].rolling(window=window_size).mean()
    return moving_avg.iloc[-1]  # 返回最后一个移动平均值

# ----------------------- 软件信息 ----------------------- #
def show_info():
    # 创建新的Toplevel窗体
    info_window = tk.Toplevel(root)
    info_window.title("About UNSWow")  # 设置窗体标题
    info_window.geometry("775x400")  # 设置窗体大小

    # 创建一个框架，用来放置Canvas和Scrollbar
    frame = Frame(info_window)
    frame.pack(fill="both", expand=True)

    # 创建Canvas来放置内容
    canvas = Canvas(frame)
    canvas.pack(side="left", fill="both", expand=True)

    # 创建Scrollbar
    scrollbar = tk.Scrollbar(frame, orient="vertical", command=canvas.yview)
    scrollbar.pack(side="right", fill="y")

    # 配置Canvas与Scrollbar的连接
    canvas.config(yscrollcommand=scrollbar.set)

    # 创建一个Frame来容纳所有内容，这样可以放到Canvas上进行滚动
    content_frame = Frame(canvas)
    canvas.create_window((0, 0), window=content_frame, anchor="nw")

    Label(content_frame,font=("Helvetica", 25),
          text="UNSWow - Personal Behavior Tracking System", justify="left").pack()
    # 在content_frame中添加信息
    info_message = """
    Version: v1.0.3 Formal
    Version Date: 2025.4.17
    Developed by: Jiawen Li
    Production Period: 14H
    Wowww! This is an unofficial UNSW(University of New South Wales) application!
    UNSWow designed for helps UNSW students(also welcome others) track their personal behaviors
    and actions, providing motivation and insights into their daily activities.
    Don't judge me that one script including all, it's robust:b

    Features:
    - Give your score for one day in UK grade system!
    - Predict your next day score for a baseline!
    - Change theme color between day and night!
    - Track work hours, study hours, and other activities.
    - Display visual progress and motivational quotes.
    - Efficient record filtering and vivid evaluations.

    This software could access by github, 100% free, and not allow for any commercial uses.
    For any feedback or issues, please contact author via jiawen.li12@student.unsw.edu.au, it's a voluntary work.
    """

    label = Label(content_frame, text=info_message,font=("Helvetica", 15), justify="left")
    label.pack(expand=True,padx=10, pady=10)

    # 添加关闭按钮
    close_button = Button(content_frame, text="back to menu", command=info_window.destroy)
    close_button.pack(pady=2)

    # 更新Canvas的scrollable区域
    content_frame.update_idletasks()
    canvas.config(scrollregion=canvas.bbox("all"))
# ----------------------- 主界面按钮 ----------------------- #
main_bspace=9
style = Style()
style.configure("TButton", font=("Helvetica", 20))

add_button = Button(root, text="Add Record",width=20, command=show_input_fields)
add_button.pack(pady=main_bspace)

score_button = Button(root, text="Your Score", width=20,command=lambda: show_scores(data))
score_button.pack(pady=main_bspace)

chart_button = Button(root, text="Show Chart", width=20,command=lambda: show_chart(data))
chart_button.pack(pady=main_bspace)

analyze_button = Button(root, text="Get Suggestion", width=20,command=lambda: analyze_track(data))
analyze_button.pack(pady=main_bspace)

filter_button = Button(root, text="Search Records",width=20, command=lambda: filter_records(data))
filter_button.pack(pady=main_bspace)

about_button = Button(root, text="About UNSWow",width=20, command=show_info)
about_button.pack(pady=main_bspace)

backup_button = Button(root, bootstyle="outline",width=20, text="Backups", command=backup)
backup_button.pack(side=tk.BOTTOM, anchor=tk.SW)

version = Label(root, text="Version 1.0.3 designed by Jiawen Li", font=('Helvetica', 9))
version.pack()

root.mainloop()