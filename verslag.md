# 1. Implementatie stap 1

## Templating

Hier moeten we hebruik maken van dictionary comprehension. Ik heb dit terug moeten opzoeken wat dit juist was.
Ik ben voor het templaten met jinja terug moeten gaan naar vorige projecten om dit terug te snappen. Ik heb hier ook de documentatie van jinja zelf gebruikt.
Voor de table in de template.html file heb ik een website gebruikt om de table te genereren zodat ik makkelijk de data hierin kwijt kan en het overzichtelijk is
Ik heb de tabel kunnen maken alleen kreeg ik de opmerkingen niet in de tabel maar kreeg ik overal /. Wat wilt zeggen dat er geen commentaar is of de studenten overeen komen met elkaar. Ik heb mijn code laten nakijken door een medestudent voor feedback en had bij een forloop de foute student gebruikt.

# 2. Implementatie stap 2

We gaan hier tewerk met mapping. We maken een dictionary met daarim een studenten alias. Ik heb gekozen voor student 1 tot 3 als key te grbuiken. Voor het nog kunnen bekijken van de auteursnamen voegen we de naam van de student in al value.

# 3. Implementatie stap 3

## Identieke inhoud

Het vergelijken van innerlijke inhoud van de .py bestanden voor het testen op fraude.
Ik heb het hier wel even moeilijk gehad, omdat ik niet met functies werk. Ik heb ook moeten uitzoeken hoe je het innerlijke bestand leest en wegschrijft in een disctionary. Dit heb ik gedaan door de documentatie van pathlib te lezen en uit te proberen. Ik heb ook moeten uitzoeken hoe ik de studenten annoniem weergeef in het html bestand. Omdat we eerst met hardcoded waardes aan het werken waren.

# 4. Implementatie stap 4

## Identieke commands

Het vergelijken van identieke commmands heb ik als volg uitgevoerd. Ik heb met de re library gezocht in de .py documentjes naar een # en hier de gehele string van genomen. Dit onderdeel is mij eigenlijk goed afgegaan doordat ik de aangewezen website van de documentatie gebruikt heb.

Het loggen naar het html bestandje is wat minder soepeler gelopen met de rede dat ik elke student met elkaar twee keer vergeleek. Dit is niet de bedoeling en heb zo mijn code moeten aanpassen zodat dit niet gebeurde. Hoe ik dit heb gevonden is door de output te loggen naar een txt bestandje met py \*.py > test.txt en hier de output goed te bekijken en te debuggen.

# 5. Impementatie stap 5

## Comments zoeken met dmv syntax boom

Ik heb hier redelijk veel mee gevochten, omdat mijn code zelf rommelig was. Ik heb dan eerst mijn code zelf uitgezocht en commentaar bijgeschreven. Eerst dacht ik dat ik bij de volgende code met de visitor moest werken maar dit gedeete was voor te vergelijken.

```python
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

```

Nadien ben ik erachter gekomen dat ik deze stap moest uitvoeren bij het zoeken naar de commentaar waardoor het gemaakelijker was om dit te implementeren. Verder heb ik ook eens gekeken daar de documentatie over dit deel. Hierdoor werdt ook veel duidelijk.

# 6. Implementatie stap 6

## Spelchecker toevoegen

Bij de oefeningen was het al meteen duidelijk wat mij te doen stond. Echter was het niet zo simpel. Nadat ik fouten had gemaakt in mijn visitor klassen en dit nagevraagd te hebben aan een medestudent. Is dit onderdeel redelijk snel en goed gelukt. Ik had een fout gemaakt bij de naamging van visit_SimpleString. Dit had ik een eigen naamgeving gegeven waardoor het niet werkte ook had ik in het begin geen node ingesteld dit moest cst.simplestring zijn. voordat ik kon vergelijken moest ik de sting stippen op backslaches en ('). Dit had ik eerst ook niet door waardoor het niet werkte. Nadien kwam ik op deze classe uit.

```python
class LexionCollector(cst.CSTVisitor):
    def __init__(self):
        self.strings = []

    def visit_SimpleString(self, node: cst.SimpleString):
        string_value = node.value.strip("\"'")
        self.strings.append(string_value)

```
