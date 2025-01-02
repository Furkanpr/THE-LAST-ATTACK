import pygame
import random
import sys
import os

# Pygame'i başlat
pygame.init()

# Ekran boyutları
GENISLIK, YUKSEKLIK = 800, 600
ekran = pygame.display.set_mode((GENISLIK, YUKSEKLIK))
pygame.display.set_caption("Uzay Oyunu")

# Varlıkları yükle
arkaPlanlar = [
    pygame.image.load("arka_plan1.jpg"),
    pygame.image.load("arka_plan2.jpg"),
    pygame.image.load("arka_plan3.jpg")
]
oyuncuResmi = pygame.image.load("uzay_gemi.png")
oyuncuMermiResmi = pygame.image.load("01.png")
dusmanResmi = pygame.image.load("uzayli.png")
dusmanMermiResmi = pygame.image.load("02.png")
anaSayfaResmi = pygame.image.load("ana_sayfa.jpg")

# Resmi ekran boyutlarına göre yeniden boyutlandır
anaSayfaResmi = pygame.transform.scale(anaSayfaResmi, (GENISLIK, YUKSEKLIK))

# Sesler
pygame.mixer.music.load("MenuMusic.mp3")
oyuncuAtesSesi = pygame.mixer.Sound("oyuncu_mermi.wav")
oyuncuVurulmaSesi = pygame.mixer.Sound("oyuncu_vurus.wav")
dusmanAtesSesi = pygame.mixer.Sound("uzayli_mermi2.wav")
dusmanVurulmaSesi = pygame.mixer.Sound("uzayli_vurus.wav")

# Yazı tipi
yaziTipi = pygame.font.Font("oyun_font.ttf", 24)

# Renkler
BEYAZ = (255, 255, 255)
KIRMIZI = (255, 0, 0)
YESIL = (0, 255, 0)
MAVI = (0, 0, 255)
ACIK_MAVI = (173, 216, 230)

# Oyun değişkenleri
oyuncuX = GENISLIK // 2
oyuncuY = YUKSEKLIK - 100
oyuncuHizi = 5
oyuncuMermileri = []

dusmanlar = []
dusmanMermileri = []
skor = 0
can = 5
seviye = 1

# Skor dosyası
SKOR_DOSYASI = "skorlar.txt"

# Düşmanları oluştur
def dusmanlariOlustur():
    for _ in range(5 + seviye * 2):
        x = random.randint(0, GENISLIK - dusmanResmi.get_width())
        y = random.randint(50, 200)  # Düşmanlar ekranın üst kısmında başlıyor
        yon = random.choice([-1, 1])  # Başlangıç yönü rastgele
        dusmanlar.append([x, y, yon])

# Oyunu sıfırla
def oyunuSifirla():
    global oyuncuX, oyuncuY, oyuncuMermileri, dusmanlar, dusmanMermileri, skor, can, seviye
    oyuncuX = GENISLIK // 2
    oyuncuY = YUKSEKLIK - 100
    oyuncuMermileri = []
    dusmanlar = []
    dusmanMermileri = []
    skor = 0
    can = 5
    seviye = 1
    dusmanlariOlustur()

# Skorları yükle
def skorlarıYukle():
    if not os.path.exists(SKOR_DOSYASI):
        return []
    with open(SKOR_DOSYASI, "r") as dosya:
        skorlar = [int(skor.strip()) for skor in dosya.readlines()]
    return skorlar

# Skorları kaydet
def skorlarıKaydet(yeni_skor):
    skorlar = skorlarıYukle()
    skorlar.append(yeni_skor)
    skorlar = sorted(skorlar, reverse=True)[:5]  # En yüksek 5 skoru tut
    with open(SKOR_DOSYASI, "w") as dosya:
        for skor in skorlar:
            dosya.write(f"{skor}\n")


def menuGoster():
    pygame.mixer.music.play(-1)  # Menü müziğini çal
    ekran.blit(anaSayfaResmi, (0, 0))



    # Yazı renkleri ve buton içi rengi
    yazRengi = (0, 0, 0)  # Siyah yazı
    butonRengi = (255, 255, 255)  # Beyaz buton içi
    cerceveRengi = (0, 0, 0)  # Siyah çerçeve

    # Buton yazılarını oluştur
    baslaButon = yaziTipi.render("Başla", True, yazRengi)
    skorButon = yaziTipi.render("Skorlar", True, yazRengi)
    cikisButon = yaziTipi.render("Çıkış", True, yazRengi)
    seceneklerButon = yaziTipi.render("Seçenekler", True, yazRengi)

    # Düğmelerin merkez noktalarını ayarla

    butonMerkezler = [
    (GENISLIK // 2 - 300, YUKSEKLIK - 100),
    (GENISLIK // 2 - 100, YUKSEKLIK - 100),
    (GENISLIK // 2 + 100, YUKSEKLIK - 100),
    (GENISLIK // 2 + 300, YUKSEKLIK - 100),
]


    # Butonların dikdörtgenlerini oluştur
    baslaRect = baslaButon.get_rect(center=butonMerkezler[0])
    skorRect = skorButon.get_rect(center=butonMerkezler[2])
    cikisRect = cikisButon.get_rect(center=butonMerkezler[3])
    seceneklerRect = seceneklerButon.get_rect(center=butonMerkezler[1])

    # Butonları ve çerçevelerini ekrana çiz
    for rect in [baslaRect, seceneklerRect,skorRect, cikisRect ]:
        pygame.draw.rect(ekran, butonRengi, rect.inflate(20, 10))  # Buton arka planı
        pygame.draw.rect(ekran, cerceveRengi, rect.inflate(20, 10), 2)  # Çerçeve

    # Yazıları ekrana çiz
    ekran.blit(baslaButon, baslaRect)
    ekran.blit(seceneklerButon, seceneklerRect)
    ekran.blit(skorButon, skorRect)
    ekran.blit(cikisButon, cikisRect)


    pygame.display.flip()

    # Etkileşim döngüsü
    bekleniyor = True
    while bekleniyor:
        for olay in pygame.event.get():
            if olay.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif olay.type == pygame.MOUSEBUTTONDOWN:
                if baslaRect.collidepoint(olay.pos):
                    bekleniyor = False
                elif skorRect.collidepoint(olay.pos):
                    skorlarMenu()
                elif seceneklerRect.collidepoint(olay.pos):
                    seceneklerMenu()
                elif cikisRect.collidepoint(olay.pos):
                    pygame.quit()
                    sys.exit()



# Skorlar menüsü
def skorlarMenu():
    ekran.fill((0, 0, 0))
    geriButon = yaziTipi.render("Geri", True, BEYAZ, KIRMIZI)
    geriRect = geriButon.get_rect(center=(GENISLIK // 2, YUKSEKLIK - 50))
    ekran.blit(geriButon, geriRect)

    skorlar = skorlarıYukle()
    for i, skor in enumerate(skorlar):
        skorYazi = yaziTipi.render(f"{i + 1}. Skor: {skor}", True, BEYAZ)
        ekran.blit(skorYazi, (GENISLIK // 2 - skorYazi.get_width() // 2, 100 + i * 30))

    pygame.display.flip()

    bekleniyor = True
    while bekleniyor:
        for olay in pygame.event.get():
            if olay.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif olay.type == pygame.MOUSEBUTTONDOWN:
                if geriRect.collidepoint(olay.pos):
                    bekleniyor = False
                    menuGoster()

def seceneklerMenu():
    global sesAcik 
     # Ses durumu için global değişken
    bekleniyor = True
    while bekleniyor:
        arkaPlan = pygame.image.load('background2.jpg')  # Buraya resminizin yolunu yazın
        arkaPlan = pygame.transform.scale(arkaPlan, (GENISLIK, YUKSEKLIK))
        ekran.blit(arkaPlan, (0, 0))
        # Geri butonu   
        geriButon = yaziTipi.render("Geri", True, BEYAZ, KIRMIZI)
        geriRect = geriButon.get_rect(center=(GENISLIK // 2, YUKSEKLIK - 50))
        ekran.blit(geriButon, geriRect)

        # Ses kapatma/açma butonu
        sesAcik =True
        sesDurumu = "Kapat" if sesAcik else "Aç"
        sesButon = yaziTipi.render(f"Ses: {sesDurumu}", True, BEYAZ, KIRMIZI)
        sesRect = sesButon.get_rect(center=(GENISLIK // 2, YUKSEKLIK - 150))
        ekran.blit(sesButon, sesRect)

        pygame.display.flip()

        # Olayları dinleme
        for olay in pygame.event.get():
            if olay.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif olay.type == pygame.MOUSEBUTTONDOWN:
                if geriRect.collidepoint(olay.pos):
                    bekleniyor = False  # Döngüyü sonlandır
                    menuGoster()  # Ana menüye dön
                elif sesRect.collidepoint(olay.pos):
                    sesAcik = not sesAcik  # Ses durumunu değiştir
                    if sesAcik:
                        pygame.mixer.music.unpause()  # Müzik devam etsin
                    else:
                        pygame.mixer.music.pause()  # Müzik duraklasın






# Oyun sonu menüsü
def oyunSonuGoster(mesaj):
    # Arka plan için degrade renkler
    arkaPlanRenk1 = (135, 206, 250)  # Açık mavi
    arkaPlanRenk2 = (25, 25, 112)  # Gece mavisi
    for y in range(YUKSEKLIK):
        renk = (
            arkaPlanRenk1[0] + (arkaPlanRenk2[0] - arkaPlanRenk1[0]) * y // YUKSEKLIK,
            arkaPlanRenk1[1] + (arkaPlanRenk2[1] - arkaPlanRenk1[1]) * y // YUKSEKLIK,
            arkaPlanRenk1[2] + (arkaPlanRenk2[2] - arkaPlanRenk1[2]) * y // YUKSEKLIK
        )
        pygame.draw.line(ekran, renk, (0, y), (GENISLIK, y))

    # Mesaj ve butonlar
    oyunSonuYazi = yaziTipi.render(mesaj, True, (0, 0, 0))  # Siyah yazı
    yenidenBaslatButon = yaziTipi.render("Yeniden Başlat", True, (0, 0, 0))
    anaSayfaButon = yaziTipi.render("Ana Sayfaya Dön", True, (0, 0, 0))

    # Buton dikdörtgenleri
    yenidenBaslatRect = yenidenBaslatButon.get_rect(center=(GENISLIK // 2 - 150, YUKSEKLIK // 2))
    anaSayfaRect = anaSayfaButon.get_rect(center=(GENISLIK // 2 + 150, YUKSEKLIK // 2))

    # Buton arka planları ve çerçeveleri
    for rect in [yenidenBaslatRect, anaSayfaRect]:
        pygame.draw.rect(ekran, (255, 255, 255), rect.inflate(20, 10))  # Beyaz arka plan
        pygame.draw.rect(ekran, (0, 0, 0), rect.inflate(20, 10), 2)  # Siyah çerçeve

    # Yazıları ekrana çiz
    ekran.blit(oyunSonuYazi, oyunSonuYazi.get_rect(center=(GENISLIK // 2, YUKSEKLIK // 3)))
    ekran.blit(yenidenBaslatButon, yenidenBaslatRect)
    ekran.blit(anaSayfaButon, anaSayfaRect)
    pygame.display.flip()

    # Etkileşim döngüsü
    bekleniyor = True
    while bekleniyor:
        for olay in pygame.event.get():
            if olay.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif olay.type == pygame.MOUSEBUTTONDOWN:
                if yenidenBaslatRect.collidepoint(olay.pos):
                    bekleniyor = False
                    oyunuSifirla()
                elif anaSayfaRect.collidepoint(olay.pos):
                    bekleniyor = False
                    menuGoster()


# Oyun döngüsü

saat = pygame.time.Clock()
pygame.mixer.music.play(-1)

menuGoster()
oyunuSifirla()

calisiyor = True
while calisiyor:
    ekran.blit(arkaPlanlar[seviye - 1], (0, 0))

    for olay in pygame.event.get():
        if olay.type == pygame.QUIT:
            calisiyor = False

    # Oyuncu hareketi
    tuslar = pygame.key.get_pressed()
    if tuslar[pygame.K_LEFT] and oyuncuX > 0:
        oyuncuX -= oyuncuHizi
    if tuslar[pygame.K_RIGHT] and oyuncuX < GENISLIK - oyuncuResmi.get_width():
        oyuncuX += oyuncuHizi
    if tuslar[pygame.K_SPACE]:
        if len(oyuncuMermileri) < 5:
            oyuncuMermileri.append([oyuncuX + oyuncuResmi.get_width() // 2, oyuncuY])
            oyuncuAtesSesi.play()

    # Oyuncu mermilerini güncelle
    for mermi in oyuncuMermileri[:]:
        mermi[1] -= 7 + seviye
        if mermi[1] < 0:
            oyuncuMermileri.remove(mermi)
        else:
            ekran.blit(oyuncuMermiResmi, (mermi[0], mermi[1]))

    # Düşmanları güncelle
    for dusman in dusmanlar[:]:
        dusman[0] += dusman[2] * (2 + seviye)  # Düşman yatay hareket ediyor
        if dusman[0] <= 0 or dusman[0] >= GENISLIK - dusmanResmi.get_width():
            dusman[2] *= -1  # Yön değiştir

        ekran.blit(dusmanResmi, (dusman[0], dusman[1]))

        # Düşman ateşi
        if random.randint(0, 50 - seviye * 5) == 0:
            dusmanMermileri.append([dusman[0] + dusmanResmi.get_width() // 2, dusman[1]])
            dusmanAtesSesi.play()

    # Düşman mermilerini güncelle
    for mermi in dusmanMermileri[:]:
        mermi[1] += 2 + seviye
        if mermi[1] > YUKSEKLIK:
            dusmanMermileri.remove(mermi)
        elif (oyuncuX < mermi[0] < oyuncuX + oyuncuResmi.get_width() and
              oyuncuY < mermi[1] < oyuncuY + oyuncuResmi.get_height()):
            dusmanMermileri.remove(mermi)
            can -= 1
            oyuncuVurulmaSesi.play()
            if can <= 0:
                skorlarıKaydet(skor)
                oyunSonuGoster("Canınız bitti, kaybettiniz! Yeniden Başlat'a veya Ana Sayfaya Dön'e Tıklayın")
        else:
            ekran.blit(dusmanMermiResmi, (mermi[0], mermi[1]))

    # Çarpışmaları kontrol et
    for mermi in oyuncuMermileri[:]:
        for dusman in dusmanlar[:]:
            if (dusman[0] < mermi[0] < dusman[0] + dusmanResmi.get_width() and
                dusman[1] < mermi[1] < dusman[1] + dusmanResmi.get_height()):
                dusmanlar.remove(dusman)
                oyuncuMermileri.remove(mermi)
                skor += 10
                dusmanVurulmaSesi.play()

    # Seviye atla
    if not dusmanlar:
        seviye += 1
        if seviye > 3:
            skorlarıKaydet(skor)
            oyunSonuGoster("Kazandınız! Yeniden Başlat'a veya Ana Sayfaya Dön'e Tıklayın")
            oyunuSifirla()
        else:
            dusmanlariOlustur()

    # Oyuncuyu çiz
    ekran.blit(oyuncuResmi, (oyuncuX, oyuncuY))

    # Skor ve canı çiz
    skorYazi = yaziTipi.render(f"Skor: {skor}", True, BEYAZ)
    canYazi = yaziTipi.render(f"Can: {can}", True, BEYAZ)
    ekran.blit(skorYazi, (10, 10))
    ekran.blit(canYazi, (10, 40))

    pygame.display.flip()
    saat.tick(60)

pygame.quit()
sys.exit()