# Save this code as app.py
from flask import Flask, jsonify, render_template, request
import calendar
from datetime import date, timedelta
import json

app = Flask(__name__)

# --- REFINED SCHEDULE & RESOURCE DATA ---
def generate_senior_schedule_with_balanced_start():
    schedule = {}
    start_date = date(2025, 8, 22)
    deadline = date(2025, 9, 15)

    # Phase 1: Dual-Track Sprint (DSA Basics + AZ-900)
    sprint_pattern = {
        # Week 1 (Aug 22-24) - Getting Started
        4: [{"time": "11:30 - 13:30", "topic": "DSA Basics: Arrays & Two Pointers", "resource": "LeetCode Patterns"}, {"time": "14:30 - 17:00", "topic": "AZ-900 Sprint: Core Concepts", "resource": "Microsoft Learn AZ-900"}], # Fri
        5: [{"time": "12:00 - 15:00", "topic": "AZ-900 Practice Questions & Review", "resource": "Microsoft Learn AZ-900"}], # Sat
        6: [{"time": "12:00 - 15:00", "topic": "AZ-900 Practice Questions & Review", "resource": "Microsoft Learn AZ-900"}], # Sun

        # Week 2 (Aug 25-31) - Arrays & Strings
        0: [{"time": "11:30 - 13:30", "topic": "DSA Basics: Arrays & Sliding Window", "resource": "LeetCode Patterns"}, {"time": "14:30 - 17:00", "topic": "AZ-900 Sprint: Azure Services", "resource": "Microsoft Learn AZ-900"}],
        1: [{"time": "11:30 - 13:30", "topic": "DSA Basics: String Manipulation", "resource": "LeetCode Patterns"}, {"time": "14:30 - 17:00", "topic": "AZ-900 Sprint: Security", "resource": "Microsoft Learn AZ-900"}],
        2: [{"time": "11:30 - 13:30", "topic": "DSA Practice: Arrays & Strings", "resource": "LeetCode Patterns"}, {"time": "14:30 - 17:00", "topic": "AZ-900 Sprint: Networking", "resource": "Microsoft Learn AZ-900"}],
        3: [{"time": "11:30 - 13:30", "topic": "Behavioral: Prep STAR stories", "resource": "Senior Behavioral Prep"}, {"time": "14:30 - 17:00", "topic": "AZ-900 Sprint: Governance", "resource": "Microsoft Learn AZ-900"}],
        4: [{"time": "11:30 - 13:30", "topic": "DSA Basics: Hashing", "resource": "LeetCode Patterns"}, {"time": "14:30 - 17:00", "topic": "AZ-900 Sprint: Cost & SLAs", "resource": "Microsoft Learn AZ-900"}],
        5: [{"time": "12:00 - 15:00", "topic": "AZ-900 Full Practice Exam", "resource": "Microsoft Learn AZ-900"}],
        6: [{"time": "12:00 - 15:00", "topic": "AZ-900 Exam Review & Weak Areas", "resource": "Microsoft Learn AZ-900"}],

        # Week 3 (Sep 1-7) - Linked Lists, Stacks, Queues
        0: [{"time": "11:30 - 13:30", "topic": "DSA Basics: Linked Lists", "resource": "LeetCode Patterns"}, {"time": "14:30 - 17:00", "topic": "AZ-900 Sprint: Review Core Concepts", "resource": "Microsoft Learn AZ-900"}],
        1: [{"time": "11:30 - 13:30", "topic": "DSA Basics: Stacks (Monotonic)", "resource": "LeetCode Patterns"}, {"time": "14:30 - 17:00", "topic": "AZ-900 Sprint: Review Services", "resource": "Microsoft Learn AZ-900"}],
        2: [{"time": "11:30 - 13:30", "topic": "DSA Basics: Queues (BFS Intro)", "resource": "GeeksforGeeks"}, {"time": "14:30 - 17:00", "topic": "AZ-900 Sprint: Review Security", "resource": "Microsoft Learn AZ-900"}],
        3: [{"time": "11:30 - 13:30", "topic": "DSA Practice: LL, Stacks, Queues", "resource": "LeetCode Patterns"}, {"time": "14:30 - 17:00", "topic": "AZ-900 Sprint: Final Review", "resource": "Microsoft Learn AZ-900"}],
        4: [{"time": "11:30 - 13:30", "topic": "DSA Basics: Review Week's Topics", "resource": "LeetCode Patterns"}, {"time": "14:30 - 17:00", "topic": "AZ-900 Sprint: Final Review", "resource": "Microsoft Learn AZ-900"}],
        5: [{"time": "12:00 - 15:00", "topic": "AZ-900 Full Practice Exam", "resource": "Microsoft Learn AZ-900"}],
        6: [{"time": "12:00 - 15:00", "topic": "AZ-900 Exam Review & Weak Areas", "resource": "Microsoft Learn AZ-900"}],

        # Week 4 (Sep 8-15) - Final Push
        0: [{"time": "11:30 - 13:30", "topic": "DSA Review: All Basics", "resource": "LeetCode Patterns"}, {"time": "14:30 - 17:00", "topic": "AZ-900: Final Review & Practice", "resource": "Microsoft Learn AZ-900"}],
        1: [{"time": "11:30 - 13:30", "topic": "DSA Review: All Basics", "resource": "LeetCode Patterns"}, {"time": "14:30 - 17:00", "topic": "AZ-900: Final Review & Practice", "resource": "Microsoft Learn AZ-900"}],
        # ... and so on until the 15th
    }
    
    # Phase 2: Post-Certification - DSA Relaunch (Medium Focus)
    dsa_relaunch_pattern = {
        0: [{"time": "11:30 - 13:30", "topic": "Medium DSA: Two Pointers & Sliding Window", "resource": "LeetCode Patterns"}, {"time": "14:30 - 16:00", "topic": "System Design: Fundamentals", "resource": "System Design Primer"}],
        1: [{"time": "11:30 - 13:30", "topic": "Medium DSA: Binary Search & Variations", "resource": "LeetCode Patterns"}, {"time": "14:30 - 16:00", "topic": "Java: Concurrency & Multithreading", "resource": "Baeldung Java Concurrency"}],
        2: [{"time": "11:30 - 13:30", "topic": "Medium DSA: Trees (BFS, DFS, Traversals)", "resource": "LeetCode Patterns"}, {"time": "14:30 - 16:00", "topic": "System Design: Case Study (TinyURL)", "resource": "Alex Xu System Design"}],
        3: [{"time": "11:30 - 13:30", "topic": "Medium DSA: Heaps & Priority Queues", "resource": "LeetCode Patterns"}, {"time": "14:30 - 16:00", "topic": "Behavioral: Project Deep Dives", "resource": "Senior Behavioral Prep"}],
        4: [{"time": "11:30 - 13:30", "topic": "Medium DSA: Graphs (BFS, DFS)", "resource": "GeeksforGeeks"}],
        5: [{"time": "12:00 - 14:00", "topic": "LeetCode Contest (Focus on Mediums)", "resource": "LeetCode Patterns"}],
        6: []
    }

    # Phase 3 & 4 (Unchanged)
    advanced_pattern = {
        0: [{"time": "11:30 - 13:00", "topic": "Hard DSA: Dynamic Programming", "resource": "LeetCode Patterns"}, {"time": "14:00 - 16:00", "topic": "System Design: Case Study (Social Feed)", "resource": "Alex Xu System Design"}],
        1: [{"time": "11:30 - 13:00", "topic": "Hard DSA: Advanced Graphs", "resource": "LeetCode Patterns"}, {"time": "14:00 - 16:00", "topic": "Mock Coding Interview", "resource": "Pramp"}],
        2: [{"time": "11:30 - 13:00", "topic": "DSA: Review Weak Area (Medium/Hard)", "resource": "LeetCode Patterns"}, {"time": "14:00 - 16:00", "topic": "System Design: Read Eng Blog", "resource": "Top Engineering Blogs"}],
        3: [{"time": "11:30 - 13:00", "topic": "Behavioral: Leadership & Influence", "resource": "Senior Behavioral Prep"}, {"time": "14:00 - 16:00", "topic": "Mock System Design Interview", "resource": "Pramp"}],
        4: [{"time": "11:30 - 13:00", "topic": "Company-Specific DSA (Atlassian)", "resource": "LeetCode Patterns"}],
        5: [{"time": "12:00 - 15:00", "topic": "Full Mock Interview Loop", "resource": "Pramp"}],
        6: []
    }
    final_pattern = {
        0: [{"time": "11:30 - 13:00", "topic": "Company-Specific DSA (Google)", "resource": "LeetCode Patterns"}, {"time": "14:00 - 15:00", "topic": "Apply & Network"}],
        1: [{"time": "11:30 - 13:00", "topic": "Company-Specific DSA (Amazon)", "resource": "LeetCode Patterns"}, {"time": "14:00 - 16:00", "topic": "System Design Review"}],
        2: [{"time": "11:30 - 13:00", "topic": "Company-Specific DSA (Microsoft)", "resource": "LeetCode Patterns"}, {"time": "14:00 - 15:00", "topic": "Follow-ups"}],
        3: [{"time": "11:30 - 13:00", "topic": "Final Behavioral Prep"}, {"time": "14:00 - 16:00", "topic": "Mock Interview with a Professional"}],
        4: [{"time": "11:30 - 13:00", "topic": "Relax & Light Review"}],
        5: [{"time": "12:00 - 14:00", "topic": "Final Project Code Review"}],
        6: []
    }

    for i in range(200):
        current_date = start_date + timedelta(days=i)
        day_of_week = current_date.weekday()
        date_str = current_date.strftime("%Y-%m-%d")
        
        if current_date <= deadline:
            day_pattern = sprint_pattern.get(day_of_week)
            # Handle cases where the pattern might not exist for a specific day of week
            if day_of_week not in sprint_pattern:
                day_pattern = sprint_pattern.get(0) # Default to Monday pattern if missing
            if day_pattern:
                schedule[date_str] = day_pattern

        else:
            days_past_deadline = (current_date - deadline).days
            if days_past_deadline <= 60:
                pattern = dsa_relaunch_pattern
            elif days_past_deadline <= 120:
                pattern = advanced_pattern
            else:
                pattern = final_pattern
            
            if pattern.get(day_of_week):
                schedule[date_str] = pattern[day_of_week]
                
    return schedule

RESOURCES = [
    {"topic": "DSA", "name": "LeetCode Patterns", "link": "https://seanprashad.com/leetcode-patterns/", "desc": "Crucial for recognizing problem types under pressure. Focus on Medium/Hard."},
    {"topic": "System Design", "name": "Alex Xu System Design", "link": "https://www.youtube.com/@ByteByteGo", "desc": "Gold standard for senior roles. Covers fundamentals and complex case studies."},
    {"topic": "Java", "name": "Baeldung Java Concurrency", "link": "https://www.baeldung.com/java-concurrency", "desc": "Essential reading for Java backend roles to master multithreading concepts."},
    {"topic": "System Design", "name": "System Design Primer", "link": "https://github.com/donnemartin/system-design-primer", "desc": "The ultimate GitHub repo for learning how to design large-scale systems."},
    {"topic": "Behavioral", "name": "Senior Behavioral Prep", "link": "https://interviewing.io/blog/behavioral-interview-questions-seniors-staff-principal-engineers", "desc": "Covers questions about leadership, impact, and ambiguity for senior roles."},
    {"topic": "Mock Interviews", "name": "Pramp", "link": "https://www.pramp.com/", "desc": "Practice full loops (Coding + System Design) with experienced peers."},
    {"topic": "System Design", "name": "Top Engineering Blogs", "link": "https://github.com/kilimchoi/engineering-blogs", "desc": "Demonstrates real-world trade-offs. Required reading for senior candidates."},
    {"topic": "Certification", "name": "Microsoft Learn AZ-900", "link": "https://learn.microsoft.com/en-us/training/paths/azure-fundamentals-describe-cloud-concepts/", "desc": "Official learning path for the Azure Fundamentals certification."},
    {"topic": "DSA", "name": "GeeksforGeeks", "link": "https://www.geeksforgeeks.org/data-structures/", "desc": "A vast library of data structure and algorithm articles and problems."},
    {"topic": "Resume", "name": "Resume Worded", "link": "https://resumeworded.com/", "desc": "Optimize your resume for senior roles and ATS."}
]
SCHEDULE_DATA = generate_senior_schedule_with_balanced_start()

# --- App Routes & API Endpoints (Unchanged) ---
@app.route('/')
def calendar_page(): return render_template('index.html')

@app.route('/resources')
def resources_page(): return render_template('resources.html', resources=RESOURCES)

@app.route('/api/schedule/day/<date_str>')
def get_day_schedule(date_str): return jsonify(SCHEDULE_DATA.get(date_str, []))

@app.route('/api/resources')
def get_resources_api(): return jsonify(RESOURCES)

@app.route('/api/calendar_data')
def get_calendar_data():
    year = request.args.get('year', date.today().year, type=int)
    month = request.args.get('month', date.today().month, type=int)
    
    first_weekday, num_days = calendar.monthrange(year, month)
    month_name = calendar.month_name[month]
    
    month_schedule = {
        k: v for k, v in SCHEDULE_DATA.items()
        if k.startswith(f"{year}-{month:02d}")
    }
    
    return jsonify({
        'year': year, 'month': month, 'monthName': month_name,
        'firstWeekday': first_weekday,
        'numDays': num_days, 'schedule': month_schedule
    })

if __name__ == '__main__':
    app.run(debug=True)