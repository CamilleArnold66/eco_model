# Oopen class room clustering
# voir https://openclassrooms.com/fr/courses/4379436-explorez-vos-donnees-avec-des-algorithme[…]z-vos-donnees-avec-un-algorithme-de-clustering-hierarchique
'''
La particularité de cette algorithme de clustering est qu'il doit garder l'ordre temporel des semaines. Normalement, un algo de clustering fusionne deux point qui sont les plus proche. Ici, seul les semaines adjacentes, les clusters adjacents peuvent fusionner. Ainsi, à chaque fois qu'il y a fusion, nous prenons bien soin de replacer le nouveau cluster dans son emplacement'''
def clustering(dem,methode_distance_cluster='ward'):
    dem=dem.to_numpy()
    nb_w, nb_heures = dem.shape
    index_new_cluster=51
    # Z liste cluster utilisé classiquement par scipy.cluster.hierarchy
    # Z sera une liste où chaque élément correspond à une fusion entre deux cluster : [Index_cluster1, Index_cluster2, distance_cluster_1_et_2 , nombre_d'element_nouveau_cluster]
    Z=[]
    #Liste des index des clusters
    l_index_cluster=np.arange(nb_w)
    #Liste des listes des indices de chaque élements des cluster.
    l_index_weeks_cluster=[[i] for i in range(nb_w)]
    # l_index_weeks_cluster[i] est les indices des semaines composant le cluster d'indice l_index_cluster[i]
    for i in range(51) :
        #Liste des similarités ou listes des ditances entre tout les clusters. l_similarity[i] est la similarité entre cluster_i et cluster_i+1
        l_similarity= []
        nb_w, nb_heures = dem.shape
        for j in range(len(l_index_cluster)-1):
            l_cluster1=dem[l_index_weeks_cluster[j]]   #Liste des semaines présents dans cluster 1
            l_cluster2=dem[l_index_weeks_cluster[j+1]] #Liste des semaines présents dans cluster 2
            # Methode de ward
            if methode_distance_cluster=='ward' :
                similarity=ward_distance(l_cluster1,l_cluster2)
            # Methode de MNVAR
            elif methode_distance_cluster=='MNVAR' :
                similarity=variance_distance(l_cluster1,l_cluster2)
            #Ancienne Methode de Camille
            elif methode_distance_cluster== 'camille' :
                similarity=camille_distance(l_index_weeks_cluster[j],l_index_weeks_cluster[j+1],dem)
            else :
                print("methode non valide, fin de l_index_cluster'algo")
                sys.exit()
            l_similarity.append(similarity)
        index_min=np.argmin(l_similarity)
        #Modification de l_index_cluster
        index_new_cluster+=1
        index_cluster1=l_index_cluster[index_min] #
        index_cluster2=l_index_cluster[index_min+1]
        l_index_cluster=np.delete(l_index_cluster,index_min,axis=0)
        l_index_cluster=np.delete(l_index_cluster,index_min,axis=0)
        l_index_cluster=np.insert(l_index_cluster,index_min,index_new_cluster)
        #Modification de l_index_weeks_cluster
        index_weeks_cluster1 = l_index_weeks_cluster.pop(index_min) # Liste des index de semaine dans cluster 1
        index_weeks_cluster2 = l_index_weeks_cluster.pop(index_min) # Liste des index de semaine dans cluster 2
        index_weeks_fusion = index_weeks_cluster1 + index_weeks_cluster2 #Liste des index des semaine du nouveau cluster formé
        l_index_weeks_cluster.insert(index_min,index_weeks_fusion)
        Z.append([index_cluster1,index_cluster2,l_similarity[index_min],len(index_weeks_fusion)])
    return(Z)

def R_M4_Demand(number_of_mean_weeks, dem,print_info=True,methode_distance_cluster='ward'):
    Z=clustering(dem,methode_distance_cluster=methode_distance_cluster)
    t= 52 - number_of_mean_weeks
    groups=fcluster(Z, number_of_mean_weeks, criterion='maxclust')
    distance=np.array(Z)[:,2]
    element=groups[0]
    group_reindexed=[0]
    for i in range(1,len(groups)) :
        if element==groups[i] :
            group_reindexed+=[group_reindexed[i-1]]
        else :
            element=groups[i]
            group_reindexed+=[group_reindexed[i-1]+1]
    if print_info :
        #Affichage du dendrogramme
        plt.figure(figsize=(8.6, 3.5))
        plt.title('Dendrogramme CAH')
        dendrogram(np.array(Z))
        plt.gca().set_ylim(bottom=1e7)  # éviter les valeurs négatives dans l'échelle logarithmique
        plt.yscale('log')
        plt.xlabel('dem')
        plt.ylabel('Distance')
        plt.axhline(y=Z[52-1-number_of_mean_weeks][2], color='r', linestyle='--',
                    label=f"seuil pour {number_of_mean_weeks} dem réprésentatives")
        plt.legend()
        plt.show()
        print()
        #Figure distance - nombre de semaine représentative
        fig = go.Figure()
        fig.add_trace(go.Scatter(x= np.arange(51,0,-1), y=distance,mode='lines'))
        fig.add_vline(x=number_of_mean_weeks, line_dash='dash', line_color='red',
                      annotation_text=f"{number_of_mean_weeks} rpresentative weeks", annotation_position='top')
        fig.update_layout(title= str(methode_distance_cluster), yaxis_title='Distance',
                          xaxis_title="Nombre de dem représentatifs",
                    width=750,height=350,margin=dict(l=50,r=150,b=30,t=50),font=dict(size=15))
        fig.show()
        print("Les regroupements de dem avec " + str(number_of_mean_weeks) + " dem représentatives se font suivant : " + str(group_reindexed))
    return np.array(group_reindexed)
