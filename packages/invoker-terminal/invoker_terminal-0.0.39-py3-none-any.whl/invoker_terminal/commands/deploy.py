import asyncio
import io
import json
import logging
import os
import time
import zipfile

from pick import pick
from solders.pubkey import Pubkey

from ..cores.anchor import addModel
from ..cores.ipfs import send_to_ipfs
from ..storage.deployed_models import addDeployedModel
from ..storage.helper import get_engine
from ..utils import generateModelUrl, getAvailableTokens, getEnvName
from price_parser import Price

def cmd_deploy(args, conf):
    filesMustExist = ["build.json", "desc.json"]
    for file in filesMustExist:
        if not os.path.isfile(file):
            print(f"I can't deploy, mising file {file}")
            os._exit(1)
            
    availableTokens = getAvailableTokens(args)
    selectedToken = availableTokens[0]["TokenName"]
    selectedTokenAddr = availableTokens[0]["Address"]
    selectedDecimalNum = availableTokens[0]["Decimal"]
    if len(availableTokens) > 1:
        tokenNames = list(map(lambda x: x["TokenName"], availableTokens))
        print(tokenNames)
        o, i = pick(tokenNames, "Which token do you want to use ?")
        selectedToken = availableTokens[i]["TokenName"]
        selectedTokenAddr = availableTokens[i]["Address"]
    print("SelectedToken {}".format(selectedToken))
    print("Selected Addr {}".format(selectedTokenAddr))
    price = Price.fromstring(input("Enter model price (e.g 0.10$): "))
    price = int(price.amount * (10 ** selectedDecimalNum ))
    ipfs_post_url = conf["system"]["ipfs_post_gateway"]

    descfile = open("desc.json", "r").read()
    buildfile = json.loads(open("build.json", "r").read())
    zip_buffer = io.BytesIO()
    zip_file = zipfile.ZipFile(zip_buffer, "a", zipfile.ZIP_DEFLATED, False)
    zip_file.writestr("model/desc.json", descfile)
    ts = time.time()
    zip_file.writestr("timestamp", str(ts))
    zip_file.close()
    buff = zip_buffer.getvalue()
    modelDescHash = send_to_ipfs(buff, ipfs_post_url)
    # load anchor now
    modelId = asyncio.run(
        addModel(
            conf, modelDescHash, Pubkey.from_string(selectedTokenAddr), price
        )
    )
    print("Check out the model at {}".format(generateModelUrl(args, modelId)))
    imageId = buildfile["id"]
    modelname = os.path.split(os.getcwd())[1]
    addDeployedModel(
        get_engine(args.db_path), getEnvName(args), modelId, imageId, modelname
    )
