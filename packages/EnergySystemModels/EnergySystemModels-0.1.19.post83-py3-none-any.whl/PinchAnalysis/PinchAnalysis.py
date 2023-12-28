import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

class PinchAnalysis:
    def __init__(self, df):

        # Créer la colonne 'integration' et la remplir avec True si elle n'existe pas
        if 'integration' not in df.columns:
            df['integration'] = True
        # Remplacer les valeurs NaN par True
        df['integration'].fillna(True, inplace=True)

        # Sélectionner les flux à intégrer
        self.liste_flux = df[df['integration'] == True].copy()  # Utilisez .copy() pour éviter le Warning

        self.rowCount = len(self.liste_flux)

        # Créer la colonne 'NatureFlux'
        self.liste_flux['NatureFlux'] = np.where(self.liste_flux['Ti'] > self.liste_flux['To'], 'HS', 'CS')

        # Créer de nouvelles colonnes pour les températures décalées
        self.liste_flux['Ti_shifted'] = np.where(self.liste_flux['NatureFlux'] == 'HS',
                                                  self.liste_flux['Ti'] - self.liste_flux['dTmin2'],
                                                  self.liste_flux['Ti'] + self.liste_flux['dTmin2'])

        self.liste_flux['To_shifted'] = np.where(self.liste_flux['NatureFlux'] == 'HS',
                                                  self.liste_flux['To'] - self.liste_flux['dTmin2'],
                                                  self.liste_flux['To'] + self.liste_flux['dTmin2'])

         # Calculer T_shifted directement dans la classe
        T_shifted = np.concatenate([self.liste_flux['Ti_shifted'].values, self.liste_flux['To_shifted'].values])
        T_shifted = np.sort(np.unique(T_shifted))[::-1]
        self.df_T_shifted = pd.DataFrame({'T_shifted': T_shifted})



                # Créer le DataFrame df_intervall
        self.df_intervall = pd.DataFrame({'Tsup': T_shifted[:-1], 'Tinf': T_shifted[1:]})
        self.df_intervall['IntervalName'] = self.df_intervall['Tsup'].astype(str) + '-' + self.df_intervall['Tinf'].astype(str)

        self.decomposition_flux()
        self.surplus_deficit()


    def decomposition_flux(self):
        # Ajouter des colonnes pour le nom du flux et la valeur de mCp à df_intervall
        self.df_intervall['FluxName'] = [[] for _ in range(len(self.df_intervall))]
        self.df_intervall['mCp'] = [[] for _ in range(len(self.df_intervall))]
        self.df_intervall['NatureFlux'] = [[] for _ in range(len(self.df_intervall))]  # Add this line
  

        # Parcourir chaque intervalle
        for idx, row in self.df_intervall.iterrows():

            # Parcourir chaque flux
            for i in range(self.rowCount):
                
               
                # Tester la condition spécifique (NatureFlux[i] == "CS")
                if (self.liste_flux['NatureFlux'][i] == "CS") and (self.liste_flux['Ti_shifted'][i] < row['Tsup']) and (self.liste_flux['To_shifted'][i] > row['Tinf']):
                    # Flux dans l'intervalle
                    self.df_intervall.at[idx, 'mCp'].append(-self.liste_flux['mCp'][i])
                    self.df_intervall.at[idx, 'FluxName'].append(self.liste_flux['name'][i])
                    self.df_intervall.at[idx, 'NatureFlux'].append(self.liste_flux['NatureFlux'][i])  # Add this line
         
                
                 

                # Tester la condition spécifique (NatureFlux[i] == "HS")
                elif (self.liste_flux['NatureFlux'][i] == "HS") and (self.liste_flux['Ti_shifted'][i] > row['Tinf']) and (self.liste_flux['To_shifted'][i] < row['Tsup']):
                    # Flux dans l'intervalle
                    self.df_intervall.at[idx, 'mCp'].append(self.liste_flux['mCp'][i])
                    self.df_intervall.at[idx, 'FluxName'].append(self.liste_flux['name'][i])
                    self.df_intervall.at[idx, 'NatureFlux'].append(self.liste_flux['NatureFlux'][i])  # Add this line
            

        # Utiliser explode pour dupliquer les lignes pour chaque valeur de mCp
        self.df_intervall = self.df_intervall.explode(['FluxName', 'mCp', 'NatureFlux']).reset_index(drop=True)
        self.df_intervall = self.df_intervall.sort_values(by=['FluxName', 'Tsup']).reset_index(drop=True)
        self.df_intervall["delta_T"]=self.df_intervall['Tsup']-self.df_intervall['Tinf']
        self.df_intervall["delta_H"]=self.df_intervall["delta_T"]*self.df_intervall["mCp"]



    def plot_shifted_streams(self):

      # Extract necessary columns from the DataFrame
      NatureFlux = self.liste_flux['NatureFlux']
      names = self.liste_flux['name']
      Ti_shifted = self.liste_flux['Ti_shifted']
      To_shifted = self.liste_flux['To_shifted']

      # Create a new figure
      plt.figure(figsize=(8, 6))

      # Plot the streams with shifted temperature scale and color based on NatureFlux
      for i in range(len(names)):
        if NatureFlux[i] == 'HS':
          plt.plot([names[i], names[i]], [Ti_shifted[i], To_shifted[i]], color='red', label=f'Stream {names[i]}')
          # Ajouter une flèche à la fin du segment
          plt.annotate('', xy=(names[i], To_shifted[i]), xytext=(names[i], To_shifted[i] + 1),
                      arrowprops=dict(arrowstyle='->', color='red', lw=1), annotation_clip=False)

        else:
          plt.plot([names[i], names[i]], [Ti_shifted[i], To_shifted[i]], color='blue', label=f'Stream {names[i]}')

          plt.annotate('', xy=(names[i], To_shifted[i]), xytext=(names[i], To_shifted[i] - 1),
                      arrowprops=dict(arrowstyle='->', color='blue', lw=1), annotation_clip=False)


      # Set y-axis ticks and labels
      y_ticks = sorted(set(Ti_shifted) | set(To_shifted))
      plt.yticks(y_ticks)

      # Add horizontal dashed lines for each temperature value
      for temp in y_ticks:
          plt.axhline(y=temp, linestyle='--', color='gray', alpha=0.7)

      # Set axis labels and title
      plt.xlabel('nom des flux')
      plt.ylabel('Température décallée (°C)')
      plt.title("Représentation des flux à l’aide de l’échelle de température unifiée")

      # Show grid
      plt.grid(True)

      # Show the plot without legend
      plt.show()

    def surplus_deficit(self):
      # Group by 'IntervalName' and aggregate the values
      self.df_surplus_deficit = self.df_intervall.groupby('IntervalName').agg({
          'Tsup': 'first',  # Keep the first value
          'Tinf': 'first',  # Keep the first value
          'FluxName':  lambda x: list(x),  # Keep the first value
          'mCp': 'sum',  # Sum the 'mCp' values
          'NatureFlux': lambda x: list(x),  # Keep the first value
          'delta_T': 'first',  # Sum the 'delta_T' values
          'delta_H': 'sum'  # Sum the 'delta_H' values
      }).reset_index()

      # Sort by 'Tsup' in descending order
      self.df_surplus_deficit = self.df_surplus_deficit.sort_values(by='Tsup', ascending=False)

      self.df_surplus_deficit['cumulative_delta_H'] =self.df_surplus_deficit['delta_H'].cumsum()

      self.EMR_chaud=abs(min(self.df_surplus_deficit['cumulative_delta_H']))


      # Créer une ligne avec la valeur 0 pour 'cumulative_delta_H'
      self.cumulative_delta_H = pd.concat([pd.Series([0], name='cumulative_delta_H'), self.df_surplus_deficit['cumulative_delta_H']], ignore_index=True)

      # Ajouter la nouvelle ligne à self.EMR_chaud
      self.cumulative_delta_H = pd.DataFrame(self.EMR_chaud + self.cumulative_delta_H)

      # Concaténer les deux colonnes dans un nouveau DataFrame
      self.GCC = pd.concat([self.df_T_shifted, self.cumulative_delta_H], axis=1)

      # Récupérer la valeur de cumulative_delta_H correspondante
      self.EMR_froid = self.GCC.loc[self.GCC['T_shifted'].idxmin(), 'cumulative_delta_H']

      # Récupérer la valeur de T_shifted correspondante à cumulative_delta_H nulle
      self.Pinch_Temperature = self.GCC.loc[self.GCC[self.GCC['cumulative_delta_H'] == 0].index, 'T_shifted'].values[0]

    

    def plot_GCC(self):

      # Tracer la courbe de composition avec les axes inversés
      plt.plot(self.GCC['cumulative_delta_H'], self.GCC['T_shifted'], marker='o', label='Courbe de Composition')

      # Ajouter des étiquettes et un titre au graphe
      plt.xlabel('cumulative_delta_H (kW)')
      plt.ylabel('T_shifted (°C)')
      plt.title('Grande Courbe de Composition')

      # Ajouter la grille
      plt.grid(True)

      # Trouver l'index du maximum de T_shifted
      max_index = self.GCC['T_shifted'].idxmax()

      # Afficher la valeur de EMR_chaud au niveau du maximum de T_shifted
      plt.text(self.GCC['cumulative_delta_H'][max_index], self.GCC['T_shifted'][max_index], f'EMR_chaud = {self.EMR_chaud} kW', verticalalignment='bottom', horizontalalignment='left')

      # Trouver l'index du minimum de T_shifted
      min_index = self.GCC['T_shifted'].idxmin()

      # Afficher la valeur de EMR_froid au niveau du minimum de T_shifted
      plt.text(self.GCC['cumulative_delta_H'][min_index], self.GCC['T_shifted'][min_index], f'EMR_froid = {self.EMR_froid} kW', verticalalignment='bottom', horizontalalignment='right')


      # Afficher la valeur de Pinch_Temperature sur l'axe des ordonnées
      plt.text(0, self.Pinch_Temperature, f'Pinch_Temperature = {self.Pinch_Temperature} °C', verticalalignment='bottom', horizontalalignment='left')


      # Afficher le graphe
      plt.show()

 
#Pinch_Analysis = PinchAnalysis(liste_flux)

