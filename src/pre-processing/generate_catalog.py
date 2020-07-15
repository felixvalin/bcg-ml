import illustris_python as il
import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl
import pandas as pd
"""
Building a PRE-PROCESSED catalog for a set of clusters
"""
## Base parameters 
num_of_clusters = 10 # Starts with most massive and descending order
basePath = '/data/TNG300-2/output' # Worst resolution TNG300
# basePath = 'sims.illustris/Illustris-3/output'
snapshot = 99 # z = 0

## Fields needed
# All 8 magnitudes, GroupFirstSub, Rel_R, GroupNSubs, isBCG, SubhaloGrNr.
# Exceptions are 3d values.
# cluster_fields = ['GroupFirstSub', 'Group_M_Crit200',  'GroupPos', 'GroupVel', 'GroupNsubs']
cluster_fields_no_exceptions = ['GroupFirstSub', 'GroupNsubs'] # Only 1-dimensional values
galaxies_fields = ['SubhaloFlag', 'SubhaloGrNr','SubhaloGasMetallicity', 'SubhaloCM', 'SubhaloMass', 'SubhaloStellarPhotometrics']
galaxies_fields_no_exceptions = ['SubhaloGrNr', 'SubhaloGasMetallicity'] # Only 1-dimensional values

df_fields = ['SubhaloGrNr', 'SubhaloSFR', 'SubhaloMass', 'U_Band', 'B_Band', 'V_Band', 'K_Band', 'g_Band', 'r_Band', 'i_Band', 'z_Band', 'GroupFirstSub', 'Group_M_Crit200', 'GroupNsubs']
df_fields = ['SubhaloGrNr', 'SubhaloGasMetallicity', 'U_Band', 'B_Band', 'V_Band', 'K_Band', 'g_Band', 'r_Band', 'i_Band', 'z_Band', 'GroupFirstSub', 'GroupNsubs']

## Load all galaxies
galaxies = il.groupcat.loadSubhalos(basePath, snapshot, fields=galaxies_fields)
all_subhalos_df = pd.DataFrame(columns=df_fields)

## Load individual clusters
for haloID in range(num_of_clusters):
    cluster = il.groupcat.loadSingle(basePath, snapshot, haloID=haloID) # Load a single complete halo
#     cluster_member_indices = np.logical_and(galaxies['SubhaloGrNr'] == haloID, galaxies['SubhaloFlag']==1) # Checks for GroupID and for correct flag (1)
    cluster_member_indices = galaxies['SubhaloGrNr'] == haloID
    cluster_members = [galaxies[field][cluster_member_indices] for field in galaxies_fields]
    
    # Find the BCG for this cluster using Subhalo position
    BCG = il.groupcat.loadSingle(basePath, snapshot, subhaloID=cluster['GroupFirstSub'])
    isBCG = np.zeros(cluster['GroupNsubs'])
    for i in range(cluster['GroupNsubs']-1):
        if (BCG['SubhaloCM'] == cluster_members[2][i]).all():
            isBCG[i] = 1
            
#     if np.sum(isBCG) != 1:
#         print("Did not find a BCG for clusterID = "+haloID)
        

    ## Generate the Pandas DataFrame
    cluster_df = pd.DataFrame()
    cluster_df['isBCG'] = isBCG
    
    ## Multi-values fields (splitted)
#     cluster_df['SubhaloCMX'] = galaxies['SubhaloCM'][cluster_member_indices][:,0]
#     cluster_df['SubhaloCMY'] = galaxies['SubhaloCM'][cluster_member_indices][:,1]
#     cluster_df['SubhaloCMZ'] = galaxies['SubhaloCM'][cluster_member_indices][:,2]
#     cluster_df['SubhaloVelX'] = galaxies['SubhaloVel'][cluster_member_indices][:,0]
#     cluster_df['SubhaloVelY'] = galaxies['SubhaloVel'][cluster_member_indices][:,1]
#     cluster_df['SubhaloVelZ'] = galaxies['SubhaloVel'][cluster_member_indices][:,2] 
    cluster_df['U_Band'] = galaxies['SubhaloStellarPhotometrics'][cluster_member_indices][:,0]
    cluster_df['B_Band'] = galaxies['SubhaloStellarPhotometrics'][cluster_member_indices][:,1]
    cluster_df['V_Band'] = galaxies['SubhaloStellarPhotometrics'][cluster_member_indices][:,2]
    cluster_df['K_Band'] = galaxies['SubhaloStellarPhotometrics'][cluster_member_indices][:,3]
    cluster_df['g_Band'] = galaxies['SubhaloStellarPhotometrics'][cluster_member_indices][:,4]
    cluster_df['r_Band'] = galaxies['SubhaloStellarPhotometrics'][cluster_member_indices][:,5]
    cluster_df['i_Band'] = galaxies['SubhaloStellarPhotometrics'][cluster_member_indices][:,6]
    cluster_df['z_Band'] = galaxies['SubhaloStellarPhotometrics'][cluster_member_indices][:,7]
    
    ## Single values fields
    for field in galaxies_fields_no_exceptions:
        cluster_df[field] = galaxies[field][cluster_member_indices]
        
    ## Cluster-wide values
    ## Multi-values fields (splitted)
#     cluster_df['GroupVelX'] = cluster['GroupVel'][0]
#     cluster_df['GroupVelY'] = cluster['GroupVel'][1]
#     cluster_df['GroupVelZ'] = cluster['GroupVel'][2] 
#     cluster_df['GroupCMX'] = cluster['GroupCM'][0]
#     cluster_df['GroupCMY'] = cluster['GroupCM'][1]
#     cluster_df['GroupCMZ'] = cluster['GroupCM'][2]
    
    ## Pre-Processed Columns
    # Generating the relative radii for each subhalo (subhaloCM-groupCM)/Group_R_Crit200
    rel_R = []
    for i in galaxies['SubhaloCM'][cluster_member_indices]:
        rel_R.append(np.linalg.norm(i - cluster['GroupCM'])/cluster['Group_R_Crit200'])
    cluster_df['Rel_R'] = rel_R
    
    ## Single values fields
    for field in cluster_fields_no_exceptions:
        cluster_df[field] = cluster[field]
        
    ## Merge with master DataFrame
    all_subhalos_df = all_subhalos_df.append(cluster_df, ignore_index=True, sort=False)

# Save as a csv file
all_subhalos_df.to_csv("/data/TNG300-2/postprocessing/catalogs/group_099.csv")
