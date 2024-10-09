# 1. Implementatie stap 1

## Templating

Hier moeten we gebruik maken van dictionary comprehension. Ik heb dit terug moeten opzoeken wat dit juist was. Ik ben voor het templaten met Jinja terug moeten gaan naar vorige projecten om dit terug te snappen. Ik heb hier ook de documentatie van Jinja zelf gebruikt. Voor de tabel in de `template.html`-file heb ik een website gebruikt om de tabel te genereren, zodat ik makkelijk de data hierin kwijt kan en het overzichtelijk is. Ik heb de tabel kunnen maken, alleen kreeg ik de opmerkingen niet in de tabel, maar kreeg ik overal een /. Wat wil zeggen dat er geen commentaar is of de studenten overeenkomen met elkaar. Ik heb mijn code laten nakijken door een medestudent voor feedback en had bij een for-loop de foute student gebruikt.

# 2. Implementatie stap 2

We gaan hier te werk met mapping. We maken een dictionary met daarin een studentenalias. Ik heb gekozen voor student 1 tot 3 als key te gebruiken. Voor het nog kunnen bekijken van de auteursnamen voegen we de naam van de student in als value.

# 3. Implementatie stap 3

## Identieke inhoud

Het vergelijken van de inhoud van de .py-bestanden voor het testen op fraude. Ik heb het hier wel even moeilijk gehad, omdat ik niet met functies werk. Ik heb ook moeten uitzoeken hoe je het innerlijke bestand leest en wegschrijft in een dictionary. Dit heb ik gedaan door de documentatie van pathlib te lezen en uit te proberen. Ik heb ook moeten uitzoeken hoe ik de studenten anoniem weergeef in het HTML-bestand, omdat we eerst met hardcoded waarden aan het werken waren.

# 4. Implementatie stap 4

## Identieke commando's

Het vergelijken van identieke commando's heb ik als volgt uitgevoerd. Ik heb met de re-library gezocht in de .py-documentjes naar een # en hier de gehele string van genomen. Dit onderdeel is mij eigenlijk goed afgegaan doordat ik de aangewezen website van de documentatie gebruikt heb.

Het loggen naar het HTML-bestandje is wat minder soepel gelopen met de reden dat ik elke student met elkaar twee keer vergeleek. Dit is niet de bedoeling en heb zo mijn code moeten aanpassen zodat dit niet gebeurde. Hoe ik dit heb gevonden is door de output te loggen naar een txt-bestandje met `py *.py > test.txt` en hier de output goed te bekijken en te debuggen.

# 5. Implementatie stap 5

## Comments zoeken met behulp van een syntaxboom

Ik heb hier redelijk veel mee gevochten, omdat mijn code zelf rommelig was. Ik heb dan eerst mijn code zelf uitgezocht en commentaar bijgeschreven. Eerst dacht ik dat ik bij de volgende code met de visitor moest werken, maar dit gedeelte was voor het vergelijken.

```python
for student1, content1 in anoniem_filedict.items():
    for student2, content2 in anoniem_filedict.items():
        if student1 < student2:  # Zorgt ervoor dat we de studenten niet meerdere keren nakijken
            if student1 != student2:
                if content1[0] == content2[0]:
                    print(student1, content1[0], student2, content2[0])
                    matrix[student1][student2].append("identieke file opdracht.py")
                if content1[1] == content2[1]:
                    print(student1, content1[1], student2, content2[1])
                    matrix[student1][student2].append("identieke commentaar")
```

Nadien ben ik erachter gekomen dat ik deze stap moest uitvoeren bij het zoeken naar de commentaar, waardoor het gemakkelijker was om dit te implementeren. Verder heb ik ook eens gekeken naar de documentatie over dit deel. Hierdoor werd ook veel duidelijk.

# 6. Implementatie stap 6

## Spelchecker toevoegen

Bij de oefeningen was het al meteen duidelijk wat mij te doen stond. Echter was het niet zo simpel. Nadat ik fouten had gemaakt in mijn visitor-klassen en dit nagevraagd te hebben aan een medestudent, is dit onderdeel redelijk snel en goed gelukt. Ik had een fout gemaakt bij de naamgeving van `visit_SimpleString`. Dit had ik een eigen naamgeving gegeven waardoor het niet werkte; ook had ik in het begin geen node ingesteld, dit moest `cst.SimpleString` zijn. Voordat ik kon vergelijken, moest ik de string splitsen op backslashes en `(')`. Dit had ik eerst ook niet door waardoor het niet werkte. Nadien kwam ik op deze klasse uit.

```python
class LexionCollector(cst.CSTVisitor):
    def __init__(self):
        self.strings = []

    def visit_SimpleString(self, node: cst.SimpleString):
        string_value = node.value.strip("\"'")
        self.strings.append(string_value)
```

# 7. Implementatie stap 7

## Code vergelijken zonder commentaar

Eerst was het nog niet goed duidelijk hoe ik hieraan moest beginnen. Nadat ik mijn code nog eens goed had nagekeken en begreep, wist ik hoe. Ik moest een klasse aanmaken die ervoor zorgt dat als ik content bezoek, de commentaar uit deze content werd gefilterd. Nadien bleek dat ik een foutje had gemaakt in mijn klasse:

```python
class CommentTransformer(cst.CSTTransformer):
    def leave_Comment(self, original_node, updated_node):
        return None
```

Dit moest eerder deze code zijn:

```python
class CommentTransformer(cst.CSTTransformer):
    def leave_Comment(self, original_node, updated_node):
        return cst.RemoveFromParent()
```

Eerst retourneerde ik niets waardoor er niets uitkwam. Later kwam er zeker iets uit, maar nog niet het juiste. Ik moest de code van de uitkomst in een variabele zetten omdat het niet als een string uit de Transformer kwam. Dit heb ik gedaan met:

```python
stripped_code = new_tree.code.strip("\n")
```

Ik heb ook meteen "\n" uit de string gehaald als deze hierin zat, zodat we alles goed kunnen vergelijken.

# 8. Implementatie stap 8

## Meerdere bestanden vergelijken met elkaar

Deze stap was niet zo moeilijk. Ik moest wat aanpassen aan hoe ik de data van de bestanden in een lijst zette. Ik moest een andere lijst aanmaken waarin ik alle data zette per .py-file. Deze lijst zit dus vol met .py-bestanden [file1, file2, ...]. Hierna moest ik de vergelijking aanpassen. Eerst werkte ik met `content[index]`, omdat alle content in een lijst zat. Bijv. `content[0]` --> de code zonder commentaar. Ik heb dit dan moeten aanpassen naar het volgende:

```python
if len(content1) != len(content2):  # We kijken hier na of er evenveel .py-bestanden per student geüpload zijn. Als dit niet zo is, geven we een errorcode.
    matrix[student1][student2].append("Vergelijking niet mogelijk: geen gelijk aantal .py-bestanden")

else:  # Vergelijken van de bestanden als er wel genoeg bestanden zijn.
    for (code1, comments1, spelfouten1), (code2, comments2, spelfouten2) in zip(content1, content2):
        if code1 == code2:
            matrix[student1][student2].append("identieke Code")
        if comments1 == comments2:
            matrix[student1][student2].append("identieke commentaar")
        if spelfouten1 and spelfouten2:
            if spelfouten1 == spelfouten2:
                matrix[student1][student2].append(
                    f"Identieke spelfout: {spelfouten1}"
                )
```

Eerst kijken of er wel evenveel .py-bestanden zijn per student. Als dit niet zo is, geven we een boodschap mee in de matrix dat de vergelijking niet mogelijk is. Stel er zijn wel evenveel .py-bestanden. Dan gaan we door de lijst en vergelijken met de andere lijst die in content zit. Hier heb ik wel even over moeten nadenken, omdat ik de vorige code simpel en duidelijk vond. Na dit geïmplementeerd te hebben, is het wel weer duidelijk hoe het werkt.

# 9. Implementatie stap 9

## Code parsen met AST

We gaan de code parsen met AST en niet meer met CST. Dit doen we omdat we bij CST meer code nodig hebben voor alles goed te kunnen vergelijken. Bij deze stap heb ik niet echt moeilijkheden gehad. Ik heb uitgezocht wat ik weg kon doen en wat ik moest veranderen aan mijn code zodat dit moest werken, bijv. de klasse die eerst de commentaar uit de broncode verwijdert, zodat we deze kunnen vergelijken met de code van een andere student. Echter bij CST werden de extra witregels niet weggehaald waardoor we niet altijd dezelfde code met elkaar vergelijken.
