#!/usr/bin/env python3
import sys
import json
import urllib.request
import urllib.parse
import html

if len(sys.argv) < 4:
    sys.exit(0)

alert_file = sys.argv[1]
chat_id = sys.argv[2]
hook_url = sys.argv[3]

try:
    with open(alert_file, 'r', encoding='utf-8') as f:
        alert = json.load(f)
except Exception as e:
    with open('/tmp/telegram_debug.log', 'a') as debug:
        debug.write(f"Loi doc file alert: {str(e)}\n")
    sys.exit(0)

rule = alert.get("rule", {})
rule_id = rule.get("id", "N/A")
rule_level = int(rule.get("level", 0))
rule_desc = html.escape(str(rule.get("description", "No description")))

agent = alert.get("agent", {})
agent_name = html.escape(str(agent.get("name", "Unknown")))
agent_ip = html.escape(str(agent.get("ip", "Unknown")))

mitre = rule.get("mitre", {})
mitre_id = mitre.get("id", ["T1059.001"])
mitre_id_str = ", ".join(mitre_id) if isinstance(mitre_id, list) else str(mitre_id)

data = alert.get("data", {})
win = data.get("win", {})
eventdata = win.get("eventdata", {})
command_line = html.escape(str(eventdata.get("commandLine", "N/A")))
parent_image = html.escape(str(eventdata.get("parentImage", "N/A")))

if rule_level >= 12:
    status_header = "🛑 <b>[CRITICAL - CHẶN ĐỨNG & TIÊU DIỆT]</b>"
    action_text = "🚨 <b>ĐÃ BỊ TIÊU DIỆT (Taskkill)</b>"
elif rule_level >= 8:
    status_header = "⚠️ <b>[HIGH - PHÁT HIỆN LẨN TRÁNH]</b>"
    action_text = "👁️‍🗨️ <b>CẢNH BÁO GIÁM SÁT (Alert Only)</b>"
else:
    status_header = "ℹ️ <b>[INFO - EVENT]</b>"
    action_text = "Ghi nhận sự kiện"

lines = [
    status_header,
    "<b>HỆ THỐNG PHÁT HIỆN EDR (T1059.001)</b>",
    "___________________________________",
    "",
    f"🛡️ <b>Mức độ:</b> Level {rule_level} (Rule: <code>{rule_id}</code>)",
    f"🎯 <b>MITRE:</b> <code>{mitre_id_str}</code>",
    f"📝 <b>Mô tả:</b> {rule_desc}",
    "",
    f"💻 <b>Nạn nhân:</b> <code>{agent_name}</code> ({agent_ip})",
    f"⚡ <b>Trạng thái:</b> {action_text}",
    "",
    "🔍 <b>Command Line:</b>",
    f"<pre>{command_line[:300]}</pre>",
    f"📁 <b>Tiến trình cha:</b> <code>{parent_image}</code>",
    "___________________________________"
]
message = "\n".join(lines)

payload = {
    "chat_id": chat_id,
    "text": message,
    "parse_mode": "HTML"
}

try:
    data_bytes = json.dumps(payload).encode('utf-8')
    req = urllib.request.Request(hook_url, data=data_bytes, headers={'Content-Type': 'application/json'})
    urllib.request.urlopen(req, timeout=10)
except Exception as e:
    with open('/tmp/telegram_debug.log', 'a') as debug:
        debug.write(f"Loi gui Telegram: {str(e)}\n")

sys.exit(0)