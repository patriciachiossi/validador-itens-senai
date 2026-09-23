import streamlit as st
import google.generativeai as genai

# 1. Configuração da Página
st.set_page_config(
    page_title="Validador SENAI",
    page_icon="⚙️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 2. Estilização CSS Personalizada (Cores no Padrão SENAI)
st.markdown("""
    
""", unsafe_allow_html=True)

# 3. Cabeçalho do App
st.markdown('
            # Bloco 2: Estrutura do Item
with st.container(border=True):
    st.markdown("#### 📝 2. Componentes da Questão")
    suporte = st.text_area("Texto de Suporte (Situação-Problema / Contexto)", height=100, placeholder="Insira o texto, cenário ou dados de entrada...")
    comando = st.text_area("Comando (Instrução Direta)", height=70, placeholder="O que o estudante deve responder?")
    
    st.markdown("**Alternativas e Gabarito**")
    ca, cb = st.columns(2)
    with ca:
        alt_a = st.text_input("A)", placeholder="Alternativa A")
        alt_b = st.text_input("B)", placeholder="Alternativa B")
    with cb:
        alt_c = st.text_input("C)", placeholder="Alternativa C")
        alt_d = st.text_input("D)", placeholder="Alternativa D")
        
    gabarito = st.radio("Selecione o Gabarito Correto:", ["A", "B", "C", "D"], horizontal=True)

btn_validar = st.button("🚀 Auditar e Refatorar Item", use_container_width=True)
if btn_validar:
    if not user_api_key:
        st.error("⚠️ Digite sua chave da API no menu lateral para iniciar.")
    elif not comando or not alt_a or not alt_b:
        st.warning("⚠️ Preencha ao menos o comando e duas alternativas para validação.")
    else:
        with st.spinner("Analisando conformidade pedagógica..."):
            try:
                genai.configure(api_key=user_api_key)
                model = genai.GenerativeModel("gemini-1.5-flash")
                
                prompt = f"""
                Você é um auditor pedagógico especialista na Metodologia SENAI de Educação Profissional.
                Avalie o item abaixo e responda estritamente formatado em Markdown limpo:

                DADOS:
                - Unidade Curricular: {uc}
                - Capacidade: {capacidade}
                - Nível Cognitivo: {nivel}
                - Texto de Suporte: {suporte}
                - Comando: {comando}
                - Alternativas: A) {alt_a} | B) {alt_b} | C) {alt_c} | D) {alt_d}
                - Gabarito Indicado: {gabarito}

                ESTRUTURA DA RESPOSTA:
                ## 🏆 Diagnóstico Geral
                - **Score de Conformidade:** [Atribua de 0 a 100%]
                - **Veredito:** [1 frase resumindo o estado da questão]

                ## 🔍 Análise Técnica
                * **Texto de Suporte:** [Avaliar autenticidade e necessidade]
                * **Comando:** [Avaliar clareza, objetividade e ausência de negações/pegadinhas]
                * **Distratores:** [Avaliar plausibilidade e paralelismo gramatical]
                ## ✨ Sugestão de Item Refatorado (Padrão SENAI)
                **Texto de Suporte:**  
                [Texto corrigido]

                **Comando:**  
                [Comando corrigido]

                **Alternativas:**  
                * **A)** [Texto]
                * **B)** [Texto]
                * **C)** [Texto]
                * **D)** [Texto]

                **Gabarito Definitivo:** [Letra e breve justificativa]
                """
                
                response = model.generate_content(prompt)
                
                tab1, tab2 = st.tabs(["📋 Relatório & Versão Final", "💾 Exportar"])
                
                with tab1:
                    st.markdown(response.text)
                    
                with tab2:
                    st.write("Baixe o relatório completo e o item corrigido em arquivo de texto:")
                    st.download_button(
                        label="⬇️ Baixar Diagnóstico (.txt)",
                        data=response.text,
                        file_name="Item_Valido_SENAI.txt",
                        mime="text/plain",
                        use_container_width=True
                    )
                    
            except Exception as e:
                st.error(f"Erro na comunicação com a IA: {e}")
else:
    st.info("👈 Preencha os campos da questão e clique em **Auditar e Refatorar Item** para gerar a análise.")
