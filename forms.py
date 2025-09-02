from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField
from wtforms.validators import DataRequired, Length

class InputForm(FlaskForm):
    course_code = SelectField(u'Course Code (*)', validators=[DataRequired()])
    terms = SelectField(u'Academic Term (*)',validators=[DataRequired()])
    bidding_windows = SelectField(u'Bidding Window (*)')
    day = SelectField(u'Day of Week', choices=['Any','MON', 'TUE', 'WED', 'THU', 'FRI', '..'])
    start_times = SelectField(u'Time Slot', choices=['Any','Morning (08:15)', 'Afternoon (12:00)', 'Evening (15:30)', 'Night (19:00)', '..'])
    professors = SelectField(u'Professors (None is default, all instructors will be shown)')
    submit = SubmitField('Search')