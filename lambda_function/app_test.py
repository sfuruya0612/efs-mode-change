# -*- coding: utf-8 -*-

import os
import sys
import boto3
import logging

logger = logging.getLogger()
formatter = '%(levelname)s : %(asctime)s : %(message)s'

for handler in logger.handlers:
    logger.removeHandler(handler)
logging.basicConfig(level=logging.INFO, format=formatter)

def lambda_handler(event, context):
    logger.info("Start function")

    client = boto3.client('efs')

    dimension = event["Records"][0]["Sns"]["Message"]["Trigger"]["Dimensions"]
    id = [id.get("value") for id in dimension if id.get("name") == "FileSystemId"]
    logger.info("FileSystemId: %s", id[0])

    # EFSの一覧を取得(Itemは適宜変更)
    try:
        res = client.describe_file_systems(
            FileSystemId = id[0],
            MaxItems = 50,
        )

    except:
        logger.warning("%s is not exists", id[0])
        sys.exit(1)

    r = res["FileSystems"][0]
    logger.info("Target EFS: %s", r["Name"])

    # ThroughputModeがburstingだった場合にprovisionedに変更
    if r["ThroughputMode"] == "bursting" and r["LifeCycleState"] == "available":
        logger.info("Update ThroughputMode to provisioned")

    else:
        logger.info("%s isn't update" % r["Name"])

    logger.info("End function")
