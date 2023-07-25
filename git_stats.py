# #######################################################################################################################################
#  Author: Luca Faggion
#  Semplice script per analizzare un repository
#  Parte della Tesi "containerizzazione e Automazione dei Test per Servizio di Integrazione continua/Rilascio continuo" UNIPR
# #######################################################################################################################################
from pydriller import Repository
import re

# Setup delle variabili
target = "https://github.com/spring-projects/spring-framework.git"
pathRegex = r".*?/src/test/.+?\.java"
csvFile = "git_stats_driller.csv"

# Carichiamo il repository
# analizeremo solo i cambiamenti ai files con estensione .java
# anazzeremo ogni ref e ogni remote disponibile
repo = Repository(target, only_modifications_with_file_types=".java", include_refs=True, include_remotes=True)

# generator per il travers dei commit
commits = repo.traverse_commits()

# Apiramo il file in scrittura
# iniziamo scrivendo la prima linea, quella delle colonne
with open(csvFile, "w") as f:
    f.write("commit,date,addition,deletions,total\n")

    for commit in commits:
        # Varibili per ogni singolo commit
        files = commit.modified_files
        added_lines = 0
        deleted_lines = 0
        commit_hash = commit.hash
        date = commit.author_date
        
        # accumuliamo added_lines e deleted_lines
        # dei soli files all'interno delle cartelle /test/
        # di ogni package
        for file in files:
            path = file.old_path or file.new_path
            if re.match(pathRegex, path):
                added_lines += file.added_lines
                deleted_lines += file.deleted_lines

        total = added_lines+deleted_lines

        # scriviamo i risultati come linea nel file
        f.write(f"{commit_hash},{date},{added_lines},{deleted_lines},{total}\n")