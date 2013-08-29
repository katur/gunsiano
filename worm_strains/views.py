from django.template import RequestContext # extends Context; needed for STATIC_URL
from django.shortcuts import render_to_response, get_object_or_404 # r_to_r loads template, passes c    ontext, renders
from worm_strains.models import *
from storage.models import *
import string

def strains(request):
	"""
	Page listing worms strains, with possible filtering
	"""
	# get all worm strains
	strains = WormStrain.objects.all().order_by('strain_sort')	
	
	for strain in strains:	
		"""
		The following, commented out, would dynamically generate genotypes 
		when they can be created from the background and a single transgene.
		For performance, all genotypes are instead hard-coded into the database,
		using the generate_genotype function in this module along with
		the script worm_strains/management/commands/insert_genotypes_into_database.py
		(which can be run with "python manage.py insert_genotypes_into_database").
		"""
		"""
		generate_genotype(strain)
	
		"""
		strain.truncated_species = strain.species.name.replace("Caenorhabditis", "C.")

	# render page
	return render_to_response('strains.html', {
		'strains':strains
	}, context_instance=RequestContext(request))


def strain(request, name):
	"""
	Page showing information on a particular worm strain.
	"""
	# get the strain
	strain = get_object_or_404(WormStrain, name=name)
	
	# get the strain lines
	lines = WormStrainLine.objects.filter(strain=strain).order_by('date_received')
	for line in lines:
		line.stocks = Stock.objects.filter(stockable=line.stockable).order_by('date_prepared')	
		for stock in line.stocks:
			stock.tubes = Container.objects.filter(stock=stock, is_thawed=False)
		
			for tube in stock.tubes:
				tube.vertical_letter = chr(tube.vertical_position + 64)		
			try:
				stock.thaw_80 = Container.objects.get(stock=stock, parent=7)
			except Container.DoesNotExist:
				stock.thaw_80 = None
			
			try:
				stock.thaw_N = Container.objects.get(stock=stock, parent=8)
			except Container.DoesNotExist:
				stock.thaw_N = None
			
	# get lab code by extracting the letters from the strain name (usually 2 letters but sometimes more)
	all = all=string.maketrans('','')	
	letters_only = all.translate(all, string.ascii_uppercase)
	strain_code = str(strain.name).translate(all, letters_only)	
	try:
		strain.lab = WormLab.objects.get(strain_code=strain_code)
	except WormLab.DoesNotExist:
		strain.lab = None
	
	
	return render_to_response('strain.html', {
		'lines':lines,
		'strain':strain,
	}, context_instance=RequestContext(request))


def generate_genotype(strain):
	if strain.transgene and strain.parent_strain:
		vector = strain.transgene.vector
		strain.genotype = strain.transgene.name + "[" + vector.parent_vector.genotype_pattern + "]"
		strain.genotype = strain.genotype.replace("gene", vector.gene)
		strain.genotype = strain.genotype.replace("promoter", vector.promoter)
		strain.genotype = strain.genotype.replace("threePrimeUTR", vector.three_prime_utr)
		if strain.parent_strain.name == "DP38":
			strain.genotype = "unc-119(ed3) III; " + strain.genotype
