from util.mongo_helper import MongoHelper
from datetime import datetime, timedelta
import json
from config import Config
from util.email_helper import EmailHelper
from apscheduler.schedulers.background import BackgroundScheduler


class KeyExpirationAlert():
    def __init__(self):
        self.scheduler = BackgroundScheduler()

        self.mongo_helper = MongoHelper()
        self.email_helper = EmailHelper()
        self.mongo_helper.mongo_connect()
        self.config = Config()
        self.notifcation_obj = self.config.get('notifications')
        self.notice1_obj = self.notifcation_obj['notice1']
        self.notice2_obj = self.notifcation_obj['notice2']
        self.final_notice_obj = self.notifcation_obj['final_notice']


    def checkKeys(self):
        query_all = self.mongo_helper.api_key_collection.find({})
        now = datetime.utcnow()
        for x in query_all:
            time_diff = (x['expirationDate'] - now).total_seconds()
            exp_notifications = x['expiration_notice']
            has_first_notice = exp_notifications['notice1']
            has_second_notice = exp_notifications['notice2']
            has_final_notice = exp_notifications['final_notice']
            notice1_time = time_diff <= self.notice1_obj['seconds_till_expiration'] and not has_first_notice
            notice2_time = time_diff <= self.notice2_obj['seconds_till_expiration'] and not has_second_notice
            final_notice_time = time_diff <= self.final_notice_obj['seconds_till_expiration'] and not has_final_notice

            if notice1_time:
                x['expiration_notice']['notice1'] = True
                print('sent: 1st notice {}'.format(x['email']))
                self.send_notification(x['email'], self.notice1_obj)

            elif notice2_time:
                x['expiration_notice']['notice2'] = True
                print('sent: 2nd notice {}'.format(x['email']))
                self.send_notification(x['email'], self.notice2_obj)
            
            elif final_notice_time:
                x['expiration_notice']['final_notice'] = True
                print('sent: final notice {}'.format(x['email']))
                self.send_notification(x['email'], self.final_notice_obj)
            else:
                #print('No update required')
                return;
            #print('updating record!')
            # update flags
            self.mongo_helper.api_key_collection.update_one(
                { '_id': x['_id'] },
                { '$set': { 'expiration_notice': x['expiration_notice'] } }, 
                upsert=False
            )

    def send_notification(self, to, notification):
        message = {
            "to": to,
            "subject": notification['subject'],
            "body": notification['body'],
        }
        self.email_helper.send_mail(message)
    
    def shutdown(self):
        self.scheduler.shutdown()

    def start_corn_job(self):
        
        self.scheduler.add_job(self.checkKeys, 'interval', seconds=self.config.get('check_expiration_freq'))
        self.scheduler.start()

