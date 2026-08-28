import streamlit as st
import json
import urllib.parse
from google import genai

st.set_page_config(
    page_title="Kişisel Stil, AI Danışman & Bakım Asistanı",
    page_icon="👔",
    layout="wide"
)

# Profil Yükle
@st.cache_data
def profil_yukle():
    with open("profil.json", "r", encoding="utf-8") as f:
        return json.load(f)

profil = profil_yukle()

# Beden Motoru
def beden_tavsiyesi_uret(parca_adi):
    adi = parca_adi.lower()
    if any(k in adi for k in ["bot", "sneaker", "loafer", "ayakkabı", "terlik", "espadril"]):
        return {"beden": "44 - 44.5 Numara (EUR)", "detay": "Ayak: 28.5 cm (11.5 cm Taraklı). Dar/sert kalıplarda 44.5 veya 45 seçin."}
    elif any(k in adi for k in ["pantolon", "chino", "jean", "kadife", "şort", "eşofman"]):
        return {"beden": "34 / 32 (veya L Beden)", "detay": "Bel: 98 cm | Uyluk: 61 cm. Kasılmayı önlemek için 'Tapered / Düz Kesim' veya kompresyonlu seçin."}
    elif any(k in adi for k in ["boxer", "içlik", "fanila", "çorap", "krem"]):
        return {"beden": "L Beden / Standart", "detay": "Sürtünmeyi önleyen uzun paçalı veya dikişsiz modeller."}
    elif "kemer" in adi:
        return {"beden": "95 - 100 cm", "detay": "98 cm pantolon beli için ideal orta delik boyudur."}
    elif any(k in adi for k in ["gömlek", "tişört", "polo", "kazak", "sweatshirt", "ceket", "kaban", "parka", "hırka", "yelek", "blazer", "overshirt", "atlet"]):
        return {"beden": "L (Regular) / XL (Slim Fit)", "detay": "Göğüs: 105 cm | Omuz: 54 cm | Biceps: 40-45 cm. Sporcu göğsünü sıkmaması için L beden."}
    return None

# Link Butonları
def link_butonlari(arama_terimi, tip="giyim"):
    q = urllib.parse.quote(arama_terimi)
    g_url = f"https://www.google.com/search?tbm=shop&q={q}"
    a_url = f"https://www.akakce.com/arama/?q={q}"
    c_url = f"https://www.cimri.com/arama?q={q}"
    
    b1, b2, b3 = st.columns(3)
    with b1:
        st.link_button("🛍️ Google", g_url, use_container_width=True)
    with b2:
        st.link_button("🔍 Akakçe", a_url, use_container_width=True)
    with b3:
        st.link_button("🏷️ Cimri", c_url, use_container_width=True)

# Kart Çizici
def urun_kartlari_ciz(liste, kategori_tipi="giyim"):
    cols = st.columns(2)
    for idx, item in enumerate(liste):
        col = cols[idx % 2]
        with col:
            with st.container(border=True):
                parca_adi = item.get("parca") or item.get("urun") or item.get("parfum")
                alt_bilgi = item.get("renk") or item.get("kategori") or ""
                arama_terimi = item.get("arama") or item.get("arama_terimi")
                
                st.subheader(parca_adi)
                if alt_bilgi:
                    st.caption(f"**Önerilen Renk / Kategori:** {alt_bilgi}")
                
                if kategori_tipi == "giyim":
                    b = beden_tavsiyesi_uret(parca_adi)
                    if b:
                        st.success(f"🎯 **Önerilen Beden:** {b['beden']}")
                        st.info(f"💡 **Kalıp Notu:** {b['detay']}")
                
                link_butonlari(arama_terimi, kategori_tipi)

# AI İstemci Yardımcısı
def ai_yanit_uret(prompt_metni, sistem_talimati):
    api_key = st.secrets.get("GEMINI_API_KEY")
    if not api_key:
        return "⚠️ Lütfen Streamlit Secrets paneline `GEMINI_API_KEY` ekleyin."
    
    client = genai.Client(api_key=api_key)
    modeller = ["gemini-3.6-flash", "gemini-3.6-flash-lite", "gemini-1.5-flash"]
    
    for m in modeller:
        try:
            res = client.models.generate_content(
                model=m,
                contents=prompt_metni,
                config=genai.types.GenerateContentConfig(
                    system_instruction=sistem_talimati,
                    temperature=0.7
                )
            )
            return res.text
        except Exception:
            continue
    return "Google sunucularında anlık yoğunluk var. Lütfen 10 saniye sonra tekrar deneyin."

# Sistem Promptu
SISTEM_PROMPTU = f"""
Sen kullanıcının kişisel stilisti, imaj danışmanı ve kozmetik içerik denetçisisin.
KULLANICI:
- Yaş/Meslek: 38 yaşında erkek İngilizce Öğretmeni (Smart-Casual / Old Money tarzı).
- Fizik: 180 cm, 86 kg, Atletik V-Vücut (Omuz: 54 cm, Göğüs: 105 cm, Bel: 92 cm, Biceps: 40-45 cm, Uyluk: 61 cm bacak kası, Ayak: 28.5 cm taraklı).
- Palet: Soft Autumn (Adaçayı, zeytin yeşili/haki, karamel, taba, kum beji, taş rengi, ekru, vizon, çikolata kahve, mat lacivert).
- Kaçınılacaklar: Zifiri siyah (spor hariç), çiğ parlak beyaz, parlak neonlar, aşırı dar tayt gibi pantolonlar.
- Spor & Sağlık: Haftada 4 gün fitness (Pzt, Sal, Per, Cum), iç bacak sürtünme hassasiyeti (Aptonia krem kullanıyor).
- Bakım: Yağlı/pürüzlü cilt, kaz ayakları, seyrek tepe saç (hacim pudrası + fiber).
- Gardırop: {json.dumps(profil.get('gardrop_arama_listesi', {}), ensure_ascii=False)}

Üslup: Net, profesyonel, gereksiz laf kalabalığı yapmayan, doğrudan çözüme odaklanan karizmatik bir uzman.
"""

# --- YAN PANEL ---
with st.sidebar:
    st.header("👤 Stil & Beden Profili")
    k = profil.get("kullanici_profili", {})
    st.markdown(f"""
    - **Meslek / Yaş:** {k.get('meslek')} ({k.get('yas')})
    - **Stil:** {k.get('stil')}
    - **Renk Paleti:** {k.get('renk_paleti')}
    - **Fizik:** {k.get('boy_cm')} cm / {k.get('kilo_kg')} kg ({k.get('fizik_tipi')})
    """)
    st.divider()
    st.subheader("📏 Net Vücut Ölçüleri")
    ust = profil["vucut_olculeri"]["ust_giyim"]
    alt = profil["vucut_olculeri"]["alt_giyim"]
    ayak = profil["vucut_olculeri"]["ayak_ve_el"]
    st.markdown(f"""
    - **Göğüs / Omuz:** {ust['gogus_cevresi_cm']} cm / {ust['omuz_genisligi_cm']} cm
    - **Kol / Biceps:** {ust['kol_boyu_cm']} cm / 40-45 cm
    - **Bel / Uyluk:** {alt['pantolon_bel_cm']} cm / {alt['ust_bacak_uyluk_cm']} cm
    - **Ayak:** {ayak['ayak_uzunlugu_cm']} cm (Taraklı Kalıp)
    """)

# --- 4 ANA SEKME ---
st.title("👔 Kişisel Stil, AI Danışman & Bakım Asistanı")

tab_ai, tab_kombin, tab_gardrop, tab_bakim = st.tabs([
    "🤖 Canlı AI Stilist & Akıllı Araçlar",
    "🎲 Akıllı Kombin & 7 Günlük Plan",
    "🛍️ Kapsül Gardırop & Alışveriş",
    "🧴 Kişisel Bakım & Duş Takvimi"
])

# ==================== 1. CANLI AI STİLİST & AKILLI ARAÇLAR ====================
with tab_ai:
    st.header("🤖 Canlı AI Stilist & Akıllı Araçlar")
    
    # 3 Hızlı Akıllı Modül
    exp1, exp2, exp3 = st.columns(3)
    
    with exp1:
        with st.popover("🛍️ Bunu Almalı mıyım?", use_container_width=True):
            st.markdown("##### 🔍 Hızlı Alışveriş Onaylayıcısı")
            alincak_urun = st.text_input("Ürün adı, kumaşı veya link açıklaması:", placeholder="Örn: %70 Pamuk %30 Keten Haki Safari Ceket")
            if st.button("Bu Parçayı Denetle", key="btn_onay"):
                if alincak_urun:
                    with st.spinner("Analiz ediliyor..."):
                        p = f"Kullanıcı şu ürünü satın almayı düşünüyor: '{alincak_urun}'. Soft Autumn paletine, atletik V-vücut ölçülerine (105 cm göğüs, 54 cm omuz, 61 cm bacak) ve gardırobundaki parçalarla uyumuna göre puanla (10 üzerinden) ve alıp almamasını 3 maddede net gerekçelendir."
                        st.markdown(ai_yanit_uret(p, SISTEM_PROMPTU))
    
    with exp2:
        with st.popover("📊 Gardırop Eksik Analizi", use_container_width=True):
            st.markdown("##### 🧩 Kapsül Boşluk Taraması")
            st.caption("Yapay zeka gardırobunuzdaki eksik parçaları tespit eder.")
            if st.button("Dolabımı Tara & Eksikleri Listele", key="btn_eksik"):
                with st.spinner("Gardırop taranıyor..."):
                    p = "Mevcut gardırop listesini incele. 4 mevsim okul, sosyal yaşam ve spor dengesinde kombin çeşitliliğini en çok artıracak eksik 3 stratejik parçayı ve nedenlerini listele."
                    st.markdown(ai_yanit_uret(p, SISTEM_PROMPTU))
                    
    with exp3:
        with st.popover("🚨 Cilt & Rutin Kurtarıcı", use_container_width=True):
            st.markdown("##### 🩹 Anlık Cilt Kurtarma")
            durum = st.selectbox("Anlık durumunuzu seçin:", [
                "Tıraş sonrası yanma ve kızarıklık var",
                "Hava çok kuru, cildim gerildi ve soyuluyor",
                "Sporda iç bacakta sürtünme tahrişi oldu",
                "Yüzümde aniden parlama ve gözenek tıkanması oldu"
            ])
            if st.button("Bu Geceki Rutini Güncelle", key="btn_kurtar"):
                with st.spinner("Reçete hazırlanıyor..."):
                    p = f"Kullanıcı şu anlık cilt problemini bildirdi: '{durum}'. Bu geceki Retinol / Asit takvimini nasıl revize etmeli? Hangi ürünleri sürüp hangilerini sürmemeli? 3 adımlı acil protokol ver."
                    st.markdown(ai_yanit_uret(p, SISTEM_PROMPTU))

    st.divider()
    st.subheader("💬 Stilistinizle Sohbet Edin")
    
    if "chat_messages" not in st.session_state:
        st.session_state.chat_messages = [
            {"role": "assistant", "content": "Merhaba! Ben kişisel stilistiniz ve bakım denetçinizim. Yarınki ders kombinlerinizi planlayabilir, bir kıyafetin kumaş kalitesini analiz edebilir veya spor salonu/cilt bakım sorularınızı yanıtlayabilirim."}
        ]
        
    chat_box = st.container(height=380)
    with chat_box:
        for msg in st.session_state.chat_messages:
            with st.chat_message(msg["role"]):
                st.markdown(msg["content"])
                
    user_input = st.chat_input("Bir soru sorun, hava durumu belirtin veya ürün içeriği yapıştırın...")
    if user_input:
        st.session_state.chat_messages.append({"role": "user", "content": user_input})
        with chat_box:
            with st.chat_message("user"):
                st.markdown(user_input)
            with st.chat_message("assistant"):
                with st.spinner("Düşünüyor..."):
                    cevap = ai_yanit_uret(user_input, SISTEM_PROMPTU)
                    st.markdown(cevap)
                    st.session_state.chat_messages.append({"role": "assistant", "content": cevap})

# ==================== 2. DİNAMİK KOMBİN & 7 GÜNLÜK PLAN ====================
with tab_kombin:
    st.header("🎲 Akıllı Kombin & 7 Günlük Yaşam Motoru")
    
    col_k1, col_k2 = st.columns(2)
    with col_k1:
        sec_mevsim = st.selectbox("📅 Mevsim Seçin:", ["Sonbahar", "Kış", "İlkbahar", "Yaz"])
    with col_k2:
        sec_ortam = st.selectbox("📍 Ortam Seçin:", [
            "Sınıf & Kurul (Akademik Smart-Casual)",
            "Hafta Sonu & Kafe (Relaxed Karizma)",
            "Akşam Yemeği & Özel Davet (Zarif)",
            "🏋️ Spor Salonu & Antrenman",
            "Pazar Dinlenme & Yürüyüş"
        ])
        
    if st.button("✨ Bu Senaryo İçin Canlı Kombin Üret", use_container_width=True, type="primary"):
        with st.spinner("Gardırop parçalarınızdan tam uyumlu kombin oluşturuluyor..."):
            prompt_kombin = f"Seçilen Mevsim: '{sec_mevsim}', Seçilen Ortam: '{sec_ortam}'. Kullanıcının gardırobundan tam uyumlu üst, alt, dış katman, ayakkabı, aksesuar ve akşam ev kıyafetini belirle. Beden ölçülerini ve kumaş dokularını belirterek karizmatik bir stil sırrı ile sun."
            st.markdown(ai_yanit_uret(prompt_kombin, SISTEM_PROMPTU))
            
    st.divider()
    st.subheader("📅 7 Günlük Eksiksiz Yaşam Planı (Dinamik AI)")
    sec_hafta_mevsim = st.selectbox("Haftalık plan hangi mevsim için hazırlansın?", ["Sonbahar", "Kış", "İlkbahar", "Yaz"], key="sb_hf")
    
    if st.button("🔄 7 Günlük Yeni Yaşam Planı Üret (Pzt - Pzr)", use_container_width=True):
        with st.spinner("7 günlük okul, spor ve sosyal yaşam planı oluşturuluyor..."):
            prompt_hafta = f"Seçilen Mevsim: '{sec_hafta_mevsim}'. Pazartesi, Salı, Perşembe, Cuma spor salonu günleri olduğunu da hesaba katarak; Pazartesi'den Pazar'a kadar hiçbir gün tekrar etmeyen 7 günlük gündüz kıyafeti, spor kıyafeti, ayakkabı ve akşam ev giyimi planı oluştur."
            st.markdown(ai_yanit_uret(prompt_hafta, SISTEM_PROMPTU))

# ==================== 3. KAPSÜL GARDIROP & ALIŞVERİŞ ====================
with tab_gardrop:
    st.header("🛍️ Kapsül Gardırop & Alışveriş Sepeti")
    st.caption("4 Mevsim Bağımsız Kapsül Koleksiyonları, Beden Uyarıları ve Arama Motorları.")
    
    kategori_secimi = st.selectbox(
        "Görüntülemek istediğiniz kapsül koleksiyonu seçin:",
        [
            "🍂 Sonbahar Kapsül Gardırobu",
            "❄️ Kış Kapsül Gardırobu",
            "🌸 İlkbahar Kapsül Gardırobu",
            "☀️ Yaz Kapsül Gardırobu",
            "🏋️ Spor Salonu & Antrenman",
            "🏃 Rahat Giyim & Yürüyüş",
            "🏠 Ev Giyimi (Loungewear)",
            "🩲 İç Giyim, Çorap & Kalkan",
            "🕶️ Aksesuarlar",
            "🪵 İmza Parfümler"
        ]
    )
    
    if "Sonbahar" in kategori_secimi:
        urun_kartlari_ciz(profil["gardrop_arama_listesi"]["sonbahar_kapsulu"], "giyim")
    elif "Kış" in kategori_secimi:
        urun_kartlari_ciz(profil["gardrop_arama_listesi"]["kis_kapsulu"], "giyim")
    elif "İlkbahar" in kategori_secimi:
        urun_kartlari_ciz(profil["gardrop_arama_listesi"]["ilkbahar_kapsulu"], "giyim")
    elif "Yaz" in kategori_secimi:
        urun_kartlari_ciz(profil["gardrop_arama_listesi"]["yaz_kapsulu"], "giyim")
    elif "Spor Salonu" in kategori_secimi:
        urun_kartlari_ciz(profil["gardrop_arama_listesi"]["spor_salonu_ve_antrenman"], "giyim")
    elif "Rahat Giyim" in kategori_secimi:
        urun_kartlari_ciz(profil["gardrop_arama_listesi"]["rahat_giyim_ve_spor"], "giyim")
    elif "Ev Giyimi" in kategori_secimi:
        urun_kartlari_ciz(profil["gardrop_arama_listesi"]["ev_giyimi"], "giyim")
    elif "İç Giyim" in kategori_secimi:
        urun_kartlari_ciz(profil["gardrop_arama_listesi"]["ic_giyim_ve_corap"], "giyim")
    elif "Aksesuarlar" in kategori_secimi:
        urun_kartlari_ciz(profil["aksesuar_listesi"], "giyim")
    elif "Parfümler" in kategori_secimi:
        st.markdown("##### ☀️ İlkbahar & Yaz")
        urun_kartlari_ciz(profil["parfum_onerileri"]["sicak_mevsimler_ilkbahar_yaz"], "parfum")
        st.divider()
        st.markdown("##### ❄️ Sonbahar & Kış")
        urun_kartlari_ciz(profil["parfum_onerileri"]["soguk_mevsimler_sonbahar_kis"], "parfum")

# ==================== 4. KİŞİSEL BAKIM & DUŞ TAKVİMİ ====================
with tab_bakim:
    st.header("🧴 Eksiksiz Kişisel Bakım & Duş Protokolü")
    
    st.markdown("""
    ### ☀️ Günlük Sabah Rutini (Her Gün Sabit — 4 Dakika)
    1. **Yüz Yıkama:** `CeraVe Blemish Control Cleanser (236 ml)` ile 40 saniye masajla yıkayıp tamponlayarak kurulayın[cite: 1].
    2. **Nemlendirme:** Hafif nemli cilde 1 pompa `CeraVe Nemlendirici Losyon` uygulayın[cite: 1].
    3. **Güneş Koruma:** Dışarı çıkmadan 15 dk önce iki parmak kuralıyla `La Roche-Posay Anthelios UVMune 400 Oil Control Fluid SPF 50+` sürün[cite: 1].
    4. **Kasık / Vücut:** Duş sonrası kurulanmış kasık bölgesine `Dalin Likit Pudra` (veya `Burt's Bees Baby Dusting Powder`) sürün; ardından uzun paçalı modal boxer giyin[cite: 1].
    5. **Saç:** Nemi alınmış saça 3 fıs `Nishman Sea Salt Spray` sıkıp fönle kurutun -> Kuru diplere `Nishman P1 Hacim Pudrası` döküp kökleri dikleştirin -> `Saç Fiberi` serpip sabitleyici sprey ile kilitleyin[cite: 1].
    """)
    
    st.divider()
    st.markdown("### 🗓️ Gün Gün Akşam ve Duş Protokolü (Pzt, Sal, Per, Cum Spor Düzeni)")
    
    pzt, sal, car, per, cum, cmt, pzr = st.tabs([
        "Pazartesi (Spor + Retinol)", 
        "Salı (Spor + Tonik)", 
        "Çarşamba (Dinlenme)", 
        "Perşembe (Spor + Retinol)", 
        "Cuma (Spor + Tonik)", 
        "Cumartesi (Dinlenme)", 
        "Pazar (Detoks)"
    ])
    
    with pzt:
        st.markdown("""
        - **🏋️ Spor Öncesi:** Bacak içine `Decathlon Aptonia Anti-Chafing Krem`[cite: 1].
        - **🚿 Duş:** `Sebamed Şampuan` + `Kabak Lifi` ve `Bioderma Gel` ile derin lifleme[cite: 1].
        - **🌙 Akşam Bakımı (Retinol):** Yüzü yıka -> Tam kurut -> 1 bezelye `Retinol %0.2` -> Kaz ayaklarına `Neutrogena Göz Kremi` -> 5 dk sonra `CeraVe Losyon` -> Kuru koltuk altına `Driclor Roll-on`[cite: 1].
        """)
    with sal:
        st.markdown("""
        - **🏋️ Spor Öncesi:** Bacak içine `Decathlon Aptonia Krem`[cite: 1].
        - **🚿 Duş:** Lifsiz hızlı 3 dk duş + `Bioderma Gel`[cite: 1].
        - **🌙 Akşam Bakımı:** Yüzü yıka -> `Neutrogena Göz Kremi` -> `CeraVe Losyon` -> Kasık ve koltuk altına pamukla `The Ordinary Glycolic Acid %7` tonik[cite: 1].
        """)
    with car:
        st.markdown("""
        - **🚿 Duş:** Lifsiz standart durulanma duşu[cite: 1].
        - **🌙 Akşam Bakımı:** Yüzü yıka -> Bolca `CeraVe Losyon` (Bariyer dinlendirme)[cite: 1].
        """)
    with per:
        st.markdown("""
        - **🏋️ Spor Öncesi:** Bacak içine `Decathlon Aptonia Krem`[cite: 1].
        - **🚿 Duş:** `Sebamed Şampuan` + `Kabak Lifi` ile derin arınma[cite: 1].
        - **🌙 Akşam Bakımı (Retinol):** Yüzü yıka -> Tam kurut -> 1 bezelye `Retinol %0.2` -> `Neutrogena Göz Kremi` -> `CeraVe Losyon` -> `Driclor Roll-on`[cite: 1].
        """)
    with cum:
        st.markdown("""
        - **🏋️ Spor Öncesi:** Bacak içine `Decathlon Aptonia Krem`[cite: 1].
        - **🚿 Duş:** Lifsiz hızlı ılık duş[cite: 1].
        - **🌙 Akşam Bakımı:** Yüzü yıka -> `Neutrogena Göz Kremi` -> `CeraVe Losyon` -> Kasık ve koltuk altına `The Ordinary Glycolic Acid %7`[cite: 1].
        """)
    with cmt:
        st.markdown("""
        - **🚿 Duş:** Standart günlük ferahlık duşu[cite: 1].
        - **🌙 Akşam Bakımı:** Yüzü yıka -> Yalnızca `CeraVe Losyon`[cite: 1].
        """)
    with pzr:
        st.markdown("""
        - **💆 Saç Derisi Detoksu:** Duştan 15 dk önce kuru saç diplerine damlalıkla `The Ordinary Glycolic Acid %7` damlatın[cite: 1].
        - **🚿 Duş:** `Sebamed Şampuan` ile 2 tur yıkayarak pudra ve fiber artıklarını temizleyin[cite: 1].
        - **🌙 Akşam Bakımı:** Yüzü yıka -> `Neutrogena Göz Kremi` -> `CeraVe Losyon`[cite: 1].
        """)
        
    st.divider()
    st.subheader("🛒 Onaylı Bakım Sepeti & Linkler")
    urun_kartlari_ciz(profil["kisisel_bakim_ve_hijyen_listesi"], "bakim")