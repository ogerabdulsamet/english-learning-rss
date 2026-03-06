#!/usr/bin/env python3
"""
Daily English Learning RSS Feed Generator
Generates daily English learning content with Turkish translations
"""

import os
import json
import google.generativeai as genai
from datetime import datetime, timezone
import xml.etree.ElementTree as ET
from xml.dom import minidom
import hashlib
import re

# Konfigürasyon
GEMINI_API_KEY = os.environ.get('GEMINI_API_KEY')
RSS_FILE = 'feed.xml'
FEED_TITLE = 'Daily English Learning Feed'
FEED_DESCRIPTION = 'Günlük İngilizce öğrenme içerikleri - Daily English learning content'
FEED_LINK = os.environ.get('FEED_LINK', 'https://your-username.github.io/your-repo/')

# İçerik seviyeleri
LEVELS = ['A1', 'A2', 'B1', 'B2', 'C1', 'C2']

# Konular havuzu
TOPICS = [
    "Technology and Innovation",
    "Travel and Culture",
    "Health and Wellness",
    "Business and Career",
    "Environment and Sustainability",
    "Food and Cooking",
    "Arts and Entertainment",
    "Science and Discovery",
    "Personal Development",
    "History and Society",
    "Sports and Fitness",
    "Education and Learning"
]

def get_daily_topic():
    """Günün konusunu belirle (deterministik)"""
    day_of_year = datetime.now().timetuple().tm_yday
    return TOPICS[day_of_year % len(TOPICS)]

def get_daily_level():
    """Günün seviyesini belirle (haftada tüm seviyeleri kapsayacak şekilde)"""
    day_of_week = datetime.now().weekday()
    return LEVELS[day_of_week % len(LEVELS)]

def get_unsplash_image_url(topic):
    """Unsplash'tan konuya uygun fotoğraf URL'i oluştur"""
    # Unsplash Source API kullanarak rastgele ama deterministik fotoğraf
    seed = hashlib.md5(f"{topic}-{datetime.now().date()}".encode()).hexdigest()[:8]
    query = topic.replace(' ', ',').lower()
    return f"https://source.unsplash.com/800x600/?{query}&sig={seed}"

def generate_daily_content(topic, level):
    """Gemini AI ile günlük içerik üret"""
    
    genai.configure(api_key=GEMINI_API_KEY)
    model = genai.GenerativeModel('gemini-pro')
    
    # Seviyeye göre kelime sayısı
    word_counts = {
        'A1': '80-100',
        'A2': '100-120',
        'B1': '120-150',
        'B2': '150-180',
        'C1': '180-220',
        'C2': '200-250'
    }
    
    word_count = word_counts.get(level, '150-200')
    
    prompt = f"""Create a daily English learning content for level {level} about "{topic}".

IMPORTANT REQUIREMENTS:
1. Write a COMPLETE paragraph ({word_count} words) in English suitable for {level} level learners
2. The paragraph MUST be substantial, interesting, informative, and natural
3. DO NOT write just 2-3 sentences - write a FULL paragraph with multiple sentences
4. Include 5-7 useful vocabulary words, phrases, or expressions from the text
5. Provide complete Turkish translation of the entire paragraph
6. List key vocabulary/phrases with Turkish meanings and example sentences

LEVEL GUIDELINES:
- A1/A2: Simple vocabulary, present tense, basic sentence structures
- B1/B2: More complex sentences, various tenses, common idioms
- C1/C2: Advanced vocabulary, nuanced expressions, sophisticated structures

FORMAT YOUR RESPONSE EXACTLY AS JSON (no extra text):
{{
    "level": "{level}",
    "topic": "{topic}",
    "title": "Engaging title (5-8 words)",
    "english_text": "A FULL paragraph here with {word_count} words. Multiple sentences covering different aspects of the topic. Include interesting details and examples.",
    "turkish_translation": "Tam Türkçe çeviri - bütün paragrafın çevirisi",
    "vocabulary": [
        {{"term": "word or phrase from text", "meaning": "Türkçe anlamı", "example": "Example sentence in English"}},
        {{"term": "another word", "meaning": "Türkçe anlamı", "example": "Example sentence"}},
        {{"term": "phrase", "meaning": "Türkçe anlamı", "example": "Example sentence"}},
        {{"term": "expression", "meaning": "Türkçe anlamı", "example": "Example sentence"}},
        {{"term": "vocabulary", "meaning": "Türkçe anlamı", "example": "Example sentence"}}
    ]
}}

WRITE A COMPLETE, SUBSTANTIAL PARAGRAPH - NOT JUST 2-3 SHORT SENTENCES!"""

    try:
        response = model.generate_content(prompt)
        text = response.text.strip()
        
        # JSON'ı çıkar (markdown kod bloğu içinde olabilir)
        json_match = re.search(r'```(?:json)?\s*(.*?)\s*```', text, re.DOTALL)
        if json_match:
            text = json_match.group(1)
        
        # Bazen sadece { ile başlıyor
        if not text.startswith('{'):
            json_start = text.find('{')
            if json_start != -1:
                text = text[json_start:]
        
        content = json.loads(text)
        
        # İçeriğin yeterli uzunlukta olduğunu kontrol et
        word_count_check = len(content.get('english_text', '').split())
        if word_count_check < 50:
            print(f"Warning: Content too short ({word_count_check} words), regenerating...")
            raise ValueError("Content too short")
        
        print(f"✓ Generated content: {word_count_check} words")
        return content
    
    except Exception as e:
        print(f"Error generating content: {e}")
        print(f"Response text: {text[:500] if 'text' in locals() else 'N/A'}")
        
        # Daha iyi fallback içerik
        return {
            "level": level,
            "topic": topic,
            "title": f"Exploring {topic} - A {level} Guide",
            "english_text": f"Today we delve into the fascinating world of {topic}. This subject offers numerous opportunities to expand our English vocabulary and understanding. Learning about {topic} helps us communicate more effectively in various real-world situations. We encounter related vocabulary and expressions in daily conversations, news articles, and professional settings. By studying this topic, we develop both our language skills and cultural awareness. The practical applications of this knowledge extend far beyond the classroom, enriching our ability to engage with English speakers globally.",
            "turkish_translation": f"Bugün {topic} konusunun büyüleyici dünyasına dalıyoruz. Bu konu, İngilizce kelime dağarcığımızı ve anlayışımızı genişletmek için çok sayıda fırsat sunuyor. {topic} hakkında öğrenmek, çeşitli gerçek hayat durumlarında daha etkili iletişim kurmamıza yardımcı oluyor. İlgili kelime ve ifadelere günlük konuşmalarda, haber makalelerinde ve profesyonel ortamlarda rastlıyoruz. Bu konuyu çalışarak hem dil becerilerimizi hem de kültürel farkındalığımızı geliştiriyoruz. Bu bilginin pratik uygulamaları sınıfın çok ötesine uzanıyor ve küresel olarak İngilizce konuşanlarla etkileşim kurma yeteneğimizi zenginleştiriyor.",
            "vocabulary": [
                {"term": "delve into", "meaning": "derinlemesine incelemek, dalmak", "example": "Let's delve into this topic more deeply."},
                {"term": "fascinating", "meaning": "büyüleyici, çok ilginç", "example": "The documentary was absolutely fascinating."},
                {"term": "expand vocabulary", "meaning": "kelime dağarcığını genişletmek", "example": "Reading helps expand your vocabulary significantly."},
                {"term": "effectively", "meaning": "etkili bir şekilde", "example": "She communicates effectively with her team."},
                {"term": "cultural awareness", "meaning": "kültürel farkındalık", "example": "Travel increases cultural awareness and understanding."}
            ]
        }

def create_rss_item(content, image_url):
    """RSS item oluştur"""
    
    item = ET.Element('item')
    
    # Title
    title = ET.SubElement(item, 'title')
    title.text = f"[{content['level']}] {content['title']}"
    
    # Link (unique per run)
    link = ET.SubElement(item, 'link')
    timestamp = datetime.now().strftime('%Y-%m-%d-%H-%M')
    link.text = f"{FEED_LINK}#{timestamp}"
    
    # Description (HTML content with proper image)
    description = ET.SubElement(item, 'description')
    
    # Escape HTML properly for RSS
    html_content = f"""<![CDATA[
    <div style="font-family: Arial, sans-serif; max-width: 700px; margin: 0 auto;">
        <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 20px; border-radius: 10px 10px 0 0;">
            <h2 style="margin: 0; font-size: 24px;">📚 Level: {content['level']}</h2>
            <p style="margin: 5px 0 0 0; opacity: 0.9;">Topic: {content['topic']}</p>
        </div>
        
        <img src="{image_url}" alt="{content['topic']}" style="width: 100%; max-width: 700px; height: auto; display: block; margin: 0;" />
        
        <div style="padding: 20px; background: #f8f9fa; border-radius: 0 0 10px 10px;">
            <h3 style="color: #333; margin-top: 0;">📖 English Text</h3>
            <p style="line-height: 1.8; color: #444; font-size: 16px; background: white; padding: 15px; border-radius: 8px; border-left: 4px solid #667eea;">
                {content['english_text']}
            </p>
            
            <h3 style="color: #333; margin-top: 30px;">🇹🇷 Türkçe Çeviri</h3>
            <p style="line-height: 1.8; color: #666; font-size: 15px; background: white; padding: 15px; border-radius: 8px; border-left: 4px solid #764ba2;">
                {content['turkish_translation']}
            </p>
            
            <h3 style="color: #333; margin-top: 30px;">💡 Key Vocabulary &amp; Phrases</h3>
            <div style="background: white; padding: 15px; border-radius: 8px;">
    """
    
    for vocab in content['vocabulary']:
        html_content += f"""
                <div style="margin-bottom: 15px; padding: 10px; background: #f0f0f0; border-radius: 5px;">
                    <strong style="color: #667eea; font-size: 16px;">{vocab['term']}</strong><br/>
                    <span style="color: #666;">📝 {vocab['meaning']}</span><br/>
                    <span style="color: #888; font-style: italic; font-size: 14px;">Example: {vocab['example']}</span>
                </div>
        """
    
    html_content += """
            </div>
        </div>
    </div>
    ]]>"""
    
    description.text = html_content
    
    # PubDate
    pub_date = ET.SubElement(item, 'pubDate')
    pub_date.text = datetime.now(timezone.utc).strftime('%a, %d %b %Y %H:%M:%S GMT')
    
    # GUID (unique per run)
    guid = ET.SubElement(item, 'guid')
    guid.set('isPermaLink', 'false')
    # Include timestamp to ensure uniqueness even on same day
    timestamp = datetime.now().strftime('%Y%m%d-%H%M%S')
    guid.text = f"daily-english-{timestamp}"
    
    # Enclosure (image) - kritik: RSS okuyucuların görseli göstermesi için
    enclosure = ET.SubElement(item, 'enclosure')
    enclosure.set('url', image_url)
    enclosure.set('type', 'image/jpeg')
    enclosure.set('length', '0')  # Bazı RSS okuyucular için gerekli
    
    # Media content (alternatif görsel yöntemi)
    # Bazı RSS okuyucular için
    media_content = ET.SubElement(item, '{http://search.yahoo.com/mrss/}content')
    media_content.set('url', image_url)
    media_content.set('type', 'image/jpeg')
    media_content.set('medium', 'image')
    
    return item

def create_or_update_rss(new_item):
    """RSS feed'i oluştur veya güncelle"""
    
    # Mevcut RSS'i yükle veya yeni oluştur
    if os.path.exists(RSS_FILE):
        tree = ET.parse(RSS_FILE)
        root = tree.getroot()
        channel = root.find('channel')
    else:
        rss = ET.Element('rss')
        rss.set('version', '2.0')
        rss.set('xmlns:atom', 'http://www.w3.org/2005/Atom')
        rss.set('xmlns:media', 'http://search.yahoo.com/mrss/')  # Media RSS namespace
        
        channel = ET.SubElement(rss, 'channel')
        
        title = ET.SubElement(channel, 'title')
        title.text = FEED_TITLE
        
        link = ET.SubElement(channel, 'link')
        link.text = FEED_LINK
        
        description = ET.SubElement(channel, 'description')
        description.text = FEED_DESCRIPTION
        
        language = ET.SubElement(channel, 'language')
        language.text = 'en-us'
        
        # Self link
        atom_link = ET.SubElement(channel, '{http://www.w3.org/2005/Atom}link')
        atom_link.set('href', f"{FEED_LINK}feed.xml")
        atom_link.set('rel', 'self')
        atom_link.set('type', 'application/rss+xml')
        
        root = rss
    
    # Yeni item'ı en başa ekle
    channel.insert(0, new_item)
    
    # Son 30 günü tut
    items = channel.findall('item')
    if len(items) > 30:
        for item in items[30:]:
            channel.remove(item)
    
    # Güzel formatla ve kaydet
    xml_str = ET.tostring(root, encoding='unicode')
    dom = minidom.parseString(xml_str)
    pretty_xml = dom.toprettyxml(indent='  ')
    
    # XML deklarasyonunu düzelt
    pretty_xml = '\n'.join([line for line in pretty_xml.split('\n') if line.strip()])
    
    with open(RSS_FILE, 'w', encoding='utf-8') as f:
        f.write(pretty_xml)
    
    print(f"✅ RSS feed updated: {RSS_FILE}")

def main():
    """Ana fonksiyon"""
    
    if not GEMINI_API_KEY:
        print("❌ Error: GEMINI_API_KEY environment variable not set")
        return
    
    print("🚀 Starting Daily English Learning RSS Generator...")
    
    # Günün konusu ve seviyesini belirle
    topic = get_daily_topic()
    level = get_daily_level()
    
    print(f"📅 Date: {datetime.now().strftime('%Y-%m-%d')}")
    print(f"📚 Level: {level}")
    print(f"📖 Topic: {topic}")
    
    # İçerik üret
    print("🤖 Generating content with Gemini AI...")
    content = generate_daily_content(topic, level)
    
    # Fotoğraf URL'i al
    image_url = get_unsplash_image_url(topic)
    print(f"🖼️  Image: {image_url}")
    
    # RSS item oluştur
    print("📝 Creating RSS item...")
    item = create_rss_item(content, image_url)
    
    # RSS feed'i güncelle
    print("💾 Updating RSS feed...")
    create_or_update_rss(item)
    
    print("✨ Done! RSS feed is ready.")
    print(f"📡 Feed URL: {FEED_LINK}feed.xml")

if __name__ == '__main__':
    main()
