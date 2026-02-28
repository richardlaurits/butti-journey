#!/usr/bin/env python3
"""
French Quiz Grader - Grade user quiz responses
"""

import json
import sys
from datetime import datetime
from pathlib import Path

AGENT_DIR = Path('/home/richard-laurits/.openclaw/workspace/agents/french-tutor-agent')
DATA_FILE = AGENT_DIR / 'progress.json'
QUIZ_LOG = AGENT_DIR / 'quiz_results.json'

def load_progress():
    if DATA_FILE.exists():
        with open(DATA_FILE, 'r') as f:
            return json.load(f)
    return {}

def save_progress(data):
    with open(DATA_FILE, 'w') as f:
        json.dump(data, f, indent=2)

def load_last_quiz():
    """Load the most recent quiz"""
    if QUIZ_LOG.exists():
        with open(QUIZ_LOG, 'r') as f:
            data = json.load(f)
            if data.get('quizzes'):
                return data['quizzes'][-1]
    return None

def grade_quiz(user_answers):
    """Grade user's quiz answers"""
    last_quiz = load_last_quiz()
    if not last_quiz:
        return "❌ Inget aktivt quiz hittades. Be om ett nytt med 'QUIZ'"
    
    questions = last_quiz.get('questions', [])
    
    # Parse user answers (format: "1-A, 2-je suis, 3-B")
    answers = {}
    for part in user_answers.split(','):
        part = part.strip()
        if '-' in part:
            try:
                num, ans = part.split('-', 1)
                answers[int(num.strip())] = ans.strip().lower()
            except:
                continue
    
    # Grade each question
    results = []
    mc_correct = 0
    mc_total = 0
    written_correct = 0
    written_total = 0
    
    for i, q in enumerate(questions, 1):
        user_ans = answers.get(i, "")
        correct_ans = q.get('correct', '').lower()
        
        if q['type'] == 'mc':
            mc_total += 1
            # For MC, find which option is correct
            is_correct = user_ans == correct_ans.lower() or \
                        (correct_ans.lower() in [opt.lower() for opt in q.get('options', [])] and 
                         user_ans.upper() in ['A', 'B', 'C', 'D'] and
                         q['options'][ord(user_ans.upper()) - ord('A')].lower() == correct_ans.lower())
            
            if is_correct:
                mc_correct += 1
                results.append(f"✅ **{i}.** Rätt!")
            else:
                results.append(f"❌ **{i}.** Fel. Rätt svar: *{q.get('correct')}*")
                
        else:  # written
            written_total += 1
            # Fuzzy matching for written answers
            is_correct = user_ans == correct_ans or \
                        (len(user_ans) > 3 and correct_ans in user_ans) or \
                        (user_ans.replace("'", " ") == correct_ans.replace("'", " "))
            
            if is_correct:
                written_correct += 1
                results.append(f"✅ **{i}.** Rätt! *{q.get('correct')}*")
            else:
                results.append(f"❌ **{i}.** Ditt svar: *{user_ans}* | Rätt: *{q.get('correct')}*")
    
    # Calculate score
    total_correct = mc_correct + written_correct
    total_questions = len(questions)
    percentage = (total_correct / total_questions * 100) if total_questions > 0 else 0
    
    # Update progress with performance data
    progress = load_progress()
    if 'quiz_performance' not in progress:
        progress['quiz_performance'] = {
            'multiple_choice_correct': 0,
            'multiple_choice_total': 0,
            'written_correct': 0,
            'written_total': 0
        }
    
    progress['quiz_performance']['multiple_choice_correct'] += mc_correct
    progress['quiz_performance']['multiple_choice_total'] += mc_total
    progress['quiz_performance']['written_correct'] += written_correct
    progress['quiz_performance']['written_total'] += written_total
    
    # Determine preferred format
    mc_rate = progress['quiz_performance']['multiple_choice_correct'] / max(progress['quiz_performance']['multiple_choice_total'], 1)
    written_rate = progress['quiz_performance']['written_correct'] / max(progress['quiz_performance']['written_total'], 1)
    
    if mc_rate > written_rate + 0.15:
        progress['quiz_performance']['preferred_format'] = 'mixed_heavy_mc'
    elif written_rate > mc_rate + 0.15:
        progress['quiz_performance']['preferred_format'] = 'mixed_heavy_written'
    else:
        progress['quiz_performance']['preferred_format'] = 'balanced'
    
    save_progress(progress)
    
    # Format output
    lines = []
    lines.append("🎓 **QUIZ-RESULTAT**")
    lines.append("")
    lines.append(f"📊 **{total_correct}/{total_questions} rätt** ({percentage:.0f}%)")
    lines.append("")
    
    if percentage >= 80:
        lines.append("🌟 Utmärkt! Du behärskar det här!")
    elif percentage >= 60:
        lines.append("👍 Bra jobbat! Fortsätt öva.")
    else:
        lines.append("💪 Fortsätt träna! Repetera glosorna.")
    
    lines.append("")
    lines.append("**Dina svar:**")
    for r in results:
        lines.append(r)
    
    lines.append("")
    lines.append("───")
    lines.append("")
    lines.append(f"📈 Multiple choice: {mc_correct}/{mc_total} rätt")
    lines.append(f"✍️ Skriva själv: {written_correct}/{written_total} rätt")
    lines.append("")
    lines.append(f"🤖 Agenten lär sig: Du presterar bäst med **{progress['quiz_performance']['preferred_format']}** format")
    lines.append("   (Nästa quiz anpassas efter detta)")
    
    return "\n".join(lines)

def main():
    if len(sys.argv) < 2:
        print("Usage: python3 quiz_grader.py '1-A, 2-je suis, 3-B'")
        sys.exit(1)
    
    user_input = sys.argv[1]
    result = grade_quiz(user_input)
    print(result)

if __name__ == "__main__":
    main()
