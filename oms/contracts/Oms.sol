// SPDX-License-Identifier: UNLICENSED
pragma solidity ^0.8.17;

// Uncomment this line to use console.log
// import "hardhat/console.sol";

contract Oms {
    event OrderSubmitted();
    event OrderFilled();
    event OrderCancelled();

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
        uint leg_id;
        address token;
        uint quantity;
        uint price_low;         // price in wei
        uint price_high;        // all orders should be denominated in Eth (wei)
        TradeSide side;
        // TODO: Any other data here?
    }

    struct OrderData {
        uint order_id;          // TODO: uint or hash?
        address payable owner;  // TODO: better name?
        OrderState state;
        int[] legs;             // Contains IDs of order legs
    }

    mapping(uint => OrderData) order_book;
    mapping(uint => OrderLeg) leg_order_book;
}

