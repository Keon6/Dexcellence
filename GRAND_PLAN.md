# Dexcellence - The Grand Plan

## TODO

### Friday

- [ ] Architecture
  - [X] Agree on an overarching schematic
  - [X] Decide on communication protocol between elements
- [ ] Pitch Deck
- [ ] Dev environment
  - Docker/Docker-Compose

### Saturday

- [ ] Functioning product
  - [ ] Standalone elements
    - [ ] UI
    - [ ] Auction Engine
      - [ ] Endpoints
        - [ ] POST order
        - [ ] GET order status
      - [ ] Auction
        - [ ] Determine optimal auction price
        - [ ] Get reference price from 1inch API
        - [ ] Auction order states
          - [ ] Internal database for tracking this?

## Protocol Schemas

### Auction Order

Order ID - string
Wallet ID - string
Order Quantity - int (units?)
Base CCY - string
Desired CCY - string
Timestamp - datetime

### Auction Order State

Order ID - string
State - categories:

- SUBMITTED
- FILLED
- INCOMPLETE

### Transaction

Wallet ID - string
Allocation Quantity - int (units?)
Timestamp - datetime

### Transaction Set

Transaction Set ID - string
Transactions - list[Transaction]


