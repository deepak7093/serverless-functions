# Monitor an Application Load Balancer unhealthy hosts/instances

This consist lambda function to monitor an application load balancer to detect unhealthy instances and provides slack notification.

## Configure

- Install required pakages

  `pip install -r requirements.txt`

- Set ENVIRONMENT VARIABLES

Inside `handler.py`, set values for 
  `DEFAULT_REGION`, `SLACK_CHANNEL_NAME` and  `SLACK_API_TOKEN`.

To generate slack api token see this:
  <https://get.slack.help/hc/en-us/articles/215770388-Create-and-regenerate-API-tokens>

- This function uses tags to identify specific resources, in this we are using `Environment = Production`.

As per your need you can modify the tags.

## Deploy and invoke

- To deploy this function  run

`# sls deploy`

- To test on local

`# sls invoker local -f handler.lambda_handler`

- To test on lambda 

`# sls invoke`

## Set Trigger

You can set CloudWatch Triggers to invoke the function.
See this: https://docs.aws.amazon.com/AmazonCloudWatch/latest/events/RunLambdaSchedule.html
