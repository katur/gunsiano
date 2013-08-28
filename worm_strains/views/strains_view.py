from django.template import RequestContext # extends Context; needed for STATIC_URL
from django.shortcuts import render_to_response, get_object_or_404 # r_to_r loads template, passes c    ontext, renders
from worm_strains.models import *

def strains(request):
	"""
	Page listing worms strains, with possible filtering
	"""
	# get all worm strains
	strains = WormStrain.objects.all().order_by('strain_sort')	
	

	"""
	The following code, commented out, dynamically creates genotypes when a transgene and parent strain are listed.
	For speed, I instead hard-coded these genotypes into the database
	using a script that resembles the code below (scripts/insert_genotypes_into_database.py).
	If the genotype format changes, it must be changed in the script and the script run to update the database.
	If we want to change back to dynamically generated genotypes, uncomment the lines below.
	"""
	"""
	for strain in strains:
		if strain.transgene and strain.parent_strain:
			vector = strain.transgene.vector
			strain.genotype = strain.transgene.name + "[" + vector.parent_vector.genotype_pattern + "]"
			strain.genotype = strain.genotype.replace("gene", vector.gene)
			strain.genotype = strain.genotype.replace("promoter", vector.promoter)
			strain.genotype = strain.genotype.replace("threePrimeUTR", vector.three_prime_utr)
			if strain.parent_strain.name == "DP38":
				strain.genotype = "unc-119(ed3) III; " + strain.genotype
	"""
	
	
	# render page
	return render_to_response('strains.html', {
		'strains':strains
	}, context_instance=RequestContext(request))
