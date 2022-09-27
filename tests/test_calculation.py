import pytest
from app.calculation import BankAccount, add, subtract, multiply, device, InsufficientFunds

@pytest.fixture()
def zero_bank_account():
    print("Creating empty bank account")
    return BankAccount()

@pytest.fixture
def bank_account():
    return BankAccount(50)

@pytest.mark.parametrize("num1, num2, expected",[
    (3, 4, 7),
    (2, 6, 8),
    (5, 4, 9)
])

def test_add(num1, num2, expected):
    print("testing add function")
    # sum == 8
    assert add(num1, num2) == expected


def test_subtract():
    assert subtract(4, 1) == 3


def test_multiple():
    # sum == 8
    assert multiply(3, 4) == 12

def test_device():
    assert device(12, 4) == 3

def test_bank_set_initial_amount(bank_account):
    #bank_account = BankAccount(50)
    assert bank_account.balance == 50

def test_bank_default_amount(zero_bank_account):
    #bank_account = BankAccount()
    print("Testing my bank account")
    assert zero_bank_account.balance == 0

def test_withdraw(bank_account):
   
    bank_account.withdraw(20)
    assert bank_account.balance == 30


def test_deposit(bank_account):
  
    bank_account.deposit(20)
    assert bank_account.balance == 70


def test_collect_interest(bank_account):
    bank_account.collect_interest()
    assert round(bank_account.balance, 6) == 55


@pytest.mark.parametrize("deposit,  withdraw, expected",[
    (300, 100, 200),
    (200, 50, 150),
    (100, 40, 60)
])

def test_bank_transaction(zero_bank_account, deposit, withdraw, expected):
    zero_bank_account.deposit(deposit)
    zero_bank_account.withdraw(withdraw)
    assert zero_bank_account.balance == expected


def test_insufficient_funds(bank_account):
    with pytest.raises(InsufficientFunds):
        bank_account.withdraw(200)
    