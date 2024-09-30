from jinja2 import Environment, FileSystemLoader, select_autoescape
from pathlib import Path

# We vragen een diractory path op om hier na te gaan naar fraude.
directory = input("Geef het pad van de folder in: ")
path = Path(directory)

# het maken van een Envirement voor het loggen in jinja
env = Environment(loader=FileSystemLoader("."), autoescape=select_autoescape())
template = env.get_template("./www/template.html")

# Initaliseren
auteursnamen = []
filedict = {}
innerpyfiles = []

# Alle benodigdheden opstellen in een dictionary voor het nakijken van froude.
if path.is_dir():
    print("Bestand gevonden!")
    files = list(path.glob("*"))
    if files:
        for file in files:
            path = file
            pyfiles = list(file.glob("*.py"))
            if pyfiles:
                for pyfile in pyfiles:
                    #print(pyfile.name)
                    bestand = pyfile.read_text()
                    #print(bestand)
                    filedict[file.name] = bestand
            else:
                print("geen py file gevonden.")
    else:
        print("Geen py bestanden gevonden.")
    print(f"filedict: {filedict}")

for text in filedict.values():
    innerpyfiles.append(text)
print(f"innerpyfiles: {innerpyfiles}")

# De autheursnamen opvragen uit de dictionary van het opgegeven path
for naam in filedict.keys():
    auteursnamen.append(naam)
print(auteursnamen)

# Studenten een alias geven zodat ze anoniem zijn.
anoniemen = {f"Student {i+1}": student for i, student in enumerate(filedict.keys())}
print(f"anoniemen: {anoniemen}")

anoniem_filedict = {anoniem: filedict[originele_student] for anoniem, originele_student in anoniemen.items()}
print(f"Anoniem filedict: {anoniem_filedict}")

# Hier maken we een dict voor het vergelijken van de studenten.
matrix = {
    student1: {student2: [] for student2 in anoniemen if student2 != student1}
    for student1 in anoniemen
}
print(f"matrix: {matrix}")

# Toevoegen van commentaren.
for student1, content1 in anoniem_filedict.items():
    for student2, content2 in anoniem_filedict.items():
        if student1 != student2:
            if content1 == content2:
                matrix[student1][student2].append("identieke file opdracht.py")
output = template.render(matrix=matrix)

# print de output naar een html bestand.
with open("./www/vergelijking_tabel.html", "w") as f:
    f.write(output)
