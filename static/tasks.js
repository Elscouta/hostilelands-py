villageApp.factory('TaskMgr', [ '$interval', '$http', '$rootScope', 'LogMgr',
  function($interval, $http, $rootScope, LogMgr) {
    var mgr = {};

    mgr.task_start = function(name) {
      $http.get('task/start/' + name + '/').success(function(data) {
        LogMgr.add_message("Task successfully started: " + name);
        $rootScope.$broadcast('reload');
      })
      .error(LogMgr.handle_server_error);
    };

    mgr.task_cancel = function(id) {
      $http.get('task/cancel/' + id + '/').success(function(data) {
        LogMgr.add_message("Task successfully cancelled.");
        $rootScope.$broadcast('reload')
      })
      .error(LogMgr.handle_server_error);
    }

    mgr.task_addworker = function(id) {
      $http.get('task/addworker/' + id + '/')
      .success(function(data) {
        $rootScope.$broadcast('reload')
      })
      .error(LogMgr.handle_server_error)
    }

    mgr.task_removeworker = function(id) {
      $http.get('task/removeworker/' + id + '/')
      .success(function(data) {
        $rootScope.$broadcast('reload')
      })
      .error(LogMgr.handle_server_error)
    }

    mgr.task_finish = function(id) {
      $http.get('task/end/' + id + '/').success(function(data) {
        LogMgr.add_message("Task finished: " + data);
        $rootScope.$broadcast('reload');
      })
      .error(LogMgr.handle_server_error);
    };

    mgr.task_check_reqs = function(reqs) {
      if (!angular.isDefined($rootScope.ressources))
        return false;

      r = true;
      $.each(reqs, function (key, val) {
        if (!angular.isDefined($rootScope.ressources[key]))
          r = false;
        else if ($rootScope.ressources[key]['current'] < val)
          r = false;
      });
      return r;
    };

    return mgr;
}]);

villageApp.controller('ProgressListCtrl', ['$scope', 'DataMgr', '$attrs', '$interval', 'TaskMgr', 
  function ($scope, DataMgr, $attrs, $interval, TaskMgr) {

    var dataurl = url('task/list/actives/' + $attrs.tasktags + '/')
    DataMgr.bind_server_data(dataurl, $scope, "tasks", {})
    DataMgr.set_server_data_tag(dataurl, "tasks");
    
    function update_progress(tasks) {
      $.each(tasks, function (key, val) {
        cc = val['current_completion'] + val['completion_speed'];
        if (cc > val['length'])
          cc = val['length'];
          tasks[key]['current_completion'] = cc;
      });

      return tasks
    }

    DataMgr.set_server_data_simulation(dataurl, 1000, update_progress)

    $scope.task_cancel = TaskMgr.task_cancel;
    $scope.task_finish = TaskMgr.task_finish;
    $scope.task_addworker = TaskMgr.task_addworker;
    $scope.task_removeworker = TaskMgr.task_removeworker;
}]);

villageApp.controller('PossibleTasksCtrl', ['$scope', 'DataMgr', '$attrs', '$sce', 'TaskMgr', 
  function ($scope, DataMgr, $attrs, $sce, TaskMgr) {
  
    var dataurl = url('task/list/possibles/' + $attrs.tasktags + '/')
    DataMgr.bind_server_data(dataurl, $scope, "tasks", {})
    DataMgr.set_server_data_tag(dataurl, "tasks")
    DataMgr.set_server_data_postprocessing(dataurl, $scope, function(data) {
      $.each(data, function (key, value) {
	data[key]['longdesc'] = $sce.trustAsHtml(value['longdesc'])
      });
    });

    $scope.task_check_reqs = TaskMgr.task_check_reqs;
    $scope.task_start = TaskMgr.task_start;
}]);
