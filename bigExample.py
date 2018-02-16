from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView

app = Flask(__name__)
app.config['SECRET_KEY'] = 'Thisissupposedtobesecret!'

# Database stuff
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:////Users/admin/Desktop/Programming/Python/Flask/Admin/database.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Database Classes
# DB Classes for Question Related Stuff
class Subject(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	title = db.Column(db.String(40), unique=True)
	# Back Reference
	blocks = db.relationship('Block', backref='subject', lazy='dynamic')
	#users = db.relationship('User', backref='subject', lazy='dynamic')
	units = db.relationship('Unit', backref='subject', lazy='dynamic')

	def __repr__(self):
		return '<Subject {}>'.format(self.title)

class Unit(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	number = db.Column(db.Integer)
	title = db.Column(db.String(40))
	# Foreign Keys
	subject_id = db.Column(db.Integer, db.ForeignKey('subject.id'))
	# Back reference
	lessons = db.relationship('Lesson', backref='unit', lazy='dynamic')

	def __repr__(self):
		return '<Unit {}: {}>'.format(self.number, self.title)

class Lesson(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	number = db.Column(db.Integer)
	title = db.Column(db.String(40))
	date_assigned = db.Column(db.DateTime)
	active = db.Column(db.Boolean)
	pdf_url = db.Column(db.String)
	# Foreign Keys
	unit_id = db.Column(db.Integer, db.ForeignKey('unit.id'))
	# Back reference
	questions = db.relationship('Question', backref='lesson', lazy='dynamic')

	def __repr__(self):
		return '<Unit: {}, Lesson: {} - {}>'.format(self.unit.number, self.number, self.title)

class Question(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	number = db.Column(db.Integer)
	html = db.Column(db.String)
	# Foreign Keys
	lesson_id = db.Column(db.Integer, db.ForeignKey('lesson.id'))
	# Back reference
	parts = db.relationship('Part', backref='question', lazy='dynamic')

	def __repr__(self):
		return '<Unit: {}, Lesson: {}, Question: {}>'.format(self.lesson.unit.number, self.lesson.number, self.number)

class Part(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	letter = db.Column(db.String(1))
	html = db.Column(db.String)
	answer = db.Column(db.String)
	# Foreign Keys
	question_id = db.Column(db.Integer, db.ForeignKey('question.id'))
	# Back reference
	responses = db.relationship('Response', backref='part', lazy='dynamic')

	def __repr__(self):
		return '<Unit: {}, Lesson: {}, Question: {}, Part: {}>'.format(self.question.lesson.unit.number, self.question.lesson.number, self.question.number, self.letter)

# DB Classes for Question Related Stuff
class Block(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	number = db.Column(db.Integer)
	# Foreign Keys
	subject_id = db.Column(db.Integer, db.ForeignKey('subject.id'))
	# Back Reference
	users = db.relationship('User', backref='block', lazy='dynamic')

	def __repr__(self):
		return '<Subject: {}, Block: {}>'.format(self.subject.title, self.number)

class User(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	account_type = db.Column(db.String(20)) # either 'Student' or 'Teacher'
	first_name = db.Column(db.String(40))
	last_name = db.Column(db.String(40))
	email = db.Column(db.String(100), unique=True)
	password = db.Column(db.String(100))
	# Foreign Keys
	#subject_id = db.Column(db.Integer, db.ForeignKey('subject.id'))
	block_id = db.Column(db.Integer, db.ForeignKey('block.id'))
	# Back Reference
	responses = db.relationship('Response', backref='user', lazy='dynamic')

	def __repr__(self):
		return '<Name: {} {}, Subject: {}>'.format(self.first_name, self.last_name, self.block.subject.title)

class Response(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	answer_text = db.Column(db.String(30))
	status = db.Column(db.Boolean)
	tries = db.Column(db.Integer)
	last_attempt_time = db.Column(db.DateTime)
	# Foreign Keys
	part_id = db.Column(db.Integer, db.ForeignKey('part.id'))
	user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

	def __repr__(self):
		return '<User: {} {}, U{}-L{}-Q{}({})>'.format(self.user.first_name, self.user.last_name, 
			self.user.block.subject.title, self.part.question.lesson.unit.number, self.part.question.lesson.number,
			self.part.question.number, self.part.letter)

admin = Admin(app, template_mode='bootstrap3')
admin.add_view(ModelView(Subject, db.session))
admin.add_view(ModelView(Unit, db.session))
admin.add_view(ModelView(Lesson, db.session))
admin.add_view(ModelView(Question, db.session))
admin.add_view(ModelView(Part, db.session))
admin.add_view(ModelView(Block, db.session))
admin.add_view(ModelView(User, db.session))
admin.add_view(ModelView(Response, db.session))

if __name__ == '__main__':
	app.run(debug='True')