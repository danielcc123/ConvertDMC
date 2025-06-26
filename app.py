import streamlit as st
from PIL import Image
import io
from PyPDF2 import PdfReader, PdfWriter
import fitz  # PyMuPDF

st.set_page_config(page_title="ConvertDMC", layout="centered")
st.title("🌀 ConvertDMC - Convertidor de Imágenes y PDFs")

st.markdown("""
**Funciones disponibles:**
- JPG a TIF
- TIF a PDF (incluye multipágina)
- TIF a JPG
- PDF a TIF (multipágina)
- Separar PDF (extrae cada página como archivo PDF)
""")

option = st.selectbox("Selecciona una operación:", [
    "JPG a TIF",
    "TIF a PDF",
    "TIF a JPG",
    "PDF a TIF",
    "Separar PDF"
])

# JPG a TIF
if option == "JPG a TIF":
    jpg = st.file_uploader("Sube una imagen JPG", type=["jpg", "jpeg"])
    if jpg:
        image = Image.open(jpg)
        buf = io.BytesIO()
        image.save(buf, format="TIFF")
        st.download_button("📥 Descargar TIF", buf.getvalue(), file_name="convertido.tif")

# TIF a PDF (multipágina si aplica)
elif option == "TIF a PDF":
    tif = st.file_uploader("Sube una imagen TIF (simple o multipágina)", type=["tif", "tiff"])
    if tif:
        image = Image.open(tif)
        images = []

        try:
            while True:
                images.append(image.copy().convert("RGB"))
                image.seek(image.tell() + 1)
        except EOFError:
            pass

        buf = io.BytesIO()
        images[0].save(buf, format="PDF", save_all=True, append_images=images[1:])
        st.download_button("📥 Descargar PDF multipágina", buf.getvalue(), file_name="convertido.pdf")

# TIF a JPG
elif option == "TIF a JPG":
    tif = st.file_uploader("Sube una imagen TIF", type=["tif", "tiff"])
    if tif:
        image = Image.open(tif).convert("RGB")
        buf = io.BytesIO()
        image.save(buf, format="JPEG")
        st.download_button("📥 Descargar JPG", buf.getvalue(), file_name="convertido.jpg")

# PDF a TIF (multipágina)
elif option == "PDF a TIF":
    pdf = st.file_uploader("Sube tu archivo PDF", type=["pdf"])
    if pdf:
        doc = fitz.open(stream=pdf.read(), filetype="pdf")
        images = []

        for page in doc:
            pix = page.get_pixmap(dpi=200)
            img = Image.open(io.BytesIO(pix.tobytes("png")))
            images.append(img.convert("RGB"))

        buf = io.BytesIO()
        images[0].save(buf, format="TIFF", save_all=True, append_images=images[1:])
        st.download_button("📥 Descargar TIF multipágina", buf.getvalue(), file_name="convertido.tif")

# Separar PDF por páginas
elif option == "Separar PDF":
    pdf = st.file_uploader("Sube tu archivo PDF", type=["pdf"])
    if pdf:
        reader = PdfReader(pdf)
        for i, page in enumerate(reader.pages):
            writer = PdfWriter()
            writer.add_page(page)
            buf = io.BytesIO()
            writer.write(buf)
            st.download_button(f"📥 Página {i+1} en PDF", buf.getvalue(), file_name=f"pagina_{i+1}.pdf")

# Pie de página y botón Ko-fi
st.markdown("---")
st.markdown("🌐 Desarrollado por Daniel Chumbipuma - **ConvertDMC**")
st.markdown("☕ ¿Te ayudó esta herramienta? Apóyame con un café:")

st.markdown("""
<div align="center">
  <a href="https://ko-fi.com/danielmarcoschumbipumacabrejos" target="_blank">
    <img src="https://storage.ko-fi.com/cdn/kofi_button.png" 
         alt="Invítame un café en ko-fi.com" 
         height="45" style="border:0px;" />
  </a>
</div>
""", unsafe_allow_html=True)

