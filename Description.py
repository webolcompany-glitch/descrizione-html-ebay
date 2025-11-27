import streamlit as st
import pandas as pd
from io import BytesIO

# -----------------------------
# Funzione per generare HTML
# -----------------------------
def generate_html(titolo, descrizione, immagine):
    return f"""<div>
<article>
<div class="container">
    <div class="row">
        <div class="col-md-12 listing-info">

            <!-- DESCRIZIONE SOPRA -->
            <div class="description-box" style="border: 1px solid #ccc; padding: 15px; border-radius: 5px; background-color: #f9f9f9; margin-bottom: 20px;">
                <p>{descrizione}</p>
            </div>

            <!-- IMMAGINE SOTTO ADATTATA -->
            <p style="text-align: center;">
                <img src="{immagine}" 
                     alt="Immagine prodotto" 
                     style="width: 100%; max-width: 800px; height: auto; border: 1px solid #ddd; border-radius: 5px;">
            </p>

        </div>
    </div>
</div>
</article>
</div>
"""

# -----------------------------
# App Streamlit
# -----------------------------
st.title("📝 Generatore Descrizioni HTML per eBay")
st.write("Carica un file Excel con i prodotti e genera automaticamente descrizioni HTML pronte per eBay.")

uploaded_file = st.file_uploader("📤 Carica file Excel", type=["xlsx"])

if uploaded_file:
    try:
        df = pd.read_excel(uploaded_file)

        required_columns = ["Title", "Description", "Item photo URL"]
        if not all(col in df.columns for col in required_columns):
            st.error(f"❌ Il file Excel deve contenere le colonne: {', '.join(required_columns)}")
        else:
            # Genera colonna HTML
            df["DescrizioneHTML"] = df.apply(lambda row: generate_html(
                titolo=row["Title"],
                descrizione=row["Description"],
                immagine=str(row["Item photo URL"]).replace(',', '.')
            ), axis=1)

            # Esporta Excel con HTML
            output = BytesIO()
            df.to_excel(output, index=False, engine='openpyxl')
            output.seek(0)

            st.success("✅ File generato con successo!")

            st.download_button(
                label="📥 Scarica file Excel con HTML",
                data=output,
                file_name="descrizioni_ebay.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )

            st.markdown("---")
            st.subheader("📌 Anteprima descrizione del primo prodotto")
            st.components.v1.html(df["DescrizioneHTML"].iloc[0], height=600, scrolling=True)

    except Exception as e:
        st.error(f"❌ Errore nella lettura del file: {e}")
else:
    st.info("Attendi il caricamento del file Excel.")