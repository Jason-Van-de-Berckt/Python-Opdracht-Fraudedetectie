from jinja2 import Environment, FileSystemLoader, select_autoescape

env = Environment(loader=FileSystemLoader("."), autoescape=select_autoescape())
template = env.get_template("./www/template.html")

auteursnamen = ["Bob", "Tim", "Jesica"]

# Studenten een alias geven zodat ze anoniem zijn.
anoniemen = {f"Student {i+1}": student for i, student in enumerate(auteursnamen)}
# print(anoniemen)

# Deze formaat hebben we nodig in jinja
# combinatie	        Kristof Michiels	        Stijn Doggen	            Vincent Nys
# Kristof Michiels	        /	            zelfde spelfout: "aray"	    zelfde spelfout: "pithon"
# Stijn Doggen	            /	                      /	                        /


# Hier maken we een dict voor het vergelijken van de studenten.
# {'bob': {'Tim': [], 'Jesica': []}, 'Tim': {'bob': [], 'Jesica': []}, 'Jesica': {'bob': [], 'Tim': []}}
matrix = {
    student1: {student2: [] for student2 in anoniemen if student2 != student1}
    for student1 in anoniemen
}

# Toevoegen van commentaren.
matrix["Student 1"]["Student 2"].append("Loop")
matrix["Student 1"]["Student 3"].append("Same object names")
matrix["Student 2"]["Student 3"].append("Same outputmessage")
# {'Bob': {'Tim': ['Loop'], 'Jesica': []}, 'Tim': {'Bob': [], 'Jesica': ['Same object names']}, 'Jesica': {'Bob': ['Same outputmessage'], 'Tim': []}}
# print(matrix)
print(template.render(matrix=matrix))
