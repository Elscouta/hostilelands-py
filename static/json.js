villageApp.factory('DataMgr', ['$rootScope', '$interval', '$http', 'LogMgr',
  function($rootScope, $interval, $http, LogMgr) {
    var mgr = {};
    mgr.server_data = {};
    mgr.server_data_by_tags = {}

    //
    // Returns whether the current piece of data is up to date and
    // can be processed by listerners
    //
    mgr._is_up_to_date = function(datainfo) {
      return datainfo["outdated"] === false && datainfo["requested"] === false
    }

    // 
    // Calls all registered functions for the given piece of data
    // and updated the relevant scope variables
    //
    mgr._postprocess = function(datainfo) {
      $.each(datainfo["variables"], function(key, val) {
        val["scope"][val["name"]] = datainfo["value"]
      });

      $.each(datainfo["postprocessings"], function(key, val) {
        val["func"](datainfo["value"])
      });
    }

    //
    // Requests the given piece of data to the server and calls 
    // processing. Will just wait if the data is currently being
    // requested.
    //
    mgr._request_data = function(datainfo) {

      if (datainfo["requested"]) {
        return
      }

      datainfo["outdated"] = false
      datainfo["requested"] = true

      $http.get(datainfo["url"])
      .success(function(data) {

	datainfo["requested"] = false
	datainfo["value"] = data["value"]

	mgr._postprocess(datainfo)

	if (datainfo["outdated"]) 
	  mgr._request_data(datainfo)

      })
      .error(function(data) {

        LogMgr.handle_server_error(data["error"]);

        datainfo["requested"] = false;

	if (datainfo["outdated"]) {
	  mgr._request_data(datainfo);
	}

      });
    }
    
    //
    // Returns the datainfo structure associated to a given url
    // Creates it if necessary.
    //
    mgr._get_datainfo = function(url) {

      if (url in mgr.server_data) {
	datainfo = mgr.server_data[url]
      } else {
        datainfo = { "url" : url, 
		     "variables" : [],
		     "postprocessings" : [],
		     "value": undefined,
		     "simulation": undefined,
		     "simulation_timer": undefined,
		     "outdated": true,
		     "requested": false };
        mgr.server_data[url] = datainfo
      }

      return datainfo
    }

    //
    // Deletes the given datainfo from the registry and the associated
    // caches.
    //
    // Calling this function on an already deleted url is fine, it will
    // just peacefully ignore.
    //
    mgr._delete_datainfo = function(url) {

      if (mgr.server_data[url] === undefined)
        return

      // CAREFUL: If variables and postprocessing were still registered,
      // there is most likely a logic error.
      mgr.server_data[url].variables = []
      mgr.server_data[url].postprocessing = []

      if (angular.isDefined(datainfo["simulation_timer"]))
        $interval.cancel(datainfo["simulation_timer"])

      delete mgr.server_data[url]

      $.each(mgr.server_data_by_tags, function (key, val) {
        delete mgr.server_data_by_tags[key][url]
      })
    }

    //
    // Checks if the datainfo is still referenced, and if not, delete it
    //
    mgr._check_alive = function(datainfo) {
      if (datainfo["variables"].length == 0 && datainfo["postprocessings"].length == 0)
        mgr._delete_datainfo(datainfo["url"])
    }

    //
    // Registers a given url as a provider of data, and binds it to a variable
    //
    mgr.bind_server_data = function(url, $scope, name, defvalue) {

      var datainfo = mgr._get_datainfo(url)
      
      if (datainfo["value"] === undefined)
        datainfo["value"] = defvalue

      datainfo["variables"].push({ "scope": $scope, "name" : name })

      $scope.$on("$destroy", function() {
        for (var i = datainfo["variables"].length - 1; i >= 0; i--) {
	  if (datainfo["variables"][i]["scope"] === $scope) 
	    datainfo["variables"].splice(i, 1)
	}

	mgr._check_alive(datainfo)
      })

      if (mgr._is_up_to_date(datainfo)) {
        $scope[name] = datainfo["value"]
      } else {
        $scope[name] = defvalue
        mgr._request_data(datainfo);
      }
    };

    //
    // Registers a given function as a processor for server data. $scope is 
    // used to determine when the postprocessing function needs to be
    // unregistered (on scope destruction)
    //
    mgr.set_server_data_postprocessing = function(url, $scope, postprocessing) {

      var datainfo = mgr._get_datainfo(url)

      datainfo["postprocessings"].push({ "scope": $scope, "func" : postprocessing })

      $scope.$on("$destroy", function() {
        for (var i = datainfo["postprocessings"].length - 1; i >= 0; i--) {
	  if (datainfo["postprocessings"][i]["scope"] === $scope) 
	    datainfo["postprocessings"].splice(i, 1)
	}

	mgr._check_alive(datainfo)
      })
 
      if (mgr._is_up_to_date(datainfo))
        postprocessing(datainfo["value"])
      else 
        mgr._request_data(datainfo);
    }

    //
    // Associates a tag to a piece of data. This data will be considered
    // outdated when the tag is passed to the reload signal
    //
    // If no tag is set, the data will never be reloaded (even on a general
    // reload)
    // 
    mgr.set_server_data_tag = function (url, tag) {
      if (mgr.server_data_by_tags[tag] === undefined) {
        mgr.server_data_by_tags[tag] = {}
      }

      mgr.server_data_by_tags[tag][url] = mgr._get_datainfo(url)
    }

    //
    // Sets a simulation function that updates the server data every
    // tick. Bound variables are updated every tick, but postprocessing
    // functions are not called.
    //
    mgr.set_server_data_simulation = function (url, tick, updatefunc) {
      var datainfo = mgr._get_datainfo(url)

//      if (angular.isDefined(datainfo["simulation_timer"]))
//        $interval.cancel(datainfo["simulation_timer"])

      datainfo["simulation"] = updatefunc

      function simulate() {
        datainfo["value"] = updatefunc(datainfo["value"])

        $.each(datainfo["variables"], function(key, val) {
          val["scope"][val["name"]] = datainfo["value"]
        });
      }

      datainfo["simulation_timer"] = $interval(simulate, tick)
    }

    //
    // Explicitly mark a tag as outdated. This is equivalent of calling 
    // reload with args = { "outdated": tag }
    //
    mgr.mark_outdated = function(tag) {
      if (mgr.server_data_by_tags[tag] === undefined)
        return

      $.each(mgr.server_data_by_tags[tag], function(i, datainfo) {
        datainfo["outdated"] = true
        mgr._request_data(datainfo) 	  
      });
    };

    // 
    // Wrapper used as a signal listener.
    //
    mgr._mark_outdated_args = function (args) {
      $.each(mgr.server_data_by_tags, function (tag, datainfos) {
        if (args["outdated"] === undefined || tag in args["outdated"]) 
          mgr.mark_outdated(tag);
      })
    }

    $rootScope.$on('reload', mgr._mark_outdated_args);

    return mgr
}]);
