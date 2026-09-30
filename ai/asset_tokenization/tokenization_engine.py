import uuid


def tokenize_asset(
    asset_id,
    asset_type,
    asset_name,
    owner,
    asset_value,
    total_tokens,
    location
):
    """
    Real Asset Tokenization Engine

    Converts the economic ownership of a real-world asset
    into a defined number of digital tokens.

    This is a prototype and does not represent legal ownership.
    """

    if asset_value <= 0:
        raise ValueError("Asset value must be greater than zero")

    if total_tokens <= 0:
        raise ValueError("Total tokens must be greater than zero")

    if not owner:
        raise ValueError("Owner is required")

    token_value = asset_value / total_tokens

    token_id = "AST-" + uuid.uuid4().hex[:10].upper()

    return {
        "tokenId": token_id,
        "assetId": asset_id,
        "assetType": asset_type,
        "assetName": asset_name,
        "owner": owner,
        "assetValue": round(asset_value, 2),
        "totalTokens": total_tokens,
        "tokenValue": round(token_value, 2),
        "location": location,
        "status": "TOKENIZED"
    }


def transfer_tokens(
    token_id,
    from_owner,
    to_owner,
    token_amount,
    total_tokens
):
    """
    Transfer a portion of tokenized asset ownership.
    """

    if token_amount <= 0:
        raise ValueError(
            "Token amount must be greater than zero"
        )

    if token_amount > total_tokens:
        raise ValueError(
            "Cannot transfer more tokens than available"
        )

    if not from_owner or not to_owner:
        raise ValueError(
            "Both sender and receiver are required"
        )

    return {
        "tokenId": token_id,
        "from": from_owner,
        "to": to_owner,
        "tokensTransferred": token_amount,
        "remainingTokens": total_tokens - token_amount,
        "status": "TRANSFERRED"
    }
