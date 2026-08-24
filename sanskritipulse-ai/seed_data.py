"""
SanskritiPulse AI - Data Engineering Pipeline
Seed Data Generator: 30 Distinct Karnataka Festivals
=====================================================
Generates a curated, culturally authentic, geographically validated dataset of 30 iconic
festivals of Karnataka with full metadata, geo-coordinates, historical provenance,
gastronomic highlights, footfall analytics, and semantic discovery tags.
"""

import json
import os
import sys
import argparse
from typing import List, Dict, Any
import pandas as pd
import numpy as np


# ---------------------------------------------------------------------------
# Authentic Raw Festival Repository (30 Distinct Karnataka Festivals)
# ---------------------------------------------------------------------------

FESTIVAL_RAW_DATA: List[Dict[str, Any]] = [
    {
        "id": "mysuru-dasara",
        "name": "Mysuru Dasara (Nada Habba)",
        "local_name": "ಮೈಸೂರು ದಸರಾ (ನಾಡಹಬ್ಬ)",
        "district": "Mysuru",
        "city": "Mysuru",
        "lat": 12.3051,
        "lng": 76.6551,
        "start_date": "2026-10-11",
        "end_date": "2026-10-20",
        "duration_days": 10,
        "season": "Sharad (Autumn / Navaratri)",
        "category": "State Festival & Royal Heritage",
        "description": "Celebrated as Karnataka's official state festival (Nada Habba), Mysuru Dasara is a 10-day extravaganza celebrating Goddess Chamundeshwari's victory over the demon Mahishasura. The heritage city illuminates with over 100,000 light bulbs at the Mysuru Palace, culminating in the grand Vijayadashami procession.",
        "cultural_significance": "Represents the triumph of righteousness (Dharma) over evil. It showcases Karnataka's rich royal lineage, royal darbar traditions, and unbroken cultural continuum preserved by the Wadiyar Dynasty.",
        "history": "Initiated in the 14th century by the Vijayanagara Empire kings as Mahanavami festival, later institutionalized in Srirangapatna by Raja Wadiyar I in 1610 and moved to Mysuru in 1799.",
        "attractions": [
            "Jamboo Savari (Grand Elephant Procession carrying the 750kg Golden Howdah)",
            "Illumination of Mysuru Palace with 100,000 bulbs",
            "Torchlight Parade at Bannimantap",
            "Yuva Dasara & Classical Music Concerts at Palace Courtyard",
            "Dasara Exhibition & Kushti (Traditional Wrestling) Tournament"
        ],
        "local_food": [
            "Mysore Pak (melt-in-mouth ghee sweet)",
            "Mysore Masala Dosa with red chili-garlic chutney",
            "Maddur Vada",
            "Nanjanagudu Rasabale (heritage GI banana)",
            "Mysore Chiroti with Badam Milk"
        ],
        "footfall": 1800000,
        "images": [
            {
                "url": "https://images.unsplash.com/photo-1600100397608-f010f443b749",
                "caption": "Mysore Palace illuminated with golden lights during Dasara",
                "is_primary": True
            },
            {
                "url": "https://images.unsplash.com/photo-1582510003544-4d00b7f74220",
                "caption": "Decorated lead tusker carrying the Golden Howdah during Jamboo Savari",
                "is_primary": False
            }
        ],
        "tags": ["heritage", "royal", "nada-habba", "mysuru-palace", "chamundeshwari", "elephant-procession", "unesco-style", "autumn"]
    },
    {
        "id": "kambala-buffalo-race",
        "name": "Kambala (Dakshina Kannada Traditional Buffalo Race)",
        "local_name": "ಕಂಬಳ (ಕರಾವಳಿಯ ಜಾನಪದ ಕ್ರೀಡೆ)",
        "district": "Dakshina Kannada",
        "city": "Moodabidri / Mangaluru",
        "lat": 13.0694,
        "lng": 74.9961,
        "start_date": "2026-11-21",
        "end_date": "2026-11-22",
        "duration_days": 2,
        "season": "Post-Monsoon / Winter",
        "category": "Folk Sports & Agrarian Heritage",
        "description": "An electrifying traditional folk sport where pairs of muscular water buffaloes driven by whip-wielding sprinters race down dual slushy paddy tracks (Kare) across Coastal Karnataka. Celebrated to appease gods for a bountiful harvest and livestock health.",
        "cultural_significance": "Deeply woven into the agrarian Tulu Nadu ethos and veneration of Lord Kadri Manjunatha and local Daivas (Bhootas) for harvest blessings and cattle protection.",
        "history": "Tracing back over 800 years to the Alupa and Hoysala dynasties, originally patronized by royal feudal landlords (Bunt households) as a test of speed and agricultural prowess.",
        "attractions": [
            "Hagga (Rope) and Kane Halage (Water Spout Height) sprint categories",
            "Laser beam sensor photo-finish timing",
            "Bhoota Kola and Daivaradhane folk invocations",
            "Traditional drum ensembles (Chande & Maddale)"
        ],
        "local_food": [
            "Neer Dosa with Kori Gassi (Mangalorean Chicken Curry)",
            "Kori Rotti (Crispy rice wafers in spiced gravy)",
            "Pathrode (steamed colocasia leaves)",
            "Mangalore Buns (banana-infused fluffy pooris)",
            "Shendi / Elaneer (Tender Coconut Payasa)"
        ],
        "footfall": 120000,
        "images": [
            {
                "url": "https://images.unsplash.com/photo-1596178065887-1198b6148b2b",
                "caption": "Jockey sprinting alongside paired water buffaloes in muddy waters",
                "is_primary": True
            }
        ],
        "tags": ["tulu-nadu", "folk-sport", "buffalo-race", "karavali", "agrarian", "mud-track", "adventure"]
    },
    {
        "id": "hampi-utsav",
        "name": "Hampi Utsav (Vijaya Utsava)",
        "local_name": "ಹಂಪಿ ಉತ್ಸವ (ವಿಜಯ ಉತ್ಸವ)",
        "district": "Vijayanagara",
        "city": "Hampi",
        "lat": 15.3350,
        "lng": 76.4600,
        "start_date": "2026-11-06",
        "end_date": "2026-11-08",
        "duration_days": 3,
        "season": "Winter / Karthika",
        "category": "Classical Arts & Heritage",
        "description": "A magnificent 3-day cultural symposium staged against the colossal UNESCO World Heritage ruins of the Vijayanagara Empire. The rugged boulder landscape and 15th-century stone temple complexes are brought alive with classical dance, music, laser shows, and rural folk arts.",
        "cultural_significance": "Commemorates the golden era of Emperor Krishnadevaraya and the Vijayanagara Empire's cultural, architectural, and literary brilliance.",
        "history": "Revived by the Government of Karnataka in modern times, rooted in the historical 'Vijaya Utsava' described by medieval foreign travelers Domingo Paes and Abdur Razzaq.",
        "attractions": [
            "Mega stages set against the backdrop of the illuminated Virupaksha Temple & Stone Chariot",
            "Sound and light spectacle across the Hemakuta and Matanga Hills",
            "Hampi by Night Heritage Walk and Coracle boating on Tungabhadra River",
            "Janapada Vahini (Folk street performance parade with Dollu Kunitha & Veeragase)"
        ],
        "local_food": [
            "Jolada Rotti with Yennegai (stuffed spicy brinjal)",
            "Shenga (Peanut) Chutney Pudi & Ranjaka (red chilli paste)",
            "Koppal style Godhi Huggi (cracked wheat jaggery porridge)",
            "Badam Milk & Belagavi Kunda"
        ],
        "footfall": 350000,
        "images": [
            {
                "url": "https://images.unsplash.com/photo-1600100397906-8d195c8053a4",
                "caption": "Illuminated Stone Chariot and Vittala Temple during Hampi Utsav",
                "is_primary": True
            }
        ],
        "tags": ["unesco", "vijayanagara", "classical-dance", "krishnadevaraya", "monuments", "tungabhadra", "heritage"]
    },
    {
        "id": "bengaluru-karaga",
        "name": "Bengaluru Karaga Shaktyotsava",
        "local_name": "ಬೆಂಗಳೂರು ಕರಗ ಶಕ್ತ್ಯೋತ್ಸವ",
        "district": "Bengaluru Urban",
        "city": "Bengaluru (Thigalarapet / Old Pete)",
        "lat": 12.9698,
        "lng": 77.5847,
        "start_date": "2026-04-01",
        "end_date": "2026-04-02",
        "duration_days": 2,
        "season": "Spring (Chaitra Poornima)",
        "category": "Religious & Folk Tradition",
        "description": "Bengaluru's oldest continuous festival celebrated by the Vahnikula Kshatriya (Thigala) community. A floral pyramid-shaped earthen pot (Karaga) symbolizing Draupadi Shakti is balanced on the head of the priest, who walks through the heart of the old city throughout the midnight hours without dropping a single petal.",
        "cultural_significance": "A rare confluence of Mahabharata epic veneration and inter-faith harmony, highlighted by the Karaga procession visiting the historic Hazrat Tawakkal Mastan Dargah.",
        "history": "Celebrated uninterrupted for over 300 years since the era of Magadi Kempe Gowda and the founding of Pete Bangalore.",
        "attractions": [
            "Midnight floral Karaga emergence from Sri Dharmaraya Swamy Temple",
            "Veerakumaras performing martial sword salutes (Alagu Sevai)",
            "Visit to Hazrat Tawakkal Mastan Dargah upholding communal brotherhood",
            "Illuminated traditional flower market (K.R. Market Pete) night walks"
        ],
        "local_food": [
            "Bengaluru Benne Masala Dosa",
            "Chitranna (Lemon rice) and Puliyogare Prasada",
            "Badam Halwa and Holige",
            "Congress Kadlekai (Spiced peanuts)",
            "Filter Coffee"
        ],
        "footfall": 550000,
        "images": [
            {
                "url": "https://images.unsplash.com/photo-1567157577867-05ccb1388e66",
                "caption": "Dharmaraya Swamy Temple night lights during Bengaluru Karaga",
                "is_primary": True
            }
        ],
        "tags": ["bengaluru", "karaga", "draupadi", "midnight-procession", "thigala", "interfaith-harmony", "pete"]
    },
    {
        "id": "pattadakal-dance-festival",
        "name": "Pattadakal Dance & Music Festival",
        "local_name": "ಪಟ್ಟದಕಲ್ಲು ನೃತ್ಯೋತ್ಸವ",
        "district": "Bagalkote",
        "city": "Pattadakal",
        "lat": 15.9483,
        "lng": 75.8166,
        "start_date": "2026-01-16",
        "end_date": "2026-01-18",
        "duration_days": 3,
        "season": "Winter / Magha",
        "category": "Classical Dance & Heritage",
        "description": "A prestigious national classical dance festival staged against the 8th-century UNESCO World Heritage sandstone temples of Pattadakal on the banks of Malaprabha River. India's top exponents of Bharatanatyam, Kathak, Odissi, and Kuchipudi perform before the magnificent Virupaksha and Mallikarjuna shrines.",
        "cultural_significance": "Celebrates the synthesis of Dravidian and Nagara temple architectural styles pioneered by the Early Badami Chalukyas.",
        "history": "Pattadakal was the ceremonial coronation city (Pattada-Kallu) of the Badami Chalukya emperors from 543 to 753 CE.",
        "attractions": [
            "Open-air classical recitals under night illumination of 8th-century temple facades",
            "Exhibition of North Karnataka handloom textiles (Ilkal Sarees & Guledgudda Khana)",
            "Sculpture appreciation tours of Chalukyan epics carved in stone"
        ],
        "local_food": [
            "Sajje (Pearl Millet) Rotti with Shenga Chutney",
            "Jowar Rotti with sprouted Moong Usli",
            "Ilkal style Gulbarga Shenga Holige (Jaggery peanut flatbread)",
            "Girmit (North Karnataka spiced puffed rice) with Mirchi Bajji"
        ],
        "footfall": 65000,
        "images": [
            {
                "url": "https://images.unsplash.com/photo-1548013146-72479768bada",
                "caption": "Illuminated Pattadakal temple complex during the national dance festival",
                "is_primary": True
            }
        ],
        "tags": ["pattadakal", "chalukya", "classical-dance", "unesco", "malaprabha", "bagalkote", "architecture"]
    },
    {
        "id": "vairamudi-brahmotsava",
        "name": "Melukote Vairamudi Brahmotsava",
        "local_name": "ಮೇಲುಕೋಟೆ ವೈರಮುಡಿ ಬ್ರಹ್ಮೋತ್ಸವ",
        "district": "Mandya",
        "city": "Melukote",
        "lat": 12.6631,
        "lng": 76.6558,
        "start_date": "2026-03-28",
        "end_date": "2026-03-29",
        "duration_days": 2,
        "season": "Spring (Phalguna Shuddha Pushya)",
        "category": "Temple & Sacred Ritual",
        "description": "One of South India's most venerated Vaishnavite festivals where Lord Cheluvanarayana Swamy is adorned with the legendary diamond-studded crown (Vairamudi) and taken out in a solemn midnight procession through the hill town of Melukote under high security.",
        "cultural_significance": "Associated with Sri Ramanujacharya who revived Melukote in the 12th century. According to legend, the diamond crown was originally bestowed upon Lord Vishnu by Garuda.",
        "history": "Celebrated for nearly a millennium since the Hoysala era under King Vishnuvardhana and Ramanujacharya's stay.",
        "attractions": [
            "Arrival of the ancient diamond crown under District Treasury armed escort",
            "Midnight Garuda Vahana procession of Lord Cheluvanarayana Swamy",
            "Kalyani stepwell holy dip and Raja Gopura illumination",
            "Vedic chanting and Divya Prabhandam recitations by Vaishnava scholars"
        ],
        "local_food": [
            "Melukote Puliyogare (famous temple tamarind rice with aromatic spices)",
            "Melukote Sweet Pongal / Sarkarai Pongal",
            "Akaravadisal (traditional jaggery milk dessert)",
            "Mandya Sugarcane Juice & Maddur Vada"
        ],
        "footfall": 250000,
        "images": [
            {
                "url": "https://images.unsplash.com/photo-1621847468516-1ed5d0df56fe",
                "caption": "Melukote Cheluvanarayana Swamy Temple Kalyani stepped tank",
                "is_primary": True
            }
        ],
        "tags": ["melukote", "vairamudi", "ramanujacharya", "mandya", "puliyogare", "temple-jewels", "vaishnavite"]
    },
    {
        "id": "kadambotsava-banavasi",
        "name": "Kadambotsava (Banavasi Heritage Festival)",
        "local_name": "ಕದಂಬೋತ್ಸವ (ಬನವಾಸಿ)",
        "district": "Uttara Kannada",
        "city": "Banavasi",
        "lat": 14.5367,
        "lng": 75.0125,
        "start_date": "2026-12-11",
        "end_date": "2026-12-13",
        "duration_days": 3,
        "season": "Winter / Hemanta",
        "category": "Historical & Literary Festival",
        "description": "Celebrated at Banavasi, the ancient 4th-century capital of the Kadamba Dynasty (first native Kannada empire). The festival honors Adikavi Pampa's immortal words that one must be born in Banavasi even as a bee to experience its sublime beauty, presenting state literary awards and traditional Yakshagana.",
        "cultural_significance": "Honors the inception of Kannada statehood and literature, conferring the prestigious 'Pampa Prashasti' state award to eminent scholars.",
        "history": "Banavasi was founded around 345 CE by King Mayurasharma of the Kadamba Dynasty, mentioned in Ashokan edicts and Ptolemy's geographical records.",
        "attractions": [
            "Presentation of the coveted Pampa Prashasti state literary award",
            "All-night Tenku and Badagu Thittu Yakshagana performances",
            "Madhukeshwara Temple sound and light presentation along the Varada River",
            "Malnad agricultural and spices exhibition"
        ],
        "local_food": [
            "Appemidi Pickle (fragrant GI tender wild mango pickle)",
            "Todadevu (wafer-thin sugarcane/jaggery crepe)",
            "Halasina Hannina Kadubu (steamed jackfruit cake in teak leaves)",
            "Malnad Kotte Kadubu with coconut chutney"
        ],
        "footfall": 75000,
        "images": [
            {
                "url": "https://images.unsplash.com/photo-1590076215667-875d4ef2d7ee",
                "caption": "Banavasi ancient temple architecture during Kadambotsava",
                "is_primary": True
            }
        ],
        "tags": ["banavasi", "kadamba", "pampa", "kannada-literature", "madhukeshwara", "malnad", "yakshagana"]
    },
    {
        "id": "tula-sankramana-talakaveri",
        "name": "Tula Sankramana (Kaveri Theerthodbhava)",
        "local_name": "ತುಲಾ ಸಂಕ್ರಮಣ (ಕಾವೇರಿ ತೀರ್ಥೋದ್ಭವ)",
        "district": "Kodagu",
        "city": "Talakaveri / Bhagamandala",
        "lat": 12.3856,
        "lng": 75.4920,
        "start_date": "2026-10-17",
        "end_date": "2026-10-18",
        "duration_days": 2,
        "season": "Sharad (Tula Month Transition)",
        "category": "Sacred River Pilgrimage & Eco-Spiritual",
        "description": "At a predetermined auspicious astrological second in the Brahmagiri Hills, Mother River Kaveri springs forth as a sudden holy gush of water in the sacred square pond (Brahma Kundike). Tens of thousands of Kodava families and pilgrims gather in mist-shrouded Talakaveri to witness the miracle and collect the divine waters.",
        "cultural_significance": "Kaveri is the lifeblood and supreme mother deity of Kodagu. Kodava brides venerate Kaveri water during weddings, and every household keeps a sacred pitcher filled with this water.",
        "history": "Mentioned in the Kaveri Purana section of the Skanda Purana, celebrated since time immemorial as the perennial birth of River Kaveri.",
        "attractions": [
            "Theerthodbhava bubbling moment at Brahma Kundike at Talakaveri",
            "Holy bath (Snana) and rituals at Triveni Sangama in Bhagamandala",
            "Traditional Kodava attire displays (Kupya Chele and traditional sarees)",
            "Scenic cloudscape atop Brahmagiri Peak trail"
        ],
        "local_food": [
            "Kadambuttu (Steamed rice flour dumplings) with spicy curry",
            "Akki Rotti with Ellu Pajji (roasted sesame chutney)",
            "Paputtu (steamed rice cake with coconut and milk)",
            "Coorg Kaapi (filter coffee with fresh estate cardamom)",
            "Kummu (Wild mushroom) curry (seasonal delicacy)"
        ],
        "footfall": 125000,
        "images": [
            {
                "url": "https://images.unsplash.com/photo-1506744038136-46273834b3fb",
                "caption": "Misty Western Ghats sunrise over Talakaveri Brahmagiri hills",
                "is_primary": True
            }
        ],
        "tags": ["talakaveri", "kodagu", "kaveri-river", "theerthodbhava", "kodava", "pilgrimage", "western-ghats"]
    },
    {
        "id": "chalukya-utsava-badami",
        "name": "Chalukya Utsava (Badami & Aihole Heritage Fest)",
        "local_name": "ಚಾಲುಕ್ಯ ಉತ್ಸವ (ಬಾದಾಮಿ & ಐಹೊಳೆ)",
        "district": "Bagalkote",
        "city": "Badami & Aihole",
        "lat": 15.9189,
        "lng": 75.6798,
        "start_date": "2026-02-06",
        "end_date": "2026-02-08",
        "duration_days": 3,
        "season": "Winter / Shishira",
        "category": "Heritage & Historical",
        "description": "Celebrated across the red sandstone cliffs of Badami (Vatapi) and the temple cradle of Aihole. Features rock-cut cave temple light projections, folk theatre, martial art demonstrations, and classical music reflecting the reign of King Pulakeshin II.",
        "cultural_significance": "Celebrates the architectural crucible where Hindu temple architecture (rock-cut caves, structural temples) was first experimented with and perfected in South India.",
        "history": "Commemorates the Badami Chalukyas who ruled from 540 CE to 757 CE, establishing an empire spanning the Deccan.",
        "attractions": [
            "Laser mapping over the red cliff face of Agastya Lake & Badami Caves",
            "Classical performances in the courtyard of Aihole's Durga Temple",
            "Rock climbing competitions on Badami's world-famous sandstone crags",
            "Chalukyan historical drama enactments"
        ],
        "local_food": [
            "Jolada Rotti with Shenga Pudi and Gural Chutney",
            "Badami style Kadabu with spicy lentil sambar",
            "North Karnataka Mirchi Bajji with Mandakki",
            "Belagavi Kunda & Dharwad Pedha"
        ],
        "footfall": 110000,
        "images": [
            {
                "url": "https://images.unsplash.com/photo-1596401057633-54a8fe8ef647",
                "caption": "Agastya Lake and Bhutanatha Temple at Badami during Chalukya Utsava",
                "is_primary": True
            }
        ],
        "tags": ["badami", "aihole", "chalukya", "rock-cut-caves", "agastya-lake", "pulakeshin", "heritage"]
    },
    {
        "id": "gavisiddheshwara-jatre-koppal",
        "name": "Koppal Gavisiddheshwara Jatre (Mahadasoha)",
        "local_name": "ಕೊಪ್ಪಳ ಗವಿಸಿದ್ದೇಶ್ವರ ಮಹಾ ರಥೋತ್ಸವ ಮತ್ತು ಮಹಾದಾಸೋಹ",
        "district": "Koppal",
        "city": "Koppal",
        "lat": 15.3486,
        "lng": 76.1554,
        "start_date": "2026-01-04",
        "end_date": "2026-01-10",
        "duration_days": 7,
        "season": "Winter (Pushya Bahula)",
        "category": "Spiritual Mass Congregation & Dasoha",
        "description": "Renowned across India as the 'Kumbh Mela of South India', this monumental spiritual gathering at Sri Gavisiddheshwara Matha draws over 2 million devotees. Celebrated with an emphasis on environmental conservation, non-violence, eye donations, and voluntary mass community feeding (Dasoha).",
        "cultural_significance": "Exemplifies the Lingayat philosophy of Kayaka (work is worship) and Dasoha (unconditional selfless mass feeding), with over 100,000 volunteers cooking and serving meals simultaneously.",
        "history": "Tracing back to the 12th-century Veerashaiva saint lineage of the Gavimatha cave hermits in the hills of Koppal.",
        "attractions": [
            "Lifting and pulling of the colossal 65-foot Brahma Ratha by a sea of lakhs of devotees",
            "Mahadasoha: Serving over 1.5 million rotis, madike kaalu, and sweets per day",
            "Mass public pledge campaigns for tree plantation, blood donation, and organ pledges",
            "Dazzling nighttime fireworks and Bhajan sessions"
        ],
        "local_food": [
            "Hot Jolada Rotti with Shenga Chutney and Junka",
            "Madike Kaalu Palya (Sprouted moth bean curry)",
            "Gavi Matha Boondi Laddu & Godhi Huggi Prasada",
            "Sajje Rotti with homemade churned white butter"
        ],
        "footfall": 2200000,
        "images": [
            {
                "url": "https://images.unsplash.com/photo-1544717305-2782549b5136",
                "caption": "Massive congregation of over a million devotees at Koppal Gavi Matha",
                "is_primary": True
            }
        ],
        "tags": ["koppal", "gavimatha", "dasoha", "kumbh-mela-south", "jatre", "chariot-pulling", "lingayat", "charity"]
    },
    {
        "id": "sirsi-marikamba-jatre",
        "name": "Sirsi Marikamba Jatre (Goddess Marikamba Fair)",
        "local_name": "ಶಿರಸಿ ಮಾರಿಕಾಂಬಾ ಜಾತ್ರೆ",
        "district": "Uttara Kannada",
        "city": "Sirsi",
        "lat": 14.6195,
        "lng": 74.8354,
        "start_date": "2026-03-03",
        "end_date": "2026-03-11",
        "duration_days": 9,
        "season": "Spring (Biennial in Phalguna)",
        "category": "Folk Fair & Temple Car",
        "description": "Karnataka's largest biennial folk temple fair celebrating Sri Marikamba Devi, the fierce guardian deity of the Malnad region. A monumental 8-day festival where the Goddess is seated on an intricately carved giant wooden chariot and taken out in a state-wide celebration.",
        "cultural_significance": "A vibrant celebration of Malnad folk culture, where devotees perform vows (Seve), carry sacred neem leaf pots, and celebrate the deity as protector against epidemics and misfortune.",
        "history": "The temple was consecrated in 1688 CE by the Sonda King Basavappa Nayaka, who brought the high-spirited sandalwood idol from Hanagal.",
        "attractions": [
            "Procession of the massive wooden ratha through the forested town of Sirsi",
            "Bedaravesha and traditional folk theatrical mask performances",
            "Grand Malnad agricultural fair and giant Ferris wheels",
            "Hagalu Vesha folk dancers and Chande percussionists"
        ],
        "local_food": [
            "Halasina Hannina Kadubu (Jackfruit sweet parcels)",
            "Bakshya (Holige) with hot coconut milk",
            "Sirsi Banana Chips fried in pure coconut oil",
            "Malnad Tambuli (cooling herbal yoghurt soup)"
        ],
        "footfall": 850000,
        "images": [
            {
                "url": "https://images.unsplash.com/photo-1609743522653-52354461cf27",
                "caption": "Decorated wooden chariot during Sirsi Marikamba Fair",
                "is_primary": True
            }
        ],
        "tags": ["sirsi", "marikamba", "malnad", "jatre", "biennial", "chariot", "folk-deity", "uttara-kannada"]
    },
    {
        "id": "saundatti-yellamma-jatre",
        "name": "Saundatti Yellamma Devi Jatre (Banada Hunnime)",
        "local_name": "ಸವದತ್ತಿ ರೇಣುಕಾ ಯಲ್ಲಮ್ಮ ಜಾತ್ರೆ (ಬನದ ಹುಣ್ಣಿಮೆ)",
        "district": "Belagavi",
        "city": "Saundatti (Yellammagudda)",
        "lat": 15.7766,
        "lng": 75.1225,
        "start_date": "2026-01-02",
        "end_date": "2026-01-05",
        "duration_days": 4,
        "season": "Winter (Margashirsha / Pausha Full Moon)",
        "category": "Tribal & Folk Pilgrimage",
        "description": "Held atop the scenic Yellammagudda hill overlooking the Malaprabha reservoir, this sacred folk pilgrimage draws over a million devotees from Karnataka, Maharashtra, and Goa. Pilgrims offer worship to Goddess Renuka Yellamma with neem leaves, turmeric (Bhandara), and silver umbrellas.",
        "cultural_significance": "A profound centre for Shakti and Matrika veneration in the Deccan, embodying deep agrarian faith and folk devotional songs (Jogiti Pada).",
        "history": "The shrine has ancient roots dating back to the Rashtrakuta and Ratta dynasties of Saundatti (11th century CE).",
        "attractions": [
            "Sea of devotees showering yellow turmeric (Bhandara) atop the hill",
            "Jogiti Nritya and Chowdki Pada folk balladeers singing Renuka's epic",
            "Sacred bath at the historic Jogula Bhavi stepwell tank",
            "Grand palanquin procession across the hilltops"
        ],
        "local_food": [
            "Jawari (Sorghum) Rotti with Shenga Pittu",
            "Belagavi Kunda (slow-caramelized milk sweet)",
            "Gokak Karadantu (nut-loaded chewy jaggery sweet)",
            "Pithla Bhakri with spicy green chilli thecha"
        ],
        "footfall": 1300000,
        "images": [
            {
                "url": "https://images.unsplash.com/photo-1544717302-de2939b7ef71",
                "caption": "Pilgrims celebrating with yellow turmeric at Yellammagudda hill",
                "is_primary": True
            }
        ],
        "tags": ["saundatti", "yellamma", "belagavi", "renuka", "bhandara", "jogiti-pada", "folk-pilgrimage"]
    },
    {
        "id": "dharmasthala-laksha-deepotsava",
        "name": "Dharmasthala Laksha Deepotsava (Festival of 100,000 Lamps)",
        "local_name": "ಧರ್ಮಸ್ಥಳ ಲಕ್ಷ ದೀಪೋತ್ಸವ",
        "district": "Dakshina Kannada",
        "city": "Dharmasthala",
        "lat": 12.9567,
        "lng": 75.3789,
        "start_date": "2026-11-28",
        "end_date": "2026-12-03",
        "duration_days": 6,
        "season": "Winter (Karthika Masa)",
        "category": "Spiritual Festival of Lights & Interfaith Unity",
        "description": "An ethereal festival of lights where the entire pilgrim town of Dharmasthala and the Netravati riverbank are illuminated with hundreds of thousands of earthen and brass oil lamps. Features the historic Sarva Dharma Sammelana (All-Faith Conference) and Sahitya Sammelana.",
        "cultural_significance": "Dharmasthala is a unique symbol of syncretism where the deity is Lord Shiva (Manjunatha), the priests are Madhwa Vaishnavas, and the administrative guardians (Heggade) are Jains.",
        "history": "Instituted over 800 years ago, upholding the 4 core tenets of Dharmasthala: Anna Dana (food), Abhaya Dana (sanctuary), Aushadha Dana (medicine), and Vidya Dana (education).",
        "attractions": [
            "Lighting of over 100,000 brass and clay lamps across the temple courtyard",
            "Sarva Dharma (Interfaith) and Sahitya (Literary) Conferences with eminent philosophers",
            "Nightly Lalitakalagalu classical concerts and Yakshagana troupes",
            "Chariot processions (Hosakatte, Kerekatte, Lalithodyana Ratha)"
        ],
        "local_food": [
            "Sri Manjunatha Temple Annadana Mahaprasada (piping hot rice, rasam, payasa)",
            "Pathrode (steamed spiced colocasia rolls)",
            "Mangalore Golibaje / Maida Vada with coconut chutney",
            "Kashaya (herbal digestive health beverage)"
        ],
        "footfall": 450000,
        "images": [
            {
                "url": "https://images.unsplash.com/photo-1514565131-fce0801e5785",
                "caption": "Illuminated rows of lamps during Laksha Deepotsava",
                "is_primary": True
            }
        ],
        "tags": ["dharmasthala", "deepotsava", "manjunatha", "lights", "sarva-dharma", "netravati", "dakshina-kannada"]
    },
    {
        "id": "udupi-paryaya-utsava",
        "name": "Udupi Sri Krishna Paryaya Mahotsava",
        "local_name": "ಉಡುಪಿ ಪರ್ಯಾಯ ಮಹೋತ್ಸವ",
        "district": "Udupi",
        "city": "Udupi",
        "lat": 13.3409,
        "lng": 74.7421,
        "start_date": "2026-01-18",
        "end_date": "2026-01-19",
        "duration_days": 2,
        "season": "Winter (Makara Sankranti Period / Biennial)",
        "category": "Sacred Biennial Handover & Vedic Ritual",
        "description": "A historic ceremonial handover of the administrative and worship rights (Puja Paryaya) of the world-famous Udupi Sri Krishna Temple among the pontiffs of the Ashta Mathas (8 monasteries). Takes place at dawn on January 18th in alternate even-numbered years.",
        "cultural_significance": "Embodies the unbroken 800-year lineage of Sri Madhwacharya's Dvaita Vedanta philosophy and peaceful rotational governance.",
        "history": "Conceived by Sri Madhwacharya in the 13th century (originally 2-month cycle) and restructured to a 2-year biennial system in 1522 CE by Sri Vadiraja Tirtha of Sodhe Matha.",
        "attractions": [
            "Early morning holy dip at Danda Tirtha and royal procession in decorated palanquins into Udupi Car Street",
            "Ceremonial handing over of the Akshaya Patra and temple shrine keys at Sarvajna Peetha",
            "Grand Durbar in Rajangana with Vedic scholars from across India",
            "All-night illumination of Udupi Car Street and Madhwa Sarovara"
        ],
        "local_food": [
            "Authentic Udupi Satvik Meal (Udupi Saaru, Menaskai, Kadubu)",
            "Goli Baje (crisp Mangalore bondas)",
            "Udupi Rava Masala Dosa",
            "Hayagriva Maddi (Bengal gram and jaggery sweet)",
            "Chitranna and Moode"
        ],
        "footfall": 400000,
        "images": [
            {
                "url": "https://images.unsplash.com/photo-1582510003544-4d00b7f74220",
                "caption": "Udupi Car Street decorated for the grand Paryaya procession",
                "is_primary": True
            }
        ],
        "tags": ["udupi", "paryaya", "krishna-matha", "madhwacharya", "ashta-matha", "dvaita", "satvik-food"]
    },
    {
        "id": "mahamastakabhisheka-shravanabelagola",
        "name": "Shravanabelagola Mahamastakabhisheka",
        "local_name": "ಶ್ರವಣಬೆಳಗೊಳ ಮಹಾಮಸ್ತಕಾಭಿಷೇಕ ಮಹೋತ್ಸವ",
        "district": "Hassan",
        "city": "Shravanabelagola",
        "lat": 12.8587,
        "lng": 76.4862,
        "start_date": "2026-02-15",
        "end_date": "2026-02-23",
        "duration_days": 9,
        "season": "Winter / Spring (Cyclic Event)",
        "category": "Grand Jain Anointment & Peace Fest",
        "description": "The world's grandest Jain festival held atop the monolithic Vindhyagiri Hill. The 57-foot-tall monolithic statue of Bhagwan Bahubali (Gommateshwara), carved in 981 CE, is ceremonially bathed from a specially erected scaffolding with milk, sugarcane juice, saffron, turmeric, sandalwood paste, and showered with gold and silver flowers.",
        "cultural_significance": "Commemorates Bahubali's spiritual victory through Ahimsa (non-violence), Tyaga (renunciation), and Kevala Jnana (supreme enlightenment).",
        "history": "Commissioned in 981 CE by Chavundaraya, the Prime Minister and Commander-in-Chief of the Western Ganga Dynasty.",
        "attractions": [
            "Pouring of 1,008 Kalashas (sacred urns) of milk, saffron, and turmeric over the 57-ft colossus",
            "Climbing the 650 stone-hewn steps of Vindhyagiri Hill overlooking Chandragiri",
            "International peace conclaves and Jain philosophical seminars",
            "Spectacular illumination of the two hills and the central white lake (Belagola)"
        ],
        "local_food": [
            "Satvik Jain Meal (No root vegetables, purely organic and cold-pressed preparations)",
            "Akki Rotti with coconut-coriander chutney",
            "Hassan style Ragi Rotti and Badam Kheer",
            "Kashaya and Holige"
        ],
        "footfall": 2800000,
        "images": [
            {
                "url": "https://images.unsplash.com/photo-1548013146-72479768bada",
                "caption": "57-foot Gommateshwara statue during the sacred head-anointing ceremony",
                "is_primary": True
            }
        ],
        "tags": ["shravanabelagola", "bahubali", "gommateshwara", "jainism", "ganga-dynasty", "ahimsa", "monolith"]
    },
    {
        "id": "hassanamba-temple-jatre",
        "name": "Hassanamba Temple Jatre (Annual Sanctum Opening)",
        "local_name": "ಹಾಸನಾಂಬ ದೇವಾಲಯ ಜಾತ್ರಾ ಮಹೋತ್ಸವ",
        "district": "Hassan",
        "city": "Hassan",
        "lat": 13.0033,
        "lng": 76.1004,
        "start_date": "2026-10-29",
        "end_date": "2026-11-08",
        "duration_days": 11,
        "season": "Autumn (Deepavali / Ashwayuja)",
        "category": "Sacred Annual Darshan & Miracle Shrine",
        "description": "A mystical temple event where the inner sanctum of the historic Hassanamba Temple opens to the public for only 10 to 14 days a year around Deepavali. When the doors are unlocked, the ghee lamp lit the previous year is found still burning, and the raw flowers offered remain fresh.",
        "cultural_significance": "Goddess Hassanamba is revered as the presiding smiling mother deity ('Hasana Amba') after whom the district of Hassan is named.",
        "history": "Built in the 12th century CE during the reign of the Hoysala dynasty who established magnificent architectural heritage in the region.",
        "attractions": [
            "Ceremonial breaking of the temple seal by the district administration and chief priests",
            "Darshan of the perennial sacred ghee lamp and fresh floral offerings from the previous year",
            "Siddeshwara Swamy car festival and Kendotsava (fire-walking ritual)",
            "Grand Deepavali fireworks and city-wide illumination"
        ],
        "local_food": [
            "Hassan Ragi Mudde with Bassaru & Upsaaru",
            "Menthe Kadubu with spicy coconut chutney",
            "Hassan style Akki Shavige (fresh rice noodles) with sweetened coconut milk",
            "Butter Dosa and Halwa"
        ],
        "footfall": 1100000,
        "images": [
            {
                "url": "https://images.unsplash.com/photo-1600100397608-f010f443b749",
                "caption": "Crowds of devotees queued outside the Hassanamba Temple for the annual darshan",
                "is_primary": True
            }
        ],
        "tags": ["hassan", "hassanamba", "annual-darshan", "miracle-lamp", "hoysala", "deepavali", "ragi-mudde"]
    },
    {
        "id": "basavanagudi-kadalekai-parishe",
        "name": "Basavanagudi Kadalekai Parishe (Groundnut Fair)",
        "local_name": "ಬಸವನಗುಡಿ ಕಡಲೆಕಾಯಿ ಪರಿಷೆ",
        "district": "Bengaluru Urban",
        "city": "Bengaluru (Basavanagudi)",
        "lat": 12.9421,
        "lng": 77.5684,
        "start_date": "2026-11-23",
        "end_date": "2026-11-25",
        "duration_days": 3,
        "season": "Winter (Last Monday of Karthika Masa)",
        "category": "Agrarian Peanut Fair & Folk Bazaar",
        "description": "Bengaluru's beloved 500-year-old groundnut fair where farmers from across Karnataka, Tamil Nadu, and Andhra Pradesh bring their first harvest of peanuts to offer to the sacred monolithic Nandi (Bull Temple) before setting up multi-kilometer street bazaars of roasted, boiled, and spiced groundnuts.",
        "cultural_significance": "Celebrates the symbiotic relationship between urban Bengaluru and the surrounding farming communities, blessed by the guardian Nandi bull.",
        "history": "Originated in the 16th century during the reign of Kempe Gowda I, when farmers placated a wild bull that rampaged groundnut fields by offering their first yield.",
        "attractions": [
            "Offerings of sacks of freshly harvested groundnuts to the giant monolithic Nandi idol",
            "Endless open-air street stalls with mountains of raw, clay-roasted, salted, and boiled peanuts",
            "Traditional giant hand-cranked wooden Ferris wheels and merry-go-rounds",
            "Vidyarthi Bhavan dosa hopping and Gandhi Bazaar cultural walking trail"
        ],
        "local_food": [
            "Hot Clay-Roasted Groundnuts (Bisi Kadalekai)",
            "Spiced Steamed Peanuts (Uppu Kadalekai)",
            "Batani Sundal and Menasinakai Bajji (Chilli fritters)",
            "Vidyarthi Bhavan Crispy Butter Masala Dosa",
            "Bobbattu / Holige (sweet stuffed flatbread)"
        ],
        "footfall": 650000,
        "images": [
            {
                "url": "https://images.unsplash.com/photo-1596401057633-54a8fe8ef647",
                "caption": "Bull Temple street fair lit up with colorful heaps of peanuts",
                "is_primary": True
            }
        ],
        "tags": ["bengaluru", "basavanagudi", "kadalekai-parishe", "bull-temple", "peanuts", "kempegowda", "street-fair"]
    },
    {
        "id": "sringeri-sharada-navaratri",
        "name": "Sringeri Sharada Sharannavaratri",
        "local_name": "ಶೃಂಗೇರಿ ಶಾರದ ಶರನ್ನವರಾತ್ರಿ ಮಹೋತ್ಸವ",
        "district": "Chikkamagaluru",
        "city": "Sringeri",
        "lat": 13.4184,
        "lng": 75.2559,
        "start_date": "2026-10-11",
        "end_date": "2026-10-20",
        "duration_days": 10,
        "season": "Autumn (Navaratri / Ashwayuja)",
        "category": "Sacred Classical & Vedic Fest",
        "description": "Celebrated at the first and premier Peetham established by Sri Adi Shankaracharya on the banks of Tunga River. Goddess Sharadamba is decorated in nine distinct divine alankaras (incarnations), and the Jagadguru Sankaracharya presides over the golden royal Durbar every evening wearing royal insignia.",
        "cultural_significance": "The epicenter of Advaita Vedanta philosophy, Vedic chanting, and classical Carnatic music offerings (Sangeeta Seva).",
        "history": "Established in the 8th century CE by Adi Shankaracharya and patronized by the founding monarchs of the Vijayanagara Empire, Harihara and Bukka.",
        "attractions": [
            "Goddess Sharadamba decorated in 9 radiant daily avatars (Brahmi, Vaishnavi, Chamundi, etc.)",
            "Evening Golden Chariot (Suvarna Ratha) and Durbar procession of the Sringeri Jagadguru",
            "Feeding the holy sacred fish in the clean waters of the Tunga River ghats",
            "Vidyaranya Vidya Peetha Vedic recitations and Chandi Homa"
        ],
        "local_food": [
            "Sringeri Temple Annaprasada (fragrant rice, piping sambar, rasam, and payasa)",
            "Malnad Halasina Hannina Happala & Kadubu",
            "Chikkamagaluru Pure Estate Filter Coffee",
            "Akki Rotti with Kayi Chutney"
        ],
        "footfall": 300000,
        "images": [
            {
                "url": "https://images.unsplash.com/photo-1548013146-72479768bada",
                "caption": "Vidyashankara Temple on the banks of Tunga River in Sringeri",
                "is_primary": True
            }
        ],
        "tags": ["sringeri", "sharadamba", "shankaracharya", "navaratri", "advaita", "chikkamagaluru", "tunga-river"]
    },
    {
        "id": "alvas-virasat-cultural-fest",
        "name": "Alva's Virasat & Nudisiri National Cultural Festival",
        "local_name": "ಆಳ್ವಾಸ್ ವಿರಾಸತ್ & ನುಡಿಸಿರಿ ರಾಷ್ಟ್ರೀಯ ಉತ್ಸವ",
        "district": "Dakshina Kannada",
        "city": "Moodabidri (Vidyagiri)",
        "lat": 13.0722,
        "lng": 74.9984,
        "start_date": "2026-12-18",
        "end_date": "2026-12-21",
        "duration_days": 4,
        "season": "Winter / Hemanta",
        "category": "National Cultural Extravaganza",
        "description": "One of India's largest integrated student and national cultural conventions featuring 50,000 youth and veteran artists performing classical Carnatic, Hindustani, Yakshagana, Manipuri, Kathakali, and folk dances on open-air mega amphitheaters.",
        "cultural_significance": "A mammoth cultural platform propagating Karnataka's language, heritage, traditional sports, and national integration.",
        "history": "Founded by visionary educationist Dr. M. Mohan Alva over 25 years ago in the Jain heritage town of Moodabidri.",
        "attractions": [
            "Grand stages hosting simultaneous performances of 1,000+ artists together",
            "Conferring of the prestigious Alva's Virasat Award to world-renowned musicians",
            "Massive traditional food court serving over 100 coastal and malnad culinary delicacies",
            "Art, sculpture, photography, and indigenous handloom exhibitions"
        ],
        "local_food": [
            "Moode (cylindrical steamed rice idlis in screwpine leaves)",
            "Mangalorean Jackfruit Chips and Halwa",
            "Goli Baje with ginger coconut chutney",
            "Banana Podi (banana fritters)"
        ],
        "footfall": 220000,
        "images": [
            {
                "url": "https://images.unsplash.com/photo-1514565131-fce0801e5785",
                "caption": "Magnificent cultural performance stage at Alva's Virasat Moodabidri",
                "is_primary": True
            }
        ],
        "tags": ["alvas-virasat", "moodabidri", "nudisiri", "classical-music", "folk-arts", "dance-festival", "youth"]
    },
    {
        "id": "kalaburagi-sharanabasaveshwara-jatre",
        "name": "Kalaburagi Sharanabasaveshwara Jatre",
        "local_name": "ಕಲಬುರಗಿ ಶರಣಬಸವೇಶ್ವರ ಮಹಾ ರಥೋತ್ಸವ",
        "district": "Kalaburagi",
        "city": "Kalaburagi (Gulbarga)",
        "lat": 17.3297,
        "lng": 76.8343,
        "start_date": "2026-03-24",
        "end_date": "2026-03-26",
        "duration_days": 3,
        "season": "Spring (Chaitra Masa)",
        "category": "Sufi-Bhakti Spiritual Fair & Dasoha",
        "description": "The landmark religious fair of Kalyana Karnataka commemorating the 19th-century Lingayat philosopher-saint Sri Sharanabasaveshwara. Features the pulling of the towering silver chariot and the public unveiling of the historic gold and silver covered bowl (Batti Gidda) and sacred staff (Padi).",
        "cultural_significance": "Celebrates the ideals of universal brotherhood, charity, and social upliftment across Hyderabad-Karnataka.",
        "history": "Commemorates Saint Sharanabasaveshwara (1760–1822 CE) who dedicated his entire life to providing famine relief and education.",
        "attractions": [
            "Pulling of the monumental Silver Ratha through the historic temple grounds",
            "Public viewing (Darshan) of the sacred relics (Batti & Padi) kept atop the dome",
            "Cattle fair (Kalyana Karnataka Hallikar and Khillari bull exhibition)",
            "Sufi Qawwali and Vachana Gayana concerts"
        ],
        "local_food": [
            "Gulbarga Malka Rotti with spicy Shenga chutney",
            "Kalaburagi Tahari (aromatic spiced rice specialty)",
            "Dharwad Pedha and Khaja sweet",
            "Jolada Rotti with Brinjal Gravy (Yennegai)"
        ],
        "footfall": 900000,
        "images": [
            {
                "url": "https://images.unsplash.com/photo-1544717305-2782549b5136",
                "caption": "Vibrant gathering during Sharanabasaveshwara chariot festival",
                "is_primary": True
            }
        ],
        "tags": ["kalaburagi", "sharanabasaveshwara", "kalyana-karnataka", "vachana", "silver-chariot", "dasoha"]
    },
    {
        "id": "kukke-subramanya-champa-shashti",
        "name": "Kukke Subramanya Champa Shashti",
        "local_name": "ಕುಕ್ಕೆ ಶ್ರೀ ಸುಬ್ರಹ್ಮಣ್ಯ ಚಂಪಾ ಷಷ್ಠಿ ಮಹೋತ್ಸವ",
        "district": "Dakshina Kannada",
        "city": "Subramanya",
        "lat": 12.6635,
        "lng": 75.6158,
        "start_date": "2026-12-14",
        "end_date": "2026-12-16",
        "duration_days": 3,
        "season": "Winter (Margashirsha Shuddha Shashti)",
        "category": "Sacred Serpentine Ritual & Car Fest",
        "description": "The premier festival at the revered Kukke Subramanya Temple nestled in the Western Ghats under the Kumara Parvatha peak. Lord Subramanya is worshipped as the supreme protector of serpents (Nagas), highlighted by the grand Brahmaratha procession and Ashlesha Bali.",
        "cultural_significance": "Regarded as the most potent pilgrimage destination in South India for Sarpa Dosha Nivarana and environmental reverence for serpents.",
        "history": "Ancient temple chronicled in the Sanatkumara Samhita of Skanda Purana where Lord Subramanya consecrated the serpent king Vasuki.",
        "attractions": [
            "Rolling and pulling of the giant wooden Brahmaratha chariot through Car Street",
            "Champa Shashti sacred bath in the holy Kumaradhara River",
            "Trekking view of the majestic Kumara Parvatha mountain backdrop",
            "Special Naga Pratishthe and Ashlesha Bali rituals"
        ],
        "local_food": [
            "Kottige (Idlis steamed in woven jackfruit leaf baskets)",
            "Kukke Temple Sweet Prasada (Laddus & Panchamrutha)",
            "Mangalore Buns with spicy coconut chutney",
            "Banana Halwa and tender coconut water"
        ],
        "footfall": 380000,
        "images": [
            {
                "url": "https://images.unsplash.com/photo-1600100397608-f010f443b749",
                "caption": "Kukke Subramanya Temple surrounded by lush Western Ghats hills",
                "is_primary": True
            }
        ],
        "tags": ["kukke-subramanya", "champa-shashti", "naga-worship", "kumaradhara", "kumara-parvatha", "brahmaratha"]
    },
    {
        "id": "bidar-utsav",
        "name": "Bidar Utsav (Bahmani Heritage & Deccan Culture)",
        "local_name": "ಬೀದರ್ ಉತ್ಸವ",
        "district": "Bidar",
        "city": "Bidar",
        "lat": 17.9174,
        "lng": 77.5303,
        "start_date": "2026-01-23",
        "end_date": "2026-01-25",
        "duration_days": 3,
        "season": "Winter / Shishira",
        "category": "Deccan Heritage & Sufi Music",
        "description": "Celebrated within the colossal triple-moated Bidar Fort and Mahmud Gawan Madrasa. Spotlights the historic fusion of Persian, Turkish, and Deccan architectural heritage, Sufi devotional music, Bidriware metal crafts, and kite festivals.",
        "cultural_significance": "Celebrates Bidar's cosmopolitan Deccan synthesis and preserves the GI-certified Bidriware craft of silver inlay on blackened zinc-copper alloy.",
        "history": "Bidar was the grand medieval capital of the Bahmani Sultanate and Barid Shahi dynasty from 1422 CE.",
        "attractions": [
            "3D projection mapping and laser shows onto the walls of the 15th-century Bidar Fort",
            "Live Bidriware artisan workshops in the historical Old City bazaars",
            "International Kite Flying Festival over the fort battlements",
            "Sufi music night featuring acclaimed Ghazal and Qawwali maestros"
        ],
        "local_food": [
            "Bidar Biryani & Dum Pukht specialties",
            "Jowar Rotti with Chana Dal Usli",
            "Bidar style Khubani ka Meetha (Apricot dessert)",
            "Malida sweet with pure ghee"
        ],
        "footfall": 120000,
        "images": [
            {
                "url": "https://images.unsplash.com/photo-1590076215667-875d4ef2d7ee",
                "caption": "Mahmud Gawan Madrasa and Bidar Fort battlements lit up at dusk",
                "is_primary": True
            }
        ],
        "tags": ["bidar", "bidar-fort", "bidriware", "bahmani", "deccan", "sufi-music", "kalyana-karnataka"]
    },
    {
        "id": "kodagu-kailpodh-huthri",
        "name": "Kodagu Kailpodh & Huthri Harvest Festival",
        "local_name": "ಕೊಡಗಿನ ಕೈಲ್‌ಪೊದ್ & ಹುತ್ತರಿ ಹಬ್ಬ",
        "district": "Kodagu",
        "city": "Madikeri / Gonikoppal",
        "lat": 12.4244,
        "lng": 75.7382,
        "start_date": "2026-09-03",
        "end_date": "2026-09-04",
        "duration_days": 2,
        "season": "Monsoon / Post-Monsoon (Bhadrapada & Margashirsha)",
        "category": "Indigenous Tribal & Harvest",
        "description": "The quintessential cultural festivals of the warrior clan of Kodagu. Kailpodh marks the worship of traditional weaponry (Kopri, Odi Katti) and agrarian tools following transplanting, while Huthri is the joyous harvesting of the first ear of golden paddy by moonlight accompanied by rhythmic Dudikott Paat folk songs.",
        "cultural_significance": "Represents the martial ethos, nature-worship, and egalitarian community solidarity of the indigenous Kodava community.",
        "history": "Unbroken ancestral tradition preserved in Kodagu Ainmanes (traditional ancestral homes) for centuries.",
        "attractions": [
            "Ayudha Puja of traditional ancestral arms and coconut-shooting shooting contests (Eedu)",
            "Solemn night procession into the paddy field for 'Poli Poli Deva' paddy cutting",
            "Kodava Valaga folk dance with swords (Bolak-aat, Kol-aat, Pariyakali)",
            "Communal feast at traditional Ainmanes in Kodava Kupya-Chele attire"
        ],
        "local_food": [
            "Kadambuttu with Pandi Curry (or traditional veg Bamboo Shoot / Kanni curry)",
            "Paputtu with Noolputtu and fresh coconut milk",
            "Thambuttu (mashed banana and roasted rice flour sweet made during Huthri)",
            "Coorg Kaapi and Kadamittu"
        ],
        "footfall": 85000,
        "images": [
            {
                "url": "https://images.unsplash.com/photo-1506744038136-46273834b3fb",
                "caption": "Lush green paddy fields and coffee valleys of Kodagu during harvest",
                "is_primary": True
            }
        ],
        "tags": ["kodagu", "kailpodh", "huthri", "kodava", "harvest", "martial-tradition", "ainmane", "coffee-hills"]
    },
    {
        "id": "kanakagiri-utsava",
        "name": "Kanakagiri Utsava (Suvarnagiri Heritage)",
        "local_name": "ಕನಕಗಿರಿ ಉತ್ಸವ",
        "district": "Koppal",
        "city": "Kanakagiri",
        "lat": 15.5728,
        "lng": 76.4228,
        "start_date": "2026-02-20",
        "end_date": "2026-02-22",
        "duration_days": 3,
        "season": "Winter / Spring",
        "category": "Heritage & Folk Arts",
        "description": "Celebrated at historical Kanakagiri ('Golden Hill'), famous for the proverb 'Kallidare Kanakagiri nodu' (If you have eyes, you must see Kanakagiri). Showcases the magnificent stone architecture of Kanakachala Lakshmi Narasimha Temple and Vijayanagara Nayaka art.",
        "cultural_significance": "Commemorates the regional cultural brilliance of the Kanakappa Nayaka chieftaincy under the Vijayanagara Empire.",
        "history": "Identified as the ancient Mauryan provincial capital 'Suvarnagiri' and later developed by Vijayanagara Nayakas in the 16th century.",
        "attractions": [
            "Sound and light spectacles around the Kanakachala Temple stone gopura",
            "Traditional Bayalata and Togalu Gombeyata (Leather Puppet Theatre)",
            "Koppal handloom khadi and Kinnal craft displays"
        ],
        "local_food": [
            "Sajje Rotti with Badanekayi Yennegai",
            "Kanakagiri style Girmit with Mirchi Bajji",
            "Shenga Chutney with hot Jolada Rotti",
            "Ghee-soaked Boondi Laddu"
        ],
        "footfall": 80000,
        "images": [
            {
                "url": "https://images.unsplash.com/photo-1548013146-72479768bada",
                "caption": "Kanakachala Lakshmi Narasimha Temple stone pavilion at Kanakagiri",
                "is_primary": True
            }
        ],
        "tags": ["kanakagiri", "koppal", "suvarnagiri", "nayaka", "kinnal-craft", "folk-arts", "temple"]
    },
    {
        "id": "lakkundi-utsava",
        "name": "Lakkundi Utsava (City of 100 Stepwells)",
        "local_name": "ಲಕ್ಕುಂಡಿ ಉತ್ಸವ (ಮೆಟ್ಟಿಲು ಬಾವಿಗಳ ನಗರಿ)",
        "district": "Gadag",
        "city": "Lakkundi",
        "lat": 15.3887,
        "lng": 75.7171,
        "start_date": "2026-02-12",
        "end_date": "2026-02-14",
        "duration_days": 3,
        "season": "Winter / Shishira",
        "category": "Art, Sculpture & Stepwell Heritage",
        "description": "Staged in the ancient city of Lokkigundi (modern Lakkundi), which was home to 101 stepped wells (Kalyanis) and 101 ornate chloritic schist temples. Features classical music by illuminated stepwells such as Musukina Bavi and Brahma Jinalaya.",
        "cultural_significance": "Celebrates the zenith of Kalyana Chalukya architectural ingenuity and the legacy of legendary patron Attimabbe ('Danachintamani').",
        "history": "Lakkundi was an imperial minting capital and a major metropolis in the 10th-12th centuries under the Western Chalukyas, Hoysalas, and Seunas.",
        "attractions": [
            "Illuminated stepwell concerts at Musukina Bavi and Kasi Vishveshwara Temple",
            "Attimabbe National Literary and Women Leadership Awards",
            "Live stone carving demonstrations by contemporary sculptors",
            "Heritage cycle tours across all surviving Kalyanis"
        ],
        "local_food": [
            "Gadag style Crispy Jolada Rotti with Shenga Pudi",
            "Moong Dal Kosambari with fresh grated coconut",
            "Churmuri / Girmit with hot chilli bajji",
            "Dharwad Pedha & Balepale"
        ],
        "footfall": 55000,
        "images": [
            {
                "url": "https://images.unsplash.com/photo-1590076215667-875d4ef2d7ee",
                "caption": "Musukina Bavi stepwell at Lakkundi lit up with traditional oil lamps",
                "is_primary": True
            }
        ],
        "tags": ["lakkundi", "gadag", "stepwells", "kalyani", "chalukya", "attimabbe", "sculpture"]
    },
    {
        "id": "kittur-utsava",
        "name": "Kittur Rani Chennamma Vijayotsava",
        "local_name": "ಕಿತ್ತೂರು ರಾಣಿ ಚೆನ್ನಮ್ಮ ವಿಜಯೋತ್ಸವ",
        "district": "Belagavi",
        "city": "Kittur",
        "lat": 15.6015,
        "lng": 74.7937,
        "start_date": "2026-10-23",
        "end_date": "2026-10-25",
        "duration_days": 3,
        "season": "Autumn (October 23-25)",
        "category": "Patriotic & Freedom Heritage",
        "description": "Celebrated with patriotic fervor in Kittur to commemorate Queen Rani Chennamma's historic armed rebellion and victory against the British East India Company in October 1824, 33 years before the 1857 Sepoy Mutiny.",
        "cultural_significance": "A symbol of Kannada valor, women leadership, and early Indian anti-colonial freedom struggle.",
        "history": "Rani Chennamma and her lieutenant Krantiveera Sangolli Rayanna routed the British forces led by John Thackeray at Kittur Fort in 1824.",
        "attractions": [
            "Veerajyoti (Torch of Valor) flame relay from Sangolli and Belagavi to Kittur Fort",
            "Spectacular light and sound reenactment of the Kittur battle within the fort ruins",
            "Traditional Mallakhamba and wrestling (Kushti) demonstrations",
            "Patriotic choral songs and folk plays on Chennamma & Sangolli Rayanna"
        ],
        "local_food": [
            "Belgaum Kunda (traditional roasted milk dessert)",
            "Gokak Karadantu (dry fruit and edible gum jaggery sweet)",
            "Jolada Rotti with Yennegai and raw onion salad",
            "Shenga Holige with ghee"
        ],
        "footfall": 160000,
        "images": [
            {
                "url": "https://images.unsplash.com/photo-1548013146-72479768bada",
                "caption": "Kittur Fort palace ruins illuminated during the Rani Chennamma festival",
                "is_primary": True
            }
        ],
        "tags": ["kittur", "rani-chennamma", "freedom-struggle", "belagavi", "sangolli-rayanna", "valor", "patriotic"]
    },
    {
        "id": "karwar-karavali-beach-utsav",
        "name": "Karwar Beach Festival (Karavali Utsava)",
        "local_name": "ಕಾರವಾರ ಬೀಚ್ ಉತ್ಸವ (ಕರಾವಳಿ ಉತ್ಸವ)",
        "district": "Uttara Kannada",
        "city": "Karwar (Rabindranath Tagore Beach)",
        "lat": 14.8080,
        "lng": 74.1240,
        "start_date": "2026-12-26",
        "end_date": "2026-12-30",
        "duration_days": 5,
        "season": "Winter / Year-End",
        "category": "Coastal Tourism & Maritime Arts",
        "description": "Staged along the crescent-shaped Rabindranath Tagore Beach where the young poet laureate Tagore was inspired to write his early verses. Features water sports, international sand sculptures, coastal Konkani music, and beach sports.",
        "cultural_significance": "Celebrates Uttara Kannada's pristine coastal ecology, naval heritage (INS Chapal Warship museum), and vibrant Konkan-Kannada syncretism.",
        "history": "Inaugurated as an annual tourism flagship in the 1990s celebrating Karwar's maritime history and literary links.",
        "attractions": [
            "Giant Sand Art sculptures created by world-renowned artists on the shoreline",
            "Paramotoring, jet skiing, and banana boat rides on Arabian Sea waters",
            "INS Chapal Warship light & laser showcase",
            "Coastal Konkani & Kannada musical fusion evenings"
        ],
        "local_food": [
            "Karwar style Cashew Green Chilli Upkari",
            "Karwari Fish Curry & Rawa Fried Surmai (or veg Phalguni coconut curries)",
            "Amboli with coconut chutney",
            "Mangalore Buns and fresh Elaneer (Tender Coconut)"
        ],
        "footfall": 140000,
        "images": [
            {
                "url": "https://images.unsplash.com/photo-1507525428034-b723cf961d3e",
                "caption": "Sunset over Rabindranath Tagore Beach in Karwar during the festival",
                "is_primary": True
            }
        ],
        "tags": ["karwar", "karavali", "beach-fest", "tagore-beach", "sand-art", "coastal", "arabian-sea"]
    },
    {
        "id": "sonda-vadiraja-mutt-rathotsava",
        "name": "Sonda Sri Vadiraja Swamy Rathotsava",
        "local_name": "ಸೋದಾ ವಾದಿರಾಜ ಸ್ವಾಮಿ ಮಹಾ ರಥೋತ್ಸವ",
        "district": "Uttara Kannada",
        "city": "Sonda (Sirsi)",
        "lat": 14.7335,
        "lng": 74.8197,
        "start_date": "2026-03-05",
        "end_date": "2026-03-07",
        "duration_days": 3,
        "season": "Spring (Phalguna Shuddha Tritiya / Aradhana)",
        "category": "Spiritual & Dvaita Vedanta Fest",
        "description": "Celebrated in the tranquil Western Ghats valley of Sonda (Sodhe), the sacred seat of Sri Vadiraja Tirtha (1480-1600 CE). Devotees gather for the pulling of the grand Trivikrama Ratha and the sacred Hayagriva Prasada distribution at the Vadiraja Brundavana.",
        "cultural_significance": "Venerates Saint Vadiraja Tirtha, a towering figure in Haridasa Sahitya, composer of 'Yuktimallika' and 'Rukminisha Vijaya'.",
        "history": "Established in the 16th century when Arasappa Nayaka, King of Sonda, gifted the principality to Saint Vadiraja.",
        "attractions": [
            "Pulling of the ancient Sri Trivikrama Temple Chariot",
            "Darshan of the sacred Rama Trivikrama stone idol and Vadiraja's Brundavana",
            "Dhavala Ganga sacred tank holy dip",
            "Haridasa Keerthane concerts by veteran classical vocalists"
        ],
        "local_food": [
            "Authentic Hayagriva Maddi (heritage sweet made with Bengal gram, jaggery, and dry fruits)",
            "Sonda Mutt Annaprasada with authentic Huli and Saaru",
            "Malnad Jackfruit Payasa",
            "Bakshya (Holige) with fresh coconut milk"
        ],
        "footfall": 60000,
        "images": [
            {
                "url": "https://images.unsplash.com/photo-1621847468516-1ed5d0df56fe",
                "caption": "Sonda Mutt temple complex and peaceful surrounding forest valley",
                "is_primary": True
            }
        ],
        "tags": ["sonda", "vadiraja", "hayagriva", "sirsi", "dvaita", "haridasa", "western-ghats"]
    },
    {
        "id": "guledgudda-channabasaveshwara-jatre",
        "name": "Guledgudda Channabasaveshwara Jatre & Weavers Fair",
        "local_name": "ಗುಳೇದಗುಡ್ಡ ಚೆನ್ನಬಸವೇಶ್ವರ ಜಾತ್ರೆ ಮತ್ತು ಕೈಮಗ್ಗ ಉತ್ಸವ",
        "district": "Bagalkote",
        "city": "Guledgudda",
        "lat": 16.0526,
        "lng": 75.9288,
        "start_date": "2026-01-20",
        "end_date": "2026-01-22",
        "duration_days": 3,
        "season": "Winter (Makara Sankranti)",
        "category": "Community Fair & Weaving Heritage",
        "description": "Celebrated in Guledgudda, famed across India as the handloom capital of the traditional 'Khana' (blouse fabric). The festival combines the spiritual car festival of Sri Channabasaveshwara with a vibrant regional handloom exhibition and wrestling tourney.",
        "cultural_significance": "Showcases the heritage GI-tagged Guledgudda Khana weaving tradition practiced by generations of master weavers.",
        "history": "Rooted in the 12th-century Vachanakara Channabasavanna's tradition, nurtured under the historical Keladi and Maratha periods.",
        "attractions": [
            "Decorated chariot pulling through the weavers' heritage quarters",
            "Live handloom demonstrations of authentic Guledgudda Khana fabrics",
            "State-level Kushti (mud wrestling) tournament",
            "North Karnataka Vachana and Janapada singing assemblies"
        ],
        "local_food": [
            "Guledgudda Shenga Holige (Thin peanut jaggery flatbread)",
            "Crispy Jolada Rotti with Badanekayi Ennegayi",
            "Spicy Mirchi Girmit",
            "Sajje Rotti with homemade white butter"
        ],
        "footfall": 95000,
        "images": [
            {
                "url": "https://images.unsplash.com/photo-1596401057633-54a8fe8ef647",
                "caption": "Handloom weaving stalls and festive street lights in Guledgudda",
                "is_primary": True
            }
        ],
        "tags": ["guledgudda", "khana", "handloom", "bagalkote", "channabasaveshwara", "weavers", "jatre"]
    },
    {
        "id": "sagara-ikkeri-malnad-utsava",
        "name": "Sagara Ikkeri & Keladi Nayaka Malnad Utsava",
        "local_name": "ಸಾಗರ ಇಕ್ಕೇರಿ & ಕೆಳದಿ ನಾಯಕ ಮಲೆನಾಡು ಉತ್ಸವ",
        "district": "Shivamogga",
        "city": "Sagara / Ikkeri",
        "lat": 14.1670,
        "lng": 75.0337,
        "start_date": "2026-12-04",
        "end_date": "2026-12-06",
        "duration_days": 3,
        "season": "Winter / Hemanta",
        "category": "Literature, Theatre & Malnad Heritage",
        "description": "Celebrated at Sagara, Ikkeri, and Keladi, the regal seats of the Keladi Nayakas (including the legendary Queen Keladi Chennamma who sheltered Shivaji's son Rajaram). Highlights include all-night Yakshagana, Rangayana theatre, and sandalwood carving.",
        "cultural_significance": "Celebrates Malnad's rich theatre tradition, Gudigar sandalwood craftsmanship, and Keladi architectural marvels.",
        "history": "Keladi and Ikkeri served as the capitals of the Keladi Nayakas from 1499 to 1763 CE.",
        "attractions": [
            "Aghoreshwara Temple illuminated sound and light evening",
            "All-night Badaguthittu Yakshagana and contemporary drama by Ninasam / Heggodu artistes",
            "Gudigar traditional sandalwood and rosewood carving exhibition",
            "Heritage trail through the Keladi Museum's ancient copper plate grants"
        ],
        "local_food": [
            "Malnad Halasina Payasa (Jackfruit Kheer)",
            "Todadevu (Paper-thin sugarcane crepe)",
            "Kotte Kadubu steamed in jackfruit leaves with coconut chutney",
            "Maland style Appemidi gojju and hot rice"
        ],
        "footfall": 48000,
        "images": [
            {
                "url": "https://images.unsplash.com/photo-1590076215667-875d4ef2d7ee",
                "caption": "Aghoreshwara Temple stone carvings at Ikkeri during the festival",
                "is_primary": True
            }
        ],
        "tags": ["sagara", "ikkeri", "keladi-nayaka", "shivamogga", "yakshagana", "ninasam", "malnad"]
    },
    {
        "id": "nanjarayapatna-kambala",
        "name": "Nanjarayapatna Riverine Kambala & Coorg Folk Meet",
        "local_name": "ನಂಜರಾಯಪಟ್ಟಣ ಕಂಬಳ ಮತ್ತು ಜಾನಪದ ಸಮ್ಮೇಳನ",
        "district": "Kodagu",
        "city": "Nanjarayapatna (Kushalnagar)",
        "lat": 12.4550,
        "lng": 75.8900,
        "start_date": "2026-12-19",
        "end_date": "2026-12-20",
        "duration_days": 2,
        "season": "Winter / Hemanta",
        "category": "Folk Sports & Agrarian Heritage",
        "description": "The unique inland Malnad-Kodagu edition of the buffalo race held along the banks of River Kaveri in Nanjarayapatna, bringing together highland Kodava and Gowda farming families in celebration of the winter harvest.",
        "cultural_significance": "A rare high-altitude agrarian buffalo sprint tradition demonstrating deep bonding between highland farmers and their cattle.",
        "history": "Conducted since the era of the Haleri Rajas of Coorg who patronized post-harvest rural games in the Cauvery basin.",
        "attractions": [
            "Thrilling buffalo sprint races along the muddy bank tracks of River Kaveri",
            "Traditional Kodava Valaga drum beats and warrior folk dances",
            "Rural archery and coconut-shooting championships"
        ],
        "local_food": [
            "Akki Rotti with spicy Thondekai Palya",
            "Kadambuttu with hot Kaveri fish curry or veg bamboo curry",
            "Coorg Kaapi with Jaggery",
            "Thambuttu (Huthri special sweet banana dumplings)"
        ],
        "footfall": 40000,
        "images": [
            {
                "url": "https://images.unsplash.com/photo-1596178065887-1198b6148b2b",
                "caption": "Highland buffalo race in progress in Nanjarayapatna, Kodagu",
                "is_primary": True
            }
        ],
        "tags": ["kodagu", "nanjarayapatna", "kambala", "kaveri-basin", "folk-sport", "kushalnagar"]
    },
    {
        "id": "mundkur-durga-parameshwari-jathre",
        "name": "Mundkur Sri Durga Parameshwari Rathotsava",
        "local_name": "ಮುಂಡ್ಕೂರು ದುರ್ಗಾಪರಮೇಶ್ವರಿ ರಥೋತ್ಸವ",
        "district": "Udupi",
        "city": "Mundkur (Karkala)",
        "lat": 13.1620,
        "lng": 74.8850,
        "start_date": "2026-02-18",
        "end_date": "2026-02-21",
        "duration_days": 4,
        "season": "Winter (Kumbha Masa / Makara)",
        "category": "Sacred Coastal Car Fest & Daivaradhane",
        "description": "Celebrated at the ancient Sri Durga Parameshwari Temple on the banks of Shambhavi River in Mundkur. Features the pulling of the grand Brahma Ratha, sacred Daivaradhane (Bhoota Kola), and classical Yakshagana prasanga performances.",
        "cultural_significance": "A major focal point of Shakti veneration and Daiva (Bhoota) harmony in coastal Udupi-Dakshina Kannada borderland.",
        "history": "Consecrated by Sage Bhargava (Parashurama Kshetra) and patronized by the local Jain and Alupa Samanthas in the 10th century.",
        "attractions": [
            "Brahma Ratha Chariot festival with traditional Chande and Maddale orchestra",
            "Bhoota Kola rituals honoring Pilichamundi and Jarandaya Daivas",
            "All-night Tenkutittu Yakshagana staged on open-air riverbank grounds"
        ],
        "local_food": [
            "Moode Idli with Koli / Veg Menaskai",
            "Goli Baje with coconut-ginger dip",
            "Kottige with sweet coconut milk",
            "Mangalorean Halwa and Patrode"
        ],
        "footfall": 85000,
        "images": [
            {
                "url": "https://images.unsplash.com/photo-1582510003544-4d00b7f74220",
                "caption": "Mundkur temple car decorated with red and yellow festoons",
                "is_primary": True
            }
        ],
        "tags": ["mundkur", "udupi", "durga-parameshwari", "rathotsava", "daivaradhane", "bhoota-kola", "karavali"]
    },
    {
        "id": "shravana-masa-koodli-sangama",
        "name": "Koodli Sangama Maha Shravanotsava",
        "local_name": "ಕೂಡ್ಲಿ ಸಂಗಮ ಮಹಾ ಶ್ರಾವಣೋತ್ಸವ",
        "district": "Shivamogga",
        "city": "Koodli (Bhadravathi / Shivamogga)",
        "lat": 14.0289,
        "lng": 75.6983,
        "start_date": "2026-08-14",
        "end_date": "2026-08-17",
        "duration_days": 4,
        "season": "Monsoon (Shravana Masa)",
        "category": "Sacred River Confluence & Shankara Mutt Fest",
        "description": "Celebrated at Koodli, the holy confluence where River Tunga and River Bhadra unite to form the mighty Tungabhadra River. Devotees take holy snana at the Sangama and attend special pujas at the 12th-century Hoysala Rameshwara temple and the historic Koodli Arya Akshobhya Teertha Matha.",
        "cultural_significance": "A sacred Sangama Kshetra where Advaita, Dvaita, and Shaiva traditions harmoniously converge with river veneration.",
        "history": "Recorded since the Hoysala Empire under King Veera Ballala II (12th century), home to ancient Advaita and Dvaita monastic seats.",
        "attractions": [
            "Maha Sangama Snana and Ganga Arati at the union point of Tunga & Bhadra rivers",
            "Darshan of the 12th-century Hoysala Chintamani Narasimha and Rameshwara shrines",
            "Vedic chanting and Rudrabhisheka during sacred Shravana Somavara"
        ],
        "local_food": [
            "Malnad Shravana Satvik Prasada (Rice, Rasam, and Halasina Payasa)",
            "Akki Rotti with Menthe Gojju",
            "Appehuli (raw mango herbal soup)",
            "Chikkamagaluru / Shivamogga Filter Coffee"
        ],
        "footfall": 90000,
        "images": [
            {
                "url": "https://images.unsplash.com/photo-1506744038136-46273834b3fb",
                "caption": "Scenic confluence of Tunga and Bhadra rivers at Koodli",
                "is_primary": True
            }
        ],
        "tags": ["koodli", "sangama", "shivamogga", "tunga", "bhadra", "tungabhadra", "hoysala", "shravana"]
    },
    {
        "id": "mudbidri-jain-basadi-deepotsava",
        "name": "Moodabidri Thousand Pillar Basadi Deepotsava",
        "local_name": "ಮೂಡುಬಿದಿರೆ ಸಾವಿರ ಕಂಬದ ಬಸದಿ ದೀಪೋತ್ಸವ",
        "district": "Dakshina Kannada",
        "city": "Moodabidri",
        "lat": 13.0690,
        "lng": 74.9960,
        "start_date": "2026-11-15",
        "end_date": "2026-11-17",
        "duration_days": 3,
        "season": "Winter (Karthika Masa / Deepavali)",
        "category": "Jain Heritage & Architectural Illumination",
        "description": "Staged at the breathtaking 1430 CE Tribhuvana Tilaka Chudamani Basadi (popularly known as the Thousand Pillar Basadi or Savira Kambada Basadi) in Moodabidri, known as the 'Jain Kashi of the South'. Thousands of clay lamps illuminate the granite colonnades and the 8-foot monolithic idol of Lord Chandranatha.",
        "cultural_significance": "Preserves priceless Jain palm-leaf manuscripts (Dhavala texts) and exemplifies Vijayanagara-era stone craftsmanship.",
        "history": "Built in 1430 CE by the local chieftain Devaraya Wodeyar and enhanced by Queen Nagala Devi with its famous 50-foot monolithic Manastambha.",
        "attractions": [
            "Illumination of the 1,000 intricately carved non-repeating granite pillars",
            "Special Darshan of the 8-ft Chandranatha Swami idol and Guru Basadi Dhavala texts",
            "Classical flute and Veena concerts in the open pillared mandapa",
            "Heritage walk across the 18 historical Jain Basadis of Moodabidri"
        ],
        "local_food": [
            "Satvik Jain Coastal Meal (No root vegetables, pure unrefined organic coconut-based curries)",
            "Moode with coconut chutney",
            "Mangalore Goli Baje",
            "Pathrode (steamed colocasia parcels)"
        ],
        "footfall": 95000,
        "images": [
            {
                "url": "https://images.unsplash.com/photo-1548013146-72479768bada",
                "caption": "Thousand Pillar Basadi in Moodabidri illuminated by thousands of lamps",
                "is_primary": True
            }
        ],
        "tags": ["moodabidri", "jain-kashi", "thousand-pillar-basadi", "chandranatha", "deepotsava", "heritage", "granite"]
    },
    {
        "id": "nanjangud-dodda-jaathre",
        "name": "Nanjangud Srikanteshwara Dodda Jathre (Gautama Ratha)",
        "local_name": "ನಂಜನಗೂಡು ಶ್ರೀ ನಂಜುಂಡೇಶ್ವರ ದೊಡ್ಡ ಜಾತ್ರೆ (ಗೌತಮ ರಥ)",
        "district": "Mysuru",
        "city": "Nanjangud",
        "lat": 12.1197,
        "lng": 76.6806,
        "start_date": "2026-03-31",
        "end_date": "2026-04-02",
        "duration_days": 3,
        "season": "Spring (Chaitra Shuddha Panchami)",
        "category": "Sacred Shaivite Car Festival",
        "description": "Known as the 'Dakshina Kashi' (Kashi of the South) on the banks of Kapila (Kabini) River. Over 300,000 pilgrims congregate for the pulling of 5 monumental wooden chariots led by the colossal 90-foot Gautama Ratha carrying Lord Srikanteshwara (Nanjundeshwara).",
        "cultural_significance": "Lord Shiva is worshipped as Nanjundeshwara, the benevolent healer who consumed the Halahala poison to save creation.",
        "history": "Dating to the Ganga Dynasty (9th century) and expanded extensively by Hoysala and Mysuru Wadiyar monarchs, including a special emerald necklace gifted by Tipu Sultan who called the deity 'Hakim Nanjunda'.",
        "attractions": [
            "Simultaneous pulling of 5 giant chariots (Gautama, Chandikeshwara, Subramanya, Ganapathi, Parvathi)",
            "Sacred holy bath (Snana) in the sacred Kapila River",
            "Darshan of the 100-foot-tall Mahadwara Gopura and nine emerald Shiva Lingas",
            "Nightly Teppotsava (coracle/float festival) on Kapila waters"
        ],
        "local_food": [
            "Nanjanagudu Rasabale (World-famous GI tagged aromatic small banana)",
            "Nanjangud style Puliyogare and Sweet Pongal",
            "Mysore Pak & Maddur Vada",
            "Kapila River style fresh tender coconut water"
        ],
        "footfall": 350000,
        "images": [
            {
                "url": "https://images.unsplash.com/photo-1600100397608-f010f443b749",
                "caption": "Colossal Gautama Ratha moving through the temple streets of Nanjangud",
                "is_primary": True
            }
        ],
        "tags": ["nanjangud", "dakshina-kashi", "srikanteshwara", "gautama-ratha", "kapila-river", "rasabale", "mysuru"]
    }
]


# ---------------------------------------------------------------------------
# Data Engineering & Validation Engine
# ---------------------------------------------------------------------------

class KarnatakaFestivalDataEngineer:
    """
    Data engineering pipeline to validate, enrich, and serialize the
    SanskritiPulse AI Karnataka Festivals dataset.
    """

    KARNATAKA_LAT_BOUNDS = (11.5, 18.6)
    KARNATAKA_LNG_BOUNDS = (74.0, 78.7)
    REQUIRED_FIELDS = [
        "id", "name", "local_name", "district", "city",
        "lat", "lng", "start_date", "end_date", "category",
        "description", "cultural_significance", "history",
        "attractions", "local_food", "footfall", "images"
    ]

    def __init__(self, raw_data: List[Dict[str, Any]]):
        self.raw_data = raw_data
        self.df: pd.DataFrame = pd.DataFrame()

    def process_and_validate(self) -> pd.DataFrame:
        """
        Loads dataset into pandas, validates coordinates, types, nulls,
        and computes derived data engineering fields.
        """
        print("🔍 [Data Pipeline] Initializing Karnataka Festivals Dataset...")
        df = pd.DataFrame(self.raw_data)

        # 1. Schema Completeness Check
        missing_cols = [col for col in self.REQUIRED_FIELDS if col not in df.columns]
        if missing_cols:
            raise ValueError(f"❌ Schema validation failed! Missing columns: {missing_cols}")

        # 2. Null Checks
        null_counts = df[self.REQUIRED_FIELDS].isnull().sum()
        if null_counts.any():
            raise ValueError(f"❌ Null values detected in required fields:\n{null_counts[null_counts > 0]}")

        # 3. Geographic Coordinates Validation within Karnataka bounding box
        invalid_lat = df[(df["lat"] < self.KARNATAKA_LAT_BOUNDS[0]) | (df["lat"] > self.KARNATAKA_LAT_BOUNDS[1])]
        invalid_lng = df[(df["lng"] < self.KARNATAKA_LNG_BOUNDS[0]) | (df["lng"] > self.KARNATAKA_LNG_BOUNDS[1])]

        if not invalid_lat.empty:
            raise ValueError(f"❌ Latitude out of Karnataka bounds for: {invalid_lat['name'].tolist()}")
        if not invalid_lng.empty:
            raise ValueError(f"❌ Longitude out of Karnataka bounds for: {invalid_lng['name'].tolist()}")

        # 4. Enrich Derived Fields
        df["footfall_formatted"] = df["footfall"].apply(
            lambda x: f"{x/1_000_000:.1f} Million+" if x >= 1_000_000 else f"{x/1_000:.0f}k+"
        )
        df["attractions_count"] = df["attractions"].apply(lambda x: len(x) if isinstance(x, list) else 0)
        df["culinary_items_count"] = df["local_food"].apply(lambda x: len(x) if isinstance(x, list) else 0)

        # Ensure start_date and end_date validity
        df["start_date"] = pd.to_datetime(df["start_date"])
        df["end_date"] = pd.to_datetime(df["end_date"])
        df["computed_duration"] = (df["end_date"] - df["start_date"]).dt.days + 1

        # Format dates back to ISO strings for export
        df["start_date"] = df["start_date"].dt.strftime("%Y-%m-%d")
        df["end_date"] = df["end_date"].dt.strftime("%Y-%m-%d")

        self.df = df
        print(f"✅ [Data Pipeline] Successfully validated and enriched {len(df)} festivals.")
        return df

    def generate_analytics_summary(self) -> Dict[str, Any]:
        """Generates statistical summary of the festivals dataset."""
        if self.df.empty:
            self.process_and_validate()

        total_footfall = int(self.df["footfall"].sum())
        avg_footfall = int(self.df["footfall"].mean())
        district_dist = self.df["district"].value_counts().to_dict()
        category_dist = self.df["category"].value_counts().to_dict()

        summary = {
            "total_festivals": len(self.df),
            "total_estimated_footfall": total_footfall,
            "average_footfall_per_festival": avg_footfall,
            "districts_covered_count": len(district_dist),
            "district_distribution": district_dist,
            "category_distribution": category_dist,
            "top_3_by_footfall": self.df.nlargest(3, "footfall")[["name", "district", "footfall_formatted"]].to_dict(orient="records")
        }
        return summary

    def export_to_json(self, output_path: str) -> str:
        """Exports the cleaned dataset to a formatted JSON array."""
        if self.df.empty:
            self.process_and_validate()

        # Convert records to native dictionary format
        records = self.df.to_dict(orient="records")

        # Clean any numpy/pandas specific types
        for item in records:
            for k, v in item.items():
                if isinstance(v, (np.int64, np.int32)):
                    item[k] = int(v)
                elif isinstance(v, (np.float64, np.float32)):
                    item[k] = float(v)

        os.makedirs(os.path.dirname(os.path.abspath(output_path)), exist_ok=True)
        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(records, f, ensure_ascii=False, indent=2)

        print(f"📁 [Export] Seed data successfully written to: {output_path}")
        return output_path

    def export_to_csv(self, output_path: str) -> str:
        """Exports the dataset to CSV format for tabular data processing."""
        if self.df.empty:
            self.process_and_validate()

        # Serialize list fields to JSON strings for CSV compatibility
        csv_df = self.df.copy()
        csv_df["attractions"] = csv_df["attractions"].apply(json.dumps)
        csv_df["local_food"] = csv_df["local_food"].apply(json.dumps)
        csv_df["images"] = csv_df["images"].apply(json.dumps)
        csv_df["tags"] = csv_df["tags"].apply(json.dumps)

        os.makedirs(os.path.dirname(os.path.abspath(output_path)), exist_ok=True)
        csv_df.to_csv(output_path, index=False, encoding="utf-8")
        print(f"📁 [Export] CSV dataset written to: {output_path}")
        return output_path


# ---------------------------------------------------------------------------
# CLI Runner
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(description="SanskritiPulse AI - Karnataka Festivals Seed Data Generator")
    parser.add_argument(
        "--json-output",
        default="festivals_karnataka.json",
        help="Path for output JSON file (default: festivals_karnataka.json)"
    )
    parser.add_argument(
        "--csv-output",
        default="festivals_karnataka.csv",
        help="Path for output CSV file (default: festivals_karnataka.csv)"
    )
    parser.add_argument(
        "--summary",
        action="store_true",
        help="Print analytical summary of the dataset"
    )

    args = parser.parse_args()

    pipeline = KarnatakaFestivalDataEngineer(FESTIVAL_RAW_DATA)
    pipeline.process_and_validate()

    # Export outputs
    json_path = os.path.abspath(args.json_output)
    csv_path = os.path.abspath(args.csv_output)

    pipeline.export_to_json(json_path)
    pipeline.export_to_csv(csv_path)

    # Print summary
    summary = pipeline.generate_analytics_summary()
    print("\n" + "=" * 60)
    print("📊 SANSKRITIPULSE AI - DATA ENGINE METRICS & SUMMARY")
    print("=" * 60)
    print(f"• Total Karnataka Festivals Seeded: {summary['total_festivals']}")
    print(f"• Total Estimated Footfall:        {summary['total_estimated_footfall']:,}")
    print(f"• Unique Districts Covered:        {summary['districts_covered_count']}")
    print("\n🏆 Top 3 Festivals by Footfall:")
    for idx, fest in enumerate(summary["top_3_by_footfall"], 1):
        print(f"  {idx}. {fest['name']} ({fest['district']}) - {fest['footfall_formatted']}")

    print("\n📍 District Coverage Breakdown:")
    for dist, count in summary["district_distribution"].items():
        print(f"  • {dist:20s}: {count} festival(s)")

    print("\n🎭 Category Distribution:")
    for cat, count in summary["category_distribution"].items():
        print(f"  • {cat:40s}: {count}")
    print("=" * 60 + "\n")


if __name__ == "__main__":
    main()
