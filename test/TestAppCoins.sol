pragma solidity >=0.4.25 <0.7.0;

import "truffle/Assert.sol";
import "truffle/DeployedAddresses.sol";
import "../contracts/AppCoins.sol";
import "../contracts/AppCoinsIAB.sol";

contract TestAppCoins {

  function testInitialBalanceUsingDeployedContract() public {
    AppCoins appc = AppCoins(DeployedAddresses.AppCoins());
    AppCoinsIAB appc_iab = AppCoinsIAB(DeployedAddresses.AppCoinsIAB());

    uint expected = 1000000000000000000000000;
    
    assert(appc_iab.play_test());
    Assert.equal(appc.totalSupply(), expected, "totalSupply should be 1000000 AppCoins");
    Assert.equal(appc.balanceOf(msg.sender), appc.totalSupply(), "Owner should have the totalSupply of AppCoins");
  }
}
