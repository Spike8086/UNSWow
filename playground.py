import tkinter as tk
import random

def animate_text():
    # 随机选择字体大小和颜色
    new_size = random.choice([16, 18, 20, 22])
    new_color = random.choice(["#FFD700", "#FF69B4", "#00FFFF", "#ADFF2F", "#FFA500"])

    # 修改 canvas 上的文本样式
    canvas.itemconfig(text_item, font=("Helvetica", new_size, "bold"), fill=new_color)

    # 递归调用形成闪耀效果
    root.after(150, animate_text)

# 初始化主窗口
root = tk.Tk()
root.geometry("600x200")
root.title("UNSWow")

# 创建黑色背景 Canvas
canvas = tk.Canvas(root, bg="black", highlightthickness=0)
canvas.pack(fill="both", expand=True)

# 创建文字并保存 item ID
text_item = canvas.create_text(
    300, 100,  # 居中位置
    text="UNSWow — Discipline Activated",
    font=("Helvetica", 20, "bold"),
    fill="white"
)

# 启动动画
animate_text()

root.mainloop()

