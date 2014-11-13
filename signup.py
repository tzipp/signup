import os

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

class SignupHandler(Handler):
    def get(self):
        self.render('signup.html')

    def post(self):
        self.response.out.write("Posteddd")

app = webapp2.WSGIApplication([('/signup', SignupHandler)], debug=True)