#!/usr/bin/env python3
"""
French Tutor Agent - FIDE A1 Level with Enhanced Vocabulary
Daily French lessons + Weekly quizzes for Richard Laurits
Goal: Pass FIDE test for Permit C
Updated: Higher vocab level, basic grammar, focus on questions
"""

import json
import random
import sys
from datetime import datetime, timedelta
from pathlib import Path

# Agent directory
AGENT_DIR = Path('/home/richard-laurits/.openclaw/workspace/agents/french-tutor-agent')
DATA_FILE = AGENT_DIR / 'progress.json'
LESSON_LOG = AGENT_DIR / 'lessons.json'
QUIZ_LOG = AGENT_DIR / 'quiz_results.json'

# UPDATED: Higher vocabulary level, more useful words
CURRICULUM = {
    "weeks": [
        {"week": 1, "theme": "Les bases avancées / Avancerade grunder", "grammar": ["être (att vara)", "avoir (att ha)", "Questions de base"], "vocab_categories": ["advanced_greetings", "useful_phrases", "question_words"]},
        {"week": 2, "theme": "Poser des questions / Ställa frågor", "grammar": ["Questions avec est-ce que", "Intonation", "Inversion"], "vocab_categories": ["question_words", "asking_directions", "making_requests"]},
        {"week": 3, "theme": "La vie quotidienne / Vardagslivet", "grammar": ["ER-verbs (1:a gruppen)", "Expressions de temps"], "vocab_categories": ["daily_routines", "time_expressions", "weather_advanced"]},
        {"week": 4, "theme": "Au travail / På jobbet", "grammar": ["IR-verbs (2:a gruppen)", "RE-verbs (3:e gruppen)", "Le futur proche (ska göra)"], "vocab_categories": ["work_professions", "office", "meetings"]},
        {"week": 5, "theme": "Nourriture et restaurants / Mat och restauranger", "grammar": ["Partitif (du, de la, des)", "Demander au restaurant"], "vocab_categories": ["food_advanced", "restaurant", "ordering"]},
        {"week": 6, "theme": "Courses et shopping / Shopping", "grammar": ["Demande de prix", "Comparatifs (mer/mindre)"], "vocab_categories": ["shopping", "clothes", "describing_items"]},
        {"week": 7, "theme": "Se déplacer / Förflyttning", "grammar": ["Aller (att åka/gå)", "Prepositions de lieu", "Demander son chemin"], "vocab_categories": ["transport_advanced", "directions", "travel_booking"]},
        {"week": 8, "theme": "La ville et services / Staden och tjänster", "grammar": ["Il y a (det finns)", "Prepositions: dans, sur, sous, à, en"], "vocab_categories": ["city_services", "emergency", "formal_situations"]},
        {"week": 9, "theme": "Les gens et relations / Människor och relationer", "grammar": ["Adjectifs (kongruens)", "Possessiva (min, din)"], "vocab_categories": ["personality_advanced", "relationships", "emotions"]},
        {"week": 10, "theme": "Loisirs et hobbies / Fritid och hobbies", "grammar": ["Aimer + infinitif", "Pouvoir, Vouloir, Devoir"], "vocab_categories": ["hobbies_advanced", "sports", "entertainment"]},
        {"week": 11, "theme": "Le passé / Dåtiden", "grammar": ["Passé composé", "Avoir/être som hjälpverb", "Raconter une journée"], "vocab_categories": ["past_events", "holidays", "storytelling"]},
        {"week": 12, "theme": "L'avenir et projets / Framtiden och projekt", "grammar": ["Futur proche", "Futur simple (grund)", "Projets futurs"], "vocab_categories": ["future_plans", "appointments", "goals"]},
    ]
}

# UPDATED: Higher level vocabulary - more useful, less basic
VOCABULARY = {
    "advanced_greetings": [
        ("Enchanté(e)", "Trevligt att träffas", "Enchanté, je m'appelle Richard.", "Trevligt att träffas, jag heter Richard."),
        ("Ça va?", "Hur är det? / Hur mår du?", "Salut, ça va?", "Hej, hur är det?"),
        ("Comment allez-vous?", "Hur mår ni? (formellt)", "Bonjour, comment allez-vous?", "God dag, hur mår ni?"),
        ("À tout à l'heure", "Vi ses strax", "À tout à l'heure!", "Vi ses strax!"),
        ("Bonne journée", "Ha en bra dag", "Bonne journée!", "Ha en bra dag!"),
        ("Bonne soirée", "Ha en bra kväll", "Bonne soirée!", "Ha en bra kväll!"),
        ("Félicitations", "Grattis", "Félicitations pour ton promotion!", "Grattis till din befordran!"),
        ("Bonne chance", "Lycka till", "Bonne chance pour l'examen!", "Lycka till på provet!"),
        ("Santé!", "Skål!", "Santé!", "Skål!"),
        ("À vos souhaits", "Prosit", "À vos souhaits! (après un éternuement)", "Prosit! (efter nysning)"),
    ],
    "question_words": [
        ("Comment?", "Hur?", "Comment allez-vous au travail?", "Hur åker ni till jobbet?"),
        ("Pourquoi?", "Varför?", "Pourquoi étudiez-vous le français?", "Varför studerar du franska?"),
        ("Où?", "Var?", "Où habitez-vous?", "Var bor ni?"),
        ("Quand?", "När?", "Quand partez-vous?", "När åker ni?"),
        ("Combien?", "Hur mycket/många?", "Combien ça coûte?", "Hur mycket kostar det?"),
        ("Quel/Quelle?", "Vilken/Vilket?", "Quelle heure est-il?", "Vilken timme är det? (Vad är klockan?)"),
        ("Qui?", "Vem?", "Qui est-ce?", "Vem är det?"),
        ("Que? / Qu'est-ce que?", "Vad?", "Qu'est-ce que c'est?", "Vad är det?"),
        ("Est-ce que...?", "Är det så att...? (frågeform)", "Est-ce que vous parlez anglais?", "Talar ni engelska?"),
        ("Quel temps fait-il?", "Hur är vädret?", "Quel temps fait-il aujourd'hui?", "Hur är vädret idag?"),
    ],
    "asking_directions": [
        ("Où se trouve...?", "Var finns...?", "Où se trouve la gare?", "Var finns stationen?"),
        ("Comment aller à...?", "Hur kommer man till...?", "Comment aller à la tour Eiffel?", "Hur kommer man till Eiffeltornet?"),
        ("C'est loin?", "Är det långt bort?", "C'est loin d'ici?", "Är det långt härifrån?"),
        ("C'est près d'ici?", "Är det nära härifrån?", "C'est près d'ici?", "Är det nära härifrån?"),
        ("Tournez à gauche", "Sväng vänster", "Tournez à gauche après le feu.", "Sväng vänster efter trafikljuset."),
        ("Tournez à droite", "Sväng höger", "Tournez à droite ici.", "Sväng höger här."),
        ("Tout droit", "Rakt fram", "Continuez tout droit.", "Fortsätt rakt fram."),
        ("Au coin de la rue", "Hörnet av gatan", "C'est au coin de la rue.", "Det är på hörnet av gatan."),
        ("En face de", "Mittemot", "C'est en face de la banque.", "Det är mittemot banken."),
        ("À côté de", " bredvid", "C'est à côté de l'église.", "Det är bredvid kyrkan."),
    ],
    "useful_phrases": [
        ("Je cherche...", "Jag letar efter...", "Je cherche la pharmacie.", "Jag letar efter apoteket."),
        ("Je voudrais...", "Jag skulle vilja...", "Je voudrais un café, s'il vous plaît.", "Jag skulle vilja ha en kaffe, tack."),
        ("Pouvez-vous m'aider?", "Kan ni hjälpa mig?", "Pouvez-vous m'aider, s'il vous plaît?", "Kan ni hjälpa mig, tack?"),
        ("Je ne comprends pas", "Jag förstår inte", "Je ne comprends pas, pouvez-vous répéter?", "Jag förstår inte, kan ni upprepa?"),
        ("Parlez plus lentement", "Tala långsammare", "Parlez plus lentement, s'il vous plaît.", "Tala långsammare, tack."),
        ("Répétez, s'il vous plaît", "Upprepa tack", "Pouvez-vous répéter, s'il vous plaît?", "Kan ni upprepa, tack?"),
        ("Je suis désolé(e)", "Jag är ledsen / Ursäkta", "Je suis désolé, je ne parle pas bien français.", "Ursäkta, jag talar inte franska så bra."),
        ("Je suis suédois/suédoise", "Jag är svensk", "Je suis suédois, j'habite en Suisse.", "Jag är svensk, jag bor i Schweiz."),
        ("Je travaille dans le marketing", "Jag arbetar inom marknadsföring", "Je travaille dans le marketing chez BD.", "Jag arbetar inom marknadsföring på BD."),
        ("J'ai deux enfants", "Jag har två barn", "J'ai deux enfants, Sigrid et Arthur.", "Jag har två barn, Sigrid och Arthur."),
    ],
    "food_advanced": [
        ("L'addition, s'il vous plaît", "Notan, tack", "L'addition, s'il vous plaît.", "Notan, tack."),
        ("Je suis allergique à...", "Jag är allergisk mot...", "Je suis allergique aux noix.", "Jag är allergisk mot nötter."),
        ("Sans gluten", "Glutenfritt", "Avez-vous des plats sans gluten?", "Har ni glutenfria rätter?"),
        ("Végétarien/végétalien", "Vegetarian/vegan", "Avez-vous des options végétariennes?", "Har ni vegetariska alternativ?"),
        ("Un verre de...", "Ett glas...", "Un verre de vin rouge, s'il vous plaît.", "Ett glas rött vin, tack."),
        ("Une carafe d'eau", "En karaff vatten", "Une carafe d'eau, s'il vous plaît.", "En karaff vatten, tack."),
        ("C'était délicieux", "Det var utsökt", "C'était délicieux, merci!", "Det var utsökt, tack!"),
        ("Le plat du jour", "Dagens rätt", "Quel est le plat du jour?", "Vad är dagens rätt?"),
        ("Le menu", "Menyn", "Puis-je voir le menu?", "Kan jag få se menyn?"),
        ("Je prendrai...", "Jag tar...", "Je prendrai le poulet.", "Jag tar kycklingen."),
    ],
    "transport_advanced": [
        ("Un aller-retour", "Tur och retur", "Un aller-retour pour Genève, s'il vous plaît.", "Tur och retur till Genève, tack."),
        ("Un aller simple", "Enkel biljett", "Un aller simple pour Paris.", "Enkel biljett till Paris."),
        ("Le prochain train", "Nästa tåg", "À quelle heure part le prochain train?", "När går nästa tåg?"),
        ("Le quai", "Perrongen", "Le train part du quai 3.", "Tåget går från perrong 3."),
        ("La correspondance", "Bytet/anslutningen", "Où est la correspondance pour Lausanne?", "Var är bytet/anslutningen till Lausanne?"),
        ("Je voudrais louer une voiture", "Jag skulle vilja hyra en bil", "Je voudrais louer une voiture pour trois jours.", "Jag skulle vilja hyra en bil i tre dagar."),
        ("Le parking", "Parkeringen", "Où est le parking le plus proche?", "Var är närmaste parkering?"),
        ("À pied", "Till fots", "C'est à 10 minutes à pied.", "Det är 10 minuter till fots."),
        ("En retard / En avance", "Försenad / I förväg", "Le train est en retard.", "Tåget är försenat."),
        ("À l'heure", "I tid", "Le bus est-il à l'heure?", "Är bussen i tid?"),
    ],
}

# UPDATED: Grammar lessons - still basic, but more focus on questions
GRAMMAR_LESSONS = {
    1: {
        "topic": "Être och Avoir - Att vara och Att ha",
        "explanation": "De två viktigaste verben på franska...",
        "examples": [("Je suis suédois.", "Jag är svensk."), ("J'ai deux enfants.", "Jag har två barn.")]
    },
    2: {
        "topic": "Questions avec 'Est-ce que' - Frågor med 'Är det så att'",
        "explanation": """
Det enklaste sättet att ställa frågor på franska!

Lägg bara "Est-ce que" framför meningen:

✅ Statement: Vous parlez anglais. (Ni talar engelska.)
❓ Question: Est-ce que vous parlez anglais? (Talar ni engelska?)

✅ Statement: Il fait beau. (Det är fint väder.)
❓ Question: Est-ce que il fait beau? (Är det fint väder?)

💡 Tips: Fungerar med ALLA verb, alla personer!
        """,
        "examples": [
            ("Est-ce que vous êtes suédois?", "Är ni svensk?"),
            ("Est-ce qu'il habite à Genève?", "Bor han i Genève?"),
            ("Est-ce que tu parles français?", "Talar du franska?"),
        ]
    },
    3: {
        "topic": "Questions med frågeord - Comment, Pourquoi, Où...",
        "explanation": """
Frågeord + est-ce que = perfekta frågor!

Comment (Hur) → Comment est-ce que...?
Pourquoi (Varför) → Pourquoi est-ce que...?
Où (Var) → Où est-ce que...?
Quand (När) → Quand est-ce que...?
Combien (Hur mycket) → Combien est-ce que...?

💡 Kortform: Man kan också säga "Comment allez-vous?" utan "est-ce que"
        """,
        "examples": [
            ("Comment est-ce que vous allez au travail?", "Hur åker ni till jobbet?"),
            ("Pourquoi est-ce que tu étudies le français?", "Varför studerar du franska?"),
            ("Où est-ce qu'il habite?", "Var bor han?"),
        ]
    },
}

# ... [rest of the file remains the same]
def load_progress():
    """Load student's progress"""
    if DATA_FILE.exists():
        with open(DATA_FILE, 'r') as f:
            return json.load(f)
    return {
        "started": datetime.now().isoformat(),
        "current_week": 1,
        "current_day": 1,
        "words_learned": [],
        "grammar_points": [],
        "total_words": 0,
        "streak": 0,
        "last_lesson": None,
        "quiz_performance": {
            "multiple_choice_correct": 0,
            "multiple_choice_total": 0,
            "written_correct": 0,
            "written_total": 0,
            "preferred_format": "mixed"
        }
    }

# ... [rest of functions remain the same]
