import os
import secrets
from PIL import Image
from flask import render_template, url_for, flash, redirect, request, abort
from restoran import app, db, bcrypt
from restoran.forms import RegistracijaForm, PrijavaForm, AzuriranjeProfilaForm, NoviRestoran
from restoran.models import Korisnik,Restoran
from flask_login import login_user, current_user, logout_user, login_required




@app.route("/")
@app.route("/pocetna")
def Pocetna():
	restorani = Restoran.query.all()
	return render_template('Pocetna.html', restorani=restorani)
	
@app.route("/registracija", methods=['GET', 'POST'])
def Registracija():
	if current_user.is_authenticated:
		return redirect(url_for('Pocetna'))
	form = RegistracijaForm()
	if form.validate_on_submit():
		skrivena_lozinka = bcrypt.generate_password_hash(form.lozinka.data).decode('utf-8')
		korisnik = Korisnik(korisnicko_ime=form.korisnicko_ime.data, email=form.email.data, lozinka=skrivena_lozinka)
		db.session.add(korisnik)
		db.session.commit()
		flash('Vas korisnicki racun je uspjesno kreiran', 'success')
		return redirect(url_for('Prijava'))
	return render_template('Registracija.html', title='Registracija', form=form)

@app.route("/prijava", methods=['GET', 'POST'])
def Prijava():
	if current_user.is_authenticated:
		return redirect(url_for('Pocetna'))
	form = PrijavaForm()
	if form.validate_on_submit():
		korisnik = Korisnik.query.filter_by(email=form.email.data).first()
		if korisnik and bcrypt.check_password_hash(korisnik.lozinka, form.lozinka.data):
			login_user(korisnik, form.zapamti.data)
			next_page = request.args.get('next')
			return redirect(next_page) if next_page else redirect(url_for('Pocetna'))
		else:
			flash("Lozinka ili email nisu tocni", "danger")
	return render_template('Prijava.html', title='Prijava', form=form)


@app.route("/odjava")
def Odjava():
	logout_user()
	return redirect(url_for('Pocetna'))

def spremi_sliku(form_slika):
	random_hex = secrets.token_hex(8)
	_, f_ext = os.path.splitext(form_slika.filename)
	slika_fn = random_hex + f_ext
	slika_path = os.path.join(app.root_path, 'static/slike_profila', slika_fn)
	form_slika.save(slika_path)

	output_size = (125, 125)
	i = Image.open(form_slika)
	i.thumbnail(output_size)
	i.save(slika_path)

	return slika_fn

@app.route("/korisnik", methods=['GET', 'POST'])
@login_required
def Korisnik_racun():
	form = AzuriranjeProfilaForm()
	if form.validate_on_submit():
		if form.slika.data:
			slika_file = spremi_sliku(form.slika.data)
			current_user.profilna_slika = slika_file
		current_user.korisnicko_ime = form.korisnicko_ime.data
		current_user.email = form.email.data
		current_user.lozinka = bcrypt.generate_password_hash(form.lozinka.data).decode('utf-8')
		db.session.commit()
		flash('Vasi podatci su uspjesno azurirani', 'success')
		return redirect (url_for('Korisnik_racun'))
	elif request.method == 'GET':
		form.korisnicko_ime.data = current_user.korisnicko_ime
		form.email.data = current_user.email
	profilna_slika = url_for('static', filename='slike_profila/' + current_user.profilna_slika)
	return render_template('Korisnik.html', title='Korisnik', profilna_slika=profilna_slika, form=form)


@app.route("/restoran/novi", methods=['GET', 'POST'])
@login_required
def Novi_Restoran():
	form = NoviRestoran()
	if form.validate_on_submit():
		restoran = Restoran(ime_restorana=form.naslov.data, lokacija=form.lokacija.data, adresa=form.adresa.data, opis=form.opis.data, ocjena=form.ocjena.data, autor=current_user)
		db.session.add(restoran)
		db.session.commit()
		flash('Uspjesno ste dodali recenziju restorana!', 'success')
		return redirect(url_for('Pocetna'))
	return render_template('NoviRestoran.html', title='Nova Recenzija', form=form, legend='Nova Recenzija')

@app.route("/restoran/<int:restoran_id>")
def RestoranP(restoran_id):
    restoran = Restoran.query.get_or_404(restoran_id)
    return render_template('Restoran.html', title=restoran.ime_restorana, restoran=restoran)


@app.route("/restoran/<int:restoran_id>/azuriraj" , methods=['GET', 'POST'])
@login_required
def Azuriraj_RestoranP(restoran_id):
	restoran = Restoran.query.get_or_404(restoran_id)
	if restoran.autor != current_user:
		abort(403)
	form = NoviRestoran()
	if form.validate_on_submit():
		restoran.ime_restorana = form.naslov.data
		restoran.lokacija = form.lokacija.data
		restoran.adresa = form.adresa.data
		restoran.opis = form.opis.data
		restoran.ocjena = form.ocjena.data
		db.session.commit()
		flash('Uspjesno ste azurirali vasu recenziju', 'success')
		return redirect(url_for('RestoranP', restoran_id=restoran.id))
	elif request.method == 'GET':
		form.naslov.data = restoran.ime_restorana
		form.lokacija.data = restoran.lokacija
		form.adresa.data = restoran.adresa
		form.opis.data = restoran.opis
		form.ocjena.data = restoran.ocjena
	return render_template('NoviRestoran.html', title='Azuriraj Recenziju', form=form, legend='Azuriraj Recenziju')

@app.route("/restoran/<int:restoran_id>/obrisi" , methods=['POST'])
@login_required
def Obrisi_Restoran(restoran_id):
	restoran = Restoran.query.get_or_404(restoran_id)
	if restoran.autor != current_user:
		abort(403)
	db.session.delete(restoran)
	db.session.commit()
	flash('Vasa recenzija je uspjesno obrisana!', 'success')
	return redirect(url_for('Pocetna'))


@app.route("/NajboljiRestorani")
def Najbolji_Restoran():
	restorani = Restoran.query.filter_by(ocjena=5).all()
	return render_template('NajboljiRestorani.html', restorani=restorani)






