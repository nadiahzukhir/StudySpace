from flask import Blueprint, render_template
from database import get_connection
from datetime import date

#create a Blueprint for the dashboard feature
dashboard_bp = Blueprint("dashboard", __name__) 

#function to count the total number of courses
def get_total_courses():
    conn = get_connection()
    
    try:
        #count all courses in the database
        #use try because the database connection may fail
        result = conn.execute(
            "SELECT COUNT(*) AS total FROM courses"
        ).fetchone()
        
        return result["total"]
    finally:
        #close the database connection
        conn.close()
        
#count total, pending and completed tasks
def get_task_stats():
    conn = get_connection()
    
    try:
        #count all tasks
        total = conn.execute(
            "SELECT COUNT(*) AS total FROM tasks"
        ).fetchone()["total"]
        
        #count pending tasks
        pending = conn.execute(
            "SELECT COUNT(*) AS total FROM tasks WHERE status = 'Pending'"
        ).fetchone()["total"]
        
        #count completed tasks
        completed = conn.execute(
            "SELECT COUNT(*) AS total FROM tasks WHERE status = 'Completed'"
        ).fetchone()["total"]
        
        return total, pending, completed
    finally:
        #close the database connection
        conn.close()
        
#calculate the percentage of completed tasks
def get_completion_rate(total, completed):
    
    #to avoid divide by zero when there are no tasks
    if total == 0:
        return 0
    
    rate  = (completed / total) * 100
    return round(rate, 1)

#get the next 5 upcoming deadlines
def get_upcoming_deadlines():
    conn = get_connection()
    
    try:
        #get today's date
        today = date.today().isoformat()
        
        #get pending tasks that are due today or later
        tasks = conn.execute("""
            SELECT tasks.title, tasks.deadline, courses.code
            FROM tasks
            JOIN courses ON tasks.course_id = courses.id
            WHERE tasks.status = 'Pending'
            AND tasks.deadline >= ?
            ORDER BY tasks.deadline ASC
            LIMIT 5
        """, (today,)).fetchall()

        return tasks

    finally:
        conn.close()
        
#get tasks that are past their deadlines 
def get_overdue_tasks():
    conn = get_connection()
    
    try:
        today = date.today().isoformat()
        
        #find pending tasks with deadlines before today
        tasks = conn.execute("""
            SELECT tasks.title, tasks.deadline, courses.code
            FROM tasks
            JOIN courses ON tasks.course_id = courses.id
            WHERE tasks.status = 'Pending'
            AND tasks.deadline < ?
            ORDER BY tasks.deadline ASC
        """, (today,)).fetchall()

        return tasks
    
    finally:
        conn.close()

    
#display the dashboard page
@dashboard_bp.route("/")
def home():
    total_courses = get_total_courses()
    total, pending, completed = get_task_stats()

    # Calculate completion percentage
    completion_rate = get_completion_rate(total, completed)
    
    #get upcoming deadlines
    upcoming_tasks = get_upcoming_deadlines()
    
    #overdue tasks
    overdue_tasks = get_overdue_tasks()

    return render_template(
        "dashboard.html",
        total_courses=total_courses,
        total_tasks=total,
        pending_tasks=pending,
        completed_tasks=completed,
        completion_rate=completion_rate,
        upcoming_tasks=upcoming_tasks,
        overdue_tasks=overdue_tasks
    )