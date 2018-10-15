#README#
########
#Le fichier de sortie (BLAST) doit etre compose de la maniere suivante:
#query id-nomdugenome-/tab subject id-nomdugenome-nomproteine /tab %identity /tab alignment length/tab mismatches /tab gap opens /tab q. start /tab q. end /tab s. start /tab s. end /tab evalue /tab bit score
#exemple->WP_009560677.1-GCF000020825.1-	WP_009560677.1-GCF000020825.1-	100.00	203	0	0	1	203	1	203	3e-149	420b
import os
import os.path




result_blast=open("/DATA/NCBI/Programcomparaison/fichiersortie_essais.txt","r")
result=open("/DATA/NCBI/Programcomparaison/result_script.txt","w")
rs=result_blast.readlines()

findex=open("/DATA/NCBI/Programcomparaison/Index_NCBI_essais.txt","r")
#findex=open(index_path,"r")
f=findex.readlines()


#------------------------------------------------------------------------------
#liste :

query_id=[] #contient le nom des sequences compares
query_id_2=[]
query_id_3=[] # reecriture de la sequence -> ajout de 
query_identity=[] #contient le ppourcentage de similarite
query_evalue=[]#contient la evalue
subject_id=[]# contient le nom des sequences+nom de la proteine de la banque de donnees
subject_id_2=[]
subject_id_3=[]
liste=[]
refseq_all_taxonomie=[]
refseq_taxonomie=[]
refseq_taxonomie_phylum=[]
refseq=[]
liste_genome_non_ok=[]
liste_different_genome=[]
#-----------------------------------------------------------------------------------
#Dictionnaire:
dic_ref_seq_phylum={}#Contient la reference du genome, et son phylum, exemple: PROTEOBACTERIA
dic_ref_seq_taxonomie={}#Contient la reference du genome et sa classe, exemple:GAMMAPROTEOBACTERIA
dic_genome={}
dic_different_percent={}
liste_genome={}
dic_different_percent={}#dic contenant les genomes avec le mauvais phylum et le pourcentage
#Fonction
def comparaison_taxonomie(a,b): #permet de compter la similarite taxonomique
	compteur=0
	for i,j in a,b:
		if i==j:
			compteur=compteur+1
		else:
			 break
	return compteur +"/5"
#Variables
compteur_sequence=0
correct=0
non_correct=0
#----------------------------------------------------------------------------------------------------------------------------	
#Permet de parcourir le fichier issue de blast, et d'en retirer le nom de la query, du sujet, son pourcentage d identite
#seul les alignements avec un WP similaire sont gardes

for line in rs:
	if line.startswith("WP"):
		line_parse=line.split(" ")
		for column in line_parse:
			columnv2=column.split("	")
			columnv3=column.split("-")
			columnv6=columnv2[1]
			columnv4=columnv3[0]
			columnv5=columnv3[2]
			columnv7=columnv6[0:14]
			if columnv4==columnv7: # remplis les listes uniquements si  les deux Wp sont identiques sinon stop
				compteur_sequence=compteur_sequence+1
	 			query_id.append(columnv2[0])
				subject_id.append(columnv2[1])
				query_identity.append(columnv2[2])
				query_evalue.append(columnv2[10])
			
for i in query_id:
	query_id_2.append(i[15:29])
for i in query_id_2:
	query_id_3.append(i[0:3]+'_'+i[3:])
for i in subject_id:
	subject_id_2.append(i[15:29])
for i in subject_id_2:
	subject_id_3.append(i[0:3]+"_"+i[3:])


#-------------------------------------------------------------------------------
#Permet de creer un dictionnaire avec Key->RefSeq et Value->Taxonomie
ref=[]
tax=[]
phy=[]

for lineindex in f:
	if lineindex.startswith("GCA"):
		lineindex_parse=lineindex.split("	")
		lineindex_parse_taxonomie=lineindex.split(";")
		ref.append(lineindex[16:31])
		tax.append(lineindex_parse_taxonomie[2:3])
		phy.append(lineindex_parse_taxonomie[1:2])

	else:
		continue
dic_phylum=dict(zip(ref,phy))
dic_tax=dict(zip(ref,tax))

#--------------------------------------------------------------------------------
liste_ref_seqs=zip(query_id_3,subject_id_3)

for x,y in liste_ref_seqs: #permet de recuperer le nom du genome, son phyllum, et son taxon grace au dictionnaire
	xref=dic_phylum.get(x) 
	xref2=dic_tax.get(x) 
	yref=dic_phylum.get(y)
	yref2=dic_tax.get(y)
	
	if xref2==yref2:
		correct=correct+1
	if xref2!=yref2:
		non_correct=non_correct+1 
		liste_genome_non_ok.append(x +"	"+str(yref2[0])+"	" +str(xref2[0])) #permet de mettre a la suite la ref du genome, son phyllum, son taxon dans une liste
		#print x,xref,xref2,y,yref,yref2

#print liste_genome_non_ok, float(non_correct)/float(len(liste_ref_seqs))*100,"%"
#-----------------------------------------------------------------------------------------
#Permet d'avoir chaque type d'erreur sans redondance
for string in liste_genome_non_ok: #permet de faire une liste de toutes les differentes possiblites
	if string in liste_different_genome:
		continue
	else:
		liste_different_genome.append(string)
#-----------------------------------------------------------------------------------------
#liste du nombre de chaque genome
nombre=0
for i in query_id_3:
	if i in liste_genome:
		nombre=nombre+1
		liste_genome[i]=nombre
	
	if i not in liste_genome:
		nombre=0
		nombre=nombre+1
		liste_genome[i]=nombre
print liste_different_genome
#---------------------------------------------------------------------------------
#Recap des differentes erreurs avec le genome et phylum ainsi que son pourcentage

for keys in liste_different_genome: #parcours la liste des genomes faux deja trier (donc pas de redondance)
	compteur=0
	for j in liste_genome_non_ok: # parcours la liste complete de tout les genome, et ajoute +1, afin de savoir combien de fois il y a cette erreur
		if j == keys:
			tot=liste_genome.get(j[0:15])
			compteur=compteur+1
			if tot=="0":
				percent=0
			else:
				percent=round(compteur*100/float(tot),4)
			dic_different_percent[keys]=percent # le genome+phyllum sont une key et le pourcentage une valeur


#--------------------------------------------------------------------------------
#Ecriture sur le fichier de sortie
result.write("RESULTAT \n")
result.write("Sequence number:"),result.write(str(compteur_sequence )),result.write("\n")
result.write("Number of correct taxonomy:"), result.write(str(correct)),result.write("\n")
result.write("Number of noncorrect taxonomy:"), result.write(str(non_correct)),result.write("\n")
result.write("\n")
result.write("#Ref seq code 	")
result.write("#Correct Class 	")
result.write("#Class 	")
result.write("#%	")
result.write("\n")
for i,j in dic_different_percent.iteritems():
	result.write(i),
	result.write(" "),
	result.write(str(j)),
	result.write("%")
	result.write("\n")


#os.system('sh C:\\temp\\script.sh') pour lancer le script r depuis python avec les result du script python 