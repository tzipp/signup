import os

import jinja2
import webapp2

template_dir = os.path.join(os.path.dirname(__file__), 'templates')

jinja_env = jinja2.Environment(loader= jinja2.FileSystemLoader(template_dir),
                               autoescape=True)

class Handler(webapp2.RequestHandler):
    def write(self, *args, **kwargs):
        self.response.out.write(*args, **kwargs)

    def render_to_string(self, template, **kw):
        t = jinja_env.get_template(template)
        return (t, kw)

    def render(self, template, **kw):
        self.write(self.render_to_string(template, **kw))

class SignupHandler(Handler):
    def get(self):
        self.response.out.write("What's up!")

    def post(self):
        self.response.out.write("Posteddd")

app = webapp2.WSGIApplication([('/signup', SignupHandler)], debug=True)