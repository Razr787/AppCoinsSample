pragma solidity ^0.5.0;  
pragma experimental ABIEncoderV2;

    contract HelloWorld {

        struct User {
            string name;
            uint age;
        }

        event NewUser(string name, uint age);

        User[] users;


        function addUser(User memory _user) public  {
            users.push(_user);
        }

        function addUserVerbose(User memory _user) public  {
            emit NewUser(_user.name, _user.age);
            users.push(_user);
        }

        function addMultipleUsersVerbose(User[] memory _users) public  {
            for(uint i = 0; i < _users.length; i++){
                emit NewUser(_users[i].name, _users[i].age);
                users.push(_users[i]);
            }
        }

        function getUser(uint index) public view returns(User memory) {
             require(index >=0 && index < users.length);
           return users[index];
        }

        function doNothing() public {
        }

        function doNothing1() public returns (bool){
            return true;
        }

        function doNothing2(uint value) public returns (bool){
            return true;
        }
    }


