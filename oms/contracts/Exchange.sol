// SPDX-License-Identifier: UNLICENSED
pragma solidity ^0.8.17;

// Uncomment this line to use console.log
// import "hardhat/console.sol";
import "./Order.sol";


contract Exchange {

    uint private _num_orders;
    mapping(uint => address) private _orders;

    constructor () {
        _num_orders = 0;
    }

    function newOrder(OrderLeg[] calldata legs)
        public
        returns (uint order_id, address new_order)
    {
        // Initialize a new Order contract
        address payable new_order_owner = payable(msg.sender);
        new_order = address(
            new Order({
                owner: new_order_owner,
                exchange: address(this),
                legs: legs
            })
        );

        // Record the order
        order_id = _num_orders;
        _orders[order_id] = address(new_order);
        _num_orders += 1;

        // Return the order metadata 
        return (order_id, new_order);
    }

    function getOrder(uint order_id) public view returns (address) {
        return _orders[order_id];
    }

    function updateOrders() public {
        // Check on-chain storage for auction fills

        // Iterate over fills and update orders
    }

    function getTransactions() private {
        // Read on-chain storage for auction fills
    }
}