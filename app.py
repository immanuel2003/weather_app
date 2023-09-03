from flask import Flask, render_template, request, redirect, url_for
from flask_login import LoginManager, UserMixin, login_user, login_required, current_user, logout_user
from weather import main as get_weather

app = Flask(__name__)
app.secret_key = "RAPTOR@1992"

login_manager = LoginManager()
login_manager.init_app(app)

#for demonstration purposes
users = {
    'immanuel2003': {'password': 'raptor@1992'},
    'immanuelsiangla': {'password': '8040'},
}

class User(UserMixin):
    def __init__(self, username):
        self.id = username
        
@login_manager.user_loader
def load_user(username):
    return User(username)

@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']

    user_data = users.get(username)
    if user_data and user_data['password'] == password:
        user = User(username)
        login_user(user)
        return redirect(url_for('index'))

    return redirect(url_for('index'))

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/', methods=['GET', 'POST']) 
def index():
    data = None
    if request.method == 'POST':
        city = request.form['CityName']
        state = request.form["StateName"]
        country = request.form["CountryName"]
        data = get_weather(city, state, country)
        
    return render_template('index.html', data=data)

if __name__ == '__main__':
    app.run(debug=True)
