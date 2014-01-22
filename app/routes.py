from flask import render_template, request, redirect, url_for, Flask
from flanker.addresslib import address, validate

app = Flask(__name__)
app.secret_key = "gk_-+x6q@c)hf*w)bh0t#fh7)mz3liy=*godtwl#3fj%&7eg6xxx("

@app.route('/')
def main_view():
	return render_template('home.html')

@app.route('/', methods=['GET', 'POST'])
def show_valid_emails():
	if request.method == 'POST':
		email = request.form['input']
		valid = address.validate_address(email) #email address object
		is_valid = None
		if valid == None:
			suggest = validate.suggest_alternate(email)
			invalid = email
			return render_template('home.html', invalid=invalid, suggest=suggest)
		else:
			is_valid = email
			return render_template('home.html', is_valid=is_valid)
	else:
		return redirect(url_for('main_view'))
if __name__ == '__main__':
    app.run(debug=True, port=5002)