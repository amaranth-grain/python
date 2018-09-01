# Test forms and inputs on Google App Engine with Python.
# Uses (limited) data validation to verify dates, but it 
# is not complete.  Dates like "February 31" are still
# treated as valid.

import webapp2

#Months used for validation of birthdate
months = ['January',
          'February',
          'March',
          'April',
          'May',
          'June',
          'July',
          'August',
          'September',
          'October',
          'November',
          'December']
          
#valid_month() returns true when the first three letters match the calendar months
month_abbreviations = dict((m[:3].lower(), m) for m in months)
def valid_month(month):
    if month:
        shortenedMonth = month[:3].lower()
        return month_abbreviations.get(shortenedMonth)

#Only validates if the date is between 1 and 31; February 31 would still evaluate as True
def valid_day(day):
    if day and day.isdigit():
        day = int(day)
        if day >= 1 and day <= 31:
            return day

#A year between 1900 and 2020 inclusive evaluates to True
def valid_year(year):
    if year and year.isdigit():
        year = int(year)
        if year >= 1900 and year <= 2020:
            return year

#sanitises user input to prevent HTML confusion
def escape_html(s):
	import cgi
	return cgi.escape(s, quote=True)

#Form HTML
form = """
	<form method="post">
		Enter your birthdate below:
		<br/>
		<input type="text" name="month" placeholder="Month" value="%(month)s">
		<input type="text" name="day" placeholder="Day" value="%(day)s">
		<input type="text" name="year" placeholder="Year" value="%(year)s">
		<div style="color: red">%(error)s</div>
		<br/>
		<input type="submit" value="Verify">
	</form>
"""

#Renders and handles main page and sanitises user HTML input
class MainPage(webapp2.RequestHandler):		
    def get(self):
    	self.response.write(form % {"error" : "", "month" : "", "day" : "", "year" : ""})
    	
    def post(self):
    	user_month = self.request.get('month')
    	user_day = self.request.get('day')
    	user_year = self.request.get('year')
    	
    	month = valid_month(user_month)
    	day = valid_day(user_day)
    	year = valid_year(user_year)
    	
        # If any single part of the date is considered invalid, prompt
        # user to input date again.
    	if not (month and day and year):
    		self.response.write(form % {"error" : "Invalid entry. Try again.", 
    		"month" : escape_html(user_month), 
    		"day" : escape_html(user_day), 
    		"year" : escape_html(user_year)})
    	else:
			self.redirect("/confirm")

# Renders confirmation page.  User is redirected here if
# date is deemed valid.
class ConfirmPage(webapp2.RequestHandler):	
	def get(self):
		self.response.write('Your birthdate has been verified.')
	
app = webapp2.WSGIApplication([
    ('/', MainPage),
    ('/confirm', ConfirmPage),
], debug=True)
