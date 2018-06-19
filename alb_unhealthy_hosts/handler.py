 #!/usr/bin/env python3
"""
## Pre-requsites: Need to add tag on loadbalancer as `Environment:Production`.Also need proper permission on S3 Bucket
Name: Enable AccessLogs for production load-balancers
Author: Deepak Dalvi
Version: 1.0.0
"""

import boto3
from slackclient import SlackClient
import itertools
DEFAULT_REGION = 'ap-southeast-1'
SLACK_API_TOKEN = ''
SLACK_CHANNEL_NAME = ''


def lambda_handler(event, context):
    sc = SlackClient(SLACK_API_TOKEN)
    alb_names = []
    alb = boto3.client('elbv2', region_name=DEFAULT_REGION)
    tg = []
    prod_lb = []
    res = alb.describe_target_groups()
    for t in res['TargetGroups']:
        tg.append(t['TargetGroupArn'])
    # print(tg) 
    for item in range(len(tg)):
        result = []
        result.append(tg[item])
        tags_res = alb.describe_tags(ResourceArns=result)
        # print(tags_res)
        for tag in tags_res['TagDescriptions'][0]['Tags']:
            try:
                if tag['Key'].lower() == 'environment' and tag['Value'].lower() == 'production':
                    prod_lb.append(
                        tags_res['TagDescriptions'][0]['ResourceArn'])
            except KeyError:
                print("error")
                continue
    print(prod_lb)

    # print(tg)
    for target in prod_lb:
        res = alb.describe_target_health(
        TargetGroupArn=target)
        name = target.split(':')[-1:][0].split('/')[1]
        # print(res)
        total = len(res['TargetHealthDescriptions'])
        count = 0
        inst_ids = []
        for item in res['TargetHealthDescriptions']:
            if item['TargetHealth']['State'] != 'healthy':
                count = count + 1
                inst_ids.append(
                    {item['Target']['Id']: item['TargetHealth']['State']})
        if count > 0:
            MSG = ">TargetGroups : *{}* \n STATE: *CRITICAL* \n UN-HEALTHY INSTANCES `{} / {}`  \n INST_IDs:`{}`".format(
            name, count, total, inst_ids)
            print(MSG)
            sc.api_call(
                    "chat.postMessage",
                    channel=SLACK_CHANNEL_NAME,
                    text=MSG
            )

    return {
                'statusCode': 200
            }

