pragma solidity >=0.4.25 <0.7.0;
pragma experimental ABIEncoderV2;

contract AdvertisementTracker
{
    event CampaignLaunched(
        address owner,
        bytes32 bidId,
        string packageName,
        uint[3] countries,
        uint price,
        uint budget,
        uint startDate,
        uint endDate,
        string endPoint
    );

    event CampaignCancelled(
        address owner,
        bytes32 bidId
    );

    event BulkPoARegistered(
        address owner,
        bytes32 bidId,
        bytes rootHash,
        bytes signature,
        uint256 newHashes
    );

    constructor() public {
    }

    function createCampaign (
        bytes32 bidId,
        string memory packageName,
        uint[3] memory countries,
        uint price,
        uint budget,
        uint startDate,
        uint endDate,
        string memory endPoint)
    public
    {
        emit CampaignLaunched(
            msg.sender,
            bidId,
            packageName,
            countries,
            price,
            budget,
            startDate,
            endDate,
            endPoint);
    }

    function createMultipleCampaigns (
        bytes32[] memory _bidIdList,
        string[] memory _packageNameList,
        uint[3][] memory _countriesList,
        uint[] memory _priceList,
        uint[] memory _budgetList,
        uint[] memory _startDateList,
        uint[] memory _endDateList,
        string[] memory _endPointList)
    public
    {
        // check if all arguments have the same length
        require(_bidIdList.length == _packageNameList.length &&
                _bidIdList.length == _countriesList.length &&
                _bidIdList.length == _priceList.length &&
                _bidIdList.length == _budgetList.length &&
                _bidIdList.length == _startDateList.length &&
                _bidIdList.length == _endDateList.length &&
                _bidIdList.length == _endPointList.length);
        for(uint i = 0; i < _bidIdList.length; i++){
            emit CampaignLaunched(
                msg.sender,
                _bidIdList[i],
                _packageNameList[i],
                _countriesList[i],
                _priceList[i],
                _budgetList[i],
                _startDateList[i],
                _endDateList[i],
                _endPointList[i]
            );
        }
    }

    function cancelCampaign (
        bytes32 bidId)
    public
    {
        emit CampaignCancelled(
            msg.sender,
            bidId);
    }

    function cancelMultipleCampaigns (
        bytes32[] memory _bidIdList)
    public
    {
        for(uint i = 0; i < _bidIdList.length; i++) {
        emit CampaignCancelled(
            msg.sender,
            _bidIdList[i]);
        }
    }

    function bulkRegisterPoA (
        bytes32 bidId,
        bytes memory rootHash,
        bytes memory signature,
        uint256 newHashes)
    public
    {
        emit BulkPoARegistered(
            msg.sender,
            bidId,
            rootHash,
            signature,
            newHashes);
    }

    function bulkRegisterPoaOfMultipleCampaigns (
        bytes32[] memory _bidIdList,
        bytes[] memory _rootHashList,
        bytes[] memory _signatureList,
        uint256[] memory _newHashesList)
    public
    {
        // check if all arguments have the same length
        require(_bidIdList.length == _rootHashList.length &&
                _bidIdList.length == _signatureList.length &&
                _bidIdList.length == _newHashesList.length);
        for(uint i = 0; i < _bidIdList.length; i++) {
            emit BulkPoARegistered(
                msg.sender,
                _bidIdList[i],
                _rootHashList[i],
                _signatureList[i],
                _newHashesList[i]
            );
        }
    }
}
