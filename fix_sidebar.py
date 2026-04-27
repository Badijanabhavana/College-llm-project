import glob

target = '<a href="/records" class="menu-item"><span class="menu-icon">📋</span><span class="menu-text">Feedback Record</span></a>'
replacement = target + '\n            <a href="/chat_history" class="menu-item"><span class="menu-icon">💬</span><span class=\"menu-text\">Chat History</span></a>'

for file in glob.glob('templates/*.html'):
    with open(file, 'r', encoding='utf-8') as f:
        content = f.read()
    if target in content and '/chat_history' not in content:
        content = content.replace(target, replacement)
        with open(file, 'w', encoding='utf-8') as f:
            f.write(content)

print("Sidebar updated successfully.")
