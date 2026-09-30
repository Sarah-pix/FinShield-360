import os
import subprocess


TEST_NETWORK = os.path.expanduser(
    "~/drunix/drunix-network/test-network"
)

PEER_BIN = os.path.expanduser(
    "~/drunix/drunix-network/bin/peer"
)

ORDERER_CA = os.path.join(
    TEST_NETWORK,
    "organizations/ordererOrganizations/example.com/tlsca/"
    "tlsca.example.com-cert.pem"
)

PEER0_ORG1_CA = os.path.join(
    TEST_NETWORK,
    "organizations/peerOrganizations/org1.example.com/tlsca/"
    "tlsca.org1.example.com-cert.pem"
)

PEER0_ORG2_CA = os.path.join(
    TEST_NETWORK,
    "organizations/peerOrganizations/org2.example.com/tlsca/"
    "tlsca.org2.example.com-cert.pem"
)

MSP_PATH = os.path.join(
    TEST_NETWORK,
    "organizations/peerOrganizations/org1.example.com/users/"
    "Admin@org1.example.com/msp"
)


def create_payment(
    payment_id,
    sender,
    receiver,
    amount,
    currency,
    risk_score,
    risk_level,
    decision,
    status
):
    env = os.environ.copy()

    env["FABRIC_CFG_PATH"] = os.path.expanduser(
        "~/drunix/drunix-network/config"
    )

    env["CORE_PEER_MSPCONFIGPATH"] = MSP_PATH
    env["CORE_PEER_LOCALMSPID"] = "Org1MSP"
    env["CORE_PEER_ADDRESS"] = "localhost:7051"
    env["CORE_PEER_TLS_ENABLED"] = "true"
    env["CORE_PEER_TLS_ROOTCERT_FILE"] = PEER0_ORG1_CA

    command = [
        PEER_BIN,
        "chaincode",
        "invoke",

        "-o",
        "localhost:7050",

        "--ordererTLSHostnameOverride",
        "orderer.example.com",

        "--tls",

        "--cafile",
        ORDERER_CA,

        "-C",
        "mychannel",

        "-n",
        "finshield",

        "--peerAddresses",
        "localhost:7051",

        "--tlsRootCertFiles",
        PEER0_ORG1_CA,

        "--peerAddresses",
        "localhost:9051",

        "--tlsRootCertFiles",
        PEER0_ORG2_CA,

        "-c",
        (
            '{"function":"CreatePayment","Args":['
            f'"{payment_id}",'
            f'"{sender}",'
            f'"{receiver}",'
            f'"{amount}",'
            f'"{currency}",'
            f'"{risk_score}",'
            f'"{risk_level}",'
            f'"{decision}",'
            f'"{status}"'
            ']}'
        )
    ]

    result = subprocess.run(
        command,
        env=env,
        capture_output=True,
        text=True
    )

    return {
        "return_code": result.returncode,
        "stdout": result.stdout,
        "stderr": result.stderr
    }
def get_all_payments():
    env = os.environ.copy()

    env["FABRIC_CFG_PATH"] = os.path.expanduser(
        "~/drunix/drunix-network/config"
    )

    env["CORE_PEER_MSPCONFIGPATH"] = MSP_PATH
    env["CORE_PEER_LOCALMSPID"] = "Org1MSP"
    env["CORE_PEER_ADDRESS"] = "localhost:7051"
    env["CORE_PEER_TLS_ENABLED"] = "true"
    env["CORE_PEER_TLS_ROOTCERT_FILE"] = PEER0_ORG1_CA

    command = [
        PEER_BIN,
        "chaincode",
        "query",
        "-C",
        "mychannel",
        "-n",
        "finshield",
        "-c",
        '{"function":"GetAllPayments","Args":[]}'
    ]

    result = subprocess.run(
        command,
        env=env,
        capture_output=True,
        text=True
    )

    return {
        "return_code": result.returncode,
        "stdout": result.stdout,
        "stderr": result.stderr
    }
