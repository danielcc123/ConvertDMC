
import streamlit as st
from PIL import Image
import os
import io
from PyPDF2 import PdfReader, PdfWriter
from pdf2image import convert_from_bytes

st.set_page_config(page_title="ConvertDMC", layout="centered")
st.title("🌀 ConvertDMC - Convertidor de Imágenes y PDFs")

st.markdown("""
**Funciones disponibles:**
- JPG a TIF
- TIF a PDF
- TIF a JPG
- PDF a TIF (página por página)
- Separar PDF (extrae cada página como PDF)
""")

option = st.selectbox("Selecciona una operación:", [
    "JPG a TIF",
    "TIF a PDF",
    "TIF a JPG",
    "PDF a TIF",
    "Separar PDF"
])

if option == "JPG a TIF":
    jpg = st.file_uploader("Sube una imagen JPG", type=["jpg", "jpeg"])
    if jpg:
        image = Image.open(jpg)
        buf = io.BytesIO()
        image.save(buf, format="TIFF")
        st.download_button("📥 Descargar TIF", buf.getvalue(), file_name="convertido.tif")

elif option == "TIF a PDF":
    tif = st.file_uploader("Sube una imagen TIF", type=["tif", "tiff"])
    if tif:
        image = Image.open(tif).convert("RGB")
        buf = io.BytesIO()
        image.save(buf, format="PDF")
        st.download_button("📥 Descargar PDF", buf.getvalue(), file_name="convertido.pdf")

elif option == "TIF a JPG":
    tif = st.file_uploader("Sube una imagen TIF", type=["tif", "tiff"])
    if tif:
        image = Image.open(tif).convert("RGB")
        buf = io.BytesIO()
        image.save(buf, format="JPEG")
        st.download_button("📥 Descargar JPG", buf.getvalue(), file_name="convertido.jpg")

elif option == "PDF a TIF":
    pdf = st.file_uploader("Sube tu archivo PDF", type=["pdf"])
    if pdf:
        images = convert_from_bytes(pdf.read(), dpi=200, fmt='tiff')
        for i, img in enumerate(images):
            buf = io.BytesIO()
            img.save(buf, format="TIFF")
            st.download_button(f"📥 Página {i+1} en TIF", buf.getvalue(), file_name=f"pagina_{i+1}.tif")

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

st.markdown("---")
st.markdown("🌐 Desarrollado por Daniel Chumbipuma - **ConvertDMC**")
st.markdown("---")
st.markdown("☕ If this tool helped you, you can support me here:")

st.markdown("---")
st.markdown("☕ If this tool helped you, you can support me here:")

st.markdown("---")
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

