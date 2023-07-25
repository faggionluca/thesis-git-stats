# #######################################################################################################################################
#  Author: Luca Faggion
#  Semplice script plottare un file csv
#  Parte della "containerizzazione e Automazione dei Test per Servizio di Integrazione continua/Rilascio continuo" Tesi UNIPR
# #######################################################################################################################################
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

# Leggiamo il file csv creato usando lo script git_stats
git_data = pd.read_csv("git_stats_driller.csv")

# Convertiamo, ordiniamo in base a alla colonna delle date
git_data['date']= pd.to_datetime(git_data['date'])
git_data.sort_values(by='date', inplace = True)

# creiamo la colonna per la CMA ( Comulative Moving Average)
git_data['average'] = git_data['total'].expanding().mean()
git_data.info()

# Inizializziamo la figura
fig, ax = plt.subplots()
fig.set_figwidth(12)

# Plottiamo le due colonne
line1 = ax.plot(git_data['date'], git_data['total'], label='cambiamenti')
ax1 = ax.twinx()
line2 = ax1.plot(git_data['date'], git_data['average'], color='orange', alpha=0.4, label='media mobile cumulativa')

# Aggiustiamo i labels per l'asse delle date
ax.xaxis.set_major_locator(mdates.YearLocator(base = 1, month = 1, day = 1))
ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y'))

# Aggiungiamo la leggenda
lines, labels = ax.get_legend_handles_labels()
lines2, labels2 = ax1.get_legend_handles_labels()
ax1.legend(lines + lines2, labels + labels2, loc=0)

ax.set_xlabel("Tempo (A)")
ax.set_ylabel(r"Cambiamenti (aggiunte/cancellazioni)")
ax1.set_ylabel(r"Media")

# salviamo l'immagine
fig.savefig("./images/spring_frameworks_test_changes.png")
print("ok")