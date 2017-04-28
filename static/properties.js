villageApp.factory('PropertyMgr', [ 'DataMgr', '$http', '$rootScope', 
  function(DataMgr, $http, $rootScope) {
    var mgr = {}

    mgr.set = function(name, v) {
      if (!angular.isDefined(v)) 
        return;
    
      $http.post('property/set/' + name + '/', { 'value': v }).success(function(data) {
      })
    }
    
    mgr.server_bind_readonly = function(name, $scope, scopename) {
      dataurl = url('property/get/' + name + '/')
      DataMgr.bind_server_data(dataurl, $scope, scopename, 0)
      DataMgr.set_server_data_tag(dataurl, "properties")
    }

    mgr.server_bind = function(name, $scope, scopename) {
      mgr.server_bind_readonly(name, $scope, scopename)
      mgr.server_bind_readonly(name, $scope, scopename+"_server")

      $scope.$watch(function () { return $scope[scopename] },
    		    function () { if ($scope[scopename] != $scope[scopename+"_server"]) mgr.set(name, $scope[scopename]) })
    }
  
    return mgr;
}]);

villageApp.controller('PoliciesCtrl', ['$scope', '$attrs', '$http', 'PropertyMgr',
  function ($scope, $attrs, $http, PropertyMgr) {
    $.each ($attrs.policies.split(' '), function (k, pname) {
      PropertyMgr.server_bind('policy:' + pname, $scope, pname)
    })
}]);

villageApp.controller('PropertyWidgetCtrl', ['$scope', '$http', '$attrs', 'PropertyMgr',
  function ($scope, $http, $attrs, PropertyMgr) {
    PropertyMgr.server_bind_readonly($attrs.propertyname, $scope, 'property_value');
}]);
