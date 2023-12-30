# import calendar
import datetime
import json
import os
import random
import time
from datetime import timedelta

import httpagentparser
import pytz
import requests
from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from django.contrib.sites.models import Site
from django.core.exceptions import FieldDoesNotExist
from django.db import transaction
from django.db.models import Q
from django.utils import timezone
from hitcount.models import Hit
from outbox_hitcount.models import HitCount, HitBrowser, HitDevice, HitOS, HitLocation

from .common_date import add_months, get_last_day_of_month

# from outbox_hitcount.models import *


# from urllib2 import urlopen

def get_response(url, timeout=60):
    '''
        Use more than one requests.get
        default # timeout 60 second (1 minutes)
    '''
    return requests.get(url, timeout=timeout)

def get_popen(url):
    '''
        use os.popen(curl ....)
    '''
    return os.popen(url).read()

def get_geolocation_opt3(str_ip_address):
    '''
        Save IP address first if request json geolocation not exists
        ref: https://www.geeksforgeeks.org/formatted-string-literals-f-strings-python/
    '''
    url = f"http://ip-api.com/json/{str_ip_address}"

    # res = requests.get(url, timeout=60) # 45 request per minute
    res = get_response(url)
    if res:
        res = res.json()       

        if 'success' not in res:
            return None
        if 'country' not in res:
            return None
        if 'city' not in res:
            return None
        if res['status'] == 'success':
            return (res['country'], res['city'])
    return None

def get_geolocation_opt1(str_ip_address):
    '''
        Save IP address first if request json geolocation not exists
        exp: 180.243.14.149
        # 1000 per hari
    '''
    url = f"curl https://ipapi.co/{str_ip_address}/json/"
    result = get_popen(url)
    if result:
        tmp = json.loads(result)

        if 'country_name' not in tmp:
            return None
        if 'city' not in tmp:
            return None
        return (tmp['country_name'], tmp['city'])
    return None

def get_geolocation_opt2(str_ip_address):
    '''
        Save IP address first if request json geolocation not exists
    '''
    # res = requests.get('http://ipwho.is/' + str_ip_address) # 10.000 request per minute
    url = f"http://ipwho.is/{str_ip_address}"  # 10.000 request per minute
    res = get_response(url)
    if res:
        res = res.json()

        if 'success' not in res:
            return None
        if 'country' not in res:
            return None
        if 'city' not in res:
            return None
        if res['success']:
            return (res['country'], res['city'])
    return None

def get_geolocation_opt4(str_ip_address):
    '''
        Save IP address first if request json geolocation not exists
        # 1000 per hari
    '''
    # result = os.popen("curl http://api.db-ip.com/v2/free/"+ str_ip_address).read() # 1000 per hari
    url = f"curl http://api.db-ip.com/v2/free/{str_ip_address}"
    result = get_popen(url)
    if result:
        tmp = json.loads(result)
        
        if 'countryName' not in tmp:
            return None
        if 'city' not in tmp:
            return None
        return (tmp['countryName'], tmp['city'])
    return None

# ada version yg belum bagus di split sehingga tersimpan
# X 10.15.5) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.1.1 Safari/605.1.15 (Applebot/0.1

def correct_version(version):
    '''
        Clean char ( and ) in version result
    '''
    if version.strip():
        tmp = version.replace("(", "<-!->")
        tmp = tmp.replace(")", "<-!->")
        return tmp.split("<-!->")[0]
    return version

def is_field_exists(model, field):
    '''
        Check field is exists
    '''
    # for field in cls._meta.get_fields(include_hidden=True):
    #     if field.name == field:
    #         return True
    # return False

    if model:
        try:
            # field = model._meta.get_field(field)
            for i in model._meta.get_fields():
                if (not i.many_to_many) and (i.name == field):
                    return True

        except FieldDoesNotExist:
            return False

        # return False    # tidak ada error, tapi data tidak ditemukan
    return False

# def get_for_object(obj, end_date):
#     ctype = ContentType.objects.get_for_model(obj)
#     hit_count, created = get_or_create(content_type=ctype, object_pk=obj.pk)
#     return hit_count

def get_or_set_browser(browser):
    '''
        create browser name if not exists
    '''
    name = browser.get('name') if browser else None
    version = browser.get('version') if browser else None

    # jika masih kosong karena tidak ada data maka set not defined
    if not name:
        name = 'none'
    if not version:
        version = 'none'
    version = correct_version(version)

    browser, created = HitBrowser.objects.get_or_create(
        name=name, version=version)
    # return HitBrowser.objects.get_or_create(name=name, version=version)
    return browser

def get_or_set_os(param_os):
    '''
        create param_os if not exists
    '''
    name = param_os.get('name') if param_os else None
    version = param_os.get('version') if param_os else None

    # jika masih kosong karena tidak ada data maka set not defined
    if not name:
        name = 'none'
    if not version:
        version = 'none'
    version = correct_version(version)

    param_os, created = HitOS.objects.get_or_create(name=name, version=version)
    return param_os

def get_or_set_device(device):
    '''
        create device if not exists
    '''
    name = device.get('name') if device else None
    version = device.get('version') if device else None

    # jika masih kosong karena tidak ada data maka set not defined
    if not name:
        name = 'none'
    if not version:
        version = 'none'
    version = correct_version(version)

    device, created = HitDevice.objects.get_or_create(
        name=name, version=version)
    return device

def get_or_set_location(ip_address):
    '''
        Location: '192.168.13.29' format string IP ADDRESS
        Khusus location field version tidak ada di ganti ip_address
        kode unik cukup IP address saja
    '''
    # ip_address = location.get('ip_address') if location else None

    # jika masih kosong karena tidak ada data maka set not defined
    if not ip_address:
        ip_address = 'none'

    location, created = HitLocation.objects.get_or_create(
        ip_address=ip_address)
    return location

# param type dict
def hitcount_insert_m2m_field(hit_count, browser, param_os, platform, ip_address):
    '''
        os di rename menjadi param_os
        karena os mengacu ke import os python
    '''
    # hit_count = data.get('hit_count')
    # browser = data.get('browser')
    # os = data.get('os')
    # platform = data.get('platform')
    # ip_address = data.get('ip_address')
    # print('inside hitcount_insert m2m', param_os, browser)

    obj = get_or_set_browser(browser)
    hit_count.hits_browser.add(obj)
    # hit_count.browser_count += 1

    # get or set os
    obj = get_or_set_os(param_os)
    hit_count.hits_os.add(obj)
    # hit_count.os_count += 1

    # get or set device
    obj = get_or_set_device(platform)
    hit_count.hits_device.add(obj)
    # hit_count.device_count += 1

    # get or set location
    obj = get_or_set_location(ip_address)
    hit_count.hits_location.add(obj)
    # hit_count.location_count += 1
    # hit_count.save()

# def special_condition(object_pk, end_date, data):
def special_condition(object_pk, data):
    '''
        Special condition:
        if site_id exists
            but object_pk not found, search on other model
            update hitcount for all model
    '''
    # jika di model yg aktif tidak ada
    model_priority = ['artikel', 'berita', 'galery_video', 'galery_foto',
                      'halaman_statis', 'pengumuman', 'social_media']  # 'link_terkait',

    for i in model_priority:
        # print('proses', i)
        field_exists = False
        content_type = ContentType.objects.filter(model=i)
        if content_type:
            ct_class = content_type.get().model_class()
            if is_field_exists(ct_class, 'site') and is_field_exists(ct_class, 'created_at'):
                field_exists = True            

        if field_exists:
            obj = ct_class.objects.filter(
                id=object_pk)  # cari site_id dari model
            site_id = None
            end_date = None

            if obj:
                site_id = obj.get().site_id
                end_date = obj.get().created_at

            if site_id and end_date:
                # cari nama site dari site_id yg di dapat
                site = Site.objects.filter(id=site_id)
                if site:
                    site = site.get()
                    content_type_site = ContentType.objects.get_for_model(
                        site)

                    hit_count, created = HitCount.objects.get_or_create(
                        content_type=content_type_site,
                        object_pk=site_id,
                        defaults={
                            'end_date': end_date,
                            'site_id': site_id
                        }
                    )
                    hit_count.count += 1

                    # hit_count.update(count=F(count)+1)
                    # print('data OS',data)
                    data = {
                        'hit_count': hit_count,
                        'browser': data['browser'],
                        'param_os': data['param_os'],
                        'platform': data['platform'],
                        'ip_address': data['ip_address']
                    }

                    hitcount_insert_m2m_field(**data)
                    hit_count.save()
                    # print(f'proses {i} saved [special condition]')
        else:
            print('[special condition] not found site id or created date')

@transaction.atomic
# def do_summary(qs, end_date):
def do_summary(qs):
    '''
        Jalankan proses summary
    '''
    j = 0
    count = qs.count()
    # result = False
    # try:
    for i in qs:
        ip_address = i.ip
        user_agent = i.user_agent
        user_agent_parser = httpagentparser.detect(user_agent)

        platform = user_agent_parser.get('platform')
        param_os = user_agent_parser.get('os')
        # bot = user_agent_parser.get('bot')
        # dist = user_agent_parser.get('dist')
        browser = user_agent_parser.get('browser')

        # hitcount_id = i.hitcount.id
        object_pk = i.hitcount.object_pk
        # print('---')
        # print()

        content_type = i.hitcount.content_type
        end_date = i.created

        # content_type_id = content_type.id
        j += 1
        # print(f"{j} of {count} object_pk {object_pk} model {content_type.model} hitcount_id {i.hitcount.id}")
        site_id = None

        # dari content type ubah mejadi object
        # dari object, cek apakah ada field site_id
        # jika ada ambil PK dari object ini
        # ct = ContentType.objects.get_for_id(content_type_id)
        # print('content type=', content_type)
        ct_class = content_type.model_class()
        # print('ct_class=', ct_class)
        # print('ct=', ct)
        # ct_class = ct.model_class()
        # print('ct_class=', ct_class)
        # Jika ct_class tidak ada berarti model tersebut tidak di temukan di project
        # misal galery_video
        # print('ct_class',ct_class)

        if ct_class:
            # print(ct_class._meta.get_fields())
            # obj = ct.get_object_for_this_type(id=object_pk)
            # print('ct_class=', ct_class)
            # print('obj=', obj)                
            # cek apakah ada field site ID

            mfound = False
            if is_field_exists(ct_class, 'site'):
                obj = ct_class.objects.filter(
                    id=object_pk)  # cari site_id dari model
                if obj:
                    site_id = obj.get().site_id
                    # print(f"site_id {site_id}")
                    mfound = True
                else:
                    print(f"site_id {object_pk} tidak ditemukan!")
            else:
                print(f'site_id tidak ditemukan di model')

            if not mfound:
                data = {
                    'hit_count': None,
                    'browser': browser,
                    'param_os': param_os,
                    'platform': platform,
                    'ip_address': ip_address
                }
                special_condition(object_pk, data)

        # 1. jika ada field site_id, maka insert summary baru content_type = site
        if site_id:
            # print('site_id',site_id)

            # cari nama site dari site_id yg di dapat
            site = Site.objects.filter(id=site_id)
            if site:
                site = site.get()
                content_type_site = ContentType.objects.get_for_model(site)

                hit_count, created = HitCount.objects.get_or_create(
                    content_type=content_type_site,
                    object_pk=site_id,
                    defaults={'end_date': end_date, 'site_id': site_id}
                )
                # print('hit_count', type(hit_count))
                hit_count.count += 1

                # hit_count.update(count=F(count)+1)
                # print('param_os',param_os)
                # print('browser',browser)
                data = {
                    'hit_count': hit_count,
                    'browser': browser,
                    'param_os': param_os,
                    'platform': platform,
                    'ip_address': ip_address
                }
                # print('data',*data)
                
                hitcount_insert_m2m_field(**data)
                hit_count.save()

        # 2. default insert content_type dari apa adanya data di Hit
        # content_type = ContentType.objects.get_for_model(i)
        if site_id:
            hit_count, created = HitCount.objects.get_or_create(
                content_type=content_type,  # data sudah ada di paling atas
                object_pk=object_pk,
                defaults={'end_date': end_date, 'site_id': site_id}
            )
        else:
            hit_count, created = HitCount.objects.get_or_create(
                content_type=content_type,  # data sudah ada di paling atas
                object_pk=object_pk,
                defaults={'end_date': end_date, 'site_id': None}
            )

        hit_count.count += 1
        # hit_count.save()
        # hit_count.update(count=F(count)+1)

        data = {
            'hit_count': hit_count,
            'browser': browser,
            'param_os': param_os,
            'platform': platform,
            'ip_address': ip_address
        }
        hitcount_insert_m2m_field(**data)
        hit_count.save()

    clear_summary_qs(qs)
    # except:
    #     print('something goes wrong!')
    #     return False

    return True

# @transaction.atomic
def clear_summary_qs(qs):
    '''
        Clear query set yg berhasil di execute
    '''
    number_removed = qs.count()
    # qs.delete()
    for i in qs:
        i.delete()

    # self.stdout.write('Successfully removed %s Hits' % number_removed)
    print(f'Successfully removed {number_removed} Hits')

# proses jumlah bulan, jika -1 maka semua di proses
# def auto_hit_summary(month_count=1):    # default 1 bulan saja, bukan semua data
def auto_hit_summary(max_data=500):    # default 1 bulan saja, bukan semua data
    '''
        Should be auto run in midnight
    '''
    time_zone = getattr(settings, 'TIME_ZONE', 'UTC')  # get setting timezone
    tz = pytz.timezone(time_zone)

    grace = getattr(settings, 'HITCOUNT_KEEP_HIT_IN_DATABASE', {'days': 30})
    period = timezone.now() - timedelta(**grace)
    # qs = Hit.objects.filter(created__lt=period)

    # seluruh data yg akan diringkas ada di qs
    # filter lagi per bulan
    # if qs:

    # ambil bulan dan tahun untuk di filter lagi
    # first_data = qs[0]

    # month_count = 1 # looping sejumlah month_count, jika -1 berarti semua data
    mcount = 3 # batasi looping 5 kali jika hasil query set kosong
    # month = period.month
    # year = period.year
    # end_day_of_month = get_last_day_of_month(year, month)    # return hari

    # # dapatkan range tanggal yang benar
    # begin_date = datetime.date(year, month, 1) # pukul 0:0:0
    # end_date = datetime.date(year, month, end_day_of_month, 23, 59, 59)
    # karena proses awal add_month2 -1 maka di add dulu disini
    tmp = add_months(period, 1)
    begin_date = datetime.datetime(tmp.year, tmp.month, 1)
    # print('datebegin', begin_date)
    
    # mulai ambil data di database
    while mcount > 0:
        begin_date = add_months(begin_date, -1)
        year = begin_date.year
        month = begin_date.month
        end_day_of_month = get_last_day_of_month(year, month)    # return hari
        end_date = datetime.datetime(year, month, end_day_of_month, 23, 59, 59)

        # add time zone
        begin_date = tz.localize(begin_date)
        end_date = tz.localize(end_date)

        # qs = Hit.objects.filter(created__gte=begin_date, created__lte=end_date)

        # !!!
        # Pakai cara ke dua, cari data lebih besar dari grace period,
        # order by created desc
        # limit 500 data (sesuai parameter)
        qs = Hit.objects.filter(created__gte=begin_date).order_by('-id')[:max_data]

        if not qs:
            mcount -= 1
        else:
            if do_summary(qs):
                # print('Begin clear summary')
                # clear_summary_qs(qs) # pindahkan di dalam modul do_summary
                print(f'Complete {mcount}')
                mcount -= 1
            else:
                return False    # jika do_summary gagal di eksekusi, maka keluar looping

            # else:
            #     print('Not Complete')

            # if month_count > 0:
            #     month_count -= 1
            # if month_count == 0:
            #     break

    return True

@transaction.atomic
def auto_get_location(request_per_minute=30, max_data=500):
    '''
        Batasi hit per ment 30 saja agar tidak di banned oleh situs gratisan
        jalankan menggunakan celery
        batasi max data 500
    '''
    start_time = datetime.datetime.now()
    stop_time = start_time + timedelta(minutes=1)
    
    print('max_data', max_data)
    hit_location = HitLocation.objects.filter(
        Q(country=None) | Q(city=None))[:max_data]
    count = 0
    waiting_list = [1, 2, 3, 4, 5, 6, 7]  # random list
    loc = 'loc1'

    for i in hit_location:
        count += 1
        ip_address = i.ip_address
        if count <= request_per_minute:
            location = get_geolocation_opt1(ip_address)            
            loc = 'loc1'
            # print(f'location {location} from {loc}')

            if not location:
                location = get_geolocation_opt2(ip_address)
                loc = 'loc2'
                # print(f'location {location} from {loc}')

            if not location:
                location = get_geolocation_opt3(ip_address)
                loc = 'loc3'
                # print(f'location {location} from {loc}')

            if not location:
                location = get_geolocation_opt4(ip_address)
                loc = 'loc4'
                # print(f'location {location} from {loc}')

            if not location:
                print(f'Location Not Found {ip_address}')
                loc = 'none'
                # print(f'location {location} from {loc}')
            else:
                i.country = location[0]
                i.city = location[1]
                print(f'Update location {ip_address} to {location} from {loc}')
                i.save()
                # sleep 1 detik agar tidak kentara
                time.sleep(random.choice(waiting_list))
        else:
            while datetime.datetime.now() < stop_time:
                print('Waiting for 1 minute')
                time.sleep(random.choice(waiting_list))  # sleep 5 detik

            # reset count
            count = 0
            start_time = datetime.datetime.now()
            stop_time = start_time + timedelta(minutes=1)
            print('Reset variable')

