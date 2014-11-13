import os
import re

import jinja2
import webapp2

template_dir = os.path.join(os.path.dirname(__file__), 'templates')

jinja_env = jinja2.Environment(loader= jinja2.FileSystemLoader(template_dir),
                               autoescape=True)

class Handler(webapp2.RequestHandler):
    def write(self, *args, **kwargs):
        self.response.out.write(*args, **kwargs)

    ## jinja2's Template objects render with either a dictionary or kwargs
    ## this is the 'context' of the template
    def render_to_string(self, template, **kw):
        t = jinja_env.get_template(template)
        return t.render(**kw)

    ## not to be confused with jinja2's render method... 
    def render(self, template, **kw):
        self.write(self.render_to_string(template, **kw))

# Verification functions for the signup
# Return boolean values context to render error messages
USER_RE = re.compile(r"^[a-zA-Z0-9_-]{3,20}$")
def valid_username(username):
    return USER_RE.match(username)

PASS_RE = re.compile(r"^.{3,20}$")
def valid_password(password):
    return PASS_RE.match(password)

def valid_email(email):
    return None

def passwords_match(password, verify):
    if password != verify:
        return False
    else:
        return True

class SignupHandler(Handler):
    def get(self):
        self.render('signup.html')

    def post(self):
        username = self.request.get('username')
        password = self.request.get('password')
        verify = self.request.get('verify')
        email = self.request.get('email')

        if not valid_username(username):
            self.render('signup.html')

        elif not valid_password(password):
            self.render('signup.html')

        elif not passwords_match(password, verify):
            self.response.out.write("password mismatch")
            self.render('signup.html')
        
        ## Really neat! Check out the redirect vs. the routing
        ## and think back to how HTTP works
        else:
            return self.redirect('/welcome?username=%s' % username)

class SuccessHandler(Handler):
    def get(self):
        username = self.request.GET['username']
        self.render('welcome.html', username=username)


app = webapp2.WSGIApplication([('/signup', SignupHandler),
                               ('/welcome', SuccessHandler),
    ], debug=True)