import streamlit as st
import instaloader
import re
import os

# 1. Configuração do Ícone e Título na aba do Navegador
st.set_page_config(
    page_title="InstaDownloader Pro",
    page_icon="📥", # Você pode usar um emoji ou o link de uma imagem
    layout="centered"
)

st.title("📥 Instagram Downloader Pro")
st.markdown("---")

# 2. Inicialização do Motor de Download
# Usamos o 'cache_resource' para não recriar o motor a cada clique do usuário
@st.cache_resource
def get_loader():
    return instaloader.Instaloader(
        download_pictures=False,
        download_video_thumbnails=False,
        save_metadata=False,
        post_metadata_txt_pattern=""
    )

L = get_loader()

# 3. Interface do Usuário
url = st.text_input("Cole o link do Reels ou Vídeo aqui:", placeholder="https://www.instagram.com/reels/...")

if st.button("GERAR DOWNLOAD", use_container_width=True):
    if url:
        try:
            # Limpeza do link (Regex) para evitar erro de metadados
            match = re.search(r'/(?:p|reels|reel)/([A-Za-z0-9_-]+)', url)
            if not match:
                st.error("Link inválido! Certifique-se de que é um post público.")
            else:
                shortcode = match.group(1)
                
                with st.spinner(f"Processando vídeo {shortcode}..."):
                    post = instaloader.Post.from_shortcode(L.context, shortcode)
                    
                    if post.is_video:
                        st.video(post.video_url)
                        st.success("Vídeo pronto!")
                        st.info("👆 Clique nos três pontinhos no vídeo (ou segure pressionado no celular) para 'Fazer download'.")
                    else:
                        st.warning("Este link parece ser de uma foto. O sistema está configurado para vídeos.")
                        
        except Exception as e:
            st.error(f"O Instagram bloqueou o acesso temporariamente ou o post é privado.")
            st.caption(f"Erro técnico: {e}")
    else:
        st.warning("Insira um link válido primeiro.")

st.markdown("---")
st.caption("Acesse pelo celular e adicione à tela de início para usar como um App!")