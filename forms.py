from flask_wtf import FlaskForm
from flask_wtf.file import FileField,  FileAllowed
from flask_login import current_user
from wtforms import StringField, PasswordField, BooleanField, SubmitField, TextAreaField, RadioField, SelectField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from restoran.models import Korisnik


class RegistracijaForm(FlaskForm):
	korisnicko_ime = StringField('Korisnicko Ime', validators=[DataRequired(), Length(min=2, max=15)])
	email = StringField('Email', validators=[DataRequired(),Email("Email mora biti valjan!")])
	lozinka = PasswordField('Lozinka', validators=[DataRequired()])
	potvrda_lozinke = PasswordField('Potvrda Lozinke', validators=[DataRequired(), EqualTo('lozinka',"Lozinke se moraju podudarat")])
	registriraj = SubmitField('Registriraj se')

	def validate_korisnicko_ime(self, korisnicko_ime):
		korisnik = Korisnik.query.filter_by(korisnicko_ime=korisnicko_ime.data).first()
		if korisnik:
			raise ValidationError('Korisnik vec postoji')
	def validate_email(self, email):
		korisnik = Korisnik.query.filter_by(email=email.data).first()
		if korisnik:
			raise ValidationError('Email vec postoji')



  

	

class PrijavaForm(FlaskForm):
	email = StringField('Email', validators=[DataRequired(),Email("Email mora biti valjan")])
	lozinka = PasswordField('Lozinka', validators=[DataRequired()])
	zapamti = BooleanField('Zapamti me')
	prijava = SubmitField('Prijavi se')



class AzuriranjeProfilaForm(FlaskForm):
	korisnicko_ime = StringField('Korisnicko Ime', validators=[DataRequired(), Length(min=2, max=15)])
	email = StringField('Email', validators=[DataRequired(),Email("Email mora biti valjan!")])
	slika = FileField('Slika', validators=[FileAllowed(['jpg','png'])])
	lozinka = PasswordField('Lozinka', validators=[DataRequired()])
	potvrdi = SubmitField('Azuriraj')


	def validate_korisnicko_ime(self, korisnicko_ime):
		if korisnicko_ime.data != current_user.korisnicko_ime:
			korisnik = Korisnik.query.filter_by(korisnicko_ime=korisnicko_ime.data).first()
			if korisnik:
				raise ValidationError('Korisnik vec postoji')
	
	def validate_email(self, email):
		if email.data != current_user.email:
			korisnik = Korisnik.query.filter_by(email=email.data).first()
			if korisnik:
				raise ValidationError('Email vec postoji')

class NoviRestoran(FlaskForm):
	naslov = StringField('Ime Restorana', validators=[DataRequired()])
	opis = TextAreaField('Sadrzaj', validators=[DataRequired()])
	ocjena = RadioField('Ocjena',choices=[('1','Ocjena 1'),('2','Ocjena 2'),('3','Ocjena 3'),('4','Ocjena 4'),('5','Ocjena 5')])
	lokacija = StringField('Lokacija', validators=[DataRequired()])
	adresa = StringField('Adresa', validators=[DataRequired()])
	unesi = SubmitField('Potvrdi')


	





	





