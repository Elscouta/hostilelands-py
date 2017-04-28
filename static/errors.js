// Manages error reporting
villageApp.factory('LogMgr', 
  function() {
    var mgr = {};
    mgr.errors = [];
    mgr.messages = [];

    mgr.add_error = function(txt) {
      mgr.errors.unshift(txt);
      mgr.messages.unshift("Error: " + txt);
    };

    mgr.add_message = function(txt) {
      mgr.messages.unshift(txt);
    }

    mgr.clear_errors = function() {
      mgr.errors = []
    };

    mgr.clear_messages = function() {
      mgr.messages = []
    }

    mgr.handle_server_error = function(data, stat) {
      mgr.clear_errors();
      
      if (stat == 400)
        mgr.add_error(data);
      else if (stat == 404)
        mgr.add_error("Unknown request.");
      else
      	mgr.add_error("Internal server error.");
    }

    return mgr;
});


// Exposes the error list of message
villageApp.controller('ErrorListCtrl', ['$scope', 'LogMgr',
  function ($scope, LogMgr) {
    $scope.errors = [];
}]);

// Exposes the message list
villageApp.controller('LogCtrl', ['$scope', 'LogMgr',
  function ($scope, LogMgr) {
    $scope.messages = LogMgr.messages;
}]);
