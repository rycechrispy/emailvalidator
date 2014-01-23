from flask import render_template, request, redirect, url_for, Flask
from flanker.addresslib import address, validate
import re

app = Flask(__name__)
app.secret_key = "gk_-+x6q@c)hf*w)bh0t#fh7)mz3liy=*godtwl#3fj%&7eg6xxx("

@app.route('/', methods=['GET', 'POST'])
def main_view():
	if request.method == 'POST':
		email = request.form['input']
		return check_emails(email)
	else:
		return render_template('home.html')

def get_unique_emails(email):
	email = re.sub('[\s\n]+', ',', email)
	list_email = list(set(email.split(","))) #remove duplicate emails
	unique_emails = ','.join(list_email)
	return unique_emails

def check_emails(email):
	unique_emails = get_unique_emails(email)

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


if __name__ == '__main__':
    app.run(debug=True, port=5002)