from flask import Flask, render_template, request, redirect, url_for, session, flash
import requests
import os
import re
from dotenv import load_dotenv
#import google.generativeai as genai
load_dotenv(override=True)
print(os.getenv("OPENROUTER_API_KEY"))
available_models = ["gpt-3.5-turbo"]
API_KEY = os.getenv("OPENROUTER_API_KEY","").strip()
print("KEY=",repr(API_KEY))

    #genai.configure(api_key=API_KEY)

app = Flask(__name__)
app.secret_key = "super_peachy_secret_key"
import database
from flask import jsonify

#if not database.is_db_initialized():
database.init_db()

otps = {}

# Detailed Mock Data for JNTU-GV
university_data = {
    "courses_overview": "<strong>📚 Academic Programs Overview</strong><br><br>"
                        "JNTU-GV offers a diverse portfolio of industry-aligned programs designed to foster innovation and leadership. "
                        "Our curriculum is constantly updated to meet global standards.<br><br>"
                        "<strong>Programs Offered:</strong><br>"
                        "• <strong>B.Tech</strong>: Computer Science (CSE), Electronics (ECE), Mechanical, Civil.<br>"
                        "• <strong>B.Sc</strong>: Physics, Chemistry, Mathematics.<br>"
                        "• <strong>Business</strong>: BBA, B.Com, MBA (Finance, Marketing, HR).<br>"
                        "• <strong>Computer Applications</strong>: MCA.<br>"
                        "• <strong>Postgraduate</strong>: M.Tech and PhD in various disciplines.<br><br>"
                        "<em>Tip: You can ask me specifically about any course, e.g., 'Tell me about CSE'.</em>",
                        
    "cse_details": "<strong>💻 Computer Science & Engineering (B.Tech - CSE)</strong><br><br>"
                   "The CSE program focuses on the core principles of computing, software development, and modern technologies. "
                   "It is designed to build a strong foundation in algorithms, system software, and emerging digital trends.<br><br>"
                   "<strong>Core Subjects:</strong> Data Structures, Artificial Intelligence, Machine Learning, Database Management, Cloud Computing, and Cyber Security.<br><br>"
                   "<strong>Career Scope:</strong> Graduates are highly sought after as Software Engineers, Data Scientists, Cloud Architects, and AI Specialists in top global tech firms.",

    "ece_details": "<strong>⚡ Electronics and Communication Engineering (B.Tech - ECE)</strong><br><br>"
                   "The ECE program bridges the gap between hardware and software, focusing on telecommunications, VLSI design, and embedded systems.<br><br>"
                   "<strong>Core Subjects:</strong> Digital Signal Processing, Microprocessors, VLSI Design, Integrated Circuits, and IoT Systems.<br><br>"
                   "<strong>Career Scope:</strong> Opportunities abound as Network Engineers, Embedded Developers, and Systems Engineers in telecommunications, aerospace, and consumer electronics.",
                   
    "mba_details": "<strong>📈 Master of Business Administration (MBA)</strong><br><br>"
                   "The JNTU-GV MBA program builds future leaders by emphasizing strategic thinking, management capabilities, and entrepreneurial spirit.<br><br>"
                   "<strong>Specializations:</strong> Finance, Human Resources, Marketing, and Operations.<br><br>"
                   "<strong>Career Scope:</strong> Graduates enter the corporate world as Investment Bankers, Marketing Managers, HR Directors, and Business Consultants.",

    "mca_details": "<strong>🖥️ Master of Computer Applications (MCA)</strong><br><br>"
                   "The JNTU-GV MCA program is a dynamic course covering advanced programming, application development, and enterprise software solutions.<br><br>"
                   "<strong>Core Subjects:</strong> Advanced Java, Python Programming, Software Engineering, Mobile App Development, and Web Technologies.<br><br>"
                   "<strong>Career Scope:</strong> Graduates flourish as App Developers, Systems Analysts, Tech Leads, and IT Consultants.",

    "fees": "<strong>💰 Fee Structure & Financial Aid</strong><br><br>"
            "As a government-affiliated university, our fees are strictly subsidized to ensure affordable education for all students without compromising on quality.<br><br>"
            "<strong>Annual Fee Breakdown:</strong><br>"
            "• <strong>B.Tech</strong>: ₹35,000 / year<br>"
            "• <strong>MBA</strong>: ₹25,000 / year<br>"
            "• <strong>MCA</strong>: ₹20,000 / year<br>"
            "• <strong>M.Tech</strong>: ₹30,000 / year<br>"
            "• <strong>Hostel & Mess</strong>: ₹25,000 / year<br><br>"
            "<strong>🎓 Financial Aid & Reimbursements:</strong><br>"
            "Eligible students can benefit from complete fee reimbursement through State Government schemes based on entrance exam merit and category guidelines.",
            
    "admission": "<strong>📝 Clear & Transparent Admission Process</strong><br><br>"
                 "Securing admission at JNTU-GV involves a highly transparent, merit-based process designed by the state government.<br><br>"
                 "<strong>Step-by-Step Guide:</strong><br>"
                 "1. <strong>Entrance Exams</strong>: You must qualify in state-level entrance examinations like TS/AP EAMCET, ICET, or GATE.<br>"
                 "2. <strong>Online Web Counseling</strong>: Participate strictly through the official state government counseling portals.<br>"
                 "3. <strong>Merit Allotment</strong>: Seat allocation is conducted entirely based on rank, category reservations, and established merit criteria.<br>"
                 "4. <strong>Document Verification</strong>: Present original documents at designated government helpline centers.<br>"
                 "5. <strong>Final Reporting</strong>: Submit your official allotment order and fee receipt at our university administration office to confirm enrollment.",
                 
    "facilities": "<strong>🏫 Premium Campus Facilities</strong><br><br>"
                  "Our expansive 150-acre campus provides an active and enriching environment, outfitted with modern infrastructure to support academic excellence.<br><br>"
                  "<strong>Key Features:</strong><br>"
                  "• <strong>Central Library</strong>: A vast, digitally enabled library with hundreds of thousands of academic books, international journals, and quiet reading zones.<br>"
                  "• <strong>Advanced Labs</strong>: Practical programming, hardware, and chemistry labs equipped with standard modern tools and internet connectivity.<br>"
                  "• <strong>Sports Complex</strong>: Wide open grounds dedicated to cricket, football, basketball, and an indoor athletics center.<br>"
                  "• <strong>Accommodations</strong>: Government-subsidized, highly secure, and hygienic hostels separate for boys and girls.<br>"
                  "• <strong>Transport & Food</strong>: A fully-functioning subsidized cafeteria and seamless connectivity via RTC buses.",
                  
    "placements": "<strong>💼 Placements & Career Growth</strong><br><br>"
                  "Our dedicated Career Development Center works tirelessly to ensure students are well-prepared for the professional world, yielding excellent placement records annually.<br><br>"
                  "<strong>Placement Highlights:</strong><br>"
                  "• <strong>Highest Package</strong>: ₹12 LPA (Lakhs Per Annum) offered by leading MNCs.<br>"
                  "• <strong>Average Package</strong>: ₹4.5 LPA across varying engineering and management disciplines.<br>"
                  "• <strong>Top Recruiters</strong>: Regular placement drives feature giants like TCS, Infosys, Wipro, Amazon, and multiple Public Sector Undertakings (PSUs).<br>"
                  "• <strong>Training Initiatives</strong>: We conduct rigorous aptitude, technical skill, and soft-skill workshops right from the third year.",

    "exams": "<strong>📅 Examination Patterns & Schedules</strong><br><br>"
             "Our assessment system is designed to ensure continuous learning and comprehensive evaluation throughout the semester.<br><br>"
             "<strong>Exam Details:</strong><br>"
             "• <strong>Mid-Term Examinations</strong>: Conducted twice per semester assessing half the syllabus each time to ensure steady progress.<br>"
             "• <strong>End-Term Examinations</strong>: A comprehensive final theory and practical exam evaluated by external and internal faculty.<br>"
             "• <strong>Grading System</strong>: We follow a widely accepted 10-point CGPA grading scale.<br>"
             "<em>The exact dates for upcoming exams are regularly updated on the student portal and campus notice boards.</em>",
             
    "hello": "<strong>👋 Welcome to JNTU-GV College Enquiry System. How can I assist you today?</strong><br><br>"
             "I am your dedicated AI Enquiry Assistant. I can provide detailed information about our curriculum, admission processes, fee structures, campus life, and placement records.<br><br>",
             
    "default": "<strong>🤖 I'm here to help!</strong><br><br>"
               "I didn't quite catch that. Could you please specify your question?<br><br>"
               "You can ask me detailed questions about:<br>"
               "• <strong>Courses</strong> (e.g., 'Tell me about CSE or MBA')<br>"
               "• <strong>Admissions</strong> (e.g., 'How to apply?')<br>"
               "• <strong>Fees</strong> (e.g., 'What is the fee structure?')<br>"
               "• <strong>Placements</strong> (e.g., 'Tell me about jobs')<br>"
               "• <strong>Exams & Facilities</strong>."
}

chat_sessions = {}

def get_bot_response(user_text, username):
    if not API_KEY or API_KEY == "your_api_key_here":
        return "<strong>System Notice:</strong> LLM is offline because the  API Key is missing. Please set API_KEY in the <code>.env</code> file.<br><br><em>Please provide a valid API key for the AI to function properly.</em>"
        
    try:
        system_instruction = """You are the official AI Enquiry Bot for JNTU-GV (Jawaharlal Nehru Technological University Gurajada Vizianagaram).

Your job is to give short, simple, and accurate answers in the chat itself. Use basic English. Use 3-4 bullet points per answer.

IMPORTANT LINK RULE:
- Only give a link when the user specifically asks about something that has an official page (like results, admissions, placements, gallery,exams,events,sports,faculty).
- For general or conversational questions, give a helpful answer with NO link.
- NEVER give the homepage link for every single answer.

===== VERIFIED KNOWLEDGE BASE =====

LEADERSHIP:
- Vice-Chancellor: Prof. V. V. Subba Rao (Ph.D., Mechanical Engineering, IIT Kharagpur)
- Registrar (i/c): Prof. D. Rajya Lakshmi (M.Tech, Ph.D)
- Principals and Deans manage academic departments across colleges.
-principal:Prof. K. Chandra Bhushana Rao Principal i/c
-vice principal: prof.G.J.Nagaraju 
link : https://jntugvcev.edu.in/admistration/principal/
[Link only if asked about admin/leadership: https://jntugvcev.edu.in/admistration/]

About College:
[link if they ask about college:https://www.jntugv.edu.in/]
COLLEGES UNDER JNTU-GV:
- JNTU-GV College of Engineering, Vizianagaram (CEV)
- JNTU-GV College of Pharmaceutical Sciences, Vizianagaram (CPSV)
- JNTU-GV Tribal College of Engineering, Kurupam (TECK)

PROGRAMS / DEPARTMENTS:
- B.Tech: CSE, ECE, EEE, Civil, Mechanical
- Pharmacy: B.Pharmacy, M.Pharmacy, Pharm.D
- PG Programs: M.Tech, MBA, MCA
- Research: Ph.D programs in various streams
[Link only if asked about programs: https://jntugvcev.edu.in/academics/courses-offered/]

ADMISSIONS:
- Admissions open after state entrance exam results are declared.
- B.Tech and B.Pharmacy: AP EAPCET or TS EAMCET
- MBA and MCA: ICET
- M.Tech: PGECET or GATE
- Students attend state counseling, verify documents at helpline centers, then report to college.
[Link only if asked about admissions: https://jntugvcev.edu.in/academics/admissions/admission-procedure/]

FEE STRUCTURE:
- Fees may vary from one course to another course
- B.Tech: Tution fee-45000  
          Admission fee-5000
          Special fee-300
-Mca & Mba: Tution fee-27000
          Admission fee-5200
          Special fee-3300
-M.Tech : Tution fee-50000
          Admission fee-5200
          Special fee-3300
Reimbursments:Eligible students can benefit from complete fee reimbursement through State Government schemes based on entrance exam merit and category guidelines.
[link only if they ask about fees: https://jntugvcev.edu.in/academics/admissions/fee-structure/]

EXAMS AND RESULTS:
- Exams are held every semester: mid-term exams and end-term exams.
- Results are published on the official exam portal: https://jntugvcev.edu.in/academics/examinations/results/
- Recent exam updates: MCA and MBA II Sem Regular and Supply Exams May-2026; B.Tech special supplementary results; B.Pharmacy results Feb-2026.
- Postponement circulars and revised exam dates are posted in notifications.
[link only if the ask about exams/notifications:https://jntugvcev.edu.in/academics/examinations/examination-time-tables/]

ONLINE PORTALS:
- Exam Results Portal: https://exams.jntugv.edu.in/results
- Placements Cell Portal: https://placementcell.jntugv.edu.in/
- Distance and Continuing Education: https://dmc.jntugv.edu.in
- Notifications and Circulars: check https://jntugvcev.edu.in main page
[Give the relevant portal link when user asks about portals]

PLACEMENTS:
- The Placements Cell provides aptitude, technical, and soft skills training.
- Campus recruitment drives are held where top companies hire students.
- Companies like TCS, Infosys, Wipro participate regularly.
- Career guidance starts from 3rd year.
[Link only if asked about placements: https://jntugvcev.edu.in/beta/placements/training-placements-cell/]

EVENTS AND ACTIVITIES:
- Annual Day and Sports Day are held every year.
- NSS (National Service Scheme) is active with community programs.
- Student clubs: Music Club, Student Activity Club, Sports and Fitness.
- Major cultural event: Ityuktha 2K24.
- Inter-Collegiate Tournaments are organized every year.
- Republic Day, Women's Day, and Independence Day are celebrated on campus.
[Link only if asked about gallery/events: https://jntugvcev.edu.in/gallery/]

FACILITIES AND HOSTELS:
- Separate hostels for boys and girls on campus.
- Sports facilities: volleyball, weightlifting, yoga courts.
- Staff quarters are available.
-there are more facilicities.
[Link only if asked about campus/facilities:https://jntugvcev.edu.in/facilities/library/ ]
[link if they ask about hostels:https://jntugvcev.edu.in/facilities/hostels/]

RESEARCH:
- The R&D Cell supports research scholars and faculty.
- Ph.D programs are offered across departments.
- Pre-Ph.D exams, subject lists, syllabus, and registration forms are available on the website.
[link if they ask about research:https://jntugvcev.edu.in/rd-cell/about-research/]

CELLS AND COMMITTEES:
- IQAC: Internal Quality Assurance Cell
- NSS Cell
- Student Grievance Redressal
- Ombudsman for student complaints
- Recruitment Grievance committee
- University Coordinators for different functions
- Incubation Center for startups
[link if they ask for cells:https://jntugvcev.edu.in/student-corner/nss/]

SWAYAM / ONLINE LEARNING:
- Students can access Swayam Central for MOOC courses.
- UGC MOOCs are also available.
- Springer journals are accessible for research.

SOCIAL MEDIA:
- YouTube: https://www.youtube.com/@JNTUGV
- Facebook: https://www.facebook.com/JNTUGurajada
- Twitter/X: https://twitter.com/JNTU_Gurajada
- Instagram: https://www.instagram.com/jntu_gurajada/
- LinkedIn: https://www.linkedin.com/in/jntugurajada/

CONTACT:
[Link only if asked about contact: https://jntugvcev.edu.in/contact-us/telephone-directory/]

===== RULES =====
1. Use 3-4 simple bullet points per answer (use <br>\u2022 for bullets).
2. Use basic English that everyone understands.
3. Give the actual answer from the knowledge base. Do NOT say \"check the website\".
4. Add a link ONLY if it is directly relevant. Use this format at the bottom:
<br><br>For more details, visit:<br><a href=\"[Link]\" target=\"_blank\">[Link]</a>
5. For general non-JNTU questions or greetings, give a helpful answer with NO link.
6. If the user asks about something not in the knowledge base, say:
I don't have specific information on that. Please visit: <a href=\"https://jntugvcev.edu.in\" target=\"_blank\">https://jntugvcev.edu.in/</a>
7. No Markdown (**). Use only HTML tags: <br>, <a>, <strong>.
"""
        
       # model = genai.GenerativeModel('gemini-2.0-flash', system_instruction=system_instruction)
        
        if username not in chat_sessions:
            chat_sessions[username] = []
            
       # chat = model.start_chat(history=chat_sessions[username])
       # response = chat.send_message(user_text)
        
        # Persist memory in the dictionary for the next request
       # chat_sessions[username] = chat.history
        
        # Clean formatting for web UI
        #text = response.text
        headers={
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }
        print("REQUEST IS ABOUT TO RUN")
        
        response = requests.post(
    "https://openrouter.ai/api/v1/chat/completions",
    headers=headers,
    json={
        "model": "gpt-3.5-turbo",
        "messages": [
            {"role": "system", "content": system_instruction},
            {"role": "user", "content": user_text}
        ]
    }
)
        print(response.status_code) 
        print(response.text)
        data = response.json()

        if "choices" not in data:
         return f"API Error: {data}"

        text = data["choices"][0]["message"]["content"]
        text = re.sub(r'\*\*(.*?)\*\*', r'<strong>\1</strong>', text)
        text = text.replace('\n', '<br>')
        
        # Log to chat history database
        database.log_chat(username, user_text, text)
        
        # Detect fallback / unanswered
        lower_resp = response.text.lower()
        if "for more details, please visit the official website" in lower_resp:
            database.add_unanswered(username, user_text)
            
        return text
    except Exception as e:
        try:
            #available_models = [m.name.replace('models/', '') for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
            models_str = ", ".join(available_models)
        except Exception as e2:
            models_str = f"Could not fetch models: {e2}"
        return f"Error:{str(e)}"

@app.route("/")
@app.route("/home")
def home():
    if "user" not in session: return redirect(url_for("login"))
    return render_template("index.html", current_user=session["user"])

@app.route("/about")
def about():
    if "user" not in session: return redirect(url_for("login"))
    content = "Welcome to the LLM-Based College Enquiry System developed for JNTU-GV.<br><br>This project is specifically designed to bridge the communication gap between prospective students and the university administration. Built with a robust Python Flask backend and a responsive, premium frontend UI, this system simulates an AI chatbot capable of guiding students regarding courses, fee structures, admissions, placements, and extensive campus facilities."
    return render_template("generic.html", current_user=session["user"], title="About the Project", content=content)

@app.route("/departments")
def departments():
    if "user" not in session: return redirect(url_for("login"))
    return render_template("departments.html", current_user=session["user"])

@app.route("/admissions")
def admissions():
    if "user" not in session: return redirect(url_for("login"))
    return render_template("admissions.html", current_user=session["user"])

@app.route("/fees")
def fees():
    if "user" not in session: return redirect(url_for("login"))
    return render_template("generic.html", current_user=session["user"], title="Fees", content=university_data["fees"])

@app.route("/placements")
def placements():
    if "user" not in session: return redirect(url_for("login"))
    return render_template("placements.html", current_user=session["user"])

@app.route("/campus")
def campus():
    if "user" not in session: return redirect(url_for("login"))
    return render_template("campus.html", current_user=session["user"])

@app.route("/chat")
def chat():
    if "user" not in session: return redirect(url_for("login"))
    return render_template("chat.html", current_user=session["user"])

@app.route("/bot-users")
def bot_users():
    if "user" not in session: return redirect(url_for("login"))
    return render_template("bot_users.html", current_user=session["user"])

@app.route("/unanswered")
def unanswered():
    if "user" not in session: return redirect(url_for("login"))
    return render_template("unanswered.html", current_user=session["user"])

@app.route("/records")
def records():
    if "user" not in session: return redirect(url_for("login"))
    return render_template("records.html", current_user=session["user"])

@app.route("/chat_history")
def chat_history():
    if "user" not in session: return redirect(url_for("login"))
    return render_template("chat_history.html", current_user=session["user"])

@app.route("/api/users")
def api_users():
    if "user" not in session: return jsonify([]), 403
    return jsonify(database.get_all_users())

@app.route("/api/unanswered")
def api_unanswered():
    if "user" not in session: return jsonify([]), 403
    return jsonify(database.get_unanswered())

@app.route("/api/feedbacks")
def api_feedbacks():
    if "user" not in session: return jsonify([]), 403
    return jsonify(database.get_feedbacks())

@app.route("/api/chat_history")
def api_chat_history():
    if "user" not in session: return jsonify([]), 403
    return jsonify(database.get_chat_history())

@app.route("/feedback", methods=["GET", "POST"])
def feedback():
    if "user" not in session: return redirect(url_for("login"))
    if request.method == "POST":
        message = request.form.get("message")
        stars = int(request.form.get("stars", 5))
        database.add_feedback(session["user"], message, stars)
        return redirect(url_for("records"))
    return render_template("feedback.html", current_user=session["user"])

@app.route("/login", methods=["GET", "POST"])
def login():
    msg = request.args.get("msg")
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        user = database.get_user(username)
        if user and user["password"] == password:
             session["user"] = username
             return redirect(url_for("home"))
        error = "Invalid credentials"
        return render_template("login.html", error=error, msg=msg)
    return render_template("login.html", msg=msg)

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form.get("username")
        email = request.form.get("email")
        mobile = request.form.get("mobile")
        password = request.form.get("password")
        if database.get_user(username):
             error = "User already exists"
             return render_template("register.html", error=error)
        database.add_user(username, email, mobile, password)
        return redirect(url_for("login", msg="Registration successful. Please login."))
    return render_template("register.html")

@app.route("/logout")
def logout():
    session.pop("user", None)
    return redirect(url_for("login"))

@app.route("/forgot_password", methods=["GET", "POST"])
def forgot_password():
    if request.method == "POST":
        identifier = request.form.get("identifier")
        found_username = None
        for user in database.get_all_users():
            if user["username"] == identifier or user["email"] == identifier or user["mobile"] == identifier:
                found_username = user["username"]
                break
        
        if found_username:
            # Generate a mock OTP (hardcoded to 1234 for testing purposes)
            otps[found_username] = "1234"
            # In a real application, send this OTP via SMS/Email
            return redirect(url_for("reset_password", username=found_username))
            
        error = "Account not found with that mobile number, email, or username."
        return render_template("forgot_password.html", error=error)
    return render_template("forgot_password.html")

@app.route("/reset_password", methods=["GET", "POST"])
def reset_password():
    username = request.args.get("username") or request.form.get("username")
    if not username:
        return redirect(url_for("forgot_password"))
        
    if request.method == "POST":
        otp = request.form.get("otp")
        new_password = request.form.get("new_password")
        
        if username in otps and otps[username] == otp:
            database.update_password(username, new_password)
            del otps[username] # Clear OTP after success
            return redirect(url_for("login", msg="Password reset successfully! You can now login."))
        
        error = "Invalid OTP provided."
        return render_template("reset_password.html", error=error, username=username)
        
    return render_template("reset_password.html", username=username)



@app.route("/get", methods=["POST"])
def chatbot_response():
    try:
        user_msg = request.form["msg"]
        username = session.get("user", "guest")
        return get_bot_response(user_msg, username)
    except Exception as e:
        return str(e), 400

if __name__ == "__main__":
    app.run(debug=True, port=5000)