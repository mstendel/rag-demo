# Trainierbare Parameter & RAG – verständliche Gesamterklärung

---

## 1. Was bedeutet „Größe“ eines LLM?

Die **Größe eines Large Language Models (LLM)** wird fast immer über die **Anzahl der trainierbaren Parameter** definiert.

**Parameter** sind Zahlen (Gewichte), die das Modell während des Trainings lernt und anpasst.

Beispiele:

* GPT‑2 small: ca. 117 Mio. Parameter
* LLaMA‑2 7B: ca. 7 Milliarden Parameter
* GPT‑3: ca. 175 Milliarden Parameter

> **Merksatz:** Die Modellgröße beschreibt nicht Datenmenge oder Kontextlänge, sondern die Anzahl lernbarer Zahlen.

---

## 2. Was ist ein trainierbarer Parameter?

Ein **trainierbarer Parameter** ist:

> Eine Zahl im Modell, die beim Training automatisch angepasst wird, um Vorhersagefehler zu reduzieren.

### Anschaulich:

* Jeder Parameter ist wie ein **Regler**
* Training = Regler fein nachstellen
* Milliarden Regler ergeben komplexes Sprachverhalten

---

## 3. Wo sitzen diese Parameter im LLM?

### 3.1 Embedding‑Layer

Jedes Token wird in einen Zahlenvektor umgewandelt.

```
"Himmel" → [0.12, -0.77, 1.03, ...]
```

* Alle Zahlen in diesen Vektoren sind **trainierbare Parameter**

---

### 3.2 Transformer‑Block (Herzstück)

#### Self‑Attention

Lernt, **welche Wörter für andere wichtig sind**.

```
[Wq] [Wk] [Wv] [Wo]
```

* Jede Gewichtsmatrix enthält Millionen Parameter

#### Feed‑Forward‑Netzwerk (größter Anteil)

```
4096 → 16384 → 4096
```

* Die Verbindungen (Gewichte) sind Parameter
* Hier liegen oft **über 60 %** aller Modellparameter

---

## 4. ASCII‑Gesamtübersicht

```
TEXT
 ↓
TOKEN
 ↓
EMBEDDING (Parameter)
 ↓
TRANSFORMER BLOCK (x N)
   ├─ Attention (Parameter)
   └─ Feed Forward (viele Parameter)
 ↓
AUSGABE
```

---

## 5. Training: Was passiert mit den Parametern?

Beim Training:

```
Vorhersage falsch
   ↓
Fehler berechnen
   ↓
Parameter minimal anpassen
```

Beispiel:

```
0.873 → 0.869
-0.221 → -0.215
```

➡️ Milliarden kleinster Anpassungen

---

## 6. Was ist RAG (Retrieval Augmented Generation)?

RAG ergänzt ein LLM um **externes Wissen**, ohne das Modell zu verändern.

```
FRAGE
 ↓
Embedding
 ↓
Vector DB (z. B. Chroma)
 ↓
Top‑K Texttreffer
 ↓
Prompt + Kontext
 ↓
LLM (unverändert)
```

---

## 7. Warum lernt RAG **keine** Parameter?

### ❌ Kein Training

* Embedding‑Modell ist fix
* Vector‑DB speichert nur Daten
* Prompt ≠ Training

➡️ **0 neue Parameter**
➡️ **0 Gewichtsänderungen**

> RAG liefert Kontext, kein Lernen.

---

## 8. Vergleich: Fine‑Tuning vs RAG

```
FINE‑TUNING               RAG
------------             ------------
Daten                     Daten
 ↓                         ↓
Training                  Vector DB
 ↓                         ↓
Parameter ändern           Kontext ändern
 ↓                         ↓
Modell neu                 Modell gleich
```

---

## 9. Warum wirkt RAG trotzdem „schlauer“?

* Mehr relevantes Wissen im Prompt
* Weniger Halluzination
* Aktuelle Informationen

> Vergleich: Du wirst nicht klüger – du hast bessere Unterlagen.

---

## 10. Merksätze (Essenz)

* **Ein LLM lernt durch Parameteränderung**
* **RAG ändert nicht das Modell, sondern den Kontext**
* **Prompting ist kein Training**
* **RAG = Wissen nachschlagen, Fine‑Tuning = Wissen lernen**

---

## 11. Wissenswertes für Nicht‑Techniker (Einordnung & Aha‑Effekte)

Dieser Abschnitt richtet sich bewusst an **Fachfremde, Entscheider, Management und Projektbeteiligte**, die kein IT‑ oder KI‑Studium haben – aber verstehen wollen, **was hier eigentlich passiert**.

---

### 11.1 „Denkt“ ein LLM wirklich?

Kurz und ehrlich: **Nein.**

Ein LLM:

* hat **kein Bewusstsein**
* hat **keine Absicht**
* hat **kein Verständnis wie ein Mensch**

Was es stattdessen tut:

> Es berechnet auf Basis von Wahrscheinlichkeiten, welches Wort als Nächstes passt.

Der Eindruck von „Denken“ entsteht, weil:

* Milliarden Parameter sehr komplexe Muster abbilden
* Sprache extrem gut statistisch modellierbar ist

---

### 11.2 Wo „sitzt“ das Wissen eines LLM?

Für Nicht‑Techniker ist dieser Punkt entscheidend:

* Wissen steckt **nicht als Text oder Faktenliste** im Modell
* Wissen steckt **verteilt in Milliarden Zahlen**

Vergleich:

* ❌ Kein Lexikon
* ❌ Kein Wikipedia
* ✅ Eher wie Erfahrung oder Intuition

> Das Modell kann nichts „nachschlagen“ – außer man gibt ihm RAG.

---

### 11.3 Warum vergisst ein LLM Dinge?

Ein LLM vergisst nichts dauerhaft – **aber es erinnert sich nur an das, was im Kontext steht**.

* Alles außerhalb des Prompts existiert für das Modell nicht
* Kein Gedächtnis über Sitzungen hinweg

➡️ Genau hier setzt **RAG** an.

---

### 11.4 Warum RAG für Organisationen so wichtig ist

RAG ist der Grund, warum KI **praktisch nutzbar** wird:

* Aktuelle Dokumente
* Eigene Richtlinien
* Interne Prozesse
* Projektdaten

Alles kann angebunden werden, **ohne das Modell zu verändern**.

> Deshalb ist RAG der Standardansatz für Unternehmen, Behörden und Projekte.

---

### 11.5 Unser gemeinsames Projekt (Praxisbezug)

In **unserem gemeinsamen Projekt** nutzen wir genau dieses Prinzip:

* Ein **unverändertes LLM**
* Eigene Inhalte (Dokumente, Wissen, Struktur)
* Eine **Vector‑Datenbank** (z. B. Chroma)
* Klare Trennung zwischen:

  * Modell (stabil)
  * Wissen (austauschbar)

Der große Vorteil:

* Inhalte können aktualisiert werden
* Ohne Neu‑Training
* Ohne GPU‑Cluster
* Ohne Risiko für das Grundmodell

---

### 11.6 Typische Fehlannahmen (und die Wahrheit)

| Annahme                          | Realität                  |
| -------------------------------- | ------------------------- |
| „Die KI lernt mit“               | ❌ Nein, nur beim Training |
| „Mehr Prompts = Lernen“          | ❌ Nein                    |
| „RAG trainiert das Modell“       | ❌ Nein                    |
| „KI speichert unsere Daten“      | ❌ Nicht im Modell         |
| „Antwort klingt sicher = stimmt“ | ❌ Kontext entscheidet     |

---

### 11.7 Die wichtigste Unterscheidung (bitte merken)

```
MODELL  ≠  WISSEN
```

* Modell = Sprachfähigkeit
* RAG = Wissenszugang

Erst beides zusammen ergibt:

> **eine verlässliche, erklärbare und steuerbare KI‑Lösung**

---

### 11.8 Ein letzter Merksatz für Entscheider

> **KI ist kein magisches Wesen.
> Sie ist ein sehr gutes Werkzeug – wenn man weiß, wie man sie füttert.**

---

**Ende**
