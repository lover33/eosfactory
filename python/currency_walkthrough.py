import teos

"""
## Example "Currency" Contract Walkthrough

EOS comes with example contracts that can be uploaded and run for testing 
purposes. Next we demonstrate how to upload and interact with the sample 
contract "currency".

### Example smart contracts

First, run the node:
"""
teos.set_verbose(False)

# Start a clean blockchain, so that every instance of the current test goes 
# the same way:
daemon = teos.Daemon()
daemon.clear()

# See a prove that the daemon is running:
print(daemon)

"""
#### Setting up a wallet and importing account key

As you've previously added plugin = eosio::wallet_api_plugin into config.ini, 
EOS wallet will be running as a part of eosiod process. Every contract requires
an associated account, so first, create a wallet.
"""
wallet = teos.Wallet("wallet")

"""
For the purpose of this walkthrough, import the private key of the 'eosio' 
account, a test account included within genesis.json, so that you're able to 
issue API commands under authority of an existing account. The private key 
referenced below is found within your config.ini and is provided to you for 
testing purposes.
"""
eosio_key = teos.EosioKey()
wallet.import_key(eosio_key)
"""

#### Creating accounts for sample "currency" contract

First, generate some public/private key pairs that will be later assigned as 
owner_key and active_key.
"""
owner_key = teos.CreateKey("owner_key")
active_key = teos.CreateKey("active_key")

"""
Run the create command where 'eosio' is the account authorizing the creation of 
the currency account and PUBLIC_KEY_1 and PUBLIC_KEY_2 are the values 
generated by the create key command
"""
account = teos.Account(
    eosio_key.account_name, "currency", owner_key, active_key
    )

"""
You should then get a JSON response back with a transaction ID confirming it 
was executed successfully.

Go ahead and check that the account was successfully created:
"""
print(account)

"""
Import the active private key generated previously in the wallet:
"""
wallet.import_key(active_key)
print(wallet)

"""
You will upload sample "currency" contract to blockchain. Before uploading a 
contract, verify that there is no current contract:
"""
code = wallet.code()
print(code)

"""
Code hash is null, there is no contract.

With an account for a contract created, upload a sample contract:
"""
account.set_contract("currency.wast", "currency.abi")

"""
As a response you should get a JSON with a transaction_id field. Your contract 
was successfully uploaded!

You can also verify that the code has been set with the following command:
"""
code = account.code()
print(code.code_hash)

"""
Now, code hash is not null anymore.

Before using the currency contract, you must issue the currency.
"""
teos.PushAction(
  "currency", "issue", 
  '{"to":"currency","quantity":"1000.0000 CUR","memo":""}', 
  permission="currency@active")
"""

./eosioc push action currency issue '{"to":"currency","quantity":"1000.0000 CUR"}' --permission currency@active
Next verify the currency contract has the proper initial balance:

./eosioc get table currency currency account
{
  "rows": [{
     "currency": 1381319428,
     "balance": 10000000
     }
  ],
  "more": false

}

"""
daemon = teos.Daemon()
daemon.clear()
wallet = teos.Wallet("default")
eosio_key = teos.EosioKey()
wallet.import_key(eosio_key)
owner_key = teos.CreateKey("owner_key")
active_key = teos.CreateKey("active_key")

account = teos.Account(
    eosio_key.account_name, "currency", owner_key, active_key
    )
print(account)
wallet.import_key(active_key)
print(wallet)
code = account.code()
print(code.code_hash)
account.set_contract("currency.wast", "currency.abi")
code = account.code()
print(code.code_hash)
"""

Transfering funds with the sample "currency" contract

Anyone can send any message to any contract at any time, but the contracts may reject messages which are not given necessary permission. Messages are not sent "from" anyone, they are sent "with permission of" one or more accounts and permission levels. The following commands show a "transfer" message being sent to the "currency" contra ct.

The content of the message is '{"from":"currency","to":"eosio","quantity":"20.0000 CUR","memo":"any string"}'. In this case we are asking the currency contract to transfer funds from itself to someone else. This requires the permission of the currency contract.

./eosioc push action currency transfer '{"from":"currency","to":"eosio","quantity":"20.0000 CUR","memo":"my first transfer"}' --permission currency@active
Below is a generalization that shows the currency account is only referenced once, to specify which contract to deliver the transfer message to.

./eosioc push action currency transfer '{"from":"${usera}","to":"${userb}","quantity":"20.0000 CUR","memo":""}' --permission ${usera}@active
As confirmation of a successfully submitted transaction, you will receive JSON output that includes a transaction_id field.


Reading sample "currency" contract balance

So now check the state of both of the accounts involved in the previous transaction.

./eosioc get table eosio currency account
{
  "rows": [{
      "currency": 1381319428,
      "balance": 200000
       }
    ],
  "more": false

}
./eosioc get table currency currency account
{
  "rows": [{
      "currency": 1381319428,
      "balance": 9800000
    }
  ],
  "more": false
}
As expected, the receiving account eosio now has a balance of 20 tokens, and the sending account now has 20 less tokens than its initial supply.



"""



