from flask_wtf import Form
from wtforms.fields import StringField
from flask_wtf.html5 import URLField
from wtforms.validators import DataRequired, url

class FrameworkForm(Form):

    framework = StringField('Code: ', validators=[DataRequired()])
    description = StringField('Description: ')

def validate(self):
    if not self.framework.data.startwith("W"):
        self.framework.data="W" + self.framework.data


    if not Form.validate(self):
        return False

    if not self.description.data:
        self.description.data=self.framework.data

    return True
