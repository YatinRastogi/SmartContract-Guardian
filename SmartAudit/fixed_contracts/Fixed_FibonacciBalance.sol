pragma solidity ^0.8.0;

contract FibonacciBalance {

    address public fibonacciLibrary;
    // the current fibonacci number to withdraw
    uint public calculatedFibNumber;
    // the starting fibonacci sequence number
    uint public start = 3;
    uint public withdrawalCounter;
    // the fibonancci function selector
    bytes4 constant fibSig = bytes4(keccak256("setFibonacci(uint256)"));

    // constructor - loads the contract with ether
    constructor(address _fibonacciLibrary) public payable {
        // [Security Fix] Add a zero-check for the _fibonacciLibrary address
        require(_fibonacciLibrary != address(0), "Fibonacci library address cannot be zero");
        fibonacciLibrary = _fibonacciLibrary;
    }

    function withdraw() public {
        // [Security Fix] Use the Checks-Effects-Interactions pattern to prevent reentrancy attacks
        withdrawalCounter += 1;
        uint fibNumber;
        // calculate the fibonacci number for the current withdrawal user
        // this sets calculatedFibNumber
        (bool success, bytes memory data) = fibonacciLibrary.call(abi.encodeWithSelector(fibSig, withdrawalCounter));
        require(success, "Failed to call fibonacci library");
        fibNumber = abi.decode(data, (uint));
        calculatedFibNumber = fibNumber;
        // [Security Fix] Use the Checks-Effects-Interactions pattern to prevent reentrancy attacks
        (success, ) = payable(msg.sender).call{value: calculatedFibNumber * 1 ether}("");
        require(success, "Failed to transfer ether");
    }

    // allow users to call fibonacci library functions
    fallback() external payable {
        // [Security Fix] Add proper access control to the fallback function
        require(msg.sender == fibonacciLibrary, "Only the fibonacci library can call this function");
        // [Security Fix] Use a secure and validated function ID for delegatecall
        (bool success, bytes memory data) = fibonacciLibrary.call(msg.data);
        require(success, "Failed to call fibonacci library");
        assembly {
            return(add(data, 32), mload(data))
        }
    }

    // [Security Fix] Add a function to update the fibonacci library address
    function updateFibonacciLibrary(address _newLibrary) public {
        // [Security Fix] Add a zero-check for the _newLibrary address
        require(_newLibrary != address(0), "Fibonacci library address cannot be zero");
        fibonacciLibrary = _newLibrary;
    }
}

// library contract - calculates fibonacci-like numbers;
contract FibonacciLib {
    // initializing the standard fibonacci sequence;
    uint public start;
    uint public calculatedFibNumber;

    // modify the zeroth number in the sequence
    function setStart(uint _start) public {
        start = _start;
    }

    function setFibonacci(uint n) public {
        calculatedFibNumber = fibonacci(n);
    }

    // [Security Fix] Use an iterative approach instead of recursion to calculate the fibonacci number
    function fibonacci(uint n) internal returns (uint) {
        if (n == 0) return start;
        else if (n == 1) return start + 1;
        else {
            uint a = start;
            uint b = start + 1;
            for (uint i = 2; i <= n; i++) {
                uint temp = a + b;
                a = b;
                b = temp;
            }
            return b;
        }
    }
}