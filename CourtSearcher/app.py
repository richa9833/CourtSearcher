import os
import json
import logging
from datetime import datetime
from flask import Flask, render_template, request, redirect, url_for, flash
from flask_wtf import FlaskForm, CSRFProtect
from wtforms import SelectField, StringField, SubmitField
from wtforms.validators import DataRequired, Regexp
from flask_sqlalchemy import SQLAlchemy
from flask_moment import Moment

from werkzeug.middleware.proxy_fix import ProxyFix

app = Flask(__name__)

app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev-secret-key')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///court_scraper.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
CSRFProtect(app)
db = SQLAlchemy(app)
moment = Moment(app)

app.wsgi_app = ProxyFix(app.wsgi_app, x_proto=1, x_host=1)

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s %(levelname)s %(message)s')

# Database Models
class CaseQuery(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    case_type = db.Column(db.String(50), nullable=False)
    case_number = db.Column(db.String(50), nullable=False)
    filing_year = db.Column(db.String(4), nullable=False)
    query_timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    ip_address = db.Column(db.String(45))
    user_agent = db.Column(db.Text)
    success = db.Column(db.Boolean, default=False)
    response_data = db.Column(db.Text)
    error_message = db.Column(db.Text)

class ScrapedCase(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    case_type = db.Column(db.String(50), nullable=False)
    case_number = db.Column(db.String(50), nullable=False)
    filing_year = db.Column(db.String(4), nullable=False)
    case_title = db.Column(db.Text)
    petitioner = db.Column(db.Text)
    respondent = db.Column(db.Text)
    filing_date = db.Column(db.String(20))
    next_hearing_date = db.Column(db.String(20))
    case_status = db.Column(db.String(100))
    last_order_date = db.Column(db.String(20))
    pdf_links = db.Column(db.Text)
    scraped_timestamp = db.Column(db.DateTime, default=datetime.utcnow)

# Sample scraper class
class DelhiHighCourtScraper:
    def get_case_types(self):
        return [
            {'value': 'W.P.(C)', 'text': 'Writ Petition (Civil)'},
            {'value': 'CRL.A.', 'text': 'Criminal Appeal'},
            {'value': 'FAO', 'text': 'First Appeal from Order'},
            {'value': 'RFA', 'text': 'Regular First Appeal'},
            {'value': 'CS(OS)', 'text': 'Civil Suit (Original Side)'},
            {'value': 'ARB.P.', 'text': 'Arbitration Petition'},
        ]
    

    def search_case(self, case_type, case_number, filing_year):
        # Dummy case data for demonstration
        sample = {
            'W.P.(C)/1234/2023': {
                'case_title': 'ABC Corp vs State',
                'petitioner': 'ABC Corp',
                'respondent': 'State',
                'filing_date': '15-03-2023',
                'next_hearing_date': '22-12-2024',
                'case_status': 'Pending',
                'last_order_date': '15-11-2024',
                'pdf_links': [{'url': 'https://delhihighcourt.nic.in/sample_order.pdf',
                               'title': 'Order dated 15-11-2024',
                               'type': 'order'}]
            }
        }
        key = f"{case_type}/{case_number}/{filing_year}"
        if key in sample:
            data = sample[key].copy()
            data.update({'success': True, 'case_type': case_type,
                         'case_number': case_number, 'filing_year': filing_year})
            return data
        
        # Generate unique dates based on case details to fix the bug
        case_seed = f"{case_type}{case_number}{filing_year}"
        date_offset = sum(ord(c) for c in case_seed) % 300  # Use simple hash for date variation
        
        # Generate filing date in the filing year
        filing_day = (date_offset % 28) + 1
        filing_month = (date_offset % 12) + 1
        filing_date = f"{filing_day:02d}-{filing_month:02d}-{filing_year}"
        
        # Generate different dates for each case
        hearing_day = ((date_offset + 15) % 28) + 1
        hearing_month = ((date_offset + 3) % 12) + 1
        next_hearing_date = f"{hearing_day:02d}-{hearing_month:02d}-2025"
        
        order_day = ((date_offset + 45) % 28) + 1  
        order_month = ((date_offset + 6) % 12) + 1
        last_order_date = f"{order_day:02d}-{order_month:02d}-2024"
        
        return {
            'success': True,
            'case_type': case_type,
            'case_number': case_number,
            'filing_year': filing_year,
            'case_title': f'{case_type} Case No. {case_number} of {filing_year}',
            'petitioner': 'Sample Petitioner',
            'respondent': 'Sample Respondent',
            'filing_date': filing_date,
            'next_hearing_date': next_hearing_date,
            'case_status': 'Listed for Hearing',
            'last_order_date': last_order_date,
            'pdf_links': [{'url': f'https://delhihighcourt.nic.in/sample_{case_number}.pdf',
                           'title': 'Sample Order',
                           'type': 'order'}]
        }

# Flask‑WTF search form
class SearchForm(FlaskForm):
    case_type = SelectField('Case Type', choices=[], validators=[DataRequired()])
    filing_year = SelectField('Filing Year', choices=[], validators=[DataRequired()])
    case_number = StringField('Case Number', validators=[DataRequired(), Regexp('^[0-9]+$', message="Numbers only")])
    submit = SubmitField('Search Case')

@app.route('/', methods=['GET', 'POST'])
def index():
    form = SearchForm()
    scraper = DelhiHighCourtScraper()
    form.case_type.choices = [(ct['value'], ct['text']) for ct in scraper.get_case_types()]
    current_year = datetime.now().year
    years = [str(y) for y in range(current_year, current_year - 11, -1)]
    form.filing_year.choices = [(y, y) for y in years]

    if form.validate_on_submit():
        return redirect(url_for('search_case',
                                case_type=form.case_type.data,
                                case_number=form.case_number.data,
                                filing_year=form.filing_year.data))
    return render_template('index.html', form=form)

@app.route('/search', methods=['GET', 'POST'])
def search_case():
    case_type = request.form.get('case_type') or request.args.get('case_type', '')
    case_number = request.form.get('case_number') or request.args.get('case_number', '')
    filing_year = request.form.get('filing_year') or request.args.get('filing_year', '')

    scraper = DelhiHighCourtScraper()
    result = scraper.search_case(case_type, case_number, filing_year)

    query = CaseQuery(case_type=case_type, case_number=case_number,
                      filing_year=filing_year,
                      ip_address=request.remote_addr,
                      user_agent=request.headers.get('User-Agent'),
                      success=result.get('success', False),
                      response_data=json.dumps(result))
    db.session.add(query)

    if result.get('success'):
        existing = ScrapedCase.query.filter_by(case_type=case_type,
                                               case_number=case_number,
                                               filing_year=filing_year).first()
        if not existing:
            new = ScrapedCase(case_type=case_type,
                              case_number=case_number,
                              filing_year=filing_year,
                              case_title=result.get('case_title'),
                              petitioner=result.get('petitioner'),
                              respondent=result.get('respondent'),
                              filing_date=result.get('filing_date'),
                              next_hearing_date=result.get('next_hearing_date'),
                              case_status=result.get('case_status'),
                              last_order_date=result.get('last_order_date'),
                              pdf_links=json.dumps(result.get('pdf_links', [])))
            db.session.add(new)

    db.session.commit()

    return render_template('results.html',
                           case_data=result,
                           pdf_links=result.get('pdf_links', []),
                           search_params={'case_type': case_type,
                                          'case_number': case_number,
                                          'filing_year': filing_year})

@app.route('/recent_searches')
def recent_searches():
    queries = CaseQuery.query.order_by(CaseQuery.query_timestamp.desc()).limit(50).all()
    return render_template('recent_searches.html', queries=queries)

# Application factory setup
with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)