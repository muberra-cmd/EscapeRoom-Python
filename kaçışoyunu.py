import random

class Oda:
    def __init__(self, ad, tanim, esyalar=None, ipucu=None):
        if esyalar is None:
            esyalar = []
        self.ad = ad
        self.tanim = tanim
        self.esyalar = esyalar
        self.ipucu = ipucu

    def bilgi_goster(self):
        bilgi = f"\n--- {self.ad} ---\n{self.tanim}\n"
        if self.esyalar:
            bilgi += "Odadaki eşyalar: " + self.esyalar[0] + "\n"
        if self.ipucu:
            bilgi += "İpucunu görmek için 'ipucu' komutunu kullanabilirsin.\n"
        return bilgi

class KilitliOda(Oda):
    def __init__(self, ad, tanim, esyalar, ipucu=None, kilitli=True, gerekli_esyalar=None):
        super().__init__(ad, tanim, esyalar, ipucu)
        self.kilitli = kilitli
        if gerekli_esyalar is None:
            gerekli_esyalar = ()
        self.gerekli_esyalar = gerekli_esyalar

    def bilgi_goster(self):
        bilgi = super().bilgi_goster()
        return bilgi

    def kilidi_ac(self, oyuncu):
        eksik = []
        for esya in self.gerekli_esyalar:  #kilitli odanın gereksinimlerini kontrol eder
            if esya not in oyuncu.envanter["esyalar"]:
                eksik.append(esya)
        if not eksik:
            self.kilitli = False
            print("Kapıyı açtın! Artık çıkışa geçebilirsin.")
        else:
            gereken = ", ".join(eksik)
            print(f"Kapıyı açmak için eksik olan: {gereken} var.")

class Oyuncu:
    def __init__(self, ad, envanter=None, bulundugu_oda=None):
        if envanter is None:
            envanter = {"esyalar": []}
        self.ad = ad
        self.envanter = envanter
        self.bulundugu_oda = bulundugu_oda


    def envanteri_goster(self):
        if self.envanter["esyalar"]:
            print("Envanterindeki eşyalar:", ", ".join(self.envanter["esyalar"]))
        else:
            print("Envanterin boş.")

def ipucu_goster(oda):
    print("İpucu:", oda.ipucu)

def esya_topla(oda, oyuncu):
    if oda.esyalar:
        esya = oda.esyalar[0]
        oyuncu.envanter["esyalar"].append(esya)
        oda.esyalar.remove(esya)
        print(f"{esya} eşyasını topladın.")
        
        if esya == "Kağıt parçası":
            mors_kodlari = {
                "1": ".----",
                "2": "..---",
                "3": "...--",
                "4": "....-",
                "5": ".....",
                "6": "-....",
                "7": "--...",
                "8": "---..",
                "9": "----.",
                "10": ".---- -----"
            }
            print("\nMors alfabesiyle 1'den 10'a kadar sayılar:")
            for num in range(1, 10):  #Kağıt parçası alındığında Mors kodlarını listeler
                print(f"{num}: {mors_kodlari[str(num)]}")
            print(f"10: {mors_kodlari['10']}")

def oda_degistir(odalar, oyuncu, hedef_index):
    oyuncu.bulundugu_oda = odalar[hedef_index]
    print(oyuncu.bulundugu_oda.bilgi_goster())

def mors_bulmaca(oyuncu):
    if "Fener" not in oyuncu.envanter["esyalar"]:  #bulmaca erişimi
        print("Duvardaki yazıyı tam göremiyorsun. Bulmacayı çözebilmek için Karanlık Salon'dan 'Fener'i topla.")
        return None
    if "Kağıt parçası" not in oyuncu.envanter["esyalar"]:
        print("Duvar yazısını yorumlamakta zorlanıyorsun. 'Kağıt parçası' sana yardımcı olabilir.")
        return None

    print("Duvarlarda bir mesaj var: '..... ----. .----'")
    tahmin = input("Mors kodunu çözüp cevabı yaz: ").strip()
    if tahmin == "591":
        print("Mors kodunu doğru çözdün! Gizli bölmeden 'Kaçış Anahtarı' çıktı.")
        if "Kaçış Anahtarı" not in oyuncu.envanter["esyalar"]:
            oyuncu.envanter["esyalar"].append("Kaçış Anahtarı")
            print("'Kaçış Anahtarı' envanterine eklendi.")
        return True
    else:
        print("Yanlış çözüm. Tekrar denemelisin.")
        return False

def yaratık_olayi(oyuncu):
    print("Karanlıkta uğultular yükseliyor... Korkunç bir yaratık sana doğru geliyor!")
    eylem = input("Saklanmak mı istersin kaçmak mı? (saklan/kaç): ")

    if eylem == "saklan":
        print("Sessizce saklandın. Yaratık seni fark edemedi, ama dikkatli olmalısın.")
        return True

    if eylem == "kaç":
        if random.choice([True, False]):
            print("Hızla kaçtın ve yaratığı atlattın! Ama yine de dikkatli olmalısın.")
            return True
        else:
            print("Yaratık seni yakaladı...")
            return False
        
def odalari_olustur():
    odalar = []

    oda1 = Oda(
        ad="Giriş Odası",
        tanim="Soğuk, rutubetli bir odada gözlerini açıyorsun. Duvarlarda çatlaklar, etrafta eski mobilyalar var.",
        esyalar=["Eski Anahtar"]
    )
    oda1.ipucu = "Çatlaklar arasında bir şey parlıyor gibi. Belki de bu yolculuk için lazım olacak."

    oda2 = Oda(
        ad="Karanlık Salon",
        tanim="Gölge ve sisin arasında duyduğun uğultular seni endişelendiriyor.",
        esyalar=["Fener"]
    )
    oda2.ipucu = "Karanlığın içinden sağ çıktın… ama her şey hâlâ gölgede. Gerçekleri görmek için bir şeye ihtiyacın var."

    oda3 = Oda(
        ad="Eski Mahzen",
        tanim="Duvarlar eski mors alfabesiyle yazılı. Gölgelerin arkasında saklı mesajlar, seni özgürlüğe götürecek yolu işaret ediyor olabilir.",
        esyalar=["Kağıt parçası"]
    )
    oda3.ipucu = "Gizli dili anlamanın anahtarı, kağıt parçasında saklı. O sayılar sana ne söylüyor olabilir?"

    oda4 = KilitliOda(
        ad="Çıkış Odası",
        tanim="Evin en son odası.",
        esyalar=[],
        kilitli=True,
        gerekli_esyalar=("Kaçış Anahtarı", "Eski Anahtar")
    )

    odalar.extend([oda1, oda2, oda3, oda4])
    return odalar

def oyunu_baslat():
    print("\n*******************************")
    oyuncu_adi = input("Lütfen adını gir: ")
    oyuncu = Oyuncu(oyuncu_adi)

    odalar = odalari_olustur()
    oyuncu.bulundugu_oda = odalar[0]
    print(oyuncu.bulundugu_oda.bilgi_goster())

    bulmaca_hakki = 3

    while True:
        print("\nKomutlar: topla, ipucu, envanter, git, bulmaca, kilitac, çık")
        komut = input("Bir komut girin: ")

        if komut == "topla":  
            esya_topla(oyuncu.bulundugu_oda, oyuncu)

        elif komut == "ipucu":
            ipucu_goster(oyuncu.bulundugu_oda)

        elif komut == "envanter":
            oyuncu.envanteri_goster()

        elif komut == "git":
            print("Hangi odaya gitmek istersin?")
            for i, oda in enumerate(odalar):  #Oda listesini numaralandırarak gösterir
                print(f"{i}: {oda.ad}")
            hedef = int(input("Oda numarasını gir: "))
            if 0 <= hedef < len(odalar):  
                if isinstance(odalar[hedef], KilitliOda) and odalar[hedef].kilitli:
                    print("Bu oda kilitli. Önce kapıyı açmalısın ('kilitac' komutunu kullan).")
                else:
                    oda_degistir(odalar, oyuncu, hedef)
                    if oyuncu.bulundugu_oda.ad == "Karanlık Salon":
                        if not yaratık_olayi(oyuncu):  #yaratık olayı sonucu
                            print("Maalesef oyunu kaybettin!")
                            return

        elif komut == "bulmaca":
            if oyuncu.bulundugu_oda.ad != "Eski Mahzen":
                print("Bu odada bulmaca bulunmuyor.")
                continue

            if bulmaca_hakki <= 0:
                print("Ne yazık ki tüm bulmaca çözme haklarını tükettin.")
                break

            sonuc = mors_bulmaca(oyuncu)

            if sonuc is None:
                continue

            bulmaca_hakki -= 1

            if sonuc:
                continue

        elif komut == "kilitac":
            print("Hangi odanın kapısını açmak istiyorsun?")
            kilitli_odalar = []
            for i, oda in enumerate(odalar):
                if isinstance(oda, KilitliOda) and oda.kilitli:  #kilit kontrolü
                    kilitli_odalar.append(i)
            if kilitli_odalar:
                hedef = int(input("Oda numarasını gir: "))
                if hedef in kilitli_odalar:
                    odalar[hedef].kilidi_ac(oyuncu)
                else:
                    print("Seçtiğin oda kilitli değil.")

        elif komut == "çık":
            print("Oyunu sonlandırıyorsun. Çıkış yapılıyor...")
            break

        if isinstance(oyuncu.bulundugu_oda, KilitliOda) and not oyuncu.bulundugu_oda.kilitli:
            print(f"\nTebrikler {oyuncu_adi}, kaçmayı başardın!")
            break

    print("\nOYUN BİTTİ.")
    print("*******************************")
oyunu_baslat()
