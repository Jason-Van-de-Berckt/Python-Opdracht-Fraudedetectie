from jinja2 import Environment, FileSystemLoader, select_autoescape
from pathlib import Path
import libcst as cst
from spellchecker import SpellChecker


class CommentCollector(cst.CSTVisitor):
    def __init__(self):
        self.comments = []

    def visit_Comment(self, node: cst.Comment):
        self.comments.append(node.value)


class LexionCollector(cst.CSTVisitor):
    def __init__(self):
        self.strings = []

    def visit_SimpleString(self, node: cst.SimpleString):
        string_value = node.value.strip("\"'")
        self.strings.append(string_value)


class CommentTransformer(cst.CSTTransformer):
    def leave_Comment(self, original_node, updated_node):
        return cst.RemoveFromParent()


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
                student_files = []
                for pyfile in pyfiles:
                    # Het voledige bestand
                    innerbestand = pyfile.read_text()
                    # inhoud van innerbestand parsen.
                    content = cst.parse_module(innerbestand)

                    # Innderbestanden zoeken naar commentaar
                    commentVisitor = CommentCollector()
                    content.visit(commentVisitor)

                    # Innerbestanden zoeken naar spelfouten in Strings
                    # Innit
                    stringVisitor = LexionCollector()
                    content.visit(stringVisitor)
                    spelfouten = []

                    # Eigelijke code
                    spel = SpellChecker(language="nl")
                    for strings in stringVisitor.strings:
                        woorden = strings.split()
                        for woord in woorden:
                            if spel.unknown([woord]):
                                spelfouten.append(woord)
                                print(f"spelfouten {spelfouten}")

                    # Commments uit syntaxboom filteren
                    transformer = CommentTransformer()
                    new_tree = content.visit(transformer)
                    # omzetten van tree naar een string om te kunnen vergelijken.
                    stripped_code = new_tree.code.strip("\n")
                    print(f"Striped code {stripped_code}")
                    
                    # Hier zetten we alle data in een niewe lijst per py file.
                    student_files.append((innerbestand, commentVisitor.comments, spelfouten))

                    # Alle py file zetten we in deze lijst zodat we deze later kunnen vergelijken met andere studenten
                    filedict[file.name] = student_files
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
anoniem_filedict = {
    anoniem: filedict[originele_student]
    for anoniem, originele_student in anoniemen.items()
}


# Hier maken we een matrix voor het vergelijken van de studenten.
matrix = {
    student1: {student2: [] for student2 in anoniemen if student2 != student1}
    for student1 in anoniemen
}
print(f"matrix: {matrix}")

# Vergelijken van studenten en toevoegen van commentaren.
for student1, content1 in anoniem_filedict.items():
    for student2, content2 in anoniem_filedict.items():
        if (
            student1 < student2
        ):  # Zorgt ervoor dat we de studenten niet meerdere keren nakijken
            if student1 != student2:
                if len(content1) != len(content2): # We kijken hier na of er evenveel py files per student geupload zijn. als dit niet is geven we een error code. 
                    matrix[student1][student2].append("Vergelijking niet mogelijk: geen geleik aantal py files")
                
                else: #Vergelijken van de bestanden als er wel genoeg bestanden zijn.
                    for(code1, comments1, spelfouten1), (code2, comments2, spelfouten2) in zip(content1, content2):
                        if code1 == code2:
                            matrix[student1][student2].append("identieke Code")
                        if comments1 == comments2:
                            matrix[student1][student2].append("identieke commentaar")
                        if spelfouten1 and spelfouten2:
                            if spelfouten1 == spelfouten2:
                                matrix[student1][student2].append(
                                    f"Identieke spelfout: {spelfouten1}"
                                )   

print(matrix)

output = template.render(matrix=matrix)

# print de output naar een html bestand.
with open("./www/vergelijking_tabel.html", "w") as f:
    f.write(output)
