from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
import pymysql 
from sqlalchemy import text

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://shesha_23:shesha1234@localhost/b556' 
db = SQLAlchemy(app)


class Disease(db.Model):
    disease_id = db.Column(db.String(255), primary_key=True)
    disease_name = db.Column(db.String(255))
    clinical_findings = db.Column(db.String(255))

class CHD(db.Model):
    CHD_id = db.Column(db.String(255), primary_key=True)
    CHD_name = db.Column(db.String(255))
    disease_id = db.Column(db.String(255), db.ForeignKey('disease.disease_id'))
    disease = db.relationship('Disease', backref='chds')

class Gene(db.Model):
    gene_id = db.Column(db.String(255), primary_key=True)
    gene_name = db.Column(db.String(255))
    gene_loci = db.Column(db.String(255))
    gene_function = db.Column(db.String(255))
    CHD_id = db.Column(db.String(255), db.ForeignKey('chd.CHD_id'))
    chd = db.relationship('CHD', backref='genes')

class CHD_Gene(db.Model):
    CHD_id = db.Column(db.String(255), db.ForeignKey('chd.CHD_id'), primary_key=True)
    gene_id = db.Column(db.String(255), db.ForeignKey('gene.gene_id'), primary_key=True)
    chd = db.relationship('CHD', backref='chd_genes')
    gene = db.relationship('Gene', backref='gene_chds')

class CHD_Disease(db.Model):
    CHD_id = db.Column(db.String(255), db.ForeignKey('chd.CHD_id'), primary_key=True)
    disease_id = db.Column(db.String(255), db.ForeignKey('disease.disease_id'), primary_key=True)
    chd = db.relationship('CHD', backref='chd_diseases')
    disease = db.relationship('Disease', backref='disease_chds')
    
with app.app_context():
    result = db.session.execute(text('SELECT 1'))  
    print(result.fetchone())



@app.route('/diseases')
def view_diseases():
    diseases = Disease.query.all()
    return render_template('diseases.html', diseases=diseases)
