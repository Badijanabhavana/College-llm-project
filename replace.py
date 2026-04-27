import os
import glob
import re

directory = r"c:/Users/Mohan/Desktop/college llm project"
files = glob.glob(os.path.join(directory, "*.py")) + glob.glob(os.path.join(directory, "templates", "*.html")) + [os.path.join(directory, "README.md")]

for f in files:
    try:
        if not os.path.exists(f): continue
        with open(f, 'r', encoding='utf-8') as file:
            content = file.read()
            
        original_content = content
            
        if f.endswith('app.py'):
            content = content.replace("<strong>👋 Welcome to JNTU-GV!</strong>", "<strong>👋 Welcome to JNTU-GV College Enquiry System. How can I assist you today?</strong>")
            content = content.replace("JNTU-GV", "JNTU-GV")
        elif f.endswith('index.html'):
            # Homepage heading
            content = content.replace('<span style="color: var(--primary-dark)">JNTU-GV</span>', '<span style="color: var(--primary-dark)">Jawaharlal Nehru Technological University Gurajada Vizianagaram (JNTU-GV)</span>')
            # Navbar title (handle regex for potential \r\n and spaces)
            content = re.sub(r'<span style="font-size: 1.2rem;">🏥</span>\s*JNTU-GV', r'<span style="font-size: 1.2rem;">🏥</span>\n                Jawaharlal Nehru Technological University Gurajada Vizianagaram (JNTU-GV)', content)
            # Then all others
            content = content.replace("JNTU-GV", "JNTU-GV")
        else:
            content = content.replace("JNTU-GV", "JNTU-GV")
            
        if content != original_content:
            with open(f, 'w', encoding='utf-8') as file:
                file.write(content)
            print(f"Updated {os.path.basename(f)}")
    except Exception as e:
        print(f"Failed {f}: {e}")
