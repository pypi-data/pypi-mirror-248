# Python
import base64
import json
from typing import Optional
import logging

import requests
from typing import Any
from urllib.parse import urljoin
import uuid
from datetime import datetime, timezone
import hashlib
import hmac

# Django
from django.conf import settings

# App
from creta.models import ApiHistory, NFT

# Variables
from creta.enum import CollectionType
from creta.utils import *

logger = logging.getLogger(__name__)


# Classes
class BaseGateway:
    def __init__(self, base_url: str):
        self.base_url = base_url

    def get_url(self, path: str) -> str:
        return urljoin(self.base_url, path)

    def get_headers(self, method: str, **kwargs):
        # Set headers
        headers = {
            'x-app-id': settings.CRETA_APP_ID,
            'x-api-key': settings.CRETA_API_KEY,
            'x-timestamp': datetime.now(timezone.utc).isoformat()
        }

        if method == 'POST':
            headers['Content-Type'] = 'application/json'

            request_id = str(uuid.uuid4())
            secret_key = settings.CRETA_SECRET_KEY  # Replace with your actual secret key

            body = json.loads(kwargs['data'])
            body['requestId'] = request_id
            query_string = object_to_query_string(body)

            # Hash the query_string using the secret_key and sha256 algorithm
            signature = base64.b64encode(hmac.new(
                key=secret_key.encode('utf-8'),
                msg=query_string.encode('utf-8'),
                digestmod=hashlib.sha256
            ).digest())
            headers['x-request-id'] = request_id
            headers['x-signature'] = signature

        return headers

    def request(self, title: str, method: str, path: str, **kwargs) -> Any:

        headers = self.get_headers(method=method, **kwargs)
        url = self.get_url(path=path)
        api_history = ApiHistory.objects.create(
            title=title,
            method=method,
            url=url,
            headers=object_to_json(headers),
        )

        # data_str = {key: value.decode('utf-8') if isinstance(value, bytes) else value for key, value in data.items()}
        # json_data = json.dumps(data_str)

        try:
            response = requests.request(method=method, url=url, headers=headers, **kwargs)
            response.raise_for_status()  # 상태 코드가 4xx나 5xx인 경우 예외 발생

        except requests.RequestException as error:
            print('------------------- REQUEST -------------------')
            print('URL: ', response.request.url)
            print('Body: ', response.request.body)
            print('Headers: ', response.request.headers)
            print('-------------------- ERROR --------------------')
            print(error)
            print('--------------------- END ---------------------')
            api_history.error = str(error)
            api_history.save()
            raise error

        # Raise exception for HTTP error status codes such as 400, 404, 500.

        result = response.json()
        api_history.response = response.json()
        api_history.save()

        if result['resultCode'] == 1:
            return result, api_history
        elif result['message']:
            print(result)
            raise Exception(result['message'])
        else:
            print(result)
            raise Exception()


class GatewayV1(BaseGateway):
    def __init__(self):
        super().__init__(base_url=urljoin(settings.CRETA_GATEWAY_HOST, f'/v1/'))

    # (NFT) List By User
    # 유저별 보유 NFT 조회
    # /v1/nfts/assets/{collectionType}/{address}?page=1&limit=30
    # /v1/nfts/assets/200001/0x628fD709BFa7fe68af024852893Ef615104445Ee?page=1&limit=1
    def get_nfts(self, address: str, page=1):
        path = 'nfts/assets/{collectionType}/{address}'.format(collectionType=CollectionType.SUPERCLUB.value, address=address)
        result, api_history = self.request(title="(NFT) List By User", method="GET", path=path, params={'page': page, 'limit': 20})
        return result

    def get_all_nfts(self, address: str):
        all_nfts = []
        page = 1

        while True:
            result = self.get_nfts(address, page)
            # 결과가 빈 배열이면 반복 종료
            if not result["result"]:
                break
            # 현재 페이지의 결과를 누적
            all_nfts.extend(result)
            # 다음 페이지로 이동
            page += 1

        return all_nfts

    def has_nft(self, address: str, token_id: str):
        nfts = self.get_all_nfts(address=address)
        for nft in nfts:
            if nft.get("token_id") == token_id:
                return True
        return False

    # (NFT) Detail
    # 특정 NFT 상세 정보
    # /v1/nfts/detail/{collectionType}/{tokenId}
    # /v1/nfts/detail/200001/10106
    def get_nft(self, token_id: str):
        path = 'nfts/detail/{collectionType}/{tokenId}'.format(collectionType=CollectionType.SUPERCLUB.value, tokenId=token_id)
        result, api_history = self.request(title="(NFT) Detail", method="GET", path=path)
        return result

    # (NFT) Transactions By User
    # 유저별 NFT 거래 내역 조회
    # /v1/tokens/transactions/{address}
    # /v1/nfts/transactions/200001/0x628fD709BFa7fe68af024852893Ef615104445Ee
    def get_nft_transactions_by_user(self, address: str):
        path = 'nfts/transactions/{collectionType}/{address}'.format(collectionType=CollectionType.SUPERCLUB.value, address=address)
        result, api_history = self.request(title="(NFT) Transactions By User", method="GET", path=path)
        return result

    # (NFT) Transactions By NFT
    # 특정 NFT 거래 내역 조회
    # /v1/nfts/history/{collectionType}/{tokenId}
    # /v1/nfts/history/200001/10103
    def get_nft_transactions_by_nft(self, token_id: str):
        path = 'nfts/history/{collectionType}/{tokenId}'.format(collectionType=CollectionType.SUPERCLUB.value, tokenId=token_id)
        result, api_history = self.request(title="(NFT) Transactions By NFT",  method="GET", path=path)
        return result

    # (NFT) Create
    # NFT 민팅
    # /v1/nfts/mint
    def create_nft(self,
            address: str,
            nft_type: int, # Club: 1, User: 2
            name: str,  # 1~63
            image_url: str,  # 10~255
            attributes: Optional[dict] = None,
            animation_url: Optional[str] = None,
            external_url: Optional[str] = None,
            extra_url: Optional[dict] = None):
        path = 'nfts/mint'
        body = {
            "collectionType": CollectionType.SUPERCLUB.value,
            "address": address,
            "nftType": nft_type,
            "name": name,
            "image": image_url,
        }

        optional_keys = ["attributes", "animation_url", "external_url", "extra_url"]
        for key in optional_keys:
            value = locals()[key]
            if value is not None:
                body[key] = value

        result, api_history = self.request(title="(NFT) Create", method="POST", path=path, data=json.dumps(body))
        request_id = api_history.headers['x-request-id']
        result['request_id'] = request_id

        instance = NFT.objects.create(
            name=name,
            nft_type=nft_type,
            attributes=attributes,
            request_id=request_id,
            image_url=image_url,
            animation_url=animation_url,
            external_url=external_url,
            extra_url=extra_url
        )

        return result, instance

    # (Nft) Status
    # NFT 민팅 현황 조회
    # /v1/nfts/mint/{collectionType}/{requestId}
    # /v1/nfts/mint/200001/3c52f871-1a01-47f3-8a9e-045d2767aab9
    def check_nft(self, request_id):
        path = 'nfts/mint/{collectionType}/{requestId}'.format(collectionType=200001, requestId=request_id)
        result, api_history = self.request(title="(NFT) Status", method="GET", path=path)

        instance = NFT.objects.get(request_id=request_id)

        if result['result']['token_id']:
            instance.token_id = result['result']['token_id']
            instance.status = 'APPROVED'
            instance.save()

        return result, instance

    # (NFT) Update
    # NFT 데이터 수정
    # /v1/nfts/update
    def update_nft(self, token_id: str, nft_type: str, name: str, attributes):
        path = 'nfts/update'
        body = {
            "collectionType": CollectionType.SUPERCLUB.value,
            "tokenId": token_id,
            "nftType": nft_type,
            "name": name,
            "attributes": attributes
        }

        result, api_history = self.request(title="(NFT) Update", method="POST", path=path, data=json.dumps(body))

        instance = NFT.objects.get(token_id=int(token_id))

        instance.name = name
        instance.nft_type = nft_type
        instance.attributes = attributes
        # instance.image_url = image_url
        # instance.animation_url = animation_url
        # instance.external_url = external_url
        # instance.extra_url = extra_url
        instance.save()

        return result, instance

    # (NFT) Transfer
    # 다른 유저에게 NFT 전송
    # /v1/nfts/transfer
    def transfer_nft(self, address_from: str, address_to: str, token_id: str):
        path = 'nfts/transfer'
        body = {
            "collectionType": CollectionType.SUPERCLUB.value,
            "from": address_from,
            "to": address_to,
            "tokenId": token_id
        }
        result, api_history = self.request(title="(NFT) transfer", method="POST", path=path, data=json.dumps(body))
        return result


# Instances
creta_sdk = GatewayV1()
