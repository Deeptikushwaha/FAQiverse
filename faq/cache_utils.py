# Create a new file: faq/cache_utils.py

from django.core.cache import cache
import redis

def view_all_cached_translations():
    """View all cached translations"""
    r = redis.Redis(host='localhost', port=6379, db=0)
    all_keys = r.keys('faq_*')
    
    translations = {}
    for key in all_keys:
        key_str = key.decode('utf-8')
        value = cache.get(key_str)
        translations[key_str] = value
    
    return translations

def clear_cached_translations():
    """Clear all cached translations"""
    r = redis.Redis(host='localhost', port=6379, db=0)
    keys = r.keys('faq_*')
    for key in keys:
        cache.delete(key.decode('utf-8'))
    return len(keys)

def get_translation_stats():
    """Get statistics about cached translations"""
    translations = view_all_cached_translations()
    stats = {
        'total_translations': len(translations),
        'languages': set(),
        'faqs': set()
    }
    
    for key in translations.keys():
        # key format: faq_id_field_lang
        parts = key.split('_')
        if len(parts) >= 4:
            stats['languages'].add(parts[3])
            stats['faqs'].add(parts[1])
    
    stats['languages'] = list(stats['languages'])
    stats['total_faqs'] = len(stats['faqs'])
    
    return stats