#!/usr/bin/env python3
"""
FIDE A1 Daily Lesson Generator
Delivers targeted French practice for FIDE A1 exam preparation
90-day curriculum aligned with exam competencies
"""

import json
import random
from datetime import datetime, timedelta
from pathlib import Path

AGENT_DIR = Path(__file__).parent

def load_curriculum():
    """Load FIDE A1 curriculum."""
    with open(AGENT_DIR / "fide_a1_curriculum.json") as f:
        return json.load(f)

def load_progress():
    """Load current progress."""
    progress_file = AGENT_DIR / "fide_progress.json"
    if progress_file.exists():
        with open(progress_file) as f:
            return json.load(f)
    return None

def save_progress(progress):
    """Save progress update."""
    with open(AGENT_DIR / "fide_progress.json", "w") as f:
        json.dump(progress, f, indent=2, default=str)

def get_current_phase(curriculum, day):
    """Determine which phase we're in based on day number."""
    for phase in curriculum["phases"]:
        day_range = phase["days"].split("-")
        start = int(day_range[0])
        end = int(day_range[1])
        if start <= day <= end:
            return phase
    return curriculum["phases"][-1]  # Default to last phase

def generate_vocabulary_lesson(phase, day):
    """Generate vocabulary based on phase and day."""
    vocab_sets = {
        "Foundation": {
            "week_1": ["Bonjour", "Salut", "Au revoir", "Merci", "S'il vous plaît", "Oui", "Non", "Pardon"],
            "week_2": ["Je", "Tu", "Il", "Elle", "Nous", "Vous", "Ils", "Elles"],
            "week_3": ["Un", "Deux", "Trois", "Quatre", "Cinq", "Six", "Sept", "Huit", "Neuf", "Dix"],
            "week_4": ["Lundi", "Mardi", "Mercredi", "Jeudi", "Vendredi", "Samedi", "Dimanche",
                       "Janvier", "Février", "Mars", "Avril", "Mai", "Juin"]
        },
        "Daily Life": {
            "week_5": ["Manger", "Boire", "Petit déjeuner", "Déjeuner", "Dîner", "Pain", "Eau", "Café"],
            "week_6": ["Maison", "Appartement", "Chambre", "Cuisine", "Salon", "Table", "Chaise", "Lit"],
            "week_7": ["Famille", "Mère", "Père", "Sœur", "Frère", "Fille", "Garçon", "Bébé"],
            "week_8": ["Temps", "Soleil", "Pluie", "Neige", "Chaud", "Froid", "Printemps", "Été"]
        },
        "Communication": {
            "week_9": ["Acheter", "Prix", "Cher", "Bon marché", "Argent", "Euro", "Magasin", "Marché"],
            "week_10": ["Restaurant", "Menu", "Addition", "Serveur", "Commander", "Pain", "Vin", "Eau"],
            "week_11": ["Gauche", "Droite", "Tout droit", "Rue", "Place", "Arrêt", "Train", "Bus"]
        },
        "Exam Preparation": {
            "week_12": ["Examen", "Réussir", "Question", "Réponse", "Comprendre", "Parler", "Écouter"],
            "week_13": ["Confiance", "Calme", "Prêt", "Capable", "Important", "Facile", "Difficile"]
        }
    }
    
    week_num = min((day // 7) + 1, 13)
    week_key = f"week_{week_num}"
    
    phase_vocab = vocab_sets.get(phase["name"], vocab_sets["Exam Preparation"])
    words = phase_vocab.get(week_key, phase_vocab.get("week_12", []))
    
    return random.sample(words, min(5, len(words)))

def generate_grammar_focus(phase, day):
    """Generate grammar focus based on phase."""
    grammar_topics = {
        "Foundation": [
            "Present tense: être (je suis, tu es, il/elle est)",
            "Present tense: avoir (j'ai, tu as, il/elle a)",
            "Gender: le (masculin) vs la (féminin)",
            "Articles: un, une, des"
        ],
        "Daily Life": [
            "Regular -er verbs: parler, manger, travailler",
            "Negation: ne...pas (Je ne comprends pas)",
            "Plurals: add -s, -x, or -aux",
            "Adjectives agree with nouns"
        ],
        "Communication": [
            "Question words: Où? Quand? Comment? Combien?",
            "Forming questions: Est-ce que...?",
            "Near future: aller + infinitive (Je vais manger)",
            "Partitive: du, de la, des"
        ],
        "Exam Preparation": [
            "Common FIDE exam phrases",
            "Polite forms: Pourriez-vous...?",
            "Expressing needs: J'ai besoin de...",
            "Giving opinions: Je pense que..."
        ]
    }
    
    topics = grammar_topics.get(phase["name"], grammar_topics["Exam Preparation"])
    return random.choice(topics)

def generate_practice_scenario(phase):
    """Generate FIDE-style practice scenario."""
    scenarios = {
        "Foundation": [
            "Introduce yourself: name, age, where you live",
            "Count from 1 to 20 and back",
            "Say the days of the week",
            "Ask 'How are you?' and respond"
        ],
        "Daily Life": [
            "Describe your morning routine",
            "Talk about your family (3 sentences)",
            "Order food at a restaurant",
            "Describe the weather today"
        ],
        "Communication": [
            "Ask for directions to the train station",
            "Buy something at a shop - ask the price",
            "Make a doctor's appointment by phone",
            "Describe your home to a friend"
        ],
        "Exam Preparation": [
            "FIDE Mock: Self-introduction (2 minutes)",
            "FIDE Mock: Answer personal questions",
            "FIDE Mock: Describe your typical day",
            "FIDE Mock: Role-play at a restaurant"
        ]
    }
    
    phase_scenarios = scenarios.get(phase["name"], scenarios["Exam Preparation"])
    return random.choice(phase_scenarios)

def generate_daily_lesson():
    """Generate complete daily lesson."""
    curriculum = load_curriculum()
    progress = load_progress()
    
    if not progress:
        print("❌ No progress file found. Starting fresh...")
        return None
    
    # Calculate current day
    start = datetime.fromisoformat(curriculum["start_date"])
    today = datetime.now()
    day_number = (today - start).days + 1
    days_remaining = (datetime.fromisoformat(curriculum["goal_date"]) - today).days
    
    # Get current phase
    phase = get_current_phase(curriculum, day_number)
    
    # Generate lesson components
    vocab = generate_vocabulary_lesson(phase, day_number)
    grammar = generate_grammar_focus(phase, day_number)
    scenario = generate_practice_scenario(phase)
    
    # Build lesson
    lesson = {
        "date": today.isoformat(),
        "day_number": day_number,
        "days_to_exam": days_remaining,
        "phase": phase["phase"],
        "phase_name": phase["name"],
        "daily_minutes": phase["daily_minutes"],
        "vocabulary": vocab,
        "grammar_focus": grammar,
        "practice_scenario": scenario,
        "exam_competency": random.choice(["oral_comprehension", "oral_production", "interaction"]),
        "motivation": f"📚 Day {day_number}/90 - {days_remaining} days until FIDE A1 exam!"
    }
    
    # Display lesson
    print("=" * 60)
    print(f"🎯 FIDE A1 FRENCH LESSON - Day {day_number} of 90")
    print("=" * 60)
    print(f"📅 {today.strftime('%A, %B %d')}")
    print(f"⏰ Target: {lesson['daily_minutes']} minutes")
    print(f"📍 Phase: {phase['name']} (Week {(day_number-1)//7 + 1})")
    print(f"🎯 Days to exam: {days_remaining}")
    print()
    print(f"📝 Today's Vocabulary ({len(vocab)} words):")
    for word in vocab:
        print(f"   • {word}")
    print()
    print(f"🔤 Grammar Focus:")
    print(f"   {grammar}")
    print()
    print(f"🎭 Practice Scenario:")
    print(f"   {scenario}")
    print()
    print(f"🎯 Exam Competency: {lesson['exam_competency'].replace('_', ' ').title()}")
    print()
    print(lesson['motivation'])
    print("=" * 60)
    
    # Update progress
    progress["exam_prep"]["current_day"] = day_number
    progress["exam_prep"]["days_remaining"] = days_remaining
    progress["exam_prep"]["phase"] = phase["phase"]
    progress["exam_prep"]["phase_name"] = phase["name"]
    
    # Add to practice log
    progress["practice_log"].append({
        "date": today.strftime("%Y-%m-%d"),
        "type": "daily_lesson",
        "duration_minutes": phase["daily_minutes"],
        "phase": phase["name"],
        "words_learned": len(vocab)
    })
    
    # Update vocabulary count
    current_words = set(progress["vocabulary"].get("learned_words", []))
    current_words.update(vocab)
    progress["vocabulary"]["learned"] = len(current_words)
    progress["vocabulary"]["learned_words"] = list(current_words)
    
    save_progress(progress)
    
    # Log activity
    with open(AGENT_DIR / "activity.log", "a") as f:
        f.write(f"[{today.isoformat()}] FIDE Lesson Day {day_number} delivered - {len(vocab)} words\n")
    
    return lesson

if __name__ == "__main__":
    lesson = generate_daily_lesson()
    if lesson:
        print("\n✅ Lesson delivered and progress updated!")
    else:
        print("\n❌ Could not generate lesson")
