import streamlit as st
import json
import urllib.parse
import random

st.set_page_config(
    page_title="Kişisel Stil, Alışveriş, Kombin & Bakım Asistanı",
    page_icon="👔",
    layout="wide"
)

# Profil Verisi Yükle
def profil_yukle():
    with open("profil.json", "r", encoding="utf-8") as f:
        return json.load(f)

profil = profil_yukle()

# Beden & Kalıp Tavsiye Motoru
def beden_tavsiyesi_uret(parca_adi):
    adi = parca_adi.lower()
    if any(k in adi for k in ["bot", "sneaker", "loafer", "ayakkabı", "terlik", "espadril"]):
        return {"beden": "44 - 44.5 Numara (EUR)", "detay": "Ayak: 28.5 cm (11.5 cm Taraklı). Dar/sert kalıplarda 44.5 veya 45 tercih edin."}
    elif any(k in adi for k in ["pantolon", "chino", "jean", "kadife", "şort", "eşofman"]):
        return {"beden": "34 / 32 (veya L Beden)", "detay": "Bel: 98 cm | Uyluk: 61 cm. Bacak kaslarını kasmaması için 'Tapered / Düz Kesim' seçin."}
    elif any(k in adi for k in ["boxer", "içlik", "fanila", "çorap"]):
        return {"beden": "L Beden / 43-46 Çorap", "detay": "Sürtünmeyi önleyen Long Leg (Uzun Paçalı) Modal kumaş tercih edin."}
    elif "kemer" in adi:
        return {"beden": "95 - 100 cm", "detay": "Pantolon beli 98 cm için ideal orta delik boyudur."}
    elif any(k in adi for k in ["gömlek", "tişört", "polo", "kazak", "sweatshirt", "ceket", "kaban", "parka", "hırka", "yelek", "blazer", "overshirt", "lounge"]):
        return {"beden": "L (Regular) / XL (Slim Fit)", "detay": "Göğüs: 105 cm | Omuz: 54 cm | Biceps: 40-45 cm. Slim fit ürünlerde +1 beden veya elastanlı seçin."}
    return None

# Arama Butonları
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

# Ürün Kartı Çizici
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

# --- ZENGİN DİNAMİK KOMBİN HAVUZU ---
DETAYLI_KOMBIN_HAVUZU = {
    "Sonbahar": {
        "Sınıf / Okul (Akademik Smart-Casual)": [
            {
                "baslik": "Klasik Akademik Başlangıç & Ton-Sür-Ton",
                "ust": "Kırık Beyaz / Açık Krem Oxford Pamuk Gömlek",
                "ust_detay": "Regular Fit (L Beden), üstten 2 düğme açık, kollar tek tur İtalyan kıvrık[cite: 1].",
                "alt": "Taş Rengi / Kum Beji Tok Gabardin Chino Pantolon",
                "alt_detay": "Tapered Kesim (34/32 Beden), ayakkabı üstüne yığılmayan paça boyu[cite: 1].",
                "dis": "Astarsız Yumuşak Lacivert Blazer Ceket",
                "dis_detay": "52 / L Beden, vatkasız dökümlü omuz[cite: 1].",
                "ayakkabi": "Ekru / Kırık Beyaz Minimalist Deri Sneaker (No: 44)",
                "aksesuar": "Taba Hakiki Süet Kemer + Kahverengi Deri Kordonlu Saat[cite: 1]",
                "ev_giyimi": "Ekru Waffle Uzun Kollu Henley Tişört + Melanj Taş Rengi Eşofman Altı + Süet Kapalı Terlik[cite: 1]",
                "stil_sirri": "Krem ve taş rengi açık tonların uyumu boyunuzu daha uzun gösterir[cite: 1]."
            },
            {
                "baslik": "İtalyan Triko & Haki Kontrastı",
                "ust": "Sıcak Karamel / Taba İnce Örgü Uzun Kollu Polo Triko",
                "ust_detay": "L Beden, triko polo yaka kravatsız lüks bir duruş sunar[cite: 1].",
                "alt": "Zeytin Yeşili / Koyu Haki Mat Pamuk Chino Pantolon",
                "alt_detay": "Tapered Kesim (34/32 Beden)[cite: 1].",
                "dis": "Taş Rengi Kısa Pamuklu Trençkot / Harrington Ceket",
                "dis_detay": "L Beden, serin sabahlar için hafif katman[cite: 1].",
                "ayakkabi": "Taba Süet Penny Loafer (No: 44.5)",
                "aksesuar": "Taba Örgü Deri Kemer + Kahve Deri Kayışlı Saat[cite: 1]",
                "ev_giyimi": "Vizon Waffle Henley Tişört + Koyu Vizon Modal Lounge Eşofman Altı[cite: 1]",
                "stil_sirri": "Karamel ile haki yeşilinin mat kontrastı Soft Autumn paletinin en zengin tonlarıdır[cite: 1]."
            },
            {
                "baslik": "Katmanlı Kışa Geçiş Şıklığı",
                "ust": "Kırık Beyaz Oxford Gömlek üzerine Vizon Yarım Fermuarlı Triko",
                "ust_detay": "Gömlek L Beden içeri sokulmuş, triko yakasından gösterilmiş[cite: 1].",
                "alt": "Çikolata Kahve Mikro Fitilli Kadife Pantolon",
                "alt_detay": "Tapered Kesim (34/32 Beden)[cite: 1].",
                "dis": "Astarsız Balıksırtı Vizon Blazer Ceket",
                "dis_detay": "52 / L Beden[cite: 1].",
                "ayakkabi": "Taba Süet Chelsea Bot (No: 44.5)",
                "aksesuar": "Taba Süet Kemer + Vizon-Haki Ekose Yün Atkı[cite: 1]",
                "ev_giyimi": "Taş Rengi Modal Ev Tişörtü + Açık Mocha Şal Yaka Hırka + Fitilli Çorap[cite: 1]",
                "stil_sirri": "Mikro fitilli kadife ve fermuarlı triko katmanı okulda maksimum konfor sağlar[cite: 1]."
            },
            {
                "baslik": "Maskülen Denim & Chino Dengesi",
                "ust": "Yumuşak Açık İndigo Chambray (Kot) Gömlek",
                "ust_detay": "L Beden, kollar dirseğe kadar katlı[cite: 1].",
                "alt": "Taş Rengi Tok Gabardin Chino Pantolon",
                "alt_detay": "34/32 Beden[cite: 1].",
                "dis": "Mat Haki Harrington Ceket",
                "dis_detay": "Ders giriş-çıkışları için rüzgar kesici dış katman[cite: 1].",
                "ayakkabi": "Ekru Deri Sneaker (Süet detaylı - No: 44)",
                "aksesuar": "Taba Süet Kemer + Mat Bronz Pilot Güneş Gözlüğü[cite: 1]",
                "ev_giyimi": "Mat Zeytin Waffle Tişört + Taş Rengi Pamuklu Eşofman Altı[cite: 1]",
                "stil_sirri": "Chambray gömlek kumaşı pamuk chino üzerinde çok temiz bir kontrast kurar[cite: 1]."
            },
            {
                "baslik": "Adaçayı Yeşili & Bej Ferahlığı",
                "ust": "Adaçayı Yeşili Keten-Pamuk Karışımlı Gömlek",
                "ust_detay": "L Beden, üstten 2 düğme açık[cite: 1].",
                "alt": "Kum Beji Gabardin Chino Pantolon",
                "alt_detay": "34/32 Beden, terzi işi düz iniş[cite: 1].",
                "dis": "Taba Hakiki Süet Overshirt (Gömlek Ceket)",
                "dis_detay": "L Beden, önü açık ceket formunda[cite: 1].",
                "ayakkabi": "Taba Süet Penny Loafer (No: 44.5)",
                "aksesuar": "Taba Süet Kemer + Deri Kordonlu Klasik Saat[cite: 1]",
                "ev_giyimi": "Ekru Modal Rahat Tişört + Keten-Pamuk Ev Şortu[cite: 1]",
                "stil_sirri": "Adaçayı yeşili ile taba süetin uyumu sonbaharda derste çok dingin ve güven veren bir otorite kurar[cite: 1]."
            }
        ],
        "Hafta Sonu / Dışarı (Relaxed & Karizmatik)": [
            {
                "baslik": "Zahmetsiz Süet Katman & Jean",
                "ust": "Ekru / Kırık Beyaz Ağır Gramajlı Basic Tişört",
                "ust_detay": "L Beden, tok yakalı %100 pamuk[cite: 1].",
                "alt": "Düz Kesim Koyu İndigo Ham Jean (Yırtıksız)",
                "alt_detay": "34/32 Beden straight fit[cite: 1].",
                "dis": "Taba / Konyak Hakiki Süet Overshirt (Gömlek Ceket)",
                "dis_detay": "L / XL Beden, önü açık[cite: 1].",
                "ayakkabi": "Ekru Minimalist Deri Sneaker (No: 44)",
                "aksesuar": "Taba Süet Kemer + Taba Pamuklu Beyzbol Şapkası[cite: 1]",
                "ev_giyimi": "Vizon Modal Tişört + Melanj Eşofman Altı + Süet Terlik[cite: 1]",
                "stil_sirri": "Taba süetin zengin dokusu ekru tişört ve koyu jean fonunda öne çıkar[cite: 1]."
            },
            {
                "baslik": "Doğal Keten & Haki Dinamikliği",
                "ust": "Adaçayı Yeşili Keten Gömlek (İçine ekru tişört)",
                "ust_detay": "L Beden, önü açık ceket gibi[cite: 1].",
                "alt": "Taş Rengi Gabardin Chino Pantolon",
                "alt_detay": "34/32 Beden[cite: 1].",
                "dis": "Mat Zeytin Yeşili Şişme Yelek",
                "dis_detay": "L Beden yürüyüş yeleği[cite: 1].",
                "ayakkabi": "Asics Gel-Kayano 31 (Vizon/Gri) veya Sneaker",
                "aksesuar": "Kahve Deri Saat + Amber Güneş Gözlüğü[cite: 1]",
                "ev_giyimi": "Ekru Waffle Henley + Kum Beji Şort[cite: 1]",
                "stil_sirri": "Adaçayı yeşili ile bej tonları hafta sonu kafede taze ve dinamik durur[cite: 1]."
            }
        ],
        "Akşam Yemeği / Özel Davet (Zarif & Maskülen)": [
            {
                "baslik": "Süetin Tek Başına Maskülen Gücü",
                "ust": "Taba / Konyak Süet Overshirt (Gömlek Formunda)",
                "ust_detay": "L Beden, üstten 2 düğme açık, manşetler tek tur kıvrık[cite: 1].",
                "alt": "Taş Rengi / Kum Beji Tok Gabardin Chino Pantolon",
                "alt_detay": "34/32 Beden[cite: 1].",
                "dis": "Tek katman odaklı süet şıklığı",
                "dis_detay": "V-fiziği öne çıkaran net duruş[cite: 1].",
                "ayakkabi": "Taba Süet Penny Loafer veya Chelsea Bot (No: 44.5)",
                "aksesuar": "Taba Süet Kemer + Deri Saat + Parfüm: Dolce & Gabbana The One EDP[cite: 1]",
                "ev_giyimi": "Çikolata Kahve Şal Yaka Hırka + İpeksi Modal Boxer + Waffle Tişört[cite: 1]",
                "stil_sirri": "Akşam loş ışıkta süet kumaş doğrudan dikkat çeker[cite: 1]."
            }
        ],
        "Pazar Rahat Dolaşma & Dinlenme": [
            {
                "baslik": "Elevated Casual Pazar Rahatlığı",
                "ust": "Ekru Yarım Fermuarlı (Half-Zip) Pamuklu Sweatshirt",
                "ust_detay": "L Beden, dik fermuarlı yaka boyun ve omuz hattını kalıplı gösterir[cite: 1].",
                "alt": "Melanj Taş Rengi Düz Paça Tok Eşofman Altı",
                "alt_detay": "Tapered Kesim, bacak kaslarını sıkmadan düz iner[cite: 1].",
                "dis": "Mat Zeytin Yeşili Şişme Yelek (Puffer Gilet)",
                "dis_detay": "Yürüyüş ve pazar kahvesi için rahat katman[cite: 1].",
                "ayakkabi": "Asics Gel-Kayano 31 (Diz Destekli Ortopedik Yürüyüş Ayakkabısı)",
                "aksesuar": "Taş Rengi Logosuz Pamuklu Beyzbol Şapkası[cite: 1]",
                "ev_giyimi": "Tüm gün: Waffle Henley Tişört + Modal Eşofman Altı + Mantar Tabanlı Süet Terlik[cite: 1]",
                "stil_sirri": "Eşofman altının paçasının lastiksiz düz inmesi salaşlığı engelleyip derli toplu gösterir[cite: 1]."
            }
        ]
    },
    "Kış": {
        "Sınıf / Okul (Akademik Smart-Casual)": [
            {
                "baslik": "Old Money Akademik Kış Zırhı",
                "ust": "Kırık Beyaz Oxford Gömlek üzerine Karamel Saç Örgü Kazak",
                "ust_detay": "Gömlek yakası kazağın içinden muntazam çıkarılmış[cite: 1].",
                "alt": "Çikolata Kahve Mikro Kadife Pantolon",
                "alt_detay": "34/32 Beden[cite: 1].",
                "dis": "Deve Tüyü (Camel) Chesterfield Yün Kaban",
                "dis_detay": "52 / L Beden[cite: 1].",
                "ayakkabi": "Acı Kahve Commando Tabanlı Hakiki Deri Bot (No: 44.5)",
                "aksesuar": "Taba Deri Eldiven + Ekose Yün Atkı[cite: 1]",
                "ev_giyimi": "Şal Yaka Hırka + Waffle Uzun Kollu Tişört + Kalın Yün Çorap[cite: 1]",
                "stil_sirri": "Saç örgü dokusu ve camel kaban kış aylarının en prestijli ikilisidir[cite: 1]."
            },
            {
                "baslik": "Şal Yaka Hırka & Oxford Asaleti",
                "ust": "Kırık Beyaz Oxford Gömlek üzerine Koyu Haki Şal Yaka Hırka",
                "ust_detay": "L Beden, ahşap düğmeli kalın hırka[cite: 1].",
                "alt": "Koyu Vizon Yün-Flanel Pantolon",
                "alt_detay": "34/32 Beden[cite: 1].",
                "dis": "Mat Zeytin Yeşili Dolgulu Parka",
                "dis_detay": "L Beden[cite: 1].",
                "ayakkabi": "Taba Süet Chelsea Bot (No: 44.5)",
                "aksesuar": "Deri Kordonlu Saat + Kaşmir Atkı[cite: 1]",
                "ev_giyimi": "Vizon Waffle Tişört + Koyu Vizon Eşofman Altı[cite: 1]",
                "stil_sirri": "Şal yaka triko sınıfta hem otoriter hem çok sıcak bir hava verir[cite: 1]."
            },
            {
                "baslik": "Monokrom Kış Triko Katmanı",
                "ust": "Ekru Balıkçı Yaka Yün Kazak",
                "ust_detay": "L Beden tok yün[cite: 1].",
                "alt": "Füme / Küllü Gri Flanel Pantolon",
                "alt_detay": "34/32 Beden[cite: 1].",
                "dis": "Astarsız Yumuşak Lacivert Blazer Ceket",
                "dis_detay": "52 / L Beden[cite: 1].",
                "ayakkabi": "Acı Kahve Deri Bot (No: 44.5)",
                "aksesuar": "Taba Süet Kemer + Deri Eldiven[cite: 1]",
                "ev_giyimi": "Ekru Modal Tişört + Taş Rengi Eşofman Altı[cite: 1]",
                "stil_sirri": "Ekru balıkçı kazak blazer içine giyildiğinde tam bir Oxford akademisyeni duruşu yaratır[cite: 1]."
            }
        ],
        "Hafta Sonu / Dışarı (Relaxed & Karizmatik)": [
            {
                "baslik": "Soğuk Hava & Karlı Gün Parka Stili",
                "ust": "Ekru Balıkçı Yaka Yün Kazak",
                "ust_detay": "L Beden tok yün[cite: 1].",
                "alt": "Koyu İndigo Ham Jean",
                "alt_detay": "34/32 Beden[cite: 1].",
                "dis": "Mat Zeytin Yeşili Kapüşonlu Dolgulu Parka",
                "dis_detay": "L Beden[cite: 1].",
                "ayakkabi": "Acı Kahve Commando Taban Deri Bot (No: 44.5)",
                "aksesuar": "Ekru Yün Bere + Taba Deri Eldiven[cite: 1]",
                "ev_giyimi": "Açık Mocha Ev Hırkası + Modal Eşofman Altı[cite: 1]",
                "stil_sirri": "Ekru kazak yüzü aydınlatırken parka maskülen duruş verir[cite: 1]."
            }
        ],
        "Akşam Yemeği / Özel Davet (Zarif & Maskülen)": [
            {
                "baslik": "Monokrom Kış Lüksü",
                "ust": "Ekru Tam Balıkçı Yaka İnce Yün Kazak",
                "ust_detay": "L Beden vücuda oturan kalıp[cite: 1].",
                "alt": "Koyu Vizon Tek Pileli Flanel Yün Pantolon",
                "alt_detay": "34/32 Beden akıcı kumaş[cite: 1].",
                "dis": "Deve Tüyü (Camel) Chesterfield Yün Kaban",
                "dis_detay": "52 / L Beden[cite: 1].",
                "ayakkabi": "Acı Kahve Hakiki Deri Bot (No: 44.5)",
                "aksesuar": "Taba Deri Eldiven + Parfüm: Dior Homme Intense[cite: 1]",
                "ev_giyimi": "Vizon Waffle Tişört + Melanj Eşofman Altı[cite: 1]",
                "stil_sirri": "Ekru balıkçı kazak ve deve tüyü kaban kışın en asil duruşudur[cite: 1]."
            }
        ],
        "Pazar Rahat Dolaşma & Dinlenme": [
            {
                "baslik": "Kışlık Sıcak Loungewear",
                "ust": "Taş Rengi Waffle Henley Tişört üzerine Açık Mocha Şal Yaka Hırka",
                "ust_detay": "L Beden yumuşak ev ve yürüyüş katmanı[cite: 1].",
                "alt": "Koyu Vizon Tapered Eşofman Altı",
                "alt_detay": "34/32 Beden[cite: 1].",
                "dis": "Mat Koyu Zeytin Parka",
                "dis_detay": "L Beden[cite: 1].",
                "ayakkabi": "Commando Tabanlı Deri Bot veya Ortopedik Sneaker",
                "aksesuar": "Ekru Yün Bere[cite: 1]",
                "ev_giyimi": "Tüm gün: Waffle Henley + Şal Yaka Hırka + Yün Çorap + Süet Terlik[cite: 1]",
                "stil_sirri": "Şal yaka hırka pazar günleri maksimum sıcaklık ve şıklık sunar[cite: 1]."
            }
        ]
    },
    "İlkbahar": {
        "Sınıf / Okul (Akademik Smart-Casual)": [
            {
                "baslik": "Ferah Bahar & Omuzda Triko",
                "ust": "Kırık Beyaz Oxford Gömlek (Üzerine Taş Rengi İnce Triko asılı)",
                "ust_detay": "Kollar dirseğe kıvrık, triko omuzda gevşek bağlı[cite: 1].",
                "alt": "Mat Zeytin Yeşili Chino Pantolon",
                "alt_detay": "34/32 Beden[cite: 1].",
                "dis": "Kum Beji Dört Cepli Safari Ceket",
                "dis_detay": "L Beden[cite: 1].",
                "ayakkabi": "Taba Süet Penny Loafer (No: 44.5)",
                "aksesuar": "Taba Örgü Deri Kemer + Kahve Deri Saat[cite: 1]",
                "ev_giyimi": "Kum Beji Modal Tişört + Keten-Pamuk Ev Pantolonu[cite: 1]",
                "stil_sirri": "Trikoyu omuza atmak çabasız bir İtalyan entelektüel havası katar[cite: 1]."
            },
            {
                "baslik": "Tozlu Petrol & Bej Tazeliği",
                "ust": "Tozlu Petrol Mavisi Açık Yaka (Johnny Collar) Polo Tişört",
                "ust_detay": "L Beden, düğmesiz ferah yaka[cite: 1].",
                "alt": "Taş Rengi Gabardin Chino Pantolon",
                "alt_detay": "34/32 Beden[cite: 1].",
                "dis": "Yumuşak Lacivert Astarsız Blazer Ceket",
                "dis_detay": "52 / L Beden[cite: 1].",
                "ayakkabi": "Ekru Minimalist Deri Sneaker (No: 44)",
                "aksesuar": "Kahve Kordonlu Saat + Amber Güneş Gözlüğü[cite: 1]",
                "ev_giyimi": "Ekru Modal Tişört + Adaçayı Ev Şortu[cite: 1]",
                "stil_sirri": "Tozlu petrol mavisi Soft Autumn paletinin en taze rengidir[cite: 1]."
            }
        ],
        "Hafta Sonu / Dışarı (Relaxed & Karizmatik)": [
            {
                "baslik": "Bahar Safari & Toprak Tonları",
                "ust": "Yanık Kiremit Kısa Kollu Triko Polo",
                "ust_detay": "L Beden ince örgü[cite: 1].",
                "alt": "Kırık Beyaz Tek Pileli Keten Pantolon",
                "alt_detay": "34/32 Beden pileli form[cite: 1].",
                "dis": "Kum Beji Safari Ceket",
                "dis_detay": "L Beden[cite: 1].",
                "ayakkabi": "Taba Süet Penny Loafer (No: 44.5)",
                "aksesuar": "Pilot Güneş Gözlüğü + Örgü Kemer[cite: 1]",
                "ev_giyimi": "Taş Rengi Modal Tişört + Kum Beji Şort[cite: 1]",
                "stil_sirri": "Yanık kiremit ile kırık beyaz bahar güneşinde teni canlandırır[cite: 1]."
            }
        ],
        "Akşam Yemeği / Özel Davet (Zarif & Maskülen)": [
            {
                "baslik": "Adaçayı & Lacivert Blazer",
                "ust": "Adaçayı Yeşili Keten-Pamuk Gömlek",
                "ust_detay": "L Beden, üstten 2 düğme açık[cite: 1].",
                "alt": "Kum Beji Chino Pantolon",
                "alt_detay": "34/32 Beden[cite: 1].",
                "dis": "Yumuşak Lacivert Astarsız Blazer Ceket",
                "dis_detay": "52 / L Beden[cite: 1].",
                "ayakkabi": "Taba Süet Loafer (No: 44.5)",
                "aksesuar": "Taba Süet Kemer + Parfüm: Tom Ford Grey Vetiver[cite: 1]",
                "ev_giyimi": "Vizon Modal Tişört + Keten-Pamuk Rahat Pantolon[cite: 1]",
                "stil_sirri": "Yeşil, bej ve lacivert akşam yemeklerinde dengeli ve resmidir[cite: 1]."
            }
        ],
        "Pazar Rahat Dolaşma & Dinlenme": [
            {
                "baslik": "İlkbahar Park & Yürüyüş Kombini",
                "ust": "Adaçayı Yeşili Premium Bisiklet Yaka Sweatshirt",
                "ust_detay": "L Beden, içine giyilen ekru tişört yakadan hafifçe görünür[cite: 1].",
                "alt": "Beli İpli Kum Beji Rahat Chino Pantolon",
                "alt_detay": "34/32 Beden[cite: 1].",
                "dis": "Mat Haki Harrington Ceket (Gerektiğinde)",
                "dis_detay": "L Beden[cite: 1].",
                "ayakkabi": "Asics Gel-Kayano 31 (Vizon / Gri)",
                "aksesuar": "Taba Beyzbol Şapkası + Güneş Gözlüğü[cite: 1]",
                "ev_giyimi": "Tüm gün: Modal Tişört + Keten Şort + Süet Terlik[cite: 1]",
                "stil_sirri": "Beli ipli chino pantolon dışarıda eşofmandan çok daha şık durur[cite: 1]."
            }
        ]
    },
    "Yaz": {
        "Sınıf / Okul (Akademik Smart-Casual)": [
            {
                "baslik": "Akdeniz Riviera Keten Şıklığı",
                "ust": "Ekru %100 Keten Gömlek (Kollar kıvrık)",
                "ust_detay": "Relaxed Fit (L Beden), terletmeyen lif[cite: 1].",
                "alt": "Kum Beji Dökümlü Keten Pantolon",
                "alt_detay": "34/32 Beden bacakları sıkmaz[cite: 1].",
                "dis": "Taş Rengi İnce Triko (Omuza asılı)",
                "dis_detay": "Klimalı odalar için katman[cite: 1].",
                "ayakkabi": "Taba Hakiki Deri Örgü Loafer (No: 44.5)",
                "aksesuar": "Örgü Deri Kemer + Kahve Deri Saat[cite: 1]",
                "ev_giyimi": "Terracotta Modal Tişört + Müslin Keten Şort[cite: 1]",
                "stil_sirri": "Baştan aşağı ekru-bej keten takımı yazın terletmeden lüks durur[cite: 1]."
            },
            {
                "baslik": "Lacivert Pique Polo Ciddiyeti",
                "ust": "Yumuşak Lacivert Premium Pique Pamuk Polo",
                "ust_detay": "L Beden, terletmeyen pike örgü[cite: 1].",
                "alt": "Taş Rengi Keten-Pamuk Pantolon",
                "alt_detay": "34/32 Beden[cite: 1].",
                "dis": "Yaz aylarında tek katman önerilir[cite: 1]",
                "dis_detay": "V-fiziği net gösterir[cite: 1].",
                "ayakkabi": "Taba Süet Penny Loafer veya Ekru Sneaker[cite: 1]",
                "aksesuar": "Taba Kemer + Amber Güneş Gözlüğü[cite: 1]",
                "ev_giyimi": "Kum Beji Modal Tişört + Adaçayı Şort[cite: 1]",
                "stil_sirri": "Lacivert ve taş rengi okulda resmiyeti korurken sıcağı hissettirmez[cite: 1]."
            }
        ],
        "Hafta Sonu / Dışarı (Relaxed & Karizmatik)": [
            {
                "baslik": "Resort Rahatlığı & Keten Şort",
                "ust": "Adaçayı Yeşili Keten Gömlek (Önü açık) + Ekru Tişört",
                "ust_detay": "İçte hafif supima pamuk tişört[cite: 1].",
                "alt": "Taş Rengi Terzi Kesim (Tailored) Bermuda Şort",
                "alt_detay": "Beden: 34, dizin 2 parmak üzerinde[cite: 1].",
                "dis": "Açık keten gömlek",
                "dis_detay": "Güneş kalkanı[cite: 1].",
                "ayakkabi": "Taba Süet Terlik (Mantar Taban)",
                "aksesuar": "Pilot Güneş Gözlüğü + Örgü Bileklik[cite: 1]",
                "ev_giyimi": "Taş Rengi Tişört + Beli Lastikli Keten Şort[cite: 1]",
                "stil_sirri": "Terzi kesim şort diz üstü bittiğinde sporcu bacaklarını estetik gösterir[cite: 1]."
            }
        ],
        "Akşam Yemeği / Özel Davet (Zarif & Maskülen)": [
            {
                "baslik": "Yaz Akşamı Terakota & Kırık Beyaz",
                "ust": "Yanık Kiremit Triko / Modal Polo",
                "ust_detay": "L Beden dökümlü doku[cite: 1].",
                "alt": "Kırık Beyaz Tek Pileli Keten Pantolon",
                "alt_detay": "34/32 Beden[cite: 1].",
                "dis": "Omuza atılmış Kum Beji İnce Triko",
                "dis_detay": "Akşam esintisi için aksesuar katman[cite: 1].",
                "ayakkabi": "Taba Hakiki Deri Örgü Loafer (No: 44.5)",
                "aksesuar": "Örgü Deri Kemer + Parfüm: Terre d'Hermès Eau Givrée[cite: 1]",
                "ev_giyimi": "Ekru Modal Tişört + Keten Ev Pantolonu[cite: 1]",
                "stil_sirri": "Kiremit tonu yaz akşamında bronz teni ve sakal rengini parlatır[cite: 1]."
            }
        ],
        "Pazar Rahat Dolaşma & Dinlenme": [
            {
                "baslik": "Yaz Pazar Sahil & Dinlenme",
                "ust": "Taş Rengi Supima İnce Pamuk Basic Tişört",
                "ust_detay": "L Beden, ipeksi hafif doku[cite: 1].",
                "alt": "Beli Bağcıklı Adaçayı Yeşili Keten Şort",
                "alt_detay": "Beden: 34, lastikli bel[cite: 1].",
                "dis": "Ekstra dış katman gerekmez[cite: 1]",
                "dis_detay": "Maksimum ferahlık[cite: 1].",
                "ayakkabi": "Vizon Süet Espadril veya Mantar Taban Terlik[cite: 1]",
                "aksesuar": "Kemik Çerçeve Güneş Gözlüğü[cite: 1]",
                "ev_giyimi": "Tüm gün: Müslin Ev Şortu + Modal Tişört + Süet Terlik[cite: 1]",
                "stil_sirri": "Doğal keten şort pazar günleri terletmeyen dinlenme konforu sunar[cite: 1]."
            }
        ]
    }
}

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

# --- ANA EKRAN SEKMELERİ ---
st.title("👔 Kişisel Stil, Alışveriş, Kombin & Bakım Asistanı")

(
    tab_kombin,
    tab_haftalik,
    tab_sb,
    tab_kis,
    tab_bahar,
    tab_yaz,
    tab_rahat,
    tab_ev,
    tab_icgiyim,
    tab_aksesuar,
    tab_bakim,
    tab_parfum,
    tab_rutin
) = st.tabs([
    "🎲 Akıllı Kombin Motoru",
    "📅 7 Günlük Yaşam Planı",
    "🍂 Sonbahar",
    "❄️ Kış",
    "🌸 İlkbahar",
    "☀️ Yaz",
    "🏃 Rahat Giyim",
    "🏠 Ev Giyimi",
    "🩲 İç Giyim & Çorap",
    "🕶️ Aksesuarlar",
    "🧴 Kişisel Bakım",
    "🪵 Parfümler",
    "🗓️ Detaylı Bakım Takvimi"
])

# 1. AKILLI KOMBİN MOTORU
with tab_kombin:
    st.header("✨ Akıllı Kombin Üretici (Mevsim & Ortam Odaklı)")
    st.caption("Her tıklamada seçilen mevsime ve ortama göre anlık, taze ve tam detaylı bir kombin üretir.")
    
    col_m, col_o = st.columns(2)
    with col_m:
        secilen_mevsim = st.selectbox("📅 Mevsim Seçin:", ["Sonbahar", "Kış", "İlkbahar", "Yaz"])
    with col_o:
        secilen_ortam = st.selectbox("📍 Ortam / Senaryo Seçin:", [
            "Sınıf / Okul (Akademik Smart-Casual)",
            "Hafta Sonu / Dışarı (Relaxed & Karizmatik)",
            "Akşam Yemeği / Özel Davet (Zarif & Maskülen)",
            "Pazar Rahat Dolaşma & Dinlenme"
        ])
        
    kombin_listesi = DETAYLI_KOMBIN_HAVUZU.get(secilen_mevsim, {}).get(secilen_ortam, [])
    
    if st.button("🎲 Bu Ortam İçin Yeni Kombin Oluştur", use_container_width=True, type="primary"):
        if kombin_listesi:
            kombin = random.choice(kombin_listesi)
            st.success(f"🎯 **{secilen_mevsim} — {secilen_ortam} Önerisi: {kombin['baslik']}**")
            
            with st.container(border=True):
                st.markdown(f"#### 💡 Stil & Duruş Sırrı: {kombin['stil_sirri']}")
                st.divider()
                
                c_sol, c_sag = st.columns(2)
                with c_sol:
                    st.markdown("### 👔 Gündüz Kıyafeti")
                    st.markdown(f"- **Üst Parça:** `{kombin['ust']}`\n  *Detay:* {kombin['ust_detay']}")
                    st.markdown(f"- **Alt Parça:** `{kombin['alt']}`\n  *Detay:* {kombin['alt_detay']}")
                    st.markdown(f"- **Dış Katman:** `{kombin['dis']}`\n  *Detay:* {kombin['dis_detay']}")
                    st.markdown(f"- **Ayakkabı:** `{kombin['ayakkabi']}`")
                
                with c_sag:
                    st.markdown("### 🕶️ Aksesuar & Ev Giyimi")
                    st.markdown(f"- **Uyumlu Aksesuarlar:** {kombin['aksesuar']}")
                    st.markdown(f"- **🏡 Akşam Ev Rahatlığı:** `{kombin['ev_giyimi']}`")
                    st.divider()
                    st.caption("Ana Parçaları Doğrudan Mağazalarda Ara:")
                    link_butonlari(kombin['ust'])

# 2. 7 GÜNLÜK DİNAMİK YAŞAM PLANI (HER TIKLAMADA TAMAMEN YENİ VE RASTGELE)
with tab_haftalik:
    st.header("📅 7 Günlük Eksiksiz Yaşam & Kombin Planı")
    st.caption("Her butona bastığınızda günlerin kıyafetleri havuzdan rastgele ve taze olarak karıştırılır; çamaşır ve ev giyimi rotasyonunu düzenler.")
    
    sec_mevsim_hafta = st.selectbox("Hangi mevsim için 7 günlük plan oluşturulsun?", ["Sonbahar", "Kış", "İlkbahar", "Yaz"], key="hafta_7gun_mevsim")
    
    if st.button("🎲 7 Günlük YENİ Yaşam Planı Oluştur (Karıştır)", use_container_width=True, type="primary"):
        mevsim_data = DETAYLI_KOMBIN_HAVUZU.get(sec_mevsim_hafta, {})
        okul_havuzu = list(mevsim_data.get("Sınıf / Okul (Akademik Smart-Casual)", []))
        haftasonu_havuzu = list(mevsim_data.get("Hafta Sonu / Dışarı (Relaxed & Karizmatik)", [])) + list(mevsim_data.get("Akşam Yemeği / Özel Davet (Zarif & Maskülen)", []))
        pazar_havuzu = list(mevsim_data.get("Pazar Rahat Dolaşma & Dinlenme", []))
        
        # Okul günleri için havuzdan rastgele karıştırma (Random shuffle & sample)
        random.shuffle(okul_havuzu)
        random.shuffle(haftasonu_havuzu)
        random.shuffle(pazar_havuzu)
        
        gunler = [
            ("Pazartesi (Okul / İş Başı)", okul_havuzu, 0),
            ("Salı (Okul / İş)", okul_havuzu, 1),
            ("Çarşamba (Okul / İş)", okul_havuzu, 2),
            ("Perşembe (Okul / İş)", okul_havuzu, 3),
            ("Cuma (Okul / Cuma Şıklığı)", okul_havuzu, 4),
            ("Cumartesi (Hafta Sonu / Sosyal Şehir)", haftasonu_havuzu, 0),
            ("Pazar (Pazar Rahat Dolaşma & Dinlenme)", pazar_havuzu, 0)
        ]
        
        for gun_adi, havuz, index_no in gunler:
            if havuz:
                k = havuz[index_no % len(havuz)]
                with st.expander(f"📌 **{gun_adi}:** {k['baslik']}", expanded=True):
                    col_a, col_b = st.columns([3, 1])
                    with col_a:
                        st.markdown(f"**👔 Gündüz:** {k['ust']}  |  **Alt:** {k['alt']}")
                        st.markdown(f"**🧥 Katman:** {k['dis']}  |  **👟 Ayakkabı:** {k['ayakkabi']}")
                        st.markdown(f"**🕶️ Aksesuar:** {k['aksesuar']}")
                        st.markdown(f"**🏡 Akşam / Evde Dinlenme:** `{k['ev_giyimi']}`")
                        st.caption(f"*Stil İpucu:* {k['stil_sirri']}")
                    with col_b:
                        st.caption("Parçayı Bul:")
                        st.link_button("🛍️ Google'da Ara", f"https://www.google.com/search?tbm=shop&q={urllib.parse.quote(k['ust'])}", use_container_width=True)

# 3. SONBAHAR ALIŞVERİŞ
with tab_sb:
    st.subheader("🍂 Sonbahar Kapsül Gardırobu")
    urun_kartlari_ciz(profil["gardrop_arama_listesi"]["sonbahar_kapsulu"], "giyim")

# 4. KIŞ ALIŞVERİŞ
with tab_kis:
    st.subheader("❄️ Kış Kapsül Eklentileri")
    urun_kartlari_ciz(profil["gardrop_arama_listesi"]["kis_eklentileri"], "giyim")

# 5. İLKBAHAR ALIŞVERİŞ
with tab_bahar:
    st.subheader("🌸 İlkbahar Kapsül Eklentileri")
    urun_kartlari_ciz(profil["gardrop_arama_listesi"]["ilkbahar_kapsulu"], "giyim")

# 6. YAZ ALIŞVERİŞ
with tab_yaz:
    st.subheader("☀️ Yaz Kapsül Gardırobu")
    urun_kartlari_ciz(profil["gardrop_arama_listesi"]["yaz_kapsulu"], "giyim")

# 7. RAHAT GİYİM & SPOR
with tab_rahat:
    st.subheader("🏃 Elevated Casual & Spor Giyim")
    urun_kartlari_ciz(profil["gardrop_arama_listesi"]["rahat_giyim_ve_spor"], "giyim")

# 8. EV GİYİMİ (YENİ EKLENDİ)
with tab_ev:
    st.subheader("🏠 Ev Giyimi (Elevated Loungewear) Alışveriş Listesi")
    urun_kartlari_ciz(profil["gardrop_arama_listesi"]["ev_giyimi"], "giyim")

# 9. İÇ GİYİM & ÇORAP (YENİ EKLENDİ)
with tab_icgiyim:
    st.subheader("🩲 İç Giyim, Çorap & Kalkan Alışveriş Listesi")
    urun_kartlari_ciz(profil["gardrop_arama_listesi"]["ic_giyim_ve_corap"], "giyim")

# 10. AKSESUARLAR
with tab_aksesuar:
    st.subheader("🕶️ Aksesuarlar & Tamamlayıcı Parçalar")
    urun_kartlari_ciz(profil["aksesuar_listesi"], "giyim")

# 11. KİŞİSEL BAKIM & HİJYEN
with tab_bakim:
    st.subheader("🧴 Onaylı Kişisel Bakım & Hijyen Sepeti")
    urun_kartlari_ciz(profil["kisisel_bakim_ve_hijyen_listesi"], "bakim")

# 12. İMZA PARFÜMLER
with tab_parfum:
    st.subheader("🪵 Mevsimlik İmza Parfümler")
    st.markdown("##### ☀️ İlkbahar & Yaz")
    urun_kartlari_ciz(profil["parfum_onerileri"]["sicak_mevsimler_ilkbahar_yaz"], "parfum")
    st.divider()
    st.markdown("##### ❄️ Sonbahar & Kış")
    urun_kartlari_ciz(profil["parfum_onerileri"]["soguk_mevsimler_sonbahar_kis"], "parfum")

# 13. DETAYLI BAKIM TAKVİMİ
with tab_rutin:
    st.header("🧴 Eksiksiz Kişisel Bakım & Hijyen Takvimi")
    st.caption("Kullanılacak tüm ürünlerin ticari tam isimleri, dozajları ve haftalık sıralaması.")
    
    st.markdown("""
    ### ☀️ Günlük Sabah Rutini (Her Gün Sabit — 4 Dakika)
    1. **Yüz Yıkama:** `CeraVe Blemish Control Cleanser (236 ml)` ile 40 saniye dairesel masajla yüzü yıkayıp havluyla tamponlayarak kurulayın[cite: 1].
    2. **Nemlendirme:** Hafif nemli cilde 1 pompa `CeraVe Nemlendirici Losyon` uygulayın[cite: 1].
    3. **Güneş Koruma:** Dışarı çıkmadan 15 dk önce iki parmak kuralıyla `La Roche-Posay Anthelios UVMune 400 Oil Control Fluid SPF 50+` kremi tüm açık yüze, boyna ve kulak kepçelerine sürün[cite: 1].
    4. **Kasık / Vücut:** Duş sonrası kurulanmış kasık bölgesine `Dalin Likit Pudra` (veya `Burt's Bees Baby Dusting Powder`) sürün; ardından uzun paçalı modal boxer giyin[cite: 1].
    5. **Saç:** Nemi alınmış saça 3 fıs `Nishman Sea Salt Spray` sıkıp fönle kurutun -> Kuru diplere `Nishman P1 Hacim Pudrası` döküp kökleri dikleştirin -> `Saç Fiberi` serpip sabitleyici sprey ile kilitleyin[cite: 1].
    """)
    
    st.divider()
    st.markdown("### 🗓️ Gün Gün Akşam ve Duş Protokolü")
    
    tp1, tp2, tp3, tp4, tp5, tp6, tp7 = st.tabs([
        "Pazartesi (Retinol)", "Salı (Tonik)", "Çarşamba (Dinlenme)", "Perşembe (Retinol)", "Cuma (Tonik)", "Cumartesi (Dinlenme)", "Pazar (Detoks)"
    ])
    
    with tp1:
        st.subheader("Pazartesi: Derin Arınma & Retinol Gecesi")
        st.markdown("""
        - **🏋️ Spor Öncesi:** İç bacak temas hattına fındık kadar `Decathlon Aptonia Anti-Chafing Krem` sürün[cite: 1].
        - **🚿 Duş:** `Sebamed Yağlı Saçlar İçin Şampuan (400 ml)` ile saçı yıkayın[cite: 1]. `Bioderma Sébium Gel Moussant` ve `Doğal Kabak Lifi` ile sırt, omuz ve göğsü lifleyin[cite: 1].
        - **🌙 Akşam Bakımı (Retinol):**
          1. Yüzü `CeraVe Blemish Control Cleanser` ile yıkayıp **2-3 dakika tamamen kurumasını bekleyin**[cite: 1].
          2. 1 bezelye tanesi `The Ordinary Retinol %0.2 in Squalane` serumu alıp tüm yüze sürün[cite: 1]. Parmakta kalan hafif artığı boyna dokundurun[cite: 1].
          3. 1 pirinç tanesi `Neutrogena Retinol Boost Göz Kremi`ni yalnızca göz çevresi kemik hattına (kaz ayaklarına) tampon hareketlerle yedirin[cite: 1].
          4. 5 dakika sonra üzerine `CeraVe Nemlendirici Losyon` sürerek kilitleyin[cite: 1].
          5. Kuru koltuk altına ter kesici `Driclor Roll-on` uygulayın[cite: 1].
        """)
        
    with tp2:
        st.subheader("Salı: Gözenek Eşitleme & Göz Bakımı")
        st.markdown("""
        - **🚿 Duş:** Lifsiz, hızlı 3 dakikalık duş[cite: 1]. `Bioderma Sébium Gel` ile köpürtüp durulanın[cite: 1]. Duş çıkışı kasıklara `Dalin Likit Pudra`[cite: 1].
        - **🌙 Akşam Bakımı:**
          1. Yüzü `CeraVe Blemish Control Cleanser` ile yıkayın -> `Neutrogena Retinol Boost Göz Kremi` sürün -> `CeraVe Nemlendirici Losyon` ile nemlendirin[cite: 1].
          2. Duş sonrası kuru pamuğa `The Ordinary Glycolic Acid %7 Toning Solution` döküp koltuk altı ve kasık kıvrımlarını silin[cite: 1]. Kuruyunca kasığa hafifçe CeraVe losyon sürün[cite: 1].
        """)

    with tp3:
        st.subheader("Çarşamba: Cilt Bariyeri Dinlendirme")
        st.markdown("""
        - **🚿 Duş:** Standart durulanma duşu[cite: 1]. `Sebamed Şampuan` + `Bioderma Sébium Gel`[cite: 1].
        - **🌙 Akşam Bakımı:**
          1. Yüzü `CeraVe Blemish Control Cleanser` ile yıkayın[cite: 1].
          2. Yalnızca bolca `CeraVe Nemlendirici Losyon` sürün (Asit ve retinol uygulanmaz, bariyer toparlanır)[cite: 1].
        """)

    with tp4:
        st.subheader("Perşembe: 2. Retinol & Lifleme Gecesi")
        st.markdown("""
        - **🏋️ Spor Öncesi:** Bacak içine `Decathlon Aptonia Anti-Chafing Krem`[cite: 1].
        - **🚿 Duş:** `Sebamed Şampuan` + `Doğal Kabak Lifi` ve `Bioderma Sébium Gel` ile derin lifleme[cite: 1].
        - **🌙 Akşam Bakımı (Retinol):**
          1. Yüzü `CeraVe Blemish Control Cleanser` ile yıkayıp tam kurulayın[cite: 1].
          2. 1 bezelye tanesi `The Ordinary Retinol %0.2 in Squalane` uygulayın[cite: 1].
          3. Kaz ayaklarına `Neutrogena Retinol Boost Göz Kremi` sürün[cite: 1].
          4. 5 dk sonra `CeraVe Nemlendirici Losyon` ile kilitleyin[cite: 1].
          5. Koltuk altına haftanın 2. dozu olan `Driclor Roll-on` uygulayın[cite: 1].
        """)

    with tp5:
        st.subheader("Cuma: Hijyen & Kasık Tonik Bakımı")
        st.markdown("""
        - **🚿 Duş:** Hızlı ılık duş + `Sebamed Şampuan` + `Bioderma Sébium Gel`[cite: 1]. Duş sonrası `Dalin Likit Pudra`[cite: 1].
        - **🌙 Akşam Bakımı:**
          1. Yüzü yıka -> `Neutrogena Retinol Boost Göz Kremi` -> `CeraVe Nemlendirici Losyon`[cite: 1].
          2. Koltuk altı ve kasık bölgesini pamukla `The Ordinary Glycolic Acid %7 Toning Solution` ile silin[cite: 1].
        """)

    with tp6:
        st.subheader("Cumartesi: Serbest Dinlenme")
        st.markdown("""
        - **🚿 Duş:** Günlük ferahlık duşu[cite: 1].
        - **🌙 Akşam Bakımı:** Yüzü `CeraVe Blemish Control Cleanser` ile yıkayıp sadece `CeraVe Nemlendirici Losyon` sürün[cite: 1].
        """)

    with tp7:
        st.subheader("Pazar: Saç Derisi Detoksu & Haftalık Kapanış")
        st.markdown("""
        - **💆 Saç Derisi Detoksu:** Duşa girmeden 15 dakika önce kuru saç diplerine damlalıkla `The Ordinary Glycolic Acid %7 Toning Solution` damlatıp bekletin[cite: 1].
        - **🚿 Duş:** `Sebamed Yağlı Saçlar İçin Şampuan` ile 2 tur yıkayarak pudra/tuz kalıntılarını arındırın[cite: 1]. `Bioderma Sébium Gel` ile vücudu yıkayın[cite: 1].
        - **🌙 Akşam Bakımı:** Yüzü yıkayın -> Kaz ayaklarına `Neutrogena Retinol Boost Göz Kremi` sürün -> `CeraVe Nemlendirici Losyon` uygulayarak yeni haftaya hazır olun[cite: 1].
        """)