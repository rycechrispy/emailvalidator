from flask import render_template, request, redirect, url_for, Flask
from flanker.addresslib import address, validate

app = Flask(__name__)
app.secret_key = "gk_-+x6q@c)hf*w)bh0t#fh7)mz3liy=*godtwl#3fj%&7eg6xxx("

@app.route('/', methods=['GET', 'POST'])
def main_view():
	if request.method == 'POST':
		email = request.form['input']
		list_email = list(set(email.split("\r\n"))) #remove duplicate emails and split each email from the new line
		
		#sort out the emails with commas, colons and spaces and the ones without
		list_without_problems, list_with_problems = [], []
		for email in list_email:
			if ' ' in email or ';' in email or ',' in email:
				list_with_problems.append(email)
			else:
				list_without_problems.append(email)

		unique_emails = ','.join(list_without_problems) #transform list to string

		#validate the good list of emails
		valid = address.validate_list(unique_emails, as_tuple=True)
		valids = valid[0] #first list in tuple is valid emails
		invalids = valid[1] #second is invalid emails

		#individually check the list with commas, colons, and spaces
		if len(list_with_problems) != 0:
			for email in list_with_problems:
				if address.validate_address(email):
					valids.append(valids)
				else:
					invalids.append(email)

		#add suggestions if there are invalid emails
		suggests = []
		if len(invalids) != 0:
			invalids = [unique_emails.encode("ascii") for unique_emails in invalids] #invalid emails come out as unicode - change to regular str and replace @@@ back to space
			suggests = [str(validate.suggest_alternate(unique_emails)).replace(" ", "") for unique_emails in invalids] #suggest alternate returns None - cast None to str
		
		return render_template('home.html', invalids=invalids, valids=valids, suggests=suggests, valid_length=len(valids), invalid_length=len(invalids))
	else:
		return render_template('home.html')

if __name__ == '__main__':
    app.run(debug=True)