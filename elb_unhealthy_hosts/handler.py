#!/usr/bin/env python3
"""
## Pre-requsites: Need to add tag on loadbalancer as `Environment:Production`.Also need proper permission on S3 Bucket
Name: Enable AccessLogs for production load-balancers
Author: Deepak Dalvi
Version: 1.0.0
"""

import boto3
from slackclient import SlackClient
DEFAULT_REGION = 'ap-southeast-1'
SLACK_API_TOKEN = ''
SLACK_CHANNEL_NAME = ''


def lambda_handler(event, context):
    sc = SlackClient(SLACK_API_TOKEN)
    elb_names = []
    tags = []
    prod_lb = []
    elb = boto3.client('elb', region_name=DEFAULT_REGION)

    res = elb.describe_load_balancers()
    for item in res['LoadBalancerDescriptions']:
        elb_names.append(item['LoadBalancerName'])

    for item in range(0, len(elb_names)):
        temp_elb = []
        tags_res = []
        temp_elb.append(elb_names[item])
        tags_res = elb.describe_tags(LoadBalancerNames=temp_elb)
        for tag in tags_res['TagDescriptions'][0]['Tags']:
            try:
                if tag['Key'].lower() == 'environment' and tag['Value'].lower() == 'production':
                    prod_lb.append(
                        tags_res['TagDescriptions'][0]['LoadBalancerName'])
            except KeyError:
                print("error")
                continue
    print(prod_lb)
    for item in prod_lb:
        unHealth_inst = []
        count = 0
        total_instances = 0
        response = elb.describe_instance_health(
            LoadBalancerName=item,
        )
        for inst in response['InstanceStates']:
            total_instances = total_instances+1
            if inst['State'] != 'InService':       
                print(inst['State'])
                unHealth_inst.append(inst['InstanceId'])
                count=count+1
                MSG = ">ELB : *{}* \n STATE: *CRITICAL* \n UN-HEALTHY INSTANCES `{} / {}`  \n INST_ID:`{}`".format(
                    item, count, total_instances, unHealth_inst)
                print(MSG)
                sc.api_call(
                    "chat.postMessage",
                    channel=SLACK_CHANNEL_NAME,
                    text=MSG
                )
    return {

                'statusCode': 200
            }
