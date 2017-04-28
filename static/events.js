villageApp.controller('EventPopupCtrl', ['DataMgr', 'LogMgr', '$http', '$scope',
  function(DataMgr, LogMgr, $http, $scope) {
    var mgr = {}
    
    mgr.lastread = -1
    mgr.unread = []
    mgr.lastunread = undefined

    mgr.next = function() {
      $scope.showcurrent = false
      mgr.lastread = mgr.unread.shift()

      if (mgr.unread.length > 0) {
        $scope.current = mgr.unread[0]
        mgr.request_current()
      } else {
        $scope.current = undefined
      }
    }

    mgr.markread = function() {
      $http.get(url('event/markread/' + $scope.current + '/'))
      mgr.next()
    }

    mgr.request_current = function() {
      $http.get(url('event/get/' + $scope.current + '/'))
      .success(function(data) {
        $scope.currentcontent = data["value"]
	$scope.showcurrent = true
      })
      .error(function(data) {
        LogMgr.handle_server_error(data["error"]);
	mgr.next()
      })
    }

    DataMgr.set_server_data_postprocessing(url('event/list/unread/'), $scope, function(data) {
      $.each(data, function(key, val) {
        if (mgr.lastread !== undefined && val < mgr.lastread) 
	  return true // continue

	if (mgr.lastunread !== undefined && val < mgr.lastunread)
	  return true // continue

	mgr.lastunread = val
	mgr.unread.push(val)

	if ($scope.current === undefined) {
	  $scope.current = val
	  mgr.request_current()
	}
      }) 
    });

    DataMgr.set_server_data_tag(url('event/list/unread/'), "events")

    $scope.current = undefined
    $scope.showcurrent = false
    $scope.currentcontent = undefined

    $scope.next = function () { mgr.next() }
    $scope.markread = function () { mgr.markread() }
}]);

