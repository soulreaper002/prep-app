# Save this code as app.py
from flask import Flask, jsonify, render_template, request
import calendar
from datetime import date, timedelta
import json

app = Flask(__name__)

# --- SCHEDULE AND RESOURCE DATA GENERATION (Unchanged) ---
def generate_complete_schedule():
    schedule = {}
    start_date = date(2025, 8, 22)
    deadline = date(2025, 9, 15)
    sprint_pattern = {
        0: [{"time": "11:30 - 15:30", "topic": "AZ-900 Sprint: Core Concepts", "resource": "Microsoft Learn AZ-900"}, {"time": "16:00 - 17:00", "topic": "Light DSA: Arrays", "resource": "LeetCode Patterns"}],
        1: [{"time": "11:30 - 15:30", "topic": "AZ-900 Sprint: Azure Services", "resource": "Microsoft Learn AZ-900"}, {"time": "16:00 - 17:00", "topic": "Light DSA: Arrays", "resource": "LeetCode Patterns"}],
        2: [{"time": "11:30 - 15:30", "topic": "AZ-900 Sprint: Security & Networking", "resource": "Microsoft Learn AZ-900"}, {"time": "16:00 - 17:00", "topic": "Light DSA: Strings", "resource": "LeetCode Patterns"}],
        3: [{"time": "11:30 - 15:30", "topic": "AZ-900 Sprint: Governance", "resource": "Microsoft Learn AZ-900"}, {"time": "16:00 - 17:00", "topic": "Light DSA: Strings", "resource": "LeetCode Patterns"}],
        4: [{"time": "11:30 - 15:30", "topic": "AZ-900 Sprint: Cost & SLAs", "resource": "Microsoft Learn AZ-900"}, {"time": "16:00 - 17:00", "topic": "Resume Review", "resource": "Resume Worded"}],
        5: [{"time": "12:00 - 15:00", "topic": "AZ-900 Practice Exam & Review", "resource": "Microsoft Learn AZ-900"}],
        6: [{"time": "12:00 - 15:00", "topic": "AZ-900 Practice Exam & Review", "resource": "Microsoft Learn AZ-900"}],
    }
    maang_patterns = {
        "months_1_2": {
            0: [{"time": "11:30 - 13:30", "topic": "DSA: Linked Lists & Stacks", "resource": "LeetCode Patterns"}, {"time": "14:30 - 16:00", "topic": "DevOps: CI/CD Concepts", "resource": "DevOps Free Course"}],
            1: [{"time": "11:30 - 13:30", "topic": "DSA: Trees & Tries", "resource": "LeetCode Patterns"}, {"time": "14:30 - 16:00", "topic": "DevOps: Source Control (Git)", "resource": "DevOps Free Course"}],
            2: [{"time": "11:30 - 13:30", "topic": "DSA: Heaps & Priority Queues", "resource": "LeetCode Patterns"}, {"time": "14:30 - 16:00", "topic": "DevOps: Infrastructure as Code", "resource": "DevOps Free Course"}],
            3: [{"time": "11:30 - 13:30", "topic": "DSA: Graphs (BFS, DFS)", "resource": "GeeksforGeeks"}, {"time": "14:30 - 16:00", "topic": "DevOps: Containers (Docker)", "resource": "DevOps Free Course"}],
            4: [{"time": "11:30 - 13:30", "topic": "DSA: Mixed Review of Week", "resource": "LeetCode Patterns"}],
            5: [{"time": "12:00 - 14:00", "topic": "Weekly Review & LeetCode Contest", "resource": "LeetCode Patterns"}],
            6: []
        },
        "months_3_4": {
            0: [{"time": "11:30 - 13:30", "topic": "Algorithms: Dynamic Programming", "resource": "LeetCode Patterns"}, {"time": "14:30 - 16:00", "topic": "System Design: Fundamentals", "resource": "System Design Primer"}],
            1: [{"time": "11:30 - 13:30", "topic": "Algorithms: Backtracking", "resource": "LeetCode Patterns"}, {"time": "14:30 - 16:00", "topic": "System Design: Case Study (TinyURL)", "resource": "ByteByteGo YouTube"}],
            2: [{"time": "11:30 - 13:30", "topic": "Algorithms: Advanced Graphs", "resource": "GeeksforGeeks"}, {"time": "14:30 - 16:00", "topic": "Behavioral Prep: STAR Method", "resource": "Interviewing.io Blog"}],
            3: [{"time": "11:30 - 13:30", "topic": "DSA: Mixed Hard Problems", "resource": "LeetCode Patterns"}, {"time": "14:30 - 16:00", "topic": "System Design: Case Study (News Feed)", "resource": "ByteByteGo YouTube"}],
            4: [{"time": "11:30 - 13:30", "topic": "Algorithms: Review of Week", "resource": "LeetCode Patterns"}],
            5: [{"time": "12:00 - 14:00", "topic": "Mock Coding Interview", "resource": "Pramp"}],
            6: []
        }
    }
    for i in range(200):
        current_date = start_date + timedelta(days=i)
        day_of_week = current_date.weekday()
        date_str = current_date.strftime("%Y-%m-%d")
        if current_date <= deadline: pattern = sprint_pattern
        else:
            days_past_deadline = (current_date - deadline).days
            if days_past_deadline <= 75: pattern = maang_patterns["months_1_2"]
            else: pattern = maang_patterns["months_3_4"]
        if pattern.get(day_of_week): schedule[date_str] = pattern[day_of_week]
    return schedule

RESOURCES = [
    {"topic": "DSA", "name": "LeetCode Patterns", "link": "https://seanprashad.com/leetcode-patterns/", "desc": "A curated list of common problem patterns for coding interviews."},
    {"topic": "System Design", "name": "ByteByteGo YouTube", "link": "https://www.youtube.com/@ByteByteGo", "desc": "Excellent, concise videos explaining complex system design concepts."},
    {"topic": "Behavioral Prep", "name": "Interviewing.io Blog", "link": "https://interviewing.io/blog", "desc": "Actionable advice and real data on technical and behavioral interviews."},
    {"topic": "Resume Building", "name": "Resume Worded", "link": "https://resumeworded.com/", "desc": "AI-powered tool to score and improve your resume and LinkedIn profile."},
    {"topic": "Mock Interviews", "name": "Pramp", "link": "https://www.pramp.com/", "desc": "Free, anonymous peer-to-peer mock interviews for developers."},
    {"topic": "System Design", "name": "System Design Primer", "link": "https://github.com/donnemartin/system-design-primer", "desc": "The ultimate GitHub repo for learning how to design large-scale systems."},
    {"topic": "DSA", "name": "GeeksforGeeks", "link": "https://www.geeksforgeeks.org/data-structures/", "desc": "A vast library of data structure and algorithm articles and problems."},
    {"topic": "Certification", "name": "Microsoft Learn AZ-900", "link": "https://learn.microsoft.com/en-us/training/paths/azure-fundamentals-describe-cloud-concepts/", "desc": "Official learning path for the Azure Fundamentals certification."},
    {"topic": "DevOps", "name": "DevOps Free Course", "link": "https://www.youtube.com/watch?v=j5Zsa_eOXeY", "desc": "A comprehensive video course covering DevOps principles and tools."}
]
SCHEDULE_DATA = generate_complete_schedule()

# --- App Routes (Unchanged) ---
@app.route('/')
def calendar_page():
    return render_template('index.html')

@app.route('/resources')
def resources_page():
    return render_template('resources.html', resources=RESOURCES)

# --- API Endpoints ---
@app.route('/api/schedule/day/<date_str>')
def get_day_schedule(date_str): return jsonify(SCHEDULE_DATA.get(date_str, []))

@app.route('/api/resources')
def get_resources_api(): return jsonify(RESOURCES)

# --- NEW API Endpoint for Calendar Data ---
@app.route('/api/calendar_data')
def get_calendar_data():
    year = request.args.get('year', date.today().year, type=int)
    month = request.args.get('month', date.today().month, type=int)
    
    # Get month details from Python's calendar module
    # calendar.setfirstweekday(calendar.MONDAY) # Set week start to Monday
    first_weekday, num_days = calendar.monthrange(year, month)
    month_name = calendar.month_name[month]
    
    # Filter schedule for the current month view
    month_schedule = {
        k: v for k, v in SCHEDULE_DATA.items()
        if k.startswith(f"{year}-{month:02d}")
    }
    
    return jsonify({
        'year': year,
        'month': month,
        'monthName': month_name,
        'firstWeekday': first_weekday, # 0=Mon, 1=Tue, ..., 6=Sun
        'numDays': num_days,
        'schedule': month_schedule
    })

if __name__ == '__main__':
    app.run(debug=True)