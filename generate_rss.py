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
    
    prompt = f"""Create a daily English learning content for level {level} about "{topic}".

REQUIREMENTS:
1. Write a short paragraph (100-150 words) in English suitable for {level} level learners
2. The content should be interesting, informative, and natural
3. Include 3-5 useful vocabulary words, phrases, or expressions
4. Provide Turkish translation of the entire paragraph
5. List key vocabulary/phrases with explanations

FORMAT YOUR RESPONSE EXACTLY AS JSON:
{{
    "level": "{level}",
    "topic": "{topic}",
    "english_text": "the English paragraph here",
    "turkish_translation": "Türkçe çeviri buraya",
    "vocabulary": [
        {{"term": "word or phrase", "meaning": "Turkish meaning", "example": "example sentence"}},
        {{"term": "word or phrase", "meaning": "Turkish meaning", "example": "example sentence"}}
    ],
    "title": "Catchy title for this content"
}}

Make it educational, engaging, and appropriate for {level} level."""

    try:
        response = model.generate_content(prompt)
        text = response.text.strip()
        
        # JSON'ı çıkar (markdown kod bloğu içinde olabilir)
        json_match = re.search(r'```json\s*(.*?)\s*```', text, re.DOTALL)
        if json_match:
            text = json_match.group(1)
        
        content = json.loads(text)
        return content
    
    except Exception as e:
        print(f"Error generating content: {e}")
        # Fallback içerik
        return {
            "level": level,
            "topic": topic,
            "title": f"Daily English Learning: {topic}",
            "english_text": f"Today we explore {topic}. This is an interesting subject that helps us improve our English skills.",
            "turkish_translation": f"Bugün {topic} konusunu keşfediyoruz. Bu, İngilizce becerilerimizi geliştirmemize yardımcı olan ilginç bir konu.",
            "vocabulary": [
                {"term": "explore", "meaning": "keşfetmek, araştırmak", "example": "We explore new ideas every day."}
            ]
        }

def create_rss_item(content, image_url):
    """RSS item oluştur"""
    
    item = ET.Element('item')
    
    # Title
    title = ET.SubElement(item, 'title')
    title.text = f"[{content['level']}] {content['title']}"
    
    # Link (unique per day)
    link = ET.SubElement(item, 'link')
    date_str = datetime.now().strftime('%Y-%m-%d')
    link.text = f"{FEED_LINK}#{date_str}"
    
    # Description (HTML content)
    description = ET.SubElement(item, 'description')
    
    html_content = f"""
    <div style="font-family: Arial, sans-serif; max-width: 700px; margin: 0 auto;">
        <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 20px; border-radius: 10px 10px 0 0;">
            <h2 style="margin: 0; font-size: 24px;">📚 Level: {content['level']}</h2>
            <p style="margin: 5px 0 0 0; opacity: 0.9;">Topic: {content['topic']}</p>
        </div>
        
        <img src="{image_url}" alt="{content['topic']}" style="width: 100%; height: auto; display: block;" />
        
        <div style="padding: 20px; background: #f8f9fa; border-radius: 0 0 10px 10px;">
            <h3 style="color: #333; margin-top: 0;">📖 English Text</h3>
            <p style="line-height: 1.8; color: #444; font-size: 16px; background: white; padding: 15px; border-radius: 8px; border-left: 4px solid #667eea;">
                {content['english_text']}
            </p>
            
            <h3 style="color: #333; margin-top: 30px;">🇹🇷 Türkçe Çeviri</h3>
            <p style="line-height: 1.8; color: #666; font-size: 15px; background: white; padding: 15px; border-radius: 8px; border-left: 4px solid #764ba2;">
                {content['turkish_translation']}
            </p>
            
            <h3 style="color: #333; margin-top: 30px;">💡 Key Vocabulary & Phrases</h3>
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
    """
    
    description.text = html_content
    
    # PubDate
    pub_date = ET.SubElement(item, 'pubDate')
    pub_date.text = datetime.now(timezone.utc).strftime('%a, %d %b %Y %H:%M:%S GMT')
    
    # GUID
    guid = ET.SubElement(item, 'guid')
    guid.set('isPermaLink', 'false')
    guid.text = f"daily-english-{datetime.now().strftime('%Y%m%d')}"
    
    # Enclosure (image)
    enclosure = ET.SubElement(item, 'enclosure')
    enclosure.set('url', image_url)
    enclosure.set('type', 'image/jpeg')
    
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
