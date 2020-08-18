const Shares = artifacts.require('./lib/Shares.sol');
const AppCoinsTracker = artifacts.require("AppCoinsTracker");
const AppCoins = artifacts.require("AppCoins");
const AppCoinsIAB = artifacts.require("AppCoinsIAB");
const Test = artifacts.require("HelloWorld");

module.exports = function(deployer) {
  deployer.deploy(Shares);
  deployer.deploy(AppCoinsTracker);
  deployer.deploy(AppCoins);
  deployer.link(Shares, AppCoinsIAB);
  deployer.deploy(AppCoinsIAB);
  deployer.deploy(Test);
};
