import re
import numpy as np
import pandas as pd

from fcm_django.models import FCMDevice

from api.models import Counter

from api.scraper import ResultScraper, ROOT_RESULTS_URL, RESULTS_URI

from django.core.mail import EmailMessage

scraper = ResultScraper(ROOT_RESULTS_URL+RESULTS_URI)

COUNTER = Counter.objects.first()

def result_status():
    try:
        scraper.scrape()
    except:
        return None

    results = pd.DataFrame.from_dict(scraper.results)

    pattern = r'Dec.*2017.*B\.Tech'
    filtered = results[results['text'].str.contains(pattern, flags=re.DOTALL)]
    
    if len(filtered) > 0:
        return (True,filtered)
    else:
        return False

def verify_result_and_notify():
    devices = FCMDevice.objects.all()
    try:
        status, df = result_status()
    except:
        return None

    if status is None:
        return None
        
    if status and COUNTER < 2:
        try:
            link = df.href[0]
        except:
            link = 'http://ipu.ac.in'

        devices.send_message(title="RESULT AA GAYA(SHAYAD)", message="ipu.ac.in dekho (or try clicking on this)", data={'click_action' : link})     
        
        COUNTER.count += 1
        COUNTER.save()
