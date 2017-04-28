//
// Manages the right side view
//
villageApp.controller('RhsCtrl', ['$scope', '$rootScope', 'DataMgr', 
  function ($scope, $rootScope, DataMgr) {
    
    DataMgr.bind_server_data(url('storage/'), $scope, "ressources", {})
    DataMgr.set_server_data_tag(url('storage/'), $scope, "ressources")
    DataMgr.set_server_data_postprocessing(url('storage/'), $scope, function (ressources) { 
      
      $scope.ressources_categories = {};
      $.each(ressources, function (key, val) {
	if ($scope.ressources_categories[val.category] === undefined) {
	  $scope.ressources_categories[val.category] = [ key ]
	} else {
	  $scope.ressources_categories[val.category].push(key)
	}
      });				 
    
    });

    // Updates all ressources indicators by the expected production
    function incr_ressources(ressources) {
      $.each(ressources, function(key, val) {
	  var res = val['current'];
	  res += val['production'];
	  if (res > val['storage'])
	    res = val['storage'];
	  if (res < 0) {
	    ressources[key]['production'] = 0
	    $rootScope.$broadcast("reload", { "outdated": [ "ressources", "events" ] } )
	    res = 0;
	  }
	  ressources[key]['current'] = res;
      });

      return ressources
    }
 
    DataMgr.set_server_data_simulation(url("storage/"), 1000, incr_ressources)
}]);

//
// A simple controller for a single ressource indicator
//
villageApp.controller('RessourceListenerCtrl', ['$scope', 'DataMgr',
  function ($scope, DataMgr) {
    DataMgr.bind_server_data(url('storage/'), $scope, "ressources", {})
}]);
