from LLM import ask_question

# ============================================================================
# QUESTIONS DE TEST (modifiez selon vos documents)
# ============================================================================
""""""
tests = [
    {
        "question": "What is a CNN?",
        "mots_cles": ["convolutional", "neural", "network"],
        "doit_repondre": True
    },
    {
        "question": "Explain pooling in CNN",
        "mots_cles": ["pooling", "max", "average"],
        "doit_repondre": True
    },
    {
        "question": "Give me a PyTorch CNN example",
        "mots_cles": ["torch", "nn.Conv2d", "forward"],
        "doit_repondre": True
    },
    {
        "question": "What is backpropagation?",
        "mots_cles": ["gradient", "backward"],
        "doit_repondre": True
    },
    
    # Questions qui DOIVENT avoir une réponse
    {
        "question": "What is the weather today?",
        "phrase_refus": "I don't know.",
        "doit_repondre": False
    },
    
    {
        "question": "Explain quantum computing",
        "phrase_refus": "I don't know.",
        "doit_repondre": False
    }
]

# ============================================================================
# FONCTION D'ÉVALUATION
# ============================================================================

def evaluer():
    print("=" * 60)
    print("🎯 TEST SIMPLE DU CHATBOT")
    print("=" * 60)
    
    score_total = 0
    nb_tests = len(tests)
    
    for i, test in enumerate(tests, 1):
        print(f"\n[{i}/{nb_tests}] {test['question']}")
        print("-" * 60)
        
        # Poser la question
        reponse = ask_question(test['question'])
        
        # Vérifier la réponse
        if test['doit_repondre']:
            # Question normale : vérifier les mots-clés
            mots_trouves = sum(1 for mot in test['mots_cles'] 
                              if mot.lower() in reponse.lower())
            
            if mots_trouves >= len(test['mots_cles']) // 2:
                print("✅ PASS - Réponse correcte")
                print(f"   Mots-clés trouvés: {mots_trouves}/{len(test['mots_cles'])}")
                score_total += 1
            else:
                print("❌ FAIL - Réponse incomplète")
                print(f"   Mots-clés trouvés: {mots_trouves}/{len(test['mots_cles'])}")
        else:
            # Question hors-sujet : doit refuser
            if test['phrase_refus'].lower() in reponse.lower():
                print("✅ PASS - Refus correct (pas d'hallucination)")
                score_total += 1
            else:
                print("❌ FAIL - HALLUCINATION détectée!")
                print(f"   Réponse: {reponse[:100]}...")
        
        print(f"   Longueur réponse: {len(reponse)} caractères")
    
    # ========================================================================
    # RÉSULTAT FINAL
    # ========================================================================
    print("\n" + "=" * 60)
    print("📊 RÉSULTAT FINAL")
    print("=" * 60)
    print(f"Score: {score_total}/{nb_tests} ({score_total/nb_tests*100:.0f}%)")
    
    if score_total == nb_tests:
        print("🟢 PARFAIT - Chatbot fonctionne correctement!")
    elif score_total >= nb_tests * 0.7:
        print("🟡 BON - Quelques améliorations possibles")
    else:
        print("🔴 PROBLÈMES - Optimisation nécessaire")
    
    print("=" * 60)

# ============================================================================
# EXÉCUTION
# ============================================================================

if __name__ == "__main__":
    evaluer()