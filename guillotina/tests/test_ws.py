from guillotina.testing import ADMIN_TOKEN

import json


async def test_hello(guillotina, container_requester):
    async with container_requester as requester:
        headers = {'AUTHORIZATION': 'Basic %s' % ADMIN_TOKEN}
        async with requester.websocket_connect(
                'db/guillotina/@ws',
                headers=headers) as ws:
            sending = {
                'op': 'GET',
                'value': '/@registry/guillotina.interfaces.registry.ILayers.active_layers'
            }

            ws.send_str(json.dumps(sending))
            message = await ws.receive_json()
            assert message == {'data': '{"value": []}', 'id': '0'}


async def test_send_close(guillotina, container_requester):
    async with container_requester as requester:
        async with requester.websocket_connect(
                'db/guillotina/@ws',
                headers={'AUTHORIZATION': 'Basic %s' % ADMIN_TOKEN}) as ws:

            ws.send_str(json.dumps({'op': 'close'}))
            async for msg in ws:  # noqa
                pass

async def test_ws_token(container_requester):
    async with container_requester as requester:
        response, status = await requester('GET', '/db/guillotina/@wstoken')
        assert status == 200
        response, status = await requester(
            'GET', '/db/guillotina?ws_token=' + response['token'],
            authenticated=False)
        assert status == 200
