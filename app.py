from flask import Flask, render_template, url_for, redirect, request
from flask_login import LoginManager, login_required, current_user, login_user, logout_user
from pymongo.errors import DuplicateKeyError

from db import get_user, save_user, get_registered_users, delete_user, update_user, \
	save_loan_plan, get_all_loan_plans, get_a_loan_plan, delete_a_loan_plan, \
	save_loan_type, get_all_loan_types, get_a_loan_type, delete_a_loan_type, \
	save_borrower, get_all_borrowers, delete_a_borrower, get_a_borrower, \
	get_borrower_with_tax_id

app = Flask(__name__)
app.config["SECRET_KEY"] = "secret_pass_code"
login_manager = LoginManager()
login_manager.login_view = 'login'
login_manager.init_app(app)


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
			message = 'Login failed, please check your credentials!'
	return render_template('login.html', message=message)


@app.route("/signup", methods=['GET', 'POST'])
def signup():
	if current_user.is_authenticated:
		return redirect(url_for('home'))

	message = ''
	if request.method == 'POST':
		first_name = request.form.get('first_name')
		last_name = request.form.get('last_name')
		email = request.form.get('email')
		password = request.form.get('password')
		try:
			save_user(first_name, last_name, email, password)
			return redirect(url_for('login'))
		except DuplicateKeyError:
			message = 'User already exists!'
	return render_template('signup.html', message=message)


@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))


@app.route("/home")
@login_required
def home():
    return render_template("base.html")


@app.route("/home/loans/", methods=['GET', 'POST'])
@login_required
def loans_view():
	if request.method == 'POST':
		loan_borrower = request.form.get('loans_borrowers_input')
		loan_type = request.form.get('loans_loan_type_input')
		loan_plan = request.form.get('loans_loan_plan_input')
		loan_amount = request.form.get('loans_amount_input')
		loan_purpose = request.form.get('loans_purpose_input')

		borrower_tax_id = loan_borrower.split('Tax-ID:')[1].strip()
		borrower_detail = get_borrower_with_tax_id(borrower_tax_id)
		total_payable, monthly_payable, penalty = calculate_values(loan_amount, loan_plan)
		# +++++++++++++++++++++++++++++ UP TO HERE +++++++++++++++++++++++++++++

	borrowers = get_all_borrowers()
	loan_types = get_all_loan_types()
	loan_plans = get_all_loan_plans()
	return render_template("loans_page.html", borrowers=borrowers,
							loan_types=loan_types, loan_plans=loan_plans)


def calculate_values(loan_amount, loan_plan):
	months = int(loan_plan.split(" ")[0])
	interest = float(loan_plan.split(" ")[2][1:4])
	penalty = float(loan_plan.split(" ")[3][0:3])
	calc_total_payable = int(loan_amount) + (int(loan_amount) * (interest / 100))
	calc_total_payable = float("{:.2f}".format(calc_total_payable))
	calc_monthly_payable = float("{:.2f}".format(calc_total_payable/months))
	calc_penalty = calc_monthly_payable * (penalty / 100)
	calc_penalty = float("{:.2f}".format(calc_penalty))
	return [calc_total_payable, calc_monthly_payable, calc_penalty]

@app.route("/home/payments/")
@login_required
def payments_view():
    return render_template("payments_page.html")


@app.route("/home/borrowers/", methods=['GET', 'POST'])
@login_required
def borrowers_view():
	if request.method == 'POST':
		first_name = request.form.get('first_name')
		last_name = request.form.get('last_name')
		address = request.form.get('address')
		contact = request.form.get('contact')
		email = request.form.get('email')
		tax_id = request.form.get('tax_id')
		try:
			save_borrower(first_name, last_name, address, contact, email, tax_id)
		except Exception as e:
			print("[EXCEPTION] ", e)
	borrowers_list = get_all_borrowers()
	return render_template("borrowers_page.html", borrowers_list=borrowers_list)


@app.route("/delete-borrower", methods=['GET', 'POST'])
def remove_a_borrower():
	if request.method == 'POST':
		borrower_email = request.form.get('delete_button_email_input')
		if get_a_borrower(borrower_email):
			delete_a_borrower(borrower_email)
			return redirect(url_for('borrowers_view'))
		else:
			print("No Such Borrower Exist!")
	return redirect(url_for('borrowers_view'))

@app.route("/home/loan_plans/", methods=['GET', 'POST'])
@login_required
def loan_plans_view():
	if request.method == 'POST':
		plan = int(request.form.get('plan'))
		interest = float(request.form.get('interest'))
		penalty = float(request.form.get('penalty'))
		years = plan // 12
		months = plan % 12
		try:
			save_loan_plan(months, years, interest, penalty)
		except Exception as e:
			print("[EXCEPTION] ", e)
	loan_plans = get_all_loan_plans()
	return render_template("loan_plans_page.html", loan_plans=loan_plans)


@app.route("/home/loan_types/", methods=['GET', 'POST'])
@login_required
def loan_types_view():
	if request.method == 'POST':
		loan_type = request.form.get('loan_type')
		description = request.form.get('description')
		try:
			save_loan_type(loan_type, description)
		except Exception as e:
			print("[EXCEPTION] ", e)
	loan_types = get_all_loan_types()
	return render_template("loan_types_page.html", loan_types=loan_types)


@app.route("/home/users/", methods=['GET', 'POST'])
@login_required
def users_view():
	if request.method == 'POST':
		first_name = request.form.get('first_name')
		last_name = request.form.get('last_name')
		email = request.form.get('email')
		password = request.form.get('password')
		has_permission = True if request.form.get('has_permission') != None else False
		is_admin = True if request.form.get('is_admin') != None else False
		try:
			save_user(first_name, last_name, email, password, has_permission, is_admin)
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
		is_admin = True if request.form.get('is_admin') != None else False
		update_user(first_name, last_name, email, password, has_permission, is_admin)
	return redirect(url_for('users_view'))


@app.route("/delete-user", methods=['GET', 'POST'])
def remove_a_user():
	if request.method == 'POST':
		email = request.form.get('delete_button_email_input')
		if get_user(email):
			delete_user(email)
			return redirect(url_for('users_view'))
	return redirect(url_for('users_view'))


@app.route("/delete-loan-plan", methods=['GET', 'POST'])
def remove_loan_plan():
	if request.method == 'POST':
		loan_plan_id = request.form.get('delete_button_id_input')
		if get_a_loan_plan(loan_plan_id):
			delete_a_loan_plan(loan_plan_id)
			return redirect(url_for('loan_plans_view'))
	return redirect(url_for('loan_plans_view'))

@app.route("/delete-loan-type", methods=['GET', 'POST'])
def remove_loan_type():
	if request.method == 'POST':
		loan_type_id = request.form.get('delete_button_id_input')
		if get_a_loan_type(loan_type_id):
			delete_a_loan_type(loan_type_id)
			return redirect(url_for('loan_types_view'))
	return redirect(url_for('loan_types_view'))



@login_manager.user_loader
def load_user(email):
    return get_user(email)


if __name__ == "__main__":
    app.run(debug=True)
