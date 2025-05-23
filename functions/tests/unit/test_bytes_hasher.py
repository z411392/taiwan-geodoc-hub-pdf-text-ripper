import pytest
from taiwan_geodoc_hub.infrastructure.hashers.bytes_hasher_adapter import (
    BytesHasherAdapter,
)
from injector import Injector


# @pytest.mark.skip(reason="")
class TestBytesHasher:
    @pytest.fixture
    def bytes_hasher(self, injector: Injector):
        return injector.get(BytesHasherAdapter)

    @pytest.mark.describe("要能夠產生 bytes 的 uuid")
    def test_bytes_uuid(
        self,
        bytes_hasher: BytesHasherAdapter,
        sample_image: bytes,
        sample_image_hash: str,
    ):
        hash_calculated = bytes_hasher(sample_image)
        assert hash_calculated == sample_image_hash
