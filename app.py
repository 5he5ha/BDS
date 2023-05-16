from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
import pymysql 
from sqlalchemy import text

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://shesha_23:shesha1234@localhost/b556' 
db = SQLAlchemy(app)


# Define database models
class Disease(db.Model):
    disease_id = db.Column(db.String(255), primary_key=True)
    disease_name = db.Column(db.String(255))
    clinical_findings = db.Column(db.String(255))

class CHD(db.Model):
    CHD_id = db.Column(db.String(255), primary_key=True)
    CHD_name = db.Column(db.String(255))


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

# Define routes
@app.route('/')
def home():
    return render_template('home.html')

@app.route('/search', methods=['GET'])
def search_results():
    search_term = request.args.get('search_term')
    search_category = request.args.get('search_category')

    if search_category == 'gene':
        results = Gene.query.filter(
            Gene.gene_name.like(f'%{search_term}%') | 
            Gene.gene_id.like(f'%{search_term}%') |
            Gene.gene_loci.like(f'%{search_term}%') |
            Gene.gene_function.like(f'%{search_term}%')
        ).all()
        return render_template('search.html', results=results, category='gene')
    
    elif search_category == 'disease':
        results = Disease.query.filter(
            Disease.disease_name.like(f'%{search_term}%') |
            Disease.disease_id.like(f'%{search_term}%') |
            Disease.clinical_findings.like(f'%{search_term}%')
        ).all()
        return render_template('search.html', results=results, category='disease')
    
    elif search_category == 'chd':
        results = CHD.query.filter(
            CHD.CHD_name.like(f'%{search_term}%') |
            CHD.CHD_id.like(f'%{search_term}%')
        ).all()
        return render_template('search.html', results=results, category='chd')
    
    else:
        return render_template('search.html', error=True)


if __name__ == '__main__':
    app.run()

