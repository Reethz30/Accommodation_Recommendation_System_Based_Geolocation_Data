import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
df=pd.read_csv('ML_Project_Data.csv')
a=['Unnamed: 14','Unnamed: 15','Unnamed: 16']
df=df.drop(a, axis=1)
df.plot(kind='scatter', x='Temperature( C)', y='Humidity', s=32, alpha=.8)
plt.gca().spines[['top', 'right',]].set_visible(False)
a=df
a=a.drop_duplicates(subset=['Area'])
a=a['Area']
a=pd.DataFrame(a)
rn=[]
for i in a['Area']:
  fil=df[df['Area']==i]
  rn.append(int(fil['Rent'].mean()))
plt.figure(figsize=(12,10))
plt.bar(a['Area'],rn,width=0.4)
plt.xticks(rotation=90)
plt.show()
df=df[df['nBHK']<=3]
df.describe()
df.boxplot()
plt.show()
x=df[df['Rent']>=150000]
df.loc[df['s.no']==447,'Rent']=23000
plt.figure(figsize=(12,10))
df.boxplot()
plt.show()
fam=[]
bac=[]
tem=[]
rf=[]
flo=[]
hum=[]
saf=[]
con=[]
n=[]
lat=[]
lon=[]
for i in a['Area']:
  fil=df[df['Area']==i]
  fam.append(int(fil['Family'].sum()))
  bac.append(int(fil['Bachelors'].sum()))
  tem.append(int(fil['Temperature( C)'].mean()))
  hum.append(int(fil['Humidity'].mean()))
  rf.append(int(fil['Rainfall'].mean()))
  flo.append(int(fil['Flooding'].mean()))
  saf.append(int(fil['Safety'].mean()))
  con.append(int(fil['Connectivity'].mean()))
  n.append(int(fil['nBHK'].mean()))
  lat.append(fil['Latitude'].mean())
  lon.append(fil['Longitude'].mean())
ndf={
    'Area': a['Area'],
    'Temperature': tem,
    'Humidity': hum,
    'Rainfall': rf,
    'Flooding': flo,
    'nBHK': n,
    'Rent': rn,
    'Safety':saf,
    'Connectivity': con,
    'Family': fam,
    'Bachelors': bac,
    'Latitude': lat,
    'Longitude': lon
}
new_df=pd.DataFrame(ndf)
plt.figure(figsize=(12,10))
new_df.boxplot()
plt.show()
j=1
an=[]
for i in a['Area']:
  an.append(j)
  j+=1
new_df.insert(0,'Area No.',an)
new_df=new_df.drop('Area',axis=1)
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
sc=StandardScaler()
sf=sc.fit_transform(new_df)
sdf=pd.DataFrame(sf)
km=KMeans(n_clusters=3,random_state=101,max_iter=300)
new_df['Cluster']=km.fit_predict(sdf)
print(new_df.head())
new_df.insert(1,'Area',a['Area'])
import folium
m1=folium.Map(location=(17.38405,78.45636),zoom_start=11.2)
cluster_color={0: 'red', 1: 'blue', 2: 'green'}
cluster_groups={0: folium.FeatureGroup(name="Difficult"),
                1: folium.FeatureGroup(name="Average"),
                2: folium.FeatureGroup(name="Reasonable")}
for _,i in new_df.iterrows():
    c=i['Cluster']
    if i['Bachelors']>10:
        type1="Bachelor & Family Friendly"
    else:
        type1="Family Friendly"
    folium.Marker(
        location=(i['Latitude'],i['Longitude']),
        icon=folium.Icon(color=cluster_color[c]),
        popup=f"Area: {i['Area']}, Rent: {i['Rent']}, Temp: {i['Temperature']}, Humidity: {i['Humidity']}, Rainfall: {i['Rainfall']}, {type1}"
    ).add_to(cluster_groups[c])

for i in cluster_groups.values():
    i.add_to(m1)
folium.LayerControl().add_to(m1)
m1
op='output.html'
m1.save(op)
