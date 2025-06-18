import pytest

from .utils import MissingProofToken


def test_missing_token(monkeypatch):
    """Test when there is no PROOF token"""
    # monkeypatch.delenv("PROOF_API_TOKEN_DEV")
    monkeypatch.setattr("tests.cromwellapi.proof.TOKEN", None)

    from .proof import ProofApi

    with pytest.raises(MissingProofToken):
        ProofApi()
