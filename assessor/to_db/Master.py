import AssessorToDb

def main_routine():
	try:
		king_a = AssessorToDb.KingAssessorETL()
		king_a.import_data()
		kitsap_a = AssessorToDb.KitsapAssessorETL()
		kitsap_a.import_data()
		pierce_a = AssessorToDb.PierceAssessorETL()
		pierce_a.import_data()
		snohomish_a = AssessorToDb.SnohomishAssessorETL()
		snohomish_a.import_data()
		print("import completed")
	except Exception as e:
		raise


main_routine()
