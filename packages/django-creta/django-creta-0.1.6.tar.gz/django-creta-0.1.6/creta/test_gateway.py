from django.test import TestCase

# App
from creta.gateway import creta_sdk


# Main
class GatewayV1Test(TestCase):
    def test_get_nfts(self):
        result = creta_sdk.get_nfts(address="0x628fD709BFa7fe68af024852893Ef615104445Ee", page=1)
        self.assertEqual(result['resultCode'], 1)

    def test_get_nft(self):
        result = creta_sdk.get_nft(token_id="10106")
        self.assertEqual(result['resultCode'], 1)

    def test_get_nft_transactions_by_user(self):
        result = creta_sdk.get_nft_transactions_by_user(address="0x628fD709BFa7fe68af024852893Ef615104445Ee")
        self.assertEqual(result['resultCode'], 1)

    def test_get_nft_transactions_by_nft(self):
        result = creta_sdk.get_nft_transactions_by_nft(token_id="10103")
        self.assertEqual(result['resultCode'], 1)

    def test_create_nft(self):
        result, instance = creta_sdk.create_nft(
            address="0x628fD709BFa7fe68af024852893Ef615104445Ee",
            nft_type=1,
            name="NFT name",
            attributes=[
                {
                    "trait_type": "Level",
                    "value": 1
                }
            ],
            image_url="https://cf.dev.superclubs.io/media/club/advertisement/8f4ee8fd-8c79-4004-aad7-88c3edbdf4ef/20230907/20230907T040903.jpg",
        )
        print('test_create_nft: ', result)

    def test_check_nft(self):
        result, instance = creta_sdk.check_nft(request_id="3c52f871-1a01-47f3-8a9e-045d2767aab9")
        self.assertEqual(result['resultCode'], 1)

    def test_update_nft(self):
        result, instance = creta_sdk.update_nft(
            token_id="10106",
            nft_type=3,
            name="Club 20",
            attributes=[{"trait_type": "Level", "value": 20}])
        self.assertEqual(result['resultCode'], 1)

    def test_transfer_nft(self):
        result = creta_sdk.transfer_nft(
            address_from="0x628fD709BFa7fe68af024852893Ef615104445Ee",
            address_to="0x7f369511e314f84e16b08413547a04e3a9552508",
            token_id="10103"
        )
        self.assertEqual(result['resultCode'], 1)