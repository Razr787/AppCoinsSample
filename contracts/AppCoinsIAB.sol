pragma solidity >=0.4.25 <0.7.0;
pragma experimental ABIEncoderV2;

import { Shares } from "./lib/Shares.sol";
import { AppCoins } from "./AppCoins.sol";

/**
@title AppCoinsIAB Interface
@author App Store Foundation
@dev Base interface to implement In-app-billing functions.
*/
contract AppCoinsIABInterface {

    /**
    @notice Function to register a in-app-billing operation
    @dev
        Registers a in-app-billing operation with the needed information and transfers the correct
        amount from the user to the developer and remaining parties.
    @param _packageName Package name of the application from which the in-app-billing was generated
    @param _sku Item id for the item bought inside the specified application
    @param _amount Value (in wei) of AppCoins to be paid for the item
    @param _addr_appc Address of the AppCoins (ERC-20) contract to be used
    @param _dev Address of the application's developer
    @param _appstore Address of the appstore to receive part of the share
    @param _oem Address of the OEM to receive part of the share
    @param _countryCode Country code of the country from which the transaction was issued
    @return {"result" : "True if the transaction was successfull"}
    */
    function buy(
        string memory _packageName, string memory _sku, uint256 _amount, address _addr_appc, address _dev,
        address _appstore, address _oem, bytes2 _countryCode)
        public
        returns (bool result);
}


contract AppCoinsIAB is AppCoinsIABInterface {

    event Buy(string packageName, string _sku, uint _amount, address _from, address _dev, address _appstore, address _oem, bytes2 countryCode);
    event OffChainBuy(address _wallet, bytes32 _rootHash);

    struct OffChainBuyElements {
        address wallet;
        bytes32 rootHash;
    }

    /**
    @notice Emits events informing offchain transactions for in-app-billing
    @dev For each wallet passed as argument, the specified roothash is emited in a OffChainBuy event.
    @param _elems List of OffChainBuyElements for which a OffChainBuy event will be issued
    */
    function informOffChainBuy2(OffChainBuyElements[] memory _elems) public {
        for(uint i = 0; i < _elems.length; i++){
            emit OffChainBuy(_elems[i].wallet, _elems[i].rootHash);
        }
    }

    /**
    @notice Emits an event informing offchain transactions for in-app-billing
    @dev
        For each wallet passed as argument, the specified roothash is emited in a OffChainBuy event.

    @param _walletList List of wallets for which a OffChainBuy event will be issued
    @param _rootHashList List of roothashs for given transactions
    */
    function testes(address _walletList, bytes32 _rootHashList)
        public
    {
            emit OffChainBuy(_walletList,_rootHashList);
    }

    /**
    @notice Emits events informing offchain transactions for in-app-billing
    @dev For each wallet passed as argument, the specified roothash is emited in a OffChainBuy event.
    @param _elem List of OffChainBuyElements for which a OffChainBuy event will be issued
    */
    function informOffChainBuy3(OffChainBuyElements memory _elem) public {
        emit OffChainBuy(_elem.wallet, _elem.rootHash);
    }

    function play_test() public returns (bool) {
        bytes32 ola = 0x111122223333444455556666777788889999AAAABBBBCCCCDDDDEEEEFFFFCCCC;
        // OffChainBuyElements memory ola1 = OffChainBuyElements(msg.sender, ola);
        // OffChainBuyElements[] storage ola2;
        return true;
    }

    /**
    @notice Emits an event informing offchain transactions for in-app-billing
    @dev
        For each wallet passed as argument, the specified roothash is emited in a OffChainBuy event.

    @param _walletList List of wallets for which a OffChainBuy event will be issued
    @param _rootHashList List of roothashs for given transactions
    */
    function informOffChainBuy(address[] memory _walletList, bytes32[] memory _rootHashList)
        public
    {
        require(_walletList.length == _rootHashList.length);
        for(uint i = 0; i < _walletList.length; i++){
            emit OffChainBuy(_walletList[i],_rootHashList[i]);
        }
    }

    function buy(string memory _packageName, string memory _sku, uint256 _amount, address _addr_appc, address _dev, address _appstore, address _oem, bytes2 _countryCode) public returns (bool) {
        require(_addr_appc != address(0));
        require(_dev != address(0));
        require(_appstore != address(0));
        require(_oem != address(0));

        AppCoins appc = AppCoins(_addr_appc);
        require(appc.allowance(msg.sender, address(this)) >= _amount);

        uint[] memory amounts = new uint[](3);
        amounts[0] = _amount * Shares.getDevShare() / 100;
        amounts[1] = _amount * Shares.getAppStoreShare() / 100;
        amounts[2] = _amount * Shares.getOEMShare() / 100;

        uint remaining = _amount - (amounts[0] + amounts[1] + amounts[2]);

        appc.transferFrom(msg.sender, _dev, amounts[0] + remaining);
        appc.transferFrom(msg.sender, _appstore, amounts[1]);
        appc.transferFrom(msg.sender, _oem, amounts[2]);

        emit Buy(_packageName, _sku, _amount, msg.sender, _dev, _appstore, _oem, _countryCode);

        return true;
    }
}
