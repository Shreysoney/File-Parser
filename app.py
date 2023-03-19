""" This module creates the flask server and database conections.

This module typically creates the flask server and have two classes
Summary_Rolling_MOM and VOC_Rolling_MOM for setting up the Database tables 
and checks whether a file is processed or not.It also dumps the error 
files in Error Folder. 
"""
import shutil
import os
from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from validate import FileModel
import parse
from logcollect import file_handler,file_formatter


app = Flask(__name__)
app.logger.addHandler(file_handler)
base_dir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(base_dir, 'app.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
class Summary_Rolling_MoM(db.Model):
    """Sets up the database schema with table name=SRM. """
    __tablename__ = 'SRM'
    id = db.Column(db.Integer, primary_key=True)
   
    Calls_Offered = db.Column(db.Integer, nullable=False)
    Abandon_after_30s = db.Column(db.Float, nullable=False)
    FCR = db.Column(db.Float, nullable=False)
    DSAT = db.Column(db.Float, nullable=False)
    CSAT= db.Column(db.Float, nullable=False)
    
    def __init__(self,Calls_Offered,Abandon_after_30s,FCR,DSAT,CSAT):
        """Initialize an instance of Summary_Rolling_MoM."""
        app.logger.info('Adding Values to Databse')
        self.Calls_Offered = Calls_Offered
        self.Abandon_after_30s = Abandon_after_30s
        self.FCR = FCR
        self.DSAT = DSAT
        self.CSAT = CSAT

    def __repr__(self):
        """Returns the object representation in string."""
        return f'Calls Offered:{self.Calls_Offered} ---------- Abandon after 30s:{self.Abandon_after_30s} ---------- FCR:{self.FCR} ---------- DSAT:{self.DSAT} ---------- CSAT:{self.CSAT}'+"\n"


class VOC_Rolling_MoM(db.Model):
    """Sets up the database schema with table name=VRM. """
    app.logger.info('Adding Values to Databse')
    __tablename__ = 'VRM'
    id = db.Column(db.Integer, primary_key=True)
    Promoters = db.Column(db.String, nullable=False)
    Passives = db.Column(db.String, nullable=False)
    Dectractors = db.Column(db.String, nullable=False)

    def __init__(self,Promoters,Passives,Dectractors):
        """Initialize an instance of Summary_Rolling_MoM."""
        self.Promoters = Promoters
        self.Passives = Passives
        self.Dectractors = Dectractors

    def __repr__(self):
        """Returns the object representation in string."""
        return f'Promoters:{self.Promoters} ---------- Passives: {self.Passives} ---------- Detractors:{self.Dectractors}'


file=""
app.logger.info('Starting the Flask Parser App ...')
@app.route('/',methods=['GET', 'POST'])
def index():
    app.logger.info('Accesing the index page')
    """ Displays Index Page and Verification.
        Diplays Index Page when GET request received and when POST request is 
        received it Checks if given file is proccessed already or not.
        If file is not proccessed it performs file-name validations and 
        then adds the data to database.
    """
    if request.method == 'GET':
        return render_template('index.html')
    else:
        print(request.form)
        try:
            global file
            for key, file in request.form.items():
                with open('ServerFolder/Processed.lst', 'r') as fileobj:
                    app.logger.info('Reading content from File.list')
                    content = fileobj.read()
                    app.logger.info('Checking file present or not')
                    if file not in content:
                        app.logger.info('File not presentin list')
                        file_object = open('ServerFolder/Processed.lst', 'a')
                        file_object.write(file+'\n')
                        file_object.close()
                        app.logger.info('Validating file')
                        validated_file = FileModel(file_name=file)
                        validated_file.give_month_year(validated_file.file_name)
                        Calls_Offered,Abandon_after_30s,FCR,DSAT,CSAT=parse.parsing_worksheet1(validated_file.file_name,FileModel.file_month,FileModel.file_year)
                        Promoters,Passives,Dectractors=parse.parsing_worksheet2(validated_file.file_name,FileModel.file_month,FileModel.file_year)
                        app.logger.info('File Validated')
                        new_obj=Summary_Rolling_MoM( Calls_Offered,Abandon_after_30s,FCR,DSAT,CSAT)
                        app.logger.info('Creating database session and adding values')
                        db.session.add(new_obj)
                        db.session.commit()
                        app.logger.info('Values Comiited and session closed')
                        app.logger.info('Creating database session and adding values')
                        new_obj1=VOC_Rolling_MoM(Promoters,Passives,Dectractors)
                        db.session.add(new_obj1)
                        db.session.commit()
                        app.logger.info('Values Comiited and session closed')
                        fileobj.close() 
                    else:
                        app.logger.error("File Already Processed")
                        return render_template('Error.html')
            return render_template('Complete.html',Passives=Passives,Dectractors=Dectractors,Promoters=Promoters,Calls_Offered=Calls_Offered,Abandon_after_30s=Abandon_after_30s,FCR=FCR,DSAT=DSAT,CSAT=CSAT)
            #add redirect to to show data or printing the data by returning fn values
        except Exception as e:
            app.logger.error("Adding file to Error Folder")
            src_path = f"/vagrant/project_flask/ClientFolder/{file}"
            dst_path = f"/vagrant/project_flask/ErrorFolder/{file}"
            shutil.copy(src_path, dst_path)
            app.logger.error("Invalid File")
            return render_template('Mistake.html',e=e)

       #app.logger.info(f'Trying to post data to app...{request.form}')
@app.route('/allSRO')
def list_alldata():
    """Lists all the information from database with table SRM"""
    SRO = Summary_Rolling_MoM.query.order_by(Summary_Rolling_MoM.id).all()
    return render_template('SRO.html', SRO=SRO)
@app.route('/allVRM')
def list_alldata1():
    """Lists all the information from database with table VRM"""
    VRM = VOC_Rolling_MoM.query.order_by(VOC_Rolling_MoM.id).all()
    return render_template('VRM.html', VRM=VRM)
   

