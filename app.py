import streamlit as st
import yfinance as yf
import pandas as pd
from datetime import datetime
import plotly.graph_objects as go
import os
import tempfile

# Set halaman dan layout sebagai perintah pertama
st.set_page_config(page_title="Dashboard Saham", layout="wide")

# Fungsi untuk memuat file CSS
def load_css(file_name):
    with open(file_name) as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

# Muat file CSS
load_css("style.css")

# Daftar contoh kode saham yang umum digunakan
saham_list = ["AALI.JK", "ABMM.JK", "ACES.JK", "ADHI.JK", "ADRO.JK", "AGRO.JK", "AISA.JK", "AKRA.JK", "AMFG.JK", "AMRT.JK", "ANTM.JK", 
"APLN.JK", "ARNA.JK", "ARTO.JK", "ASGR.JK", "ASII.JK", "ASRI.JK", "ASSA.JK", "AUTO.JK", "BACA.JK", "BALI.JK", "BBCA.JK",
"BBHI.JK", "BBKP.JK", "BBNI.JK", "BBRI.JK", "BBTN.JK", "BBYB.JK", "BCAP.JK", "BDMN.JK", "BEST.JK", "BFIN.JK", "BINA.JK",
"BIRD.JK", "BISI.JK", "BJBR.JK", "BJTM.JK", "BMRI.JK", "BMTR.JK", "BNGA.JK", "BNII.JK", "BRMS.JK", "BRPT.JK", "BSDE.JK",
"BSIM.JK", "BTPN.JK", "BUDI.JK", "BUMI.JK", "BVIC.JK", "BWPT.JK", "BYAN.JK", "CASS.JK", "CFIN.JK", "CMNP.JK", "CPIN.JK",
"CTRA.JK", "DEWA.JK", "DILD.JK", "DLTA.JK", "DMAS.JK", "DOID.JK", "DSNG.JK", "DSSA.JK", "ELSA.JK", "EMTK.JK", "ENRG.JK",
"ERAA.JK", "ESSA.JK", "EXCL.JK", "GEMS.JK", "GGRM.JK", "GJTL.JK", "GWSA.JK", "HEXA.JK", "HITS.JK", "HRUM.JK", "ICBP.JK",
"IMAS.JK", "IMPC.JK", "INCO.JK", "INDF.JK", "INDY.JK", "INKP.JK", "INPC.JK", "INTP.JK", "ISAT.JK", "ISSP.JK", "ITMG.JK",
"JKON.JK", "JPFA.JK", "JSMR.JK", "JTPE.JK", "KBLI.JK", "KIJA.JK", "KKGI.JK", "KLBF.JK", "LPCK.JK", "LPKR.JK", "LPPF.JK",
"LSIP.JK", "LTLS.JK", "MAIN.JK", "MAPI.JK", "MAYA.JK", "MBSS.JK", "MCOR.JK", "MDKA.JK", "MDLN.JK", "MEDC.JK", "MEGA.JK",
"MFIN.JK", "MIDI.JK", "MIKA.JK", "MLBI.JK", "MLIA.JK", "MLPL.JK", "MMLP.JK", "MNCN.JK", "MPMX.JK", "MPPA.JK", "MTDL.JK",
"MTLA.JK", "MYOH.JK", "MYOR.JK", "NISP.JK", "PANR.JK", "PANS.JK", "PGAS.JK", "PNBN.JK", "PNIN.JK", "PNLF.JK", "PTBA.JK",
"PTPP.JK", "PTRO.JK", "PUDP.JK", "PWON.JK", "RAJA.JK", "RALS.JK", "SAME.JK", "SCMA.JK", "SDRA.JK", "SGRO.JK", "SIDO.JK",
"SILO.JK", "SIMP.JK", "SMBR.JK", "SMDR.JK", "SMGR.JK", "SMMA.JK", "SMRA.JK", "SMSM.JK", "SOCI.JK", "SRAJ.JK", "SRTG.JK",
"SSIA.JK", "SSMS.JK", "TBIG.JK", "TBLA.JK", "TINS.JK", "TKIM.JK", "TLKM.JK", "TMAS.JK", "TOBA.JK", "TOTL.JK", "TOWR.JK",
"TPMA.JK", "TRIM.JK", "TSPC.JK", "ULTJ.JK", "UNIC.JK", "UNTR.JK", "UNVR.JK", "WIIM.JK", "WINS.JK", "WTON.JK", "SHIP.JK",
"PRDA.JK", "BRIS.JK", "CARS.JK", "CLEO.JK", "WOOD.JK", "HRTA.JK", "HOKI.JK", "MARK.JK", "MCAS.JK", "WEGE.JK", "PSSI.JK",
"MORA.JK", "PBID.JK", "BTPS.JK", "SPTO.JK", "HEAL.JK", "TUGU.JK", "MSIN.JK", "MAPA.JK", "IPCC.JK", "FILM.JK", "GOOD.JK",
"BOLA.JK", "KEEN.JK", "TEBE.JK", "PSGO.JK", "UCID.JK", "SAMF.JK", "VICI.JK", "BANK.JK", "UNIQ.JK", "TAPG.JK", "BMHS.JK", 
"MCOL.JK", "RSGK.JK", "CMNT.JK", "MTEL.JK", "CMRY.JK", "RMKE.JK", "AVIA.JK", "DRMA.JK", "ADMR.JK", "STAA.JK", "MTMH.JK",
"TRGU.JK", "AXIO.JK", "HATM.JK", "JARR.JK", "ELPI.JK", "CBUT.JK", "MKTR.JK", "OMED.JK", "BSBK.JK", "VTNY.JK", "SUNI.JK",
"PGEO.JK", "HILL.JK", "BDKR.JK", "CUAN.JK", "NCKL.JK", "RAAM.JK", "SMIL.JK", "AMMN.JK", "MAHA.JK", "CNMA.JK", "ERAL.JK",
"HUMI.JK", "BREN.JK", "MSTI.JK", "MSJA.JK", "ALII.JK", "GOLF.JK", "BLES.JK", "POWR.JK"]

# Judul Aplikasi dengan warna yang menarik
st.markdown("<h1 style='text-align: center; color: #1E90FF;'>Dashboard Saham Interaktif</h1>", unsafe_allow_html=True)

# Membuat kolom untuk input parameter di sidebar
st.sidebar.header("Parameter Saham")
# Menggunakan st.selectbox untuk memberikan opsi auto-complete dari daftar saham
symbol = st.sidebar.selectbox("Kode Saham", saham_list)
entry_price = st.sidebar.number_input("Harga Entry", value=0)
stop_loss = st.sidebar.number_input("Stop-Loss", value=0)
target_price = st.sidebar.number_input("Target Price", value=0)

# Gunakan slider untuk menyesuaikan data period
period = st.sidebar.select_slider("Pilih Periode Data", options=['5d', '1mo', '3mo', '6mo', '1y'], value='5d')
submit = st.sidebar.button("Tampilkan")

# Fungsi untuk menyimpan hasil realisasi ke CSV secara otomatis
def autosave_to_csv(dataframe):
    # Buat file di folder temporer untuk menghindari masalah perizinan
    temp_dir = tempfile.gettempdir()
    filename = os.path.join(temp_dir, "hasil_realisasi.csv")
    dataframe.to_csv(filename, index=False)
    return filename

# Informasi Saham di Sidebar
if symbol:
    st.sidebar.write("### Informasi Saham")
    try:
        stock_info = yf.Ticker(symbol)
        stock_details = stock_info.info

        # Menampilkan informasi saham di sidebar
        st.sidebar.write(f"**Nama Perusahaan:** {stock_details.get('longName', 'Tidak Diketahui')}")
        st.sidebar.write(f"**Sektor:** {stock_details.get('sector', 'Tidak Diketahui')}")
        st.sidebar.write(f"**Harga Sekarang:** {stock_details.get('currentPrice', 'Tidak Diketahui')}")
        st.sidebar.write(f"**Kapitalisasi Pasar:** {stock_details.get('marketCap', 'Tidak Diketahui')}")
    except Exception as e:
        st.sidebar.error(f"Tidak dapat mengambil informasi untuk kode saham {symbol}. Error: {e}")

# Membuat Dashboard dengan Tabs
if submit:
    tabs = st.tabs(["Overview", "Grafik", "Hasil Realisasi"])

    # Data Saham dari Yahoo Finance
    stock_data = yf.download(symbol, period=period, interval='1d')

    if stock_data.empty:
        st.error("Tidak ada data yang ditemukan. Periksa kode saham yang dimasukkan.")
    else:
        # **Tab 1: Overview**
        with tabs[0]:
            st.markdown("<h2 style='color: #1E90FF;'>Overview Saham</h2>", unsafe_allow_html=True)
            col1, col2, col3 = st.columns(3)

            # Tampilkan ringkasan data saham
            col1.metric("Harga Saat Ini", stock_data['Close'].iloc[-1])
            col3.metric("Volume", stock_data['Volume'].iloc[-1])

        # **Tab 2: Grafik**
        with tabs[1]:
            st.markdown("<h2 style='color: #1E90FF;'>Grafik Candlestick</h2>", unsafe_allow_html=True)

            # Grafik Candlestick dengan warna yang lebih menarik
            fig = go.Figure(data=[go.Candlestick(
                x=stock_data.index,
                open=stock_data['Open'],
                high=stock_data['High'],
                low=stock_data['Low'],
                close=stock_data['Close'],
                increasing_line_color='green', decreasing_line_color='red'
            )])

            # Layout untuk grafik
            fig.update_layout(
                title=f'Grafik Saham {symbol}',
                yaxis_title='Harga',
                xaxis_title='Tanggal',
                xaxis_rangeslider_visible=False,
                height=600,
                template="plotly_dark"
            )
            st.plotly_chart(fig, use_container_width=True)

        # **Tab 3: Hasil Realisasi**
        with tabs[2]:
            st.markdown("<h2 style='color: #1E90FF;'>Hasil Realisasi Prediksi</h2>", unsafe_allow_html=True)

            # Menyiapkan hasil prediksi
            realizations = []
            for index, row in stock_data.iterrows():
                high = row['High']
                low = row['Low']
                date = index.date()
                current_price = row['Close']
                price_change_percent = ((current_price - entry_price) / entry_price) * 100 if entry_price != 0 else 0

                result = "❗Belum mencapai target atau stop-loss"
                if low < stop_loss:
                    result = f"⚠️ Stop-loss tercapai dengan harga {low}"
                if high >= target_price:
                    result = f"✅ Target tercapai dengan harga {high}"

                realizations.append({
                    "Tanggal": date,
                    "Hasil": result,
                    "Harga Entry": entry_price,
                    "Harga Sekarang": current_price,
                    "Persentase Perubahan": f"{price_change_percent:.2f}%"
                })

            # Konversi hasil prediksi ke DataFrame
            result_df = pd.DataFrame(realizations)

            # Autosave hasil realisasi ke CSV
            csv_filename = autosave_to_csv(result_df)

            # Tampilkan tabel hasil realisasi
            st.table(result_df)

            # Tambahkan fitur download hasil prediksi dalam bentuk CSV
            csv_data = result_df.to_csv(index=False)
            st.download_button(
                label="Download Hasil Realisasi CSV",
                data=csv_data,
                file_name='hasil_realisasi.csv',  # Nama file konsisten, tidak membuat dobel file
                mime='text/csv'
            )

# Footer dengan informasi
st.markdown("<br><hr><div style='text-align: center;'>© 2024 Dashboard Saham Interaktif</div>", unsafe_allow_html=True)
