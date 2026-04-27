import sqlite3
import os

DB_NAME = "database.db"

def get_db_connection():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db_connection()
    c = conn.cursor()
    
    # Create Users Table
    c.execute('''
        CREATE TABLE IF NOT EXISTS users (
            username TEXT PRIMARY KEY,
            email TEXT,
            mobile TEXT,
            password TEXT,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Create Chat History Table
    c.execute('''
        CREATE TABLE IF NOT EXISTS chat_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT,
            user_msg TEXT,
            bot_response TEXT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Create Unanswered Questions Table
    c.execute('''
        CREATE TABLE IF NOT EXISTS unanswered (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT,
            query TEXT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Create Feedbacks Table
    c.execute('''
        CREATE TABLE IF NOT EXISTS feedbacks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT,
            message TEXT,
            stars INTEGER,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    
    conn.commit()
    conn.close()

    seed_dummy_data()

def seed_dummy_data():
    conn = get_db_connection()
    c = conn.cursor()

    users = [
        ("harshitha", "harshi@example.com", "9876543210", "password123"),
        ("ramesh", "ramesh@example.com", "9876543211", "ramesh@123"),
        ("priyanka", "priya@example.com", "9876543212", "priyanka11"),
        ("admin", "admin@jntugv.edu.in", "9999999999", "adminpass"),
        ("mohan", "mohan@example.com", "9876543213", "mohan123"),
    ]
    for u in users:
        try:
            c.execute('INSERT INTO users (username, email, mobile, password) VALUES (?, ?, ?, ?)', u)
        except sqlite3.IntegrityError:
            pass

    c.execute("SELECT COUNT(*) FROM chat_history")
    if c.fetchone()[0] == 0:
        chats = [
            ("harshitha", "What is the fee for B.Tech CSE?", "<strong>💰 Fee Structure & Financial Aid</strong><br><br>As a government-affiliated university...<br>• <strong>B.Tech</strong>: ₹35,000 / year"),
            ("ramesh", "Tell me about MBA placements", "<strong>💼 Placements & Career Growth</strong><br><br>Our highest package is ₹12 LPA..."),
            ("priyanka", "How do I apply for admissions?", "<strong>📝 Clear & Transparent Admission Process</strong><br><br>1. <strong>Entrance Exams</strong>: You must qualify..."),
            ("mohan", "What are the hostel facilities?", "<strong>🏫 Premium Campus Facilities</strong><br><br>Accommodations: Government-subsidized, highly secure..."),
        ]
        for ch in chats:
            c.execute('INSERT INTO chat_history (username, user_msg, bot_response) VALUES (?, ?, ?)', ch)

    c.execute("SELECT COUNT(*) FROM feedbacks")
    if c.fetchone()[0] == 0:
        feedbacks = [
            ("harshitha", "This chatbot makes finding information so much easier without navigating through complex pages.", 5),
            ("ramesh", "Good interface. But some more details on faculty would be nice.", 4),
            ("mohan", "Very helpful for new students like me looking for fee details.", 5),
            ("priyanka", "The response time is very quick. Great job!", 5),
            ("anonymous_user", "I wanted to know about sports quota but couldn't find much info.", 3),
        ]
        for fb in feedbacks:
            c.execute('INSERT INTO feedbacks (username, message, stars) VALUES (?, ?, ?)', fb)

    c.execute("SELECT COUNT(*) FROM unanswered")
    if c.fetchone()[0] == 0:
        unanswered = [
            ("priyanka", "What is the cutoff rank for ECE under sports quota?"),
            ("ramesh", "Are there any research positions available for MBA students?"),
            ("mohan", "Can I change my branch after the 1st year?"),
            ("unknown_user", "Is there a bus facility from Visakhapatnam to JNTUGV?"),
            ("harshitha", "Who is the contact person for international alumni relations?"),
        ]
        for un in unanswered:
            c.execute('INSERT INTO unanswered (username, query) VALUES (?, ?)', un)

    conn.commit()
    conn.close()

# Users
def add_user(username, email, mobile, password):
    try:
        conn = get_db_connection()
        conn.execute('INSERT INTO users (username, email, mobile, password) VALUES (?, ?, ?, ?)',
                     (username, email, mobile, password))
        conn.commit()
        conn.close()
        return True
    except sqlite3.IntegrityError:
        return False

def get_user(username):
    conn = get_db_connection()
    user = conn.execute('SELECT * FROM users WHERE username = ?', (username,)).fetchone()
    conn.close()
    return dict(user) if user else None

def get_all_users():
    conn = get_db_connection()
    users = conn.execute('SELECT * FROM users ORDER BY created_at DESC').fetchall()
    conn.close()
    return [dict(row) for row in users]

def update_password(username, new_password):
    conn = get_db_connection()
    conn.execute('UPDATE users SET password = ? WHERE username = ?', (new_password, username))
    conn.commit()
    conn.close()

# Chat
def log_chat(username, user_msg, bot_response):
    conn = get_db_connection()
    conn.execute('INSERT INTO chat_history (username, user_msg, bot_response) VALUES (?, ?, ?)',
                 (username, user_msg, bot_response))
    conn.commit()
    conn.close()

def get_chat_history(username=None):
    conn = get_db_connection()
    if username:
        chats = conn.execute('SELECT * FROM chat_history WHERE username = ? ORDER BY timestamp ASC', (username,)).fetchall()
    else:
        chats = conn.execute('SELECT * FROM chat_history ORDER BY timestamp DESC').fetchall()
    conn.close()
    return [dict(row) for row in chats]

# Unanswered
def add_unanswered(username, query):
    conn = get_db_connection()
    conn.execute('INSERT INTO unanswered (username, query) VALUES (?, ?)', (username, query))
    conn.commit()
    conn.close()

def get_unanswered():
    conn = get_db_connection()
    results = conn.execute('SELECT * FROM unanswered ORDER BY timestamp DESC').fetchall()
    conn.close()
    return [dict(row) for row in results]

# Feedback
def add_feedback(username, message, stars):
    conn = get_db_connection()
    conn.execute('INSERT INTO feedbacks (username, message, stars) VALUES (?, ?, ?)',
                 (username, message, stars))
    conn.commit()
    conn.close()

def get_feedbacks():
    conn = get_db_connection()
    results = conn.execute('SELECT * FROM feedbacks ORDER BY timestamp DESC').fetchall()
    conn.close()
    return [dict(row) for row in results]
