// SPDX-License-Identifier: UNLICENSED
pragma solidity ^0.8.17;

// Uncomment this line to use console.log
// import "hardhat/console.sol";
import "@openzeppelin/contracts/token/ERC20/IERC20.sol";

// An order has a finite set of possible states
enum OrderState {
    Submitted,  // Received by contract but not yet stored on-chain
    Active,     // Recorded in on-chain storage, awaiting fill
    Filled,     // Terminal state: Maximum quantity filled
    Cancelled   // Terminal state: Owner does not wish to complete
}

enum TradeSide {
    Buy,
    Sell
}

struct OrderLeg {
    address token;
    uint quantity;
    uint price_low;         // price in wei
    uint price_high;        // all orders should be denominated in Eth (wei)
    TradeSide side;
}


contract Order {
    event Received(address, uint);

    address _exchange;                          // The address of the Exchange contract
    address payable _owner;                     // The address that can receive the filled order
    uint _balance;                              // Tracks the Eth funds in the contract
    mapping(IERC20 => uint) _token_balances;    // Tracks the funds in the contract
    OrderState _state;                          // Tracks the state of the order
    OrderLeg[] _legs;                           // An array of child orders

    function validateSellLeg(OrderLeg memory leg) internal {
        // Validates an order leg with TradeSide.Sell
        // TODO: check that this address has been allocated the specified token quantity
    }
    function validateBuyLeg(OrderLeg memory leg) internal {
        // Validates an order leg with TradeSide.Buy
        // TODO: check that this contract has been allocated the specified Eth quantity
    }
    function submit() internal {
        // Records the validated order data with on-chain storage node (IPFS, SWARM, etc)
    }

    function addLeg(OrderLeg memory leg) internal {
        // Validate the order leg
        if (leg.side == TradeSide.Sell) {
            validateSellLeg(leg);
        }
        if (leg.side == TradeSide.Buy) {
            validateBuyLeg(leg);
        }

        _legs.push(leg);
    }

    constructor(
        address exchange,
        address payable owner,
        OrderLeg[] memory legs
    ) payable {       
        // Add legs to contract
        for (uint i = 0; i < legs.length; i++){
            addLeg(legs[i]);
        }

        // Validate order legs
        // Initialize contract values
        _exchange = exchange;
        _owner = owner;
        _balance = msg.value;
        _state = OrderState.Submitted;

        // Submit the order to on-chain storage
        submit();
    }

    // Public Getters
    function getOwner() public view returns (address) {
        return _owner;
    }
    function getState() public view returns (OrderState) {
        return _state;
    }
    function getBalance() public view returns (uint) {
        return _balance;
    }

    // Public Setters
    function cancel() public {
        // Modify state to cancel
        // Require active state
    }
    function withdraw() public {
        // Require terminal state
        // Transfer token balances and eth balances to owner
        // Confirm values before sending
    }

    receive() external payable {
        emit Received(msg.sender, msg.value);
        _balance += msg.value;
    }

}
