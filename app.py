from flask import Flask, render_template, url_for, redirect, request
from flask_login import LoginManager, login_required, current_user, login_user, logout_user

from db import get_user, save_user, get_registered_users, delete_user, update_user

app = Flask(__name__)
app.config["SECRET_KEY"] = "secret_pass_code"
login_manager = LoginManager()
login_manager.login_view = 'login'
login_manager.init_app(app)

# GROUP_ID = None

@app.route('/', methods=['GET', 'POST'])
def login():
	if current_user.is_authenticated:
		return redirect(url_for('home'))

	message = ''
	if request.method == 'POST':
		email = request.form.get('email')
		password = request.form.get('password')
		user_object = get_user(email)
		if user_object and user_object.check_password(password):
			login_user(user_object)
			return redirect(url_for('home'))
		else:
			message = 'Login Failed!'
	return render_template('login.html', message=message)

@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route("/home")
@login_required
def home():
    return render_template("base.html")

@app.route("/home/loans/")
@login_required
def loans_view():
    return render_template("loans_page.html")

@app.route("/home/payments/")
@login_required
def payments_view():
    return render_template("payments_page.html")

@app.route("/home/borrowers/")
@login_required
def borrowers_view():
    return render_template("borrowers_page.html")

@app.route("/home/loan_plans/")
@login_required
def loan_plans_view():
    return render_template("loan_plans_page.html")

@app.route("/home/loan_types/")
@login_required
def loan_types_view():
    return render_template("loan_types_page.html")

@app.route("/home/users/", methods=['GET', 'POST'])
@login_required
def users_view():
	if request.method == 'POST':
		first_name = request.form.get('first_name')
		last_name = request.form.get('last_name')
		email = request.form.get('email')
		password = request.form.get('password')
		has_permission = True if request.form.get('has_permission') != None else False
		try:
			save_user(first_name, last_name, email, password, has_permission)
		except Exception as e:
			print("[EXCEPTION] ", e)
	members = get_registered_users()
	return render_template("users_page.html", members=members)

@app.route("/home/users/edit", methods=['GET', 'POST'])
def edit_member():
	if request.method == 'POST':
		email = request.form.get('edit_button_email_input')
		current_member = get_user(email)
		if current_member:
			return render_template("users_page_update.html", current_member=current_member)
		else:
			print("Email Adress does not exist!")
	return redirect(url_for('users_view'))

@app.route("/home/users/update", methods=['GET', 'POST'])
def update_member():
	if request.method == 'POST':
		first_name = request.form.get('first_name')
		last_name = request.form.get('last_name')
		email = request.form.get('email')
		password = request.form.get('password')
		has_permission = True if request.form.get('has_permission') != None else False
		update_user(first_name, last_name, email, password, has_permission)
	return redirect(url_for('users_view'))


@app.route("/delete-user", methods=['GET', 'POST'])
def remove_a_user():
	if request.method == 'POST':
		email = request.form.get('delete_button_email_input')
		if get_user(email):
			delete_user(email)
			return redirect(url_for('users_view'))
	return redirect(url_for('users_view'))

@login_manager.user_loader
def load_user(email):
    return get_user(email)

if __name__ == "__main__":
    app.run(debug=True)
