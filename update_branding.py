import os
import glob
import re

directory = r"c:/Users/Mohan/Desktop/college llm project"
files = glob.glob(os.path.join(directory, "*.py")) + glob.glob(os.path.join(directory, "templates", "*.html")) + [os.path.join(directory, "README.md")]

full_name = "Jawaharlal Nehru Technological University Gurajada Vizianagaram (JNTU-GV)"
short_name = "JNTU-GV"

for f in files:
    try:
        if not os.path.exists(f): continue
        with open(f, 'r', encoding='utf-8') as file:
            content = file.read()
            
        original_content = content
        
        # 1. Update Title tags
        content = re.sub(r'<title>(.*?) \| JNTU-GV</title>', rf'<title>\1 | {short_name}</title>', content)
        content = re.sub(r'<title>JNTU-GV (.*?)</title>', rf'<title>{short_name} \1</title>', content)
        
        # 2. Update Navbar/Topbar Logos
        content = content.replace("JNTU-GV", short_name)
        
        # 3. Handle Hero/Main Headings (In templates)
        if f.endswith('admissions.html'):
            content = content.replace(f"Begin Your Journey at <span>{short_name}</span>", f"Begin Your Journey at <span>{full_name}</span>")
            content = content.replace(f"secure your future at {short_name}", f"secure your future at {full_name}")
        
        if f.endswith('campus.html'):
            content = content.replace(f"Life at <span>{short_name}</span>", f"Life at <span>{full_name}</span>")
            
        if f.endswith('departments.html'):
             # Usually departments just use JNTU-GV but let's check hero
             pass

        # 4. Handle app.py specific content
        if f.endswith('app.py'):
            # Already did some in previous turn, but ensuring consistency
            content = content.replace("JNTU-GV", short_name)
            # Fix Welcome message if not exact
            content = re.sub(r'"hello": "<strong>👋 Welcome to JNTU-GV College Enquiry System. How can I assist you today\?</strong><br><br>"', r'"hello": "<strong>👋 Welcome to JNTU-GV College Enquiry System. How can I assist you today?</strong><br><br>"', content)

        # 5. README.md
        if f.endswith('README.md'):
             content = content.replace(short_name, full_name)

        if content != original_content:
            with open(f, 'w', encoding='utf-8') as file:
                file.write(content)
            print(f"Updated {os.path.basename(f)}")
    except Exception as e:
        print(f"Failed {f}: {e}")
