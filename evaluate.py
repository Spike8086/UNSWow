import json

# 定义所有评价内容
evaluations = {
    "high_first": [
        "🎓 High 1st: Exceptional performance! You're leading the UNSWow squad!",
        "🎓 High 1st: Phenomenal! You're in beast mode!",
        "🎓 High 1st: UNSWow salutes your elite discipline!",
        "🎓 High 1st: Outstanding! You're rewriting the playbook!",
        "🎓 High 1st: Commanding the day like a general!",
        "🎓 High 1st: You've earned a parade in your honour!",
        "🎓 High 1st: Your discipline could crack diamonds!",
        "🎓 High 1st: Supreme focus — UNSWow legend status!",
        "🎓 High 1st: A masterclass in self-mastery!",
        "🎓 High 1st: Simply unstoppable. Keep charging!",
        "🎓 High 1st: There's nothing you can't conquer!",
        "🎓 High 1st: An unstoppable force of focus and will!",
        "🎓 High 1st: The gold standard of dedication!",
        "🎓 High 1st: You’re in a league of your own!",
        "🎓 High 1st: Unmatched persistence — you make it look easy!",
        "🎓 High 1st: A true visionary in motion!",
        "🎓 High 1st: Your growth is exponential!",
        "🎓 High 1st: Excellence is your baseline!",
        "🎓 High 1st: A champion’s mindset through and through!"
    ],
    "first": [
        "🏅 1st Class Honours: Excellent work! Keep riding the wave of success.",
        "🏅 1st Class Honours: You're setting a powerful pace!",
        "🏅 1st Class Honours: Momentum is your middle name!",
        "🏅 1st Class Honours: Laser focus detected!",
        "🏅 1st Class Honours: Big moves, solid gains.",
        "🏅 1st Class Honours: UNSWow is impressed!",
        "🏅 1st Class Honours: You've got the fire today!",
        "🏅 1st Class Honours: Quality effort, no doubt!",
        "🏅 1st Class Honours: That’s how champions rise!",
        "🏅 1st Class Honours: Keep the engines running hot!",
        "🏅 1st Class Honours: You’re making waves — stay relentless!",
        "🏅 1st Class Honours: Victory is in your sights!",
        "🏅 1st Class Honours: Consistency at its finest!",
        "🏅 1st Class Honours: Keep sharpening your craft!",
        "🏅 1st Class Honours: You're proving greatness every day!",
        "🏅 1st Class Honours: Big vision, big impact!",
        "🏅 1st Class Honours: Focus and fire, always on point!",
        "🏅 1st Class Honours: Unshakable commitment to excellence!",
        "🏅 1st Class Honours: Your best is yet to come!"
    ],
    "two_one": [
        "🎖️ 2:1 Honours: Solid and promising! You're building real momentum.",
        "🎖️ 2:1 Honours: Good stuff — you're on track!",
        "🎖️ 2:1 Honours: Keep refining, you're getting sharper.",
        "🎖️ 2:1 Honours: You're warming up for greatness.",
        "🎖️ 2:1 Honours: Real work, real progress.",
        "🎖️ 2:1 Honours: Solid execution — onward!",
        "🎖️ 2:1 Honours: You're pushing with purpose.",
        "🎖️ 2:1 Honours: Just a few more tweaks to excellence.",
        "🎖️ 2:1 Honours: The climb is steady — don’t stop!",
        "🎖️ 2:1 Honours: Discipline level rising — keep it up!",
        "🎖️ 2:1 Honours: You're at a critical point, stay focused!",
        "🎖️ 2:1 Honours: Consistent effort, steady progress!",
        "🎖️ 2:1 Honours: Excellence is within reach — keep pushing!",
        "🎖️ 2:1 Honours: Great effort, now refine the details!",
        "🎖️ 2:1 Honours: The momentum is there, accelerate!",
        "🎖️ 2:1 Honours: You're climbing higher every day!",
        "🎖️ 2:1 Honours: Stay on course — you’ve got this!",
        "🎖️ 2:1 Honours: You're building strong foundations!",
        "🎖️ 2:1 Honours: You're elevating your standards, keep it up!",
        "🎖️ 2:1 Honours: Keep the drive going — you’re almost there!"
    ],
    "two_two": [
        "📘 2:2 Honours: Not bad, but the climb to excellence continues!",
        "📘 2:2 Honours: There’s fire in the engine, add more fuel!",
        "📘 2:2 Honours: A decent day — tomorrow we elevate!",
        "📘 2:2 Honours: You're keeping afloat, now let's rise!",
        "📘 2:2 Honours: Foundation’s there — build upward!",
        "📘 2:2 Honours: Slightly wobbly but still walking the path.",
        "📘 2:2 Honours: More is possible — let’s go!",
        "📘 2:2 Honours: UNSWow wants more spark tomorrow!",
        "📘 2:2 Honours: Not bad — but you’re capable of better.",
        "📘 2:2 Honours: Step up the game — we believe in you!",
        "📘 2:2 Honours: Progress is steady, now let’s accelerate!",
        "📘 2:2 Honours: You’re halfway there — push for more!",
        "📘 2:2 Honours: Keep it up — excellence is close!",
        "📘 2:2 Honours: You’ve got the foundation — now build it strong!",
        "📘 2:2 Honours: Stronger focus will take you further!",
        "📘 2:2 Honours: A step forward, now take a leap!",
        "📘 2:2 Honours: Refine your approach and watch it shine!",
        "📘 2:2 Honours: You’re on the right track — more effort needed!",
        "📘 2:2 Honours: A good day, let’s keep the momentum going!",
        "📘 2:2 Honours: You’re moving in the right direction, aim higher!"
    ],
    "fail": [
        "🔴 Fail: A reset is needed. Recharge and bounce back tomorrow!",
        "🔴 Fail: Fall down seven times, stand up eight.",
        "🔴 Fail: No shame — just reboot and return stronger.",
        "🔴 Fail: Learn from the fall, rise with intent.",
        "🔴 Fail: The fight isn't over — UNSWow believes in your return.",
        "🔴 Fail: Tough day? Build the comeback story.",
        "🔴 Fail: Reset mindset. Tomorrow = redemption.",
        "🔴 Fail: Brick wall hit. Climb it or break it.",
        "🔴 Fail: Let this fuel tomorrow's fire.",
        "🔴 Fail: Shake it off — UNSWow waits for your bounce back!",
            "🔴 Fail: You're not done — it's time to get up and try again!",
    "🔴 Fail: Don’t let today define you — rise up stronger!",
    "🔴 Fail: A setback is just the beginning of a greater comeback!",
    "🔴 Fail: You’ve stumbled, now it’s time to sprint!",
    "🔴 Fail: Today was a trial, tomorrow is your victory!" "🔴 Fail: You’re down, but not out. Tomorrow’s your chance to shine!",
    "🔴 Fail: Every failure is a lesson — let it fuel your comeback.",
    "🔴 Fail: Failure is only temporary, your rise will be unstoppable.",
    "🔴 Fail: Today was a bump, but tomorrow's road is yours to conquer.",
    "🔴 Fail: The journey is tough, but you’ve got the strength to bounce back.",
    "🔴 Fail: Failure is just a stepping stone to success — take the next step!",
    "🔴 Fail: This moment doesn’t define you. Rise, learn, and crush it next time.",
    "🔴 Fail: Don’t dwell on today’s setback — make tomorrow count.",
    "🔴 Fail: Every champion faces defeat — it’s how you come back that matters.",
    "🔴 Fail: You’ve been knocked down, but the fight isn’t over. Stand tall!"
    ]
}

# 保存为 JSON 文件
file_path = "./evaluations.json"
with open(file_path, "w", encoding="utf-8") as f:
    json.dump(evaluations, f, ensure_ascii=False, indent=2)

file_path


