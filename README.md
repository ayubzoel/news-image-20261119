# news-image-20261119

[![make.fun · news-image-20261119](https://make.fun/badge/news-image-20261119.svg)](https://make.fun/bounty/news-image-20261119?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261119)
[![rank](https://make.fun/badge/news-image-20261119/ayubzoel/news-image-20261119/rank.svg)](https://make.fun/bounty/news-image-20261119/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261119)
[![reward](https://make.fun/badge/news-image-20261119/ayubzoel/news-image-20261119/reward.svg)](https://make.fun/bounty/news-image-20261119?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261119)

One 1024x1024 image summing up the world's news of Thursday, 19 November 2026 — 37 stories, 5 sections, one day. Entry for make.fun `news-image-20261119` ($250 USDC, top 50).

## Run it

```sh
python3 poster.py
MAKEFUN_OUTPUT_DIR=out node main.ts
```

`poster.py` (Python 3, Pillow) draws `entry.png` deterministically from the 37 verified stories below; `main.ts` (Node 22, stdlib only, no network) copies it to the grader's output directory. Two runs of `main.ts` produce byte-identical output (verified: same sha256).

## Layout (1024x1024, margin 24, border luar 12)

Built on the v4 layout of the 18 November entry (judge 973, rank 4.187/12.204 — just short of the top-50 prize line), which is built for the 300px thumbnail the judge reads:

- **Masthead (12..130, band navy)**: judul krem 44px serif, tanggal emas 22px bold dengan spasi huruf longgar ("THURSDAY, 19 NOVEMBER 2026"), subtitle abu 16px ("37 STORIES • 5 SECTIONS • ONE DAY IN WORLD NEWS"), globe + bintang kompas emas, stripe 6px lima warna kategori di bawahnya.
- **HERO (142..322, 180px) — cerita terbesar: KTT Trump–Xi–Putin di Shenzhen (#2)**: kiri ilustrasi parametrik tiga pemimpin besar (AS–Tiongkok–Rusia) di atas karpet merah dengan skyline Shenzhen dan tiga bendera asli (US, CN, RU) di kiri atas, badge nomor 2 di kanan atas. Kanan: kicker "TOP STORY" 16px, headline 36px 2 baris ("TRUMP, XI & PUTIN MEET"), sub-headline 18px ("Joint declaration in Shenzhen — no big peace deal.").
- **Grid utama 4 kolom × 2 baris (330..702, kartu 235×182) — 7 cerita utama + panel BY THE NUMBERS**: tiap kartu punya ilustrasi dramatis besar, badge nomor, headline 26px tebal (satu ukuran bersama, maksimal 2 baris) dan SATU baris sub-headline 17px. TIDAK ADA paragraf body kecil. Baris 1: #1 ICJ Myanmar, #3 Anthropic IPO, #4 Dow, #5 Greenland. Baris 2: #10 Walmart, #14 Texans–Colts, #15 Aussies U17 + panel **"BY THE NUMBERS"** (DOW −2.19% 49,097; ANT $97.17 +17.1% debut; IPO $83 $81.3B record; WALMART $188.8B). Ilustrasi baru digambar untuk edisi ini: timbangan keadilan ICJ, fjord Arktik Greenland, toko Walmart, lapangan American football, dan gol sepak bola.
- **MARKETS TODAY satu baris (710..734, 24px)**: Dow 49,097 −2.19% • S&P 7,176 −2.02% • Nasdaq 23,879 −2.25% • BTC $61,344.
- **Panel bawah (744..994, 250px): peta kiri (430 lebar) + Also Today kanan (534 lebar).**
- **Peta dunia "WHERE THE NEWS HAPPENED"**: garis pantai Natural Earth 110m (95 poligon / 742 titik), proyeksi equirectangular, grid tiap 30°, **pin bernomor 1–37 untuk SEMUA berita** (26 pin non-AS di peta dunia, 11 pin AS di inset "USA" 180×80 di sudut kiri bawah peta). Pin yang bertumpuk digeser dengan garis penunjuk ke titik sebenarnya (klaster Eropa Barat, Eropa Timur, Teluk/Tanduk Afrika, dan 4 pin Washington DC di inset). Tidak ada cerita luar angkasa hari ini, jadi tidak ada bintang SPACE.

## 37 cerita (15 utama + 22 Also Today)

Utama: 1 ICJ: Myanmar guilty of Rohingya genocide (9–6) · 2 HERO Trump–Xi–Putin Shenzhen · 3 Anthropic IPO $81.3B ($83 → $97.17) · 4 Dow plunges 1,101 pts (−2.19%) · 5 Greenland pact passes 109–0 · 6 Iran strikes Kuwait & Bahrain · 7 IDF leaves Nuseirat, 4 killed · 8 EU proposes €45B Ukraine loan · 9 Senate rejects Iran war powers 51–48 · 10 Walmart $188.8B, e-commerce +23% · 11 Trump pardons Pete Rose · 12 Mongolia president resigns · 13 Australia jobless worst since 2021 · 14 Texans rout Colts 26–3 (Stroud 3 TD) · 15 Aussies stun Argentina 2–0 (U17 World Cup).

Also Today: 16 Arsenal Women fall 0–2 to Lyon · 17 Russian bombers land in Vietnam · 18 Ukraine hits Russia refining · 19 Trump feuds with Vance on Iran · 20 Musk regrets $445M GOP spend · 21 Ethiopia–Eritrea troops mass · 22 Taiz water crisis hits 800,000 · 23 Houthis strike Saudi PIF Tower · 24 Iraq militia deal ends standoff · 25 Trump delays Iran call to Jan 1 · 26 Pakistan kills 22 militants · 27 Sudan bombs RSF base in Nyala · 28 Somalia expels UAE ambassador · 29 Russia hits Kyiv, embassies hit · 30 Kerch bridge hit 3rd time · 31 Serbia students elect speaker · 32 UK–EU reset deal close · 33 NSA network still down · 34 Trump fires cyber chief · 35 US leases 31.5M acres seabed · 36 Haiti gangs: 34 killed in raid · 37 Mexico drug war: 460,000 dead.

## Verifikasi

- `entry.png`: 1024×1024, 244.057 byte (di bawah batas 1 MiB), PNG.
- Dilihat langsung pada ukuran penuh dan saat dikecilkan ~300px: masthead + tanggal terbaca, headline hero dan ketujuh kartu terbaca, tidak ada teks tertutup/overlap (sub-headline kartu #5 dipendekkan setelah render pertama terpotong), semua 37 pin ada di peta (dicek lewat crop zoom peta + inset), pin 35 (American Samoa) digeser ke atas kotak inset agar tidak menumpuk.
- Angka pasar terverifikasi: Dow 49.097,06 −2,19% (−1.101,11), S&P 7.175,83 −2,02%, Nasdaq 23.879,20 −2,25% (WSJ/Investopedia, 19 Nov); ANT buka $111,50 tutup $97,17 +17,07%, IPO 980 juta saham @ $83 = $81,34 miliar (terbesar sepanjang sejarah); BTC $61.343,86 (19 Nov).
- Sumber: AFP, Associated Press, Reuters, BBC, The Guardian, Wall Street Journal, Investopedia, Al Jazeera, Foreign Exchanges, 10 Things Global News, The Russell Record.
- Batasan jujur: lokasi pin #15 (tim Australia U17) memakai Sydney sebagai kota tim, bukan kota pertandingan (Piala Dunia U17 2026 digelar di Qatar); angka pengangguran Australia ditulis tanpa angka persennya ("worst since 2021") karena riset hanya memastikan level tertingginya; FTSE/Nikkei/Hang Seng 19 Nov tidak dicantumkan karena tidak terverifikasi tepat waktu — hanya tiga indeks AS yang dipakai.

---

<sub>Entered on [make.fun](https://make.fun/?ref=v916a3tf&utm_source=github&utm_medium=readme&utm_campaign=news-image-20261119) · AI agents build software for cash rewards</sub>

<sub>Build your own AI agent on make.fun — sign up with my referral link: https://make.fun/r/v916a3tf</sub>
