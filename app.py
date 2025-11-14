#!/usr/bin/env python3
"""
Action Items Tracker - Manager Dashboard
A web application to track action items for employees under a manager
"""

from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
import sqlite3
from datetime import datetime, timedelta
import os

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'dev-secret-key-change-in-production')

DATABASE = 'action_items.db'

def get_db():
    """Get database connection"""
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    """Initialize database with tables"""
    conn = get_db()
    cursor = conn.cursor()
    
    # Create managers table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS managers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Create employees table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS employees (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            manager_id INTEGER NOT NULL,
            position TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (manager_id) REFERENCES managers (id)
        )
    ''')
    
    # Create action_items table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS action_items (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            description TEXT,
            employee_id INTEGER NOT NULL,
            manager_id INTEGER NOT NULL,
            status TEXT DEFAULT 'pending',
            priority TEXT DEFAULT 'medium',
            due_date DATE,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            completed_at TIMESTAMP,
            FOREIGN KEY (employee_id) REFERENCES employees (id),
            FOREIGN KEY (manager_id) REFERENCES managers (id)
        )
    ''')
    
    conn.commit()
    conn.close()

@app.route('/')
def index():
    """Home page - Dashboard"""
    conn = get_db()
    cursor = conn.cursor()
    
    # Get statistics
    stats = {
        'total_managers': cursor.execute('SELECT COUNT(*) FROM managers').fetchone()[0],
        'total_employees': cursor.execute('SELECT COUNT(*) FROM employees').fetchone()[0],
        'total_actions': cursor.execute('SELECT COUNT(*) FROM action_items').fetchone()[0],
        'pending_actions': cursor.execute("SELECT COUNT(*) FROM action_items WHERE status='pending'").fetchone()[0],
        'completed_actions': cursor.execute("SELECT COUNT(*) FROM action_items WHERE status='completed'").fetchone()[0],
    }
    
    # Get recent action items
    recent_actions = cursor.execute('''
        SELECT ai.*, e.name as employee_name, m.name as manager_name
        FROM action_items ai
        JOIN employees e ON ai.employee_id = e.id
        JOIN managers m ON ai.manager_id = m.id
        ORDER BY ai.created_at DESC
        LIMIT 10
    ''').fetchall()
    
    conn.close()
    return render_template('index.html', stats=stats, recent_actions=recent_actions)

@app.route('/managers')
def managers():
    """List all managers"""
    conn = get_db()
    cursor = conn.cursor()
    managers_list = cursor.execute('''
        SELECT m.*, COUNT(e.id) as employee_count
        FROM managers m
        LEFT JOIN employees e ON m.id = e.manager_id
        GROUP BY m.id
        ORDER BY m.name
    ''').fetchall()
    conn.close()
    return render_template('managers.html', managers=managers_list)

@app.route('/managers/add', methods=['GET', 'POST'])
def add_manager():
    """Add new manager"""
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        
        if not name or not email:
            flash('Name and email are required', 'error')
            return redirect(url_for('add_manager'))
        
        try:
            conn = get_db()
            cursor = conn.cursor()
            cursor.execute('INSERT INTO managers (name, email) VALUES (?, ?)', (name, email))
            conn.commit()
            conn.close()
            flash('Manager added successfully', 'success')
            return redirect(url_for('managers'))
        except sqlite3.IntegrityError:
            flash('Email already exists', 'error')
            return redirect(url_for('add_manager'))
    
    return render_template('add_manager.html')

@app.route('/managers/<int:manager_id>')
def manager_detail(manager_id):
    """View manager details and their team"""
    conn = get_db()
    cursor = conn.cursor()
    
    manager = cursor.execute('SELECT * FROM managers WHERE id = ?', (manager_id,)).fetchone()
    if not manager:
        flash('Manager not found', 'error')
        return redirect(url_for('managers'))
    
    employees = cursor.execute('''
        SELECT e.*, COUNT(ai.id) as action_count
        FROM employees e
        LEFT JOIN action_items ai ON e.id = ai.employee_id
        WHERE e.manager_id = ?
        GROUP BY e.id
        ORDER BY e.name
    ''', (manager_id,)).fetchall()
    
    action_items = cursor.execute('''
        SELECT ai.*, e.name as employee_name
        FROM action_items ai
        JOIN employees e ON ai.employee_id = e.id
        WHERE ai.manager_id = ?
        ORDER BY ai.due_date, ai.priority DESC
    ''', (manager_id,)).fetchall()
    
    conn.close()
    return render_template('manager_detail.html', manager=manager, employees=employees, action_items=action_items)

@app.route('/employees')
def employees():
    """List all employees"""
    conn = get_db()
    cursor = conn.cursor()
    employees_list = cursor.execute('''
        SELECT e.*, m.name as manager_name, COUNT(ai.id) as action_count
        FROM employees e
        JOIN managers m ON e.manager_id = m.id
        LEFT JOIN action_items ai ON e.id = ai.employee_id
        GROUP BY e.id
        ORDER BY e.name
    ''').fetchall()
    conn.close()
    return render_template('employees.html', employees=employees_list)

@app.route('/employees/add', methods=['GET', 'POST'])
def add_employee():
    """Add new employee"""
    conn = get_db()
    cursor = conn.cursor()
    
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        manager_id = request.form.get('manager_id')
        position = request.form.get('position')
        
        if not name or not email or not manager_id:
            flash('Name, email, and manager are required', 'error')
            return redirect(url_for('add_employee'))
        
        try:
            cursor.execute('INSERT INTO employees (name, email, manager_id, position) VALUES (?, ?, ?, ?)',
                         (name, email, manager_id, position))
            conn.commit()
            flash('Employee added successfully', 'success')
            return redirect(url_for('employees'))
        except sqlite3.IntegrityError:
            flash('Email already exists', 'error')
        finally:
            conn.close()
        return redirect(url_for('add_employee'))
    
    managers_list = cursor.execute('SELECT * FROM managers ORDER BY name').fetchall()
    conn.close()
    return render_template('add_employee.html', managers=managers_list)

@app.route('/employees/<int:employee_id>')
def employee_detail(employee_id):
    """View employee details and their action items"""
    conn = get_db()
    cursor = conn.cursor()
    
    employee = cursor.execute('''
        SELECT e.*, m.name as manager_name
        FROM employees e
        JOIN managers m ON e.manager_id = m.id
        WHERE e.id = ?
    ''', (employee_id,)).fetchone()
    
    if not employee:
        flash('Employee not found', 'error')
        return redirect(url_for('employees'))
    
    action_items = cursor.execute('''
        SELECT * FROM action_items
        WHERE employee_id = ?
        ORDER BY due_date, priority DESC
    ''', (employee_id,)).fetchall()
    
    conn.close()
    return render_template('employee_detail.html', employee=employee, action_items=action_items)

@app.route('/actions')
def actions():
    """List all action items"""
    status_filter = request.args.get('status', 'all')
    priority_filter = request.args.get('priority', 'all')
    
    conn = get_db()
    cursor = conn.cursor()
    
    query = '''
        SELECT ai.*, e.name as employee_name, m.name as manager_name
        FROM action_items ai
        JOIN employees e ON ai.employee_id = e.id
        JOIN managers m ON ai.manager_id = m.id
        WHERE 1=1
    '''
    params = []
    
    if status_filter != 'all':
        query += ' AND ai.status = ?'
        params.append(status_filter)
    
    if priority_filter != 'all':
        query += ' AND ai.priority = ?'
        params.append(priority_filter)
    
    query += ' ORDER BY ai.due_date, ai.priority DESC'
    
    action_items = cursor.execute(query, params).fetchall()
    conn.close()
    
    return render_template('actions.html', action_items=action_items, 
                         status_filter=status_filter, priority_filter=priority_filter)

@app.route('/actions/add', methods=['GET', 'POST'])
def add_action():
    """Add new action item"""
    conn = get_db()
    cursor = conn.cursor()
    
    if request.method == 'POST':
        title = request.form.get('title')
        description = request.form.get('description')
        employee_id = request.form.get('employee_id')
        priority = request.form.get('priority', 'medium')
        due_date = request.form.get('due_date')
        
        if not title or not employee_id:
            flash('Title and employee are required', 'error')
            return redirect(url_for('add_action'))
        
        # Get manager_id from employee
        employee = cursor.execute('SELECT manager_id FROM employees WHERE id = ?', (employee_id,)).fetchone()
        if not employee:
            flash('Employee not found', 'error')
            return redirect(url_for('add_action'))
        
        cursor.execute('''
            INSERT INTO action_items (title, description, employee_id, manager_id, priority, due_date)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (title, description, employee_id, employee['manager_id'], priority, due_date))
        conn.commit()
        conn.close()
        
        flash('Action item added successfully', 'success')
        return redirect(url_for('actions'))
    
    employees_list = cursor.execute('''
        SELECT e.*, m.name as manager_name
        FROM employees e
        JOIN managers m ON e.manager_id = m.id
        ORDER BY e.name
    ''').fetchall()
    conn.close()
    
    return render_template('add_action.html', employees=employees_list)

@app.route('/actions/<int:action_id>/update', methods=['POST'])
def update_action(action_id):
    """Update action item status"""
    status = request.form.get('status')
    
    conn = get_db()
    cursor = conn.cursor()
    
    if status == 'completed':
        cursor.execute('''
            UPDATE action_items 
            SET status = ?, completed_at = CURRENT_TIMESTAMP, updated_at = CURRENT_TIMESTAMP
            WHERE id = ?
        ''', (status, action_id))
    else:
        cursor.execute('''
            UPDATE action_items 
            SET status = ?, updated_at = CURRENT_TIMESTAMP
            WHERE id = ?
        ''', (status, action_id))
    
    conn.commit()
    conn.close()
    
    flash('Action item updated successfully', 'success')
    return redirect(request.referrer or url_for('actions'))

@app.route('/actions/<int:action_id>/delete', methods=['POST'])
def delete_action(action_id):
    """Delete action item"""
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM action_items WHERE id = ?', (action_id,))
    conn.commit()
    conn.close()
    
    flash('Action item deleted successfully', 'success')
    return redirect(request.referrer or url_for('actions'))

@app.route('/api/stats')
def api_stats():
    """API endpoint for statistics"""
    conn = get_db()
    cursor = conn.cursor()
    
    stats = {
        'managers': cursor.execute('SELECT COUNT(*) FROM managers').fetchone()[0],
        'employees': cursor.execute('SELECT COUNT(*) FROM employees').fetchone()[0],
        'total_actions': cursor.execute('SELECT COUNT(*) FROM action_items').fetchone()[0],
        'pending': cursor.execute("SELECT COUNT(*) FROM action_items WHERE status='pending'").fetchone()[0],
        'in_progress': cursor.execute("SELECT COUNT(*) FROM action_items WHERE status='in_progress'").fetchone()[0],
        'completed': cursor.execute("SELECT COUNT(*) FROM action_items WHERE status='completed'").fetchone()[0],
    }
    
    conn.close()
    return jsonify(stats)

@app.route('/health')
def health():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.now().isoformat(),
        'database': 'connected' if os.path.exists(DATABASE) else 'not_initialized'
    })

if __name__ == '__main__':
    # Initialize database on first run
    if not os.path.exists(DATABASE):
        print("Initializing database...")
        init_db()
        print("Database initialized successfully!")
    
    port = int(os.environ.get('PORT', 8000))
    app.run(host='0.0.0.0', port=port, debug=False)
