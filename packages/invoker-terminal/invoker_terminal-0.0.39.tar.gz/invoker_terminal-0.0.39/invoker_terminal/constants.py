from typing import Literal

local_test_token_addr = "Ea5TtVJBHJchqzthA6bQfF31ac16jvV3TxukDPsiSkvE"

dev_test_token_addr = "CYxjHjAiMoXiReaVDNJrJ5ECHFLE3Q9iHAxEhbU118LV"

mainnet_usdc_addr = "EPjFWdd5AufqSSqeM2qN1xzybapC8G4wEGGkZwyTDt1v"
mainnet_tether_addr = "Es9vMFrzaCERmJfrF4H2FYD4KCoNkY11McCe8BenwNYB"

InvokerEnvironment = Literal["local", "dev", "mainnet"]


class InvokerEnv:
    LOCAL = "local"
    DEV = "dev"
    MAINNET = "mainnet"


TokenMap = {
    InvokerEnv.LOCAL: [
        {
            "TokenName": "InvokerLocalTestToken",
            "Address": local_test_token_addr,
            "Decimal": 6
        },
    ],
    InvokerEnv.DEV: [
        {
            "TokenName": "InvokerDevToken",
            "Address": dev_test_token_addr,
            "Decimal": 6
        }
    ],
    InvokerEnv.MAINNET: [
        {
            "TokenName": "USDC (Circle)",
            "Address": mainnet_usdc_addr,
            "Decimal": 6
        },
        {
            "TokenName": "USDT (Tether)",
            "Address": mainnet_tether_addr,
            "Decimal": 6
        },
    ],
}
