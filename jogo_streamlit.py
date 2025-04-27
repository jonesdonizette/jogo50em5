import streamlit as st
import random

# Configurar a página
st.set_page_config(page_title="50 em 5", page_icon="🎯")

# Personalizar a aparência com sua identidade visual
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
    footer {
        visibility: hidden;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# 🎵 Funções para tocar trilha e efeitos
def tocar_trilha():
    st.markdown(
        """
        <audio id="trilha" autoplay loop>
            <source src="https://www.soundhelix.com/examples/mp3/SoundHelix-Song-1.mp3" type="audio/mpeg">
        </audio>
        """,
        unsafe_allow_html=True
    )

def tocar_efeito(link_som):
    st.markdown(
        f"""
        <audio autoplay>
            <source src="{link_som}" type="audio/mpeg">
        </audio>
        """,
        unsafe_allow_html=True
    )

# Links dos efeitos
LINK_VITORIA = "https://assets.mixkit.co/sfx/preview/mixkit-achievement-bell-600.mp3"
LINK_ERRO = "https://assets.mixkit.co/sfx/preview/mixkit-arcade-retro-game-over-213.mp3"
LINK_GAMEOVER = "https://assets.mixkit.co/sfx/preview/mixkit-player-losing-or-failing-2042.mp3"

# 🏆 Título atualizado
st.title("🎯 50 em 5")
st.write("Tente adivinhar o número secreto entre 1 e 50 em apenas 5 tentativas!")

# 🔄 Inicializar variáveis
if "numero_secreto" not in st.session_state:
    st.session_state.numero_secreto = random.randint(1, 50)

if "tentativas" not in st.session_state:
    st.session_state.tentativas = 0

if "limite" not in st.session_state:
    st.session_state.limite = 5

if "som_liberado" not in st.session_state:
    st.session_state.som_liberado = False

# 🔊 Botão para liberar a música
if not st.session_state.som_liberado:
    if st.button("🔊 Ativar Música"):
        tocar_trilha()
        st.session_state.som_liberado = True
else:
    tocar_trilha()

# 🎮 Palpite
palpite = st.number_input("Digite seu palpite:", min_value=1, max_value=50, step=1)
enviar = st.button("🎯 Enviar Palpite")

# 🎯 Lógica principal
if enviar:
    st.session_state.tentativas += 1

    if palpite == st.session_state.numero_secreto:
        tocar_efeito(LINK_VITORIA)
        st.success(f"🎉 Parabéns! Você acertou em {st.session_state.tentativas} tentativas!")
        st.balloons()
        for key in ["numero_secreto", "tentativas", "limite", "som_liberado"]:
            if key in st.session_state:
                del st.session_state[key]
    elif st.session_state.tentativas >= st.session_state.limite:
        tocar_efeito(LINK_GAMEOVER)
        st.error(f"💀 Game Over! O número secreto era {st.session_state.numero_secreto}.")
        for key in ["numero_secreto", "tentativas", "limite", "som_liberado"]:
            if key in st.session_state:
                del st.session_state[key]
    else:
        tocar_efeito(LINK_ERRO)
        if palpite < st.session_state.numero_secreto:
            st.warning("📈 O número secreto é MAIOR que seu palpite.")
        else:
            st.warning("📉 O número secreto é MENOR que seu palpite.")

# Mostrar tentativas restantes
if "limite" in st.session_state:
    st.info(f"🔄 Tentativas restantes: {st.session_state.limite - st.session_state.tentativas}")

# ✍️ Assinatura no rodapé
st.markdown(
    """
    <div style='text-align: center; padding-top: 2rem; font-size: 14px; color: #00FFFF;'>
        Desenvolvido por <b>Jones Donizette</b>
    </div>
    """,
    unsafe_allow_html=True
)
