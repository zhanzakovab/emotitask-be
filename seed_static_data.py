# seed_static_data.py
from sqlalchemy.orm import Session
from app.models.database_models import Question, Answer, MBTIType, ChatStyle
from app.database import SessionLocal

# 1. Prepare your static data as lists of dicts or tuples

questions = [
    # 10 fun, scenario-based MBTI questions
    {"question": "It’s a rare, completely free Saturday with perfect weather. How do you kick it off?"},
    {"question": "You walk into a house-party where you know only the host. What’s your immediate move?"},
    {"question": "During a fast-moving brainstorm at work or class, you usually…"},
    {"question": "Learning something brand new on YouTube, you care most about…"},
    {"question": "Reading a trending novel, what hooks you?"},

    {"question": "At your dream job, which feedback excites you more?"},
    {"question": "Big decision time: a friend asks your advice. You default to…"},
    {"question": "Mid-debate on Discord, the part you secretly enjoy is…"},
    {"question": "A project’s kickoff meeting is tomorrow. Tonight you’re most likely to…"},
    {"question": "You wake up to an empty weekend, no commitments. Your perfect plan is to…"}
]

answers = [
    # Question 1
    {"question_id": 1, "answer": "Rally a bunch of friends for an impromptu adventure downtown"},
    {"question_id": 1, "answer": "DM a few pals to grab coffee and wander"},
    {"question_id": 1, "answer": "Curl up solo with your favourite show or game"},
    {"question_id": 1, "answer": "Take a peaceful nature walk alone, phone on Do Not Disturb"},

    # Question 2
    {"question_id": 2, "answer": "Bounce around introducing yourself to everyone"},
    {"question_id": 2, "answer": "Slide into a small group chat in the kitchen for chill convo"},
    {"question_id": 2, "answer": "Hang back, observe the vibe, chat once approached"},
    {"question_id": 2, "answer": "Locate the pet / balcony and people-watch in peace"},

    # Question 3
    {"question_id": 3, "answer": "Fire off ideas as they pop into your head"},
    {"question_id": 3, "answer": "Share after a quick think so the convo stays lively"},
    {"question_id": 3, "answer": "Listen, mull things over, then offer a polished thought"},
    {"question_id": 3, "answer": "Sketch ideas privately first, share them later in chat"},

    # Question 4
    {"question_id": 4, "answer": "Clear step-by-step tutorials with real demos"},
    {"question_id": 4, "answer": "Practical hacks you can copy right away"},
    {"question_id": 4, "answer": "The bigger concept behind why it works"},
    {"question_id": 4, "answer": "The future possibilities the idea unlocks"},

    # Question 5
    {"question_id": 5, "answer": "Sensory details that make the world feel tangible"},
    {"question_id": 5, "answer": "Everyday characters you could totally know IRL"},
    {"question_id": 5, "answer": "Hidden symbols & Easter-eggs to decode"},
    {"question_id": 5, "answer": "Philosophical themes you can debate for hours"},

    # Question 6
    {"question_id": 6, "answer": "‘Great execution—exactly followed the proven playbook.’"},
    {"question_id": 6, "answer": "‘Love how practical your solution is—instantly usable.’"},
    {"question_id": 6, "answer": "‘Brilliant twist—never would’ve thought of that angle.’"},
    {"question_id": 6, "answer": "‘Your vision redefines where we’re headed long-term.’"},

    # Question 7
    {"question_id": 7, "answer": "Lay out the cold facts and probabilities"},
    {"question_id": 7, "answer": "Step back emotionally, list pros & cons logically"},
    {"question_id": 7, "answer": "Ask how each option aligns with their values"},
    {"question_id": 7, "answer": "Tune into the mood and reassure them you’ve got them"},

    # Question 8
    {"question_id": 8, "answer": "Spotting logical fallacies like a detective"},
    {"question_id": 8, "answer": "Stress-testing ideas until only the strongest survive"},
    {"question_id": 8, "answer": "Hearing the human story behind each viewpoint"},
    {"question_id": 8, "answer": "Guiding everyone toward a warm, mutual ‘aha’ moment"},

    # Question 9
    {"question_id": 9, "answer": "Build a colour-coded timeline with fixed milestones"},
    {"question_id": 9, "answer": "Pre-assign tasks in Notion so morning runs smoothly"},
    {"question_id": 9, "answer": "Leave wiggle-room so you can pivot if inspiration strikes"},
    {"question_id": 9, "answer": "Wait to see the vibes tomorrow before locking anything"},

    # Question 10
    {"question_id": 10, "answer": "Immediately map out activities in your calendar"},
    {"question_id": 10, "answer": "Knock out errands so Monday-you feels accomplished"},
    {"question_id": 10, "answer": "Decide each morning based on your current mood"},
    {"question_id": 10, "answer": "Let random invites and surprises dictate the flow"},
]

mbti_types = [
    {"persona_id": "INTJ", "name": "The Architect", "description": "Imaginative, strategic, and always planning three steps ahead."},
    {"persona_id": "INTP", "name": "The Thinker", "description": "Curious and logical minds who live to analyze and understand everything."},
    {"persona_id": "ENTJ", "name": "The Commander", "description": "Bold, visionary leaders who love to organize and execute big plans."},
    {"persona_id": "ENTP", "name": "The Debater", "description": "Energetic brainstormers who challenge ideas just for the thrill of it."},

    {"persona_id": "INFJ", "name": "The Advocate", "description": "Insightful idealists who fight for purpose and quietly move mountains."},
    {"persona_id": "INFP", "name": "The Mediator", "description": "Empathetic, dreamy creatives with deep values and a love for meaning."},
    {"persona_id": "ENFJ", "name": "The Protagonist", "description": "Inspiring motivators who light up rooms and lift up people."},
    {"persona_id": "ENFP", "name": "The Campaigner", "description": "Free-spirited enthusiasts full of ideas, emotions, and energy."},

    {"persona_id": "ISTJ", "name": "The Logistician", "description": "Reliable and practical planners who value structure and order."},
    {"persona_id": "ISFJ", "name": "The Defender", "description": "Quiet protectors with a strong sense of duty and a kind heart."},
    {"persona_id": "ESTJ", "name": "The Executive", "description": "Organized and confident leaders who get things done."},
    {"persona_id": "ESFJ", "name": "The Consul", "description": "Warm and loyal helpers who love bringing people together."},

    {"persona_id": "ISTP", "name": "The Virtuoso", "description": "Independent experimenters who love building, fixing, and hacking life."},
    {"persona_id": "ISFP", "name": "The Adventurer", "description": "Creative souls who live in the moment and chase beauty and freedom."},
    {"persona_id": "ESTP", "name": "The Dynamo", "description": "Bold risk-takers who thrive on action, thrills, and quick thinking."},
    {"persona_id": "ESFP", "name": "The Entertainer", "description": "Charismatic performers who light up the room and live for the vibe."}
]

chat_styles = [
    # 1. INTJ – The Architect
    {"mbti_type_id": 1, "keywords": '{"style": "strategic, concise, logical"}', "temperature": 0.6},
    # 2. INTP – The Thinker
    {"mbti_type_id": 2, "keywords": '{"style": "curious, analytical, abstract"}', "temperature": 0.7},
    # 3. ENTJ – The Commander
    {"mbti_type_id": 3, "keywords": '{"style": "direct, efficient, assertive"}', "temperature": 0.6},
    # 4. ENTP – The Debater
    {"mbti_type_id": 4, "keywords": '{"style": "playful, clever, spontaneous"}', "temperature": 0.85},

    # 5. INFJ – The Advocate
    {"mbti_type_id": 5, "keywords": '{"style": "warm, thoughtful, visionary"}', "temperature": 0.75},
    # 6. INFP – The Mediator
    {"mbti_type_id": 6, "keywords": '{"style": "gentle, encouraging, dreamy"}', "temperature": 0.85},
    # 7. ENFJ – The Protagonist
    {"mbti_type_id": 7, "keywords": '{"style": "motivational, empathetic, inspiring"}', "temperature": 0.8},
    # 8. ENFP – The Campaigner
    {"mbti_type_id": 8, "keywords": '{"style": "upbeat, quirky, imaginative"}', "temperature": 0.9},

    # 9. ISTJ – The Logistician
    {"mbti_type_id": 9, "keywords": '{"style": "organized, factual, grounded"}', "temperature": 0.5},
    # 10. ISFJ – The Defender
    {"mbti_type_id": 10, "keywords": '{"style": "supportive, calm, loyal"}', "temperature": 0.6},
    # 11. ESTJ – The Executive
    {"mbti_type_id": 11, "keywords": '{"style": "structured, assertive, pragmatic"}', "temperature": 0.55},
    # 12. ESFJ – The Consul
    {"mbti_type_id": 12, "keywords": '{"style": "caring, social, inclusive"}', "temperature": 0.7},

    # 13. ISTP – The Virtuoso
    {"mbti_type_id": 13, "keywords": '{"style": "pragmatic, cool-headed, action-oriented"}', "temperature": 0.65},
    # 14. ISFP – The Adventurer
    {"mbti_type_id": 14, "keywords": '{"style": "gentle, aesthetic, expressive"}', "temperature": 0.8},
    # 15. ESTP – The Dynamo
    {"mbti_type_id": 15, "keywords": '{"style": "bold, fast-paced, witty"}', "temperature": 0.85},
    # 16. ESFP – The Entertainer
    {"mbti_type_id": 16, "keywords": '{"style": "fun, expressive, high-energy"}', "temperature": 0.9},
]

def seed():
    db: Session = SessionLocal()

    # Clear existing static data first (optional, for dev/testing)
    db.query(Question).delete()
    db.query(Answer).delete()
    db.query(MBTIType).delete()
    db.query(ChatStyle).delete()
    db.commit()

    # Insert Questions
    db.add_all([Question(**q) for q in questions])
    db.commit()

    # Insert Answers
    db.add_all([Answer(**a) for a in answers])
    db.commit()

    # Insert MBTI Types
    db.add_all([MBTIType(**m) for m in mbti_types])
    db.commit()

    # Insert Chat Styles
    db.add_all([ChatStyle(**c) for c in chat_styles])
    db.commit()

    db.close()
    print("Static data seeded.")

if __name__ == '__main__':
    seed()