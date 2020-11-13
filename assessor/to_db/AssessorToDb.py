import requests, zipfile, io
import os
import pandas as pd
from datetime import date
import urllib
import pyodbc
import sqlalchemy

class AssessorETL(object):

	def __init__(self):
		self.working_dir = './working'
		self.file_dict = {}
		self.schema = ''


	def create_working_dir(self):
		try:
			if not os.path.isdir(self.working_dir):
				os.mkdir(self.working_dir)
		except Exception as e:
			print('error in create_working_dir routine')
			raise

	def download_and_unzip(self, url):
		try:
			self.create_working_dir()
			r = requests.get(url)
			z = zipfile.ZipFile(io.BytesIO(r.content))
			z.extractall(self.working_dir)
		except Exception as e:
			raise

	def download_files(self):
		try:
			fd = self.file_dict
			for f in fd.keys():
				fname = fd[f][0]
				fname = fname.replace(' ', '%20')
				fname = self.url_base + fname
				self.download_and_unzip(fname)
		except Exception as e:
			raise

	def file_name_to_table_name(self, file_name):
		try:
		    s = file_name
		    s = s.replace('EXTR_','')
		    s = s[:-4]
		    return s
		except Exception as e:
			raise


	def files_to_df_dict(self):
	    try:
	        df_dict = {}
	        for f in os.scandir(working_dir):
	            f = f.name
	            if f[-4:] == '.txt':
	                key = self.file_name_to_table_name(f)
	                df = pd.read_csv(working_dir + '/' + f,
				                	sep='|',
				                	encoding = 'ISO-8859-1')
	                df_dict[key] = df
	        return df_dict
	    except Exception as e:
	        print('filename: {}'.format(f))
	        raise


	def create_df_dict(self):
	    try:
	        df_dict = {}
	        for k in self.file_dict:
	            f = self.file_dict[k][0]
	            f = f.replace('.zip', '.txt')
	            if f[-4:] == '.txt':
	                df = pd.read_csv(self.working_dir + "/" + f,
	                                 sep='|',
	                                 encoding="ISO-8859-1")
	            elif f[-4:] == '.csv':
	            	df = pd.read_csv(self.working_dir + '/' + f,
	            					encoding='ISO-8859-1')
	            df_dict[k] = df
	        return df_dict
	    except Exception as e:
	        raise


	def process_csv_files(self):
	    try:
	        #df_dict = csv_files_to_df_dict()
	        df_dict = self.create_df_dict()
	        # for each df in df_dict, send df to Sockeye
	        self.make_engine()
	        today = date.today()
	        for df_key in df_dict.keys():
	            df = df_dict[df_key]
	            str_date = today.strftime("_%Y%m%d")
	            table_name = df_key +  str_date
	            df.to_sql(name=table_name, schema=self.schema, con=self.engine)
	    except Exception as e:
	        print(df_key)
	        raise


	def make_engine(self):
	    """
	    Make connections to the database
	    """
	    try:
	        conn_string = "DRIVER={{ODBC Driver 17 for SQL Server}}; " \
	            "SERVER={}; DATABASE={}; trusted_connection=yes".format(
	                'AWS-PROD-SQL\\Sockeye',
	                'Assessor')
	        #self.sql_conn = pyodbc.connect(conn_string)
	        params = urllib.parse.quote_plus(conn_string)
	        engine = sqlalchemy.create_engine("mssql+pyodbc:///?odbc_connect=%s" % params)
	        self.engine = engine
	    except Exception as e:
	        print(e.args[0])
	        raise

	def import_data(self):
		try:
			print("importing data for {}".format(self.schema))
			self.download_files()
			#self.process_csv_files()
		except Exception as e:
			print(e.args[0])
			raise


class PierceAssessorETL(AssessorETL):
	import PierceColNames as pcn

	def __init__(self):
		super().__init__()
		self.schema = 'Pierce'
		self.file_dict = {'appraisal_account': ['appraisal_account.zip', pcn.appraisal_account_cols],
	            # 'improvement': ['improvement.zip', pcn.improvement_cols],
	            # 'improvement_builtas': ['improvement_builtas.zip', pcn.improvement_builtas_cols],
	            # 'land_attribute': ['land_attribute.zip', pcn.land_attribute_cols],
	            'improvement_detail': ['improvement_detail.zip', pcn.improvement_detail_cols]}
		self.url_base = 'https://online.co.pierce.wa.us/datamart/'


	def create_df_dict(self):
	    try:
	        df_dict = {}
	        for k in self.file_dict:
	            f = self.file_dict[k][0]
	            f = f.replace('.zip', '.txt')
	            if f[-4:] == '.txt':
	                df = pd.read_csv(self.working_dir + "/" + f,
	                                 sep='|',
	                                 encoding="ISO-8859-1",
	                                 names=self.file_dict[k][1])
	                df_dict[k] = df
	        return df_dict
	    except Exception as e:
	        raise


class KingAssessorETL(AssessorETL):

	def __init__(self):
		super().__init__()
		self.working_dir = './working_king'
		self.schema = 'King'
		self.file_dict = {'parcel': ['Parcel.zip'],
		            'RealPropAcct': ['Real Property Account.zip'],
		            'CondoComplexAndUnits': ['Condo Complex and Units.zip'],
		            'ResBuilding': ['Residential Building.zip'],
		            'ApartmentComplex': ['Apartment Complex.zip'],
			        'CommercialBuilding': ['Commercial Building.zip']}
		self.url_base = 'https://aqua.kingcounty.gov/extranet/assessor/'
