from langchain_ollama import ChatOllama
from langchain_core.messages import SystemMessage, HumanMessage

# 1. Configuration du modèle
# temperature=0.7 rend la réponse un peu plus naturelle/créative pour un chat standard
llm = ChatOllama(model="mistral", temperature=0,num_gpu=99,num_thread=4)

def test_mistral_pur(query):
    # 2. Création des messages
    # J'ai retiré toutes les mentions de "CONTEXTE" pour qu'il utilise son propre savoir.
    system_prompt = (
         "You are an AI Tutor specialized in Deep Learning, with strong expertise in Convolutional Neural Networks (CNNs).\n"
        "Your mission is to help the student understand theoretical concepts, design robust CNN architectures, "
        "and debug Deep Learning code in a clear and pedagogical way.\n\n"
        "==================================================\n"
        "INSTRUCTIONS (MUST BE STRICTLY FOLLOWED)\n"
        "==================================================\n"
        "1. SOURCE PRIORITY: Primarily rely on the provided CONTEXT. Quote or accurately rephrase it if the answer exists there.\n"
        "2. PEDAGOGY & EXPLANATION: Always explain 'why' and 'how'. For code or model mistakes, explain the cause and consequences.\n"
        "3. CODE QUALITY: If providing code (Python, PyTorch, TensorFlow, Keras), make it clean, optimized, and commented line by line for beginners.\n"
        "4. HONESTY: If the answer is NOT in the context, explicitly state so, then provide general knowledge as complementary information.\n"
        "5. LANGUAGE & STYLE: Always respond in clear, professional, well-structured English.\n"
        "=================================================="
    )

    messages = [
        SystemMessage(content=system_prompt),
        # On envoie juste la question brute, sans l'enrober dans un contexte
        HumanMessage(content=query)
    ]
    
    print(f"En attente de la réponse de Mistral...")
    
    # 3. Appel du modèle
    try:
        response = llm.invoke(messages)
        return response.content
    except Exception as e:
        return f"Erreur lors de l'appel : {e}"

# 4. Test simple
if __name__ == "__main__":
    question = "give me code of CNN"
    print(f"Question : {question}")
    print("-" * 30)
    
    # Appel sans contexte
    reponse = test_mistral_pur(question)
    
    print("RÉPONSE :")
    print(reponse)