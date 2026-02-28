#!/usr/bin/env python3
"""
French Tutor Agent - FIDE A1 Level with Adaptive Quiz
Daily French lessons + Weekly quizzes for Richard Laurits
Goal: Pass FIDE test for Permit C
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

# ... [keep existing CURRICULUM, VOCABULARY, GRAMMAR_LESSONS from original file]
# FIDE A1 Curriculum - Structured progression
CURRICULUM = {
    "weeks": [
        {"week": 1, "theme": "Les bases / Grunderna", "grammar": ["être (att vara)", "avoir (att ha)", "Articles définis"], "vocab_categories": ["greetings", "numbers_1_20", "days_months"]},
        {"week": 2, "theme": "Se présenter / Presentera sig", "grammar": ["être - présent", "avoir - présent", "Questions de base"], "vocab_categories": ["personal_info", "nationalities", "family_basic"]},
        {"week": 3, "theme": "La vie quotidienne / Vardagslivet", "grammar": ["ER-verbs (1:a gruppen)", "Negation"], "vocab_categories": ["daily_routines", "time", "home"]},
        {"week": 4, "theme": "Au travail / På jobbet", "grammar": ["IR-verbs (2:a gruppen)", "RE-verbs (3:e gruppen)"], "vocab_categories": ["work_professions", "office", "actions"]},
        {"week": 5, "theme": "Nourriture / Mat", "grammar": ["Partitif (du, de la, des)", "Quantifiers"], "vocab_categories": ["food", "drinks", "restaurant"]},
        {"week": 6, "theme": "Courses / Shopping", "grammar": ["Demande de prix", "C'est / Il est"], "vocab_categories": ["shopping", "clothes", "colors"]},
        {"week": 7, "theme": "Se déplacer / Förflyttning", "grammar": ["Aller (att åka/gå)", "Prepositions de lieu"], "vocab_categories": ["transport", "directions", "places"]},
        {"week": 8, "theme": "La ville / Staden", "grammar": ["Il y a (det finns)", "Prepositions: dans, sur, sous"], "vocab_categories": ["city", "services", "weather"]},
        {"week": 9, "theme": "Les gens / Människor", "grammar": ["Adjectifs (kongruens)", "Description physique"], "vocab_categories": ["appearance", "personality", "relationships"]},
        {"week": 10, "theme": "Loisirs / Fritid", "grammar": ["Aimer + infinitif", "Pouvoir, Vouloir"], "vocab_categories": ["hobbies", "sports", "entertainment"]},
        {"week": 11, "theme": "Le passé / Dåtiden", "grammar": ["Passé composé", "Avoir/être som hjälpverb"], "vocab_categories": ["past_events", "holidays", "experiences"]},
        {"week": 12, "theme": "L'avenir / Framtiden", "grammar": ["Futur proche", "Demain, la semaine prochaine"], "vocab_categories": ["plans", "appointments", "time_expressions"]},
    ]
}

# Simplified vocabulary for testing
VOCABULARY = {
    "greetings": [
        ("Bonjour", "God dag / Hej", "Bonjour, comment allez-vous?", "God dag, hur mår ni?"),
        ("Salut", "Hej (informellt)", "Salut, ça va?", "Hej, hur är det?"),
        ("Au revoir", "Adjö / Hej då", "Au revoir et à bientôt!", "Hej då, vi ses snart!"),
        ("Merci", "Tack", "Merci beaucoup!", "Tack så mycket!"),
        ("S'il vous plaît", "Snälla / Var god", "Un café, s'il vous plaît.", "En kaffe, tack."),
        ("Excusez-moi", "Ursäkta mig", "Excusez-moi, où est la gare?", "Ursäkta, var är stationen?"),
        ("Je suis", "Jag är", "Je suis suédois.", "Jag är svensk."),
        ("J'habite", "Jag bor", "J'habite à Prangins.", "Jag bor i Prangins."),
        ("Je voudrais", "Jag skulle vilja", "Je voudrais un café.", "Jag skulle vilja ha en kaffe."),
        ("Je ne comprends pas", "Jag förstår inte", "Pardon, je ne comprends pas.", "Förlåt, jag förstår inte."),
    ],
    "numbers_1_20": [
        ("Un", "En / Ett", "J'ai un frère.", "Jag har en bror."),
        ("Deux", "Två", "Il est deux heures.", "Klockan är två."),
        ("Dix", "Tio", "J'habite ici depuis dix ans.", "Jag har bott här i tio år."),
        ("Vingt", "Tjugo", "J'ai vingt euros.", "Jag har tjugo euro."),
    ],
}

GRAMMAR_LESSONS = {
    1: {
        "topic": "Être och Avoir - Att vara och Att ha",
        "explanation": "De två viktigaste verben på franska...",
        "examples": [("Je suis suédois.", "Jag är svensk."), ("J'ai deux enfants.", "Jag har två barn.")]
    },
    2: {
        "topic": "ER-verbs (1:a konjugationen)",
        "explanation": "Regelbundna verb på -ER...",
        "examples": [("Je travaille à Genève.", "Jag arbetar i Genève."), ("Nous habitons à Prangins.", "Vi bor i Prangins.")]
    },
}

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
            "preferred_format": "mixed"  # 'mc', 'written', or 'mixed'
        }
    }

def save_progress(data):
    """Save progress to file"""
    DATA_FILE.parent.mkdir(exist_ok=True)
    with open(DATA_FILE, 'w') as f:
        json.dump(data, f, indent=2)

def load_quiz_results():
    """Load quiz history"""
    if QUIZ_LOG.exists():
        with open(QUIZ_LOG, 'r') as f:
            return json.load(f)
    return {"quizzes": []}

def save_quiz_result(quiz_data):
    """Save quiz result"""
    QUIZ_LOG.parent.mkdir(exist_ok=True)
    data = load_quiz_results()
    data["quizzes"].append(quiz_data)
    with open(QUIZ_LOG, 'w') as f:
        json.dump(data, f, indent=2)

def is_sunday():
    """Check if today is Sunday"""
    return datetime.now().weekday() == 6

def is_wednesday():
    """Check if today is Wednesday"""
    return datetime.now().weekday() == 2

def get_adaptive_format(performance):
    """Determine best quiz format based on history"""
    mc_rate = performance.get('multiple_choice_correct', 0) / max(performance.get('multiple_choice_total', 1), 1)
    written_rate = performance.get('written_correct', 0) / max(performance.get('written_total', 1), 1)
    
    # If user is much better at one format, lean that way
    if mc_rate > written_rate + 0.2:
        return "mixed_heavy_mc"  # 70% MC, 30% written
    elif written_rate > mc_rate + 0.2:
        return "mixed_heavy_written"  # 30% MC, 70% written
    else:
        return "balanced"  # 50/50

def generate_weekly_quiz(progress):
    """Generate adaptive weekly quiz"""
    # Get words from this week
    recent_words = progress.get('words_learned', [])[-50:]  # Last 50 words
    
    if len(recent_words) < 5:
        return None  # Not enough words yet
    
    # Select 8-10 words for quiz
    quiz_words = random.sample(recent_words, min(8, len(recent_words)))
    
    # Determine format based on performance
    perf = progress.get('quiz_performance', {})
    format_type = get_adaptive_format(perf)
    
    questions = []
    
    for word in quiz_words:
        # Find word details
        word_data = None
        for cat, words in VOCABULARY.items():
            for w in words:
                if w[0] == word:
                    word_data = w
                    break
            if word_data:
                break
        
        if not word_data:
            continue
        
        fr, sv, ex_fr, ex_sv = word_data
        
        # Decide question type
        if format_type == "mixed_heavy_mc":
            is_mc = random.random() < 0.7
        elif format_type == "mixed_heavy_written":
            is_mc = random.random() < 0.3
        else:
            is_mc = random.random() < 0.5
        
        if is_mc:
            # Multiple choice
            wrong = random.sample([w[1] for cat in VOCABULARY.values() for w in cat if w[1] != sv], 3)
            options = [sv] + wrong
            random.shuffle(options)
            
            questions.append({
                "type": "mc",
                "question": f"Vad betyder '{fr}'?",
                "options": options,
                "correct": sv,
                "word": fr
            })
        else:
            # Written
            questions.append({
                "type": "written",
                "question": f"Översätt till franska: '{sv}'",
                "correct": fr,
                "hint": ex_fr,
                "word": sv
            })
    
    return {
        "format_type": format_type,
        "questions": questions[:10],  # Max 10 questions
        "total_questions": len(questions[:10])
    }

def format_quiz(quiz_data, progress):
    """Format quiz for Telegram"""
    if not quiz_data:
        return None
    
    lines = []
    lines.append("🎓 **VECKO-QUIZ - Franská**")
    lines.append(f"📅 Vecka {progress['current_week']} | ~5-10 minuter")
    lines.append("")
    lines.append("💡 **Så här fungerar det:**")
    lines.append("• Skriv dina svar i ett meddelande")
    lines.append("• Svara med frasen 'QUIZ SVAR:' följt av dina svar")
    lines.append("• Jag rättar och ger feedback!")
    lines.append("")
    lines.append("───")
    lines.append("")
    
    for i, q in enumerate(quiz_data['questions'], 1):
        lines.append(f"**{i}. {q['question']}**")
        
        if q['type'] == 'mc':
            for j, opt in enumerate(q['options'], 1):
                letter = ['A', 'B', 'C', 'D'][j-1]
                lines.append(f"   {letter}) {opt}")
            lines.append(f"   _Ditt svar (t.ex. 'A')_")
        else:
            lines.append(f"   💭 _Skriv på franska_")
            lines.append(f"   💡 Tips: {q['hint']}")
        
        lines.append("")
    
    lines.append("───")
    lines.append("")
    lines.append("**Skicka dina svar så här:**")
    lines.append("`QUIZ SVAR: 1-A, 2-je suis, 3-B, ...`")
    lines.append("")
    lines.append("🎯 Lycka till!")
    
    return "\n".join(lines)

def format_daily_lesson(progress):
    """Format regular daily lesson"""
    # Get current week
    week_num = progress.get('current_week', 1)
    week_data = CURRICULUM['weeks'][week_num - 1]
    
    lines = []
    lines.append("🇫🇷 **FRENCH TUTOR - Dagens Lektion**")
    lines.append(f"📅 Vecka {week_num}: {week_data['theme']}")
    lines.append(f"📊 Dag {progress['current_day']} | Totalt ord: {progress['total_words']}")
    lines.append("")
    
    # Check for quiz reminders
    if is_wednesday():
        lines.append("💡 **Påminnelse:** Vecko-quiz på söndag!")
        lines.append("")
    
    # Grammar section
    grammar_id = ((progress['current_day'] - 1) % 3) + 1  # Cycle through grammar
    grammar = GRAMMAR_LESSONS.get(grammar_id, GRAMMAR_LESSONS[1])
    lines.append(f"📚 **Grammatik: {grammar['topic']}**")
    lines.append(grammar['explanation'])
    lines.append("")
    
    lines.append("📝 **Exempel:**")
    for fr, sv in grammar['examples'][:3]:
        lines.append(f"   🇫🇷 {fr}")
        lines.append(f"   🇸🇪 {sv}")
        lines.append("")
    
    # Vocabulary
    lines.append("───")
    lines.append("🗣️ **10 Nya Glosor**")
    lines.append("")
    
    # Select vocabulary for current week
    vocab_to_show = []
    for cat in week_data['vocab_categories'][:2]:  # First 2 categories
        if cat in VOCABULARY:
            for word_tuple in VOCABULARY[cat][:5]:  # 5 words per category
                if word_tuple[0] not in progress.get('words_learned', []):
                    vocab_to_show.append(word_tuple)
    
    # Show up to 10 words
    for i, (fr, sv, ex_fr, ex_sv) in enumerate(vocab_to_show[:10], 1):
        lines.append(f"**{i}. {fr}**")
        lines.append(f"   🇸🇪 {sv}")
        lines.append(f"   💬 {ex_fr}")
        lines.append(f"      {ex_sv}")
        lines.append("")
        
        # Add to learned words
        if fr not in progress['words_learned']:
            progress['words_learned'].append(fr)
            progress['total_words'] += 1
    
    lines.append("───")
    lines.append("💡 **Dagens 5-minuters övning:**")
    lines.append("• Säg orden högt 3 gånger")
    lines.append("• Skriv EN egen mening med 'Je suis' eller 'J'ai'")
    lines.append("• Försök hälsa på dig själv i spegeln")
    lines.append("")
    
    if is_sunday():
        lines.append("🎯 **Söndag = Quiz-dag!**")
        lines.append("Skriv 'QUIZ' för att få veckans test.")
    else:
        lines.append("🎯 **Mål:** FIDE A1 → Permit C")
    
    lines.append("⏰ Nästa lektion: Imorgon 08:00")
    
    return "\n".join(lines), vocab_to_show[:10]

def main():
    """Main function - generate lesson or quiz"""
    progress = load_progress()
    
    # Check if user requested quiz
    if len(sys.argv) > 1 and sys.argv[1].upper() == 'QUIZ':
        quiz = generate_weekly_quiz(progress)
        if quiz:
            print(format_quiz(quiz, progress))
            save_progress(progress)
        else:
            print("📚 Du behöver lära dig fler ord först! Fortsätt med dagliga lektioner.")
        return
    
    # Generate daily lesson
    today = datetime.now().date()
    
    # Update progress
    if progress.get('last_lesson') != str(today):
        progress['last_lesson'] = str(today)
        progress['current_day'] += 1
        
        # Advance week every 7 days
        if progress['current_day'] % 7 == 0:
            progress['current_week'] = min(progress['current_week'] + 1, 12)
    
    # Generate lesson
    lesson_text, new_words = format_daily_lesson(progress)
    
    # Save progress
    save_progress(progress)
    
    # Log lesson
    LESSON_LOG.parent.mkdir(exist_ok=True)
    lessons = []
    if LESSON_LOG.exists():
        with open(LESSON_LOG, 'r') as f:
            lessons = json.load(f)
    
    lessons.append({
        "date": datetime.now().isoformat(),
        "week": progress['current_week'],
        "day": progress['current_day'],
        "words": [w[0] for w in new_words]
    })
    
    with open(LESSON_LOG, 'w') as f:
        json.dump(lessons, f, indent=2)
    
    print(lesson_text)

if __name__ == "__main__":
    main()
