import MySQLdb
import sys

def main():
        db = MySQLdb.connect(user="root", db="gunsiano", read_default_file="~/.my.cnf")
        c = db.cursor()
        num_rows = c.execute("""
		SELECT child.id, parent.name, transgene.id, transgene.name
		FROM worm_strains_wormstrain AS child
		LEFT JOIN worm_strains_wormstrain AS parent
		ON child.parent_strain_id = parent.id
		LEFT JOIN worm_strains_transgene AS transgene
		ON child.transgene_id = transgene.id
		WHERE child.parent_strain_id IS NOT NULL 
		AND child.transgene_id IS NOT NULL
	""")
        result = c.fetchall()
        c.close()
	print "Number of strains to generate genotypes for is " + str(num_rows)

	i = 0
        for row in result:
                strain_id = row[0]
                parent_strain_name = row[1]
		transgene_id = row[2]
                transgene_name = row[3]
                
		c = db.cursor()
		num_rows = c.execute("""
			SELECT child.gene, child.promoter, child.three_prime_utr, parent.genotype_pattern
			FROM vectors_vector AS child
			LEFT JOIN vectors_vector AS parent
			ON child.parent_vector_id = parent.id
			LEFT JOIN worm_strains_transgene
			ON worm_strains_transgene.vector_id=child.id
			WHERE worm_strains_transgene.id=%s
		""", (transgene_id))
		result = c.fetchall()
		c.close()
		
		for row in result:
			gene = row[0]
			promoter = row[1]
			three_prime_utr = row[2]
			genotype_pattern = row[3]
			genotype = transgene_name + "[" + genotype_pattern + "]"
			genotype = genotype.replace("gene", gene)
			genotype = genotype.replace("promoter", promoter)
			genotype = genotype.replace("threePrimeUTR", three_prime_utr)
			if parent_strain_name == "DP38":
				genotype = "unc-119(ed3) III; " + genotype
			print genotype
                c = db.cursor()
                c.execute("""UPDATE worm_strains_wormstrain SET genotype = %s WHERE id=%s;COMMIT;""", (genotype, strain_id))
                i += 1
		c.close()
			
	print i
        db.close()

main()
