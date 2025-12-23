from langchain_ollama import ChatOllama
from langchain_core.messages import SystemMessage, HumanMessage

# 1. Configuration du modèle (Directement via Ollama)
# On utilise temperature=0.7 pour laisser un peu de créativité au modèle
llm = ChatOllama(model="deepseek-coder", temperature=0)

def test_deepseek(prompt_utilisateur):
    # 2. Création des messages
    # On définit un rôle système pour éviter qu'il ne réponde qu'en code
    messages = [
        SystemMessage(content="Tu es un assistant IA polyvalent et utile. Réponds toujours en français."),
        HumanMessage(content=prompt_utilisateur)
    ]
    
    print("En attente de DeepSeek...")
    
    # 3. Appel du modèle
    try:
        response = llm.invoke(messages)
        return response.content
    except Exception as e:
        return f"Erreur lors de l'appel : {e}"

# 4. Test simple
if __name__ == "__main__":
    question = "c quoi nn.Conv1d"
    print(f"Question : {question}")
    print("-" * 30)
    
    reponse = test_deepseek(question)
    print("RÉPONSE :")
    print(reponse)