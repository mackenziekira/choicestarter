import stripe

#testing api key, should be changed and stored in a config.py file that lives outside git
stripe.api_key = "sk_test_BQokikJOvBiI2HlWgH4olfQ2"


def create_uuid():
    #todo use python uuid library
    return "UNIQUEVALUE"


def create_charge(charge_amount, token):
    uuid = create_uuid()
    charge = stripe.Charge.create(
        amount=charge_amount,
        currency="usd",
        source=token,
        transfer_group=uuid
    )
    print(charge)
    return charge


def charge_customer(our_customer, charge_amount):
    uuid = create_uuid()
    charge = stripe.Charge.create(
        amount=charge_amount,
        currency="usd",
        customer=our_customer,
        transfer_group=uuid
    )
    return charge


def create_transfer(transfer_amount, destination_account):
    #todo look through the db to figure out what transfer group(s) to use
    uuid = create_uuid()
    transfer = stripe.Transfer.create(
        amount=transfer_amount,
        currency="usd",
        destination=destination_account,
        transfer_group=uuid
    )
    print(transfer)


def create_user(token):
    customer = stripe.Customer.create(
        source=token
    )
    return customer.id
