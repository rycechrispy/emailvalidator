from flask import render_template, request, redirect, url_for, Flask
from flanker.addresslib import address, validate
import re

app = Flask(__name__)
app.secret_key = "gk_-+x6q@c)hf*w)bh0t#fh7)mz3liy=*godtwl#3fj%&7eg6xxx("

@app.route('/')
def main_view():
	return render_template('home.html')

@app.route('/', methods=['GET', 'POST'])
def show_valid_emails():
	if request.method == 'POST':
		email = request.form['input']
		return check_mulitple_email(email)
		# if "\n" in email:
		# 	return check_mulitple_email(email)
		# else:
		# 	return check_single_email(email)
	else:
		return redirect(url_for('main_view'))

def check_mulitple_email(email):
	email = re.sub('[\s\n]+', ',', email)
	list_email = list(set(email.split(","))) #remove duplicate emails
	unique_emails = ','.join(list_email)

	valid = address.validate_list(unique_emails, as_tuple=True)
	valid_emails = valid[0] #first list in tuple is valid emails
	invalid_emails = valid[1] #second is invalid emails

	valids, invalids, suggests = [], [], []
	if len(valid_emails) != 0:
		valids = valid_emails
	if len(invalid_emails) != 0:
		invalids = [unique_emails.encode("ascii") for unique_emails in invalid_emails] #invalid emails come out as unicode - change to regular str
		suggests = [str(validate.suggest_alternate(unique_emails)) for unique_emails in invalids] #suggest alternate returns None - cast None to str

	return render_template('home.html', invalids=invalids, valids=valids, suggests=suggests, valid_length=len(valids), invalid_length=len(invalids))


	## n1
	# is_valid, invalid, suggest = '', '', ''
	# if len(valid_emails) != 0:
	# 	is_valid = str(valid_emails)
	# if len(invalid_emails) != 0:
	# 	stringify = [email.encode("ascii") for email in invalid_emails]
	# 	invalid = ', '.join(stringify)
	# 	suggested_emails = [str(validate.suggest_alternate(email)) for email in stringify]
	# 	suggest = ', '.join(suggested_emails)

	#return str(suggested_emails)
	# return render_template('home.html', invalid=invalid, is_valid=is_valid, suggest=suggest)

	## n2
	# is_valid, invalids, suggests = [], [], []
	# if len(valid_emails) != 0:
	# 	is_valid = str(valid_emails)
	# if len(invalid_emails) != 0:
	# 	invalids = [email.encode("ascii") for email in invalid_emails]
	# 	suggests = [str(validate.suggest_alternate(email)) for email in invalids]

	# return render_template('home.html', invalids=invalids, is_valid=is_valid, suggests=suggests, length=len(invalids))

def check_single_email(email):
	valid = address.validate_address(email) #email address object
	is_valid = None
	if valid == None:
		suggest = validate.suggest_alternate(email)
		invalid = email
		return render_template('home.html', invalid=invalid, suggest=suggest)
	else:
		is_valid = email
		return render_template('home.html', is_valid=is_valid)

if __name__ == '__main__':
    app.run(debug=True, port=5002)