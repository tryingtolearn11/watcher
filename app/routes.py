from app import app



@app.route('/')
@app.route('/index')
def index():
    return "Index PAGE"








@app.route('/login')
def login():
    return "LOGIN PAGE"


