// Initialization of app
var villageApp = angular.module('villageApp', ['ngRoute']);

// HOLY SHIT WE ARE FUCKED. RUN FOR THIS HILLS
// ----------------------------> []
villageApp.config(function($interpolateProvider) {
  $interpolateProvider.startSymbol('{$');
  $interpolateProvider.endSymbol('$}');
});

// Setup routing
villageApp.config(function($routeProvider) {
  $routeProvider
  .when('/building/:buildingname', {
    templateUrl: function(urlattr) {
      return url('building/show/' + urlattr.buildingname + '/')
    },
    controller: 'BuildingCtrl'
  })
  .when('/manager/:managername', {
    templateUrl: function(urlattr) {
      return url('manager/' + urlattr.managername + '/')
    },
    controller: 'BuildingCtrl'
  })
  .otherwise({
    templateUrl: url('building/show/townhall/'),
    controller: 'BuildingCtrl'
  });
});

// WTF ARE WE DOING THERE ARE YOU GUYS SERIOUS
villageApp.run(function($rootScope, $templateCache) {
  $rootScope.$on('$routeChangeStart', function(event, next, current) {
    $templateCache.removeAll();
  });
});

// Manages... uh?
villageApp.controller('MainCtrl', function() {
});

// Manages the building menu view
villageApp.controller('BuildingListCtrl', ['$scope', 'DataMgr',
  function($scope, DataMgr) {
    DataMgr.bind_server_data(url('building/list/'), $scope, "buildings");
    DataMgr.set_server_data_tag(url('building/list/'), "buildings"); 
}]);

// Manages the main building view
villageApp.controller('BuildingCtrl', ['$scope',
  function($scope) {

}]);

