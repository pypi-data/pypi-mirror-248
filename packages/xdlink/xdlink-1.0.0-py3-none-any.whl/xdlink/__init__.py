import asyncio
import aiohttp
import json

async def xdlink(session,urls,channelid=""):
    strurls = ''
    i = 0
    for u in urls:
        strurls += str(u)
        if i < len(urls)-1:
            strurls += '\n'
        i+=1
    api = 'https://xd-core-api.onrender.com/xdlinks/encode'
    jsondata = {'channelid':channelid,'urls':strurls}
    headers = {'Content-Type':'application/json','Accept': '*/*','Origin':'https://xdownloader.surge.sh','Referer':'https://xdownloader.surge.sh/'}
    async with session.post(api,data=json.dumps(jsondata),headers=headers) as resp:
        html = await resp.text()
    jsonresp = json.loads(html)
    if 'data' in jsonresp:
        return jsonresp['data']
    return None