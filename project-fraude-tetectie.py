from jinja2 import Environment, FileSystemLoader, select_autoescape

env = Environment(loader=FileSystemLoader("."), autoescape=select_autoescape())
template = env.get_template("./www/template.html")

auteursnamen = ["Bob", "Tim", "Jesica"]

# Deze formaat hebben we nodig in jinja
#combinatie	        Kristof Michiels	        Stijn Doggen	            Vincent Nys
#Kristof Michiels	        /	            zelfde spelfout: "aray"	    zelfde spelfout: "pithon"
#Stijn Doggen	            /	                      /	                        /


# Hier maken we een dict voor het vergelijken van de studenten.
# {'bob': {'Tim': [], 'Jesica': []}, 'Tim': {'bob': [], 'Jesica': []}, 'Jesica': {'bob': [], 'Tim': []}}
matrix = {student1: {studenten: [] for studenten in auteursnamen if studenten != student1}
        for student1 in auteursnamen} 

# Toevoegen van commentaren.
matrix["Bob"]["Tim"].append("Loop")
matrix["Tim"]["Jesica"].append("Same object names")
matrix["Jesica"]["Bob"].append("Same outputmessage")
# {'Bob': {'Tim': ['Loop'], 'Jesica': []}, 'Tim': {'Bob': [], 'Jesica': ['Same object names']}, 'Jesica': {'Bob': ['Same outputmessage'], 'Tim': []}}

print(template.render(matrix=matrix))

