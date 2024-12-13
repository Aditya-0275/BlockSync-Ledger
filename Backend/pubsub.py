import time
from pubnub.pubnub import PubNub
from pubnub.pnconfiguration import PNConfiguration
from pubnub.callbacks import SubscribeCallback
from Backend.Blockchain.block_module import Block
from Backend.Wallet.transaction import Transaction


pnconfig = PNConfiguration()
pnconfig.subscribe_key = 'sub-c-a046df9c-3881-4c71-9af3-ecd0cb094d3a'
pnconfig.publish_key = 'pub-c-2358e40a-4b27-439a-aa81-98217d02f627'
pnconfig.uuid = "my-app-user-1234"


CHANNELS = {
    'TEST_CHANNEL': 'TEST_CHANNEL',
    'BLOCK_CHANNEL': 'BLOCK_CHANNEL',
    'TRANSACTION': 'TRANSACTION'
}


class Listener(SubscribeCallback):
    def __init__(self, blockchain, transaction_pool):
        self.blockchain = blockchain
        self.transaction_pool = transaction_pool

    def message(self, pubnub, message_object):
        print(
            f'\n-- Channel: {message_object.channel} | Message: {message_object.message}')

        if message_object.channel == CHANNELS['BLOCK_CHANNEL']:
            block = Block.from_json(message_object.message)
            potential_chain = self.blockchain.chain[:]
            potential_chain.append(block)

            try:
                self.blockchain.replace_chain(potential_chain)
                self.transaction_pool.clear_blockchain_transactions(
                    self.blockchain
                )
                print(f'\n -- Successfully replaced a local chain')
            except Exception as e:
                print(f'\n -- Did not replace chain: {e}')

        elif message_object.channel == CHANNELS['TRANSACTION']:
            transaction = Transaction.from_json(message_object.message)
            self.transaction_pool.set_transaction(transaction)
            print(f'\n -- Set the new transaction in the transaction pool.')


class PubSub:
    """
    Handles the publish/subscribe layer of the application.
    Provides communication between the nodes of the blockchain network.
    """

    def __init__(self, blockchain, transaction_pool):
        self.pubnub = PubNub(pnconfig)
        self.pubnub.subscribe().channels(CHANNELS.values()).execute()
        self.pubnub.add_listener(Listener(blockchain, transaction_pool))

    def publish(self, channel, message):
        """
        Publish the message object to the channel.
        """
        self.pubnub.publish().channel(channel).message(message).sync()

    def broadcast_block(self, block):
        """
        Broadcast a block object to all nodes.
        """
        self.publish(CHANNELS['BLOCK_CHANNEL'], block.to_json())

    def broadcast_transaction(self, transaction):
        """
        Broadcast a transaction to all nodes.
        """
        self.publish(CHANNELS['TRANSACTION'], transaction.to_json())


def main():
    pubsub = PubSub()
    time.sleep(1)
    pubsub.publish(CHANNELS['TEST_CHANNEL'], {'foo': 'bar'})


if __name__ == '__main__':
    main()
