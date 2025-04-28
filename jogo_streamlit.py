import streamlit as st
import random
import pandas as pd
import os

# Configurar a página
st.set_page_config(page_title="50 em 5", page_icon="🎯", layout="centered", initial_sidebar_state="collapsed")

# Esconder o menu do Streamlit
hide_menu_style = """
    <style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    </style>
"""
st.markdown(hide_menu_style, unsafe_allow_html=True)

# Estilo visual
st.markdown(
    """
    <style>
    .stApp {
        background-color: #0A0A23;
        color: white;
        padding: 2rem;
    }
    h1, h2, h3 {
        color: white;
        text-align: center;
        font-weight: bold;
    }
    .stButton>button {
        background-color: #00FFFF;
        color: #0A0A23;
        font-weight: bold;
        border-radius: 8px;
        padding: 0.75rem 1.5rem;
        font-size: 1rem;
    }
    .stButton>button:hover {
        background-color: #00CCCC;
        color: white;
    }
    .stNumberInput>div>div>input {
        background-color: #0A0A23;
        color: white;
        border: 2px solid #00FFFF;
        border-radius: 6px;
    }
    </style>
    """,
    unsafe_allow_html=True
)
# Funções para tocar trilha sonora e efeitos
def tocar_trilha():
    st.markdown(
        """
        <audio id="trilha" autoplay loop style="display:none;">
          <source src="https://www.soundhelix.com/examples/mp3/SoundHelix-Song-1.mp3" type="audio/mpeg">
        </audio>
        """,
        unsafe_allow_html=True
    )

def tocar_efeito(link_som):
    st.markdown(
        f"""
        <audio autoplay style="display:none;">
          <source src="{link_som}" type="audio/mpeg">
        </audio>
        """,
        unsafe_allow_html=True
    )

# Links dos efeitos
LINK_PALPITE_ERRADO = "https://assets.mixkit.co/sfx/preview/mixkit-arcade-retro-game-over-213.mp3"
LINK_VITORIA = "https://assets.mixkit.co/sfx/preview/mixkit-achievement-bell-600.mp3"
LINK_GAMEOVER = "https://assets.mixkit.co/sfx/preview/mixkit-player-losing-or-failing-2042.mp3"
# Arquivo de ranking
ranking_file = "ranking.csv"

# Inicializar sessão
if "email" not in st.session_state:
    st.session_state.email = ""
if "nickname" not in st.session_state:
    st.session_state.nickname = ""
if "telefone" not in st.session_state:
    st.session_state.telefone = ""
if "creditos" not in st.session_state:
    st.session_state.creditos = 100
if "numero_secreto" not in st.session_state:
    st.session_state.numero_secreto = random.randint(1, 50)
if "tentativas" not in st.session_state:
    st.session_state.tentativas = 0
if "trilha_ativa" not in st.session_state:
    st.session_state.trilha_ativa = False

# Tela de login/cadastro
if st.session_state.email == "":
    st.title("🎯 50 em 5")
    email = st.text_input("Digite seu E-mail:", max_chars=50)
    nick = st.text_input("Escolha seu Nickname:", max_chars=20)
    telefone = st.text_input("Digite seu Telefone (somente números):", max_chars=15)

    if email and nick and telefone:
        # Verifica se já existe cadastro
        if os.path.exists(ranking_file):
            df = pd.read_csv(ranking_file)
            if email in df["Email"].values:
                dados = df[df["Email"] == email].iloc[0]
                st.session_state.email = dados["Email"]
                st.session_state.nickname = dados["Nick"]
                st.session_state.telefone = dados["Telefone"]
                st.session_state.creditos = dados["Créditos"]
                st.rerun()
            else:
                st.session_state.email = email
                st.session_state.nickname = nick
                st.session_state.telefone = telefone
                st.session_state.creditos = 100
                st.rerun()
        else:
            st.session_state.email = email
            st.session_state.nickname = nick
            st.session_state.telefone = telefone
            st.session_state.creditos = 100
            st.rerun()
else:
    # Tela de jogo
    st.title("🎯 50 em 5")

    # Botão para ativar música
    if not st.session_state.trilha_ativa:
        if st.button("🔊 Ativar Música"):
            tocar_trilha()
            st.session_state.trilha_ativa = True
    else:
        tocar_trilha()

    st.write(f"👤 Jogador: **{st.session_state.nickname}**")
    st.write(f"💰 Créditos: **{st.session_state.creditos}**")
    st.write(f"🧠 Tentativas nesta rodada: **{st.session_state.tentativas + 1}/5**")

    palpite = st.number_input("Digite seu palpite:", min_value=1, max_value=50, step=1)
    enviar = st.button("🎯 Enviar Palpite")

    if enviar and st.session_state.creditos > 0:
        st.session_state.creditos -= 1
        st.session_state.tentativas += 1

        if palpite == st.session_state.numero_secreto:
            if st.session_state.tentativas == 1:
                bonus = 50
            elif st.session_state.tentativas == 2:
                bonus = 40
            elif st.session_state.tentativas == 3:
                bonus = 30
            elif st.session_state.tentativas == 4:
                bonus = 20
            elif st.session_state.tentativas == 5:
                bonus = 10
            else:
                bonus = 0

            st.session_state.creditos += bonus
            st.success(f"🎉 Parabéns, {st.session_state.nickname}! Você acertou em {st.session_state.tentativas} tentativas!")
            tocar_efeito(LINK_VITORIA)
            st.balloons()

            # Atualizar ranking
            if os.path.exists(ranking_file):
                df = pd.read_csv(ranking_file)
                df = df[df["Email"] != st.session_state.email]
            else:
                df = pd.DataFrame(columns=["Email", "Nick", "Telefone", "Tentativas", "Créditos", "Pontos Ganhos"])

            nova_linha = {"Email": st.session_state.email,
                          "Nick": st.session_state.nickname,
                          "Telefone": st.session_state.telefone,
                          "Tentativas": st.session_state.tentativas,
                          "Créditos": st.session_state.creditos,
                          "Pontos Ganhos": bonus}
            df = pd.concat([df, pd.DataFrame([nova_linha])], ignore_index=True)
            df.to_csv(ranking_file, index=False)

            st.session_state.numero_secreto = random.randint(1, 50)
            st.session_state.tentativas = 0

        elif st.session_state.tentativas >= 5:
            st.error(f"💀 Não acertou, {st.session_state.nickname}! O número secreto era {st.session_state.numero_secreto}.")
            tocar_efeito(LINK_GAMEOVER)
            st.session_state.numero_secreto = random.randint(1, 50)
            st.session_state.tentativas = 0

        else:
            if palpite < st.session_state.numero_secreto:
                st.warning("Dica do Jones, tente um número maior!")
            else:
                st.warning("Dica do Jones, tente um número menor!")
            tocar_efeito(LINK_PALPITE_ERRADO)

    if st.session_state.creditos <= 0:
        st.warning("⚠️ Você ficou sem créditos!")
        if st.button("🔄 RESETAR CRÉDITOS"):
            st.session_state.creditos = 100
            st.session_state.numero_secreto = random.randint(1, 50)
            st.session_state.tentativas = 0
            st.success("Créditos resetados para 100!")

    st.subheader("🏆 Ranking dos Jogadores")
    if os.path.exists(ranking_file):
        ranking = pd.read_csv(ranking_file)
        ranking_sorted = ranking.sort_values(by=["Créditos", "Pontos Ganhos"], ascending=[False, False])
        st.dataframe(ranking_sorted[["Nick", "Tentativas", "Créditos", "Pontos Ganhos"]])

# Rodapé
st.markdown(
    """
    <div style='text-align: center; padding-top: 2rem; font-size: 14px; color: #00FFFF;'>
        Desenvolvido por <b>Jones Donizette</b>
    </div>
    """,
    unsafe_allow_html=True
)

