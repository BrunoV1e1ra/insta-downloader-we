import streamlit as st
import instaloader
import re

# Configuração da página
st.set_page_config(page_title="InstaDownloader Pro", page_icon="📥")

st.title("📥 Instagram Downloader Pro")

# Função para criar o motor de download com um "disfarce" de navegador
@st.cache_resource
def get_loader():
    L = instaloader.Instaloader(
        download_pictures=False,
        download_videos=True,
        download_video_thumbnails=False,
        save_metadata=False,
        post_metadata_txt_pattern=""
    )
    # Define um User-Agent para parecer um navegador comum
    L.context._session.headers.update({
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
    })
    return L

L = get_loader()

url = st.text_input("Cole o link aqui:", placeholder="https://www.instagram.com/reel/...")

if st.button("GERAR DOWNLOAD", use_container_width=True):
    if url:
        try:
            # Limpa o link para pegar apenas o código do vídeo
            match = re.search(r'/(?:p|reels|reel)/([A-Za-z0-9_-]+)', url)
            if not match:
                st.error("Link inválido ou de perfil privado.")
            else:
                shortcode = match.group(1)
                with st.spinner("Conectando ao Instagram..."):
                    post = instaloader.Post.from_shortcode(L.context, shortcode)
                    
                    if post.is_video:
                        st.video(post.video_url)
                        st.success("Pronto! No celular, segure no vídeo acima para salvar.")
                    else:
                        st.warning("Este link não aponta para um vídeo.")
                        
        except Exception as e:
            if "401" in str(e) or "429" in str(e):
                st.error("⚠️ O Instagram bloqueou o servidor temporariamente por excesso de acessos.")
                st.info("Tente novamente em alguns minutos ou use um link de outro vídeo público.")
            else:
                st.error(f"Erro inesperado: {e}")
    else:
        st.warning("Insira um link.")
