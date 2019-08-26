from datetime import datetime
from restoran import db, login_manager
from flask_login import UserMixin

@login_manager.user_loader
def load_korisnik(korisnik_id):
    return Korisnik.query.get(int(korisnik_id))
    
class Korisnik(db.Model, UserMixin):
	id = db.Column(db.Integer, primary_key=True)
	korisnicko_ime = db.Column(db.String(20), unique=True, nullable=False)
	email = db.Column(db.String(120), unique=True, nullable=False)
	profilna_slika = db.Column(db.String(20), nullable=False, default='default.jpg')
	lozinka = db.Column(db.String(60), nullable=False)
	restorani = db.relationship('Restoran', backref='autor', lazy=True)
	def __repr__(self):
		return f"Korisnik('{self.korisnicko_ime}','{self.lozinka}', '{self.email}', '{self.profilna_slika}')"

	
class Restoran(db.Model):

	id = db.Column(db.Integer, primary_key=True)
	ime_restorana = db.Column(db.String(50), nullable=False)
	opis = db.Column(db.Text)
	ocjena = db.Column(db.String(50), nullable=False)
	lokacija = db.Column(db.String(50), nullable=False)
	adresa = db.Column(db.String(50), nullable=False)
	datum = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
	korisnik_id = db.Column(db.Integer, db.ForeignKey('korisnik.id'), nullable=False)

	def __repr__(self):
		return f"Restoran('{self.ime_restorana}','{self.lokacija}','{self.adresa}','{self.opis}','{self.datum}', '{self.ocjena}')"

