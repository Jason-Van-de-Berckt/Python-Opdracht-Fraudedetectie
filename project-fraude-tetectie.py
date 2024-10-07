from jinja2 import Environment, FileSystemLoader, select_autoescape
from pathlib import Path
import libcst as cst


class CommentCollector(cst.CSTVisitor):
    def __init__(self):
        self.comments = []
    
    def visit_Comment(self, node: cst.Comment):
        self.comments.append(node.value)

# We vragen een diractory path op om hier na te gaan naar fraude.
directory = input("Geef het pad van de folder in: ")
path = Path(directory)

# het maken van een Envirement voor het loggen in jinja
env = Environment(loader=FileSystemLoader("."), autoescape=select_autoescape())
template = env.get_template("./www/template.html")

# Initaliseren
auteursnamen = []
filedict = {}

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
                    # Het voledige bestand
                    innerbestand = pyfile.read_text()
                    # inhoud van innerbestand parsen.
                    content = cst.parse_module(innerbestand)
                    # Innderbestanden zoeken naar commentaar
                    commentVisitor = CommentCollector()
                    content.visit(commentVisitor)
                    # Alle uitkomsten in een dictionarie zetten voor te kunnen vergelijken
                    filedict[file.name] = [innerbestand, commentVisitor.comments]
            else:
                print("geen py file gevonden.")
    else:
        print("Geen py bestanden gevonden.")
    print(f"filedict: {filedict}")

# De autheursnamen opvragen uit de dictionary van het opgegeven path
for naam in filedict.keys():
    auteursnamen.append(naam)
print(auteursnamen)

# Studenten een alias geven zodat ze anoniem zijn.
anoniemen = {f"Student {i+1}": student for i, student in enumerate(filedict.keys())}
anoniem_filedict = {anoniem: filedict[originele_student] for anoniem, originele_student in anoniemen.items()}


# Hier maken we een matrix voor het vergelijken van de studenten.
matrix = {
    student1: {student2: [] for student2 in anoniemen if student2 != student1}
    for student1 in anoniemen
}
print(f"matrix: {matrix}")

# Vergelijken van studenten en toevoegen van commentaren.
for student1, content1 in anoniem_filedict.items():
    for student2, content2 in anoniem_filedict.items():
        if student1 < student2: # Zorgt ervoor dat we de studenten niet meerdere keren nakijken
            if student1 != student2:
                if content1[0] == content2[0]:
                    print(student1,content1[0], student2, content2[0])
                    matrix[student1][student2].append("identieke file opdracht.py")
                if content1[1] == content2[1]:
                    print(student1, content1[1], student2, content2[1])
                    matrix[student1][student2].append("identieke commentaar")

print(matrix)

output = template.render(matrix=matrix)

# print de output naar een html bestand.
with open("./www/vergelijking_tabel.html", "w") as f:
    f.write(output)
