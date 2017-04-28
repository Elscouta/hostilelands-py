//////////////////////////////// WRAPPERS ///////////////////////////////////
function hashtable_as_array(hashtable)
{
  if (!hashtable) 
    return [];

  var filtered = []
  $.each(hashtable, function(key, val) {
    filtered.push({ 'key': key, 
    		    'value': val });
  });

  return filtered;
}
villageApp.filter('hashtableAsArray', function() { return hashtable_as_array; });

//////////////////////////// FORMAT FUNCTIONS ///////////////////////////////

function humanize_float(number, is_integer)
{
  if (number < 10 && !is_integer) 
    return number.toFixed(3)
  else if (number < 100 && !is_integer)
    return number.toFixed(2)
  else if (number < 1000 && !is_integer)
    return number.toFixed(1)
  else if (number < 10000)
    return number.toFixed(0)
  else if (number < 100000)
    return (number / 1000).toFixed(2) + "K"
  else if (number < 1000000)
    return (number / 1000).toFixed(1) + "K"
  else if (number < 10000000)
    return (number / 1000).toFixed(0) + "K"
  else if (number < 100000000)
    return (number / 1000000).toFixed(2) + "M"
  else if (number < 1000000000)
    return (number / 1000000).toFixed(1) + "M"
  else if (number < 10000000000)
    return (number / 1000000).toFixed(0) + "M"
  else
    return (number / 1000000000).toFixed(2) + "G"
}
villageApp.filter('humanizeQty', function() { return humanize_float; });

function humanize_relative_float(number)
{
  if (number < 0)
    return "-" + humanize_float(- number);
  else
    return "+" + humanize_float(number);
}
villageApp.filter('humanizeProd', function() { return humanize_relative_float; });

villageApp.directive('myTooltip',  
  function() {
    return {
      restrict: 'A',
      link: function(scope, element, attrs) {
        var tooltipSpan, x, y;

        element.mousemove(function(e) {
	  scope.tooltipalign = {}
	
	  if (e.clientX < 0.65 * window.innerWidth) {
	    scope.tooltipalign["left"] = e.clientX + 15
	  } else {
	    scope.tooltipalign["right"] = window.innerWidth - e.clientX - 15
	  }

	  if (e.clientY < 0.65 * window.innerHeight) {
	    scope.tooltipalign["top"] = e.clientY + 15
	  } else {
	    scope.tooltipalign["bottom"] = window.innerHeight - e.clientY - 15
	  }

//	  alert("e.clientX " + e.clientX + " -- " +
//	        "e.clientY " + e.clientY + " -- " +
//		"width " + window.innerWidth + " -- " +
//		"height " + window.innerHeight)

	  scope.show = 1;
        });
	element.mouseleave(function(e) {
	  scope.show = 0;
	});
      }
    };
});

function describe_ratio(strratio)
{
  ratio = parseInt(strratio);

  if (ratio < 0)
    return "Invalid"
  else if (ratio < 15)
    return "Extremely Low"
  else if (ratio < 30)
    return "Very Low"
  else if (ratio < 40)
    return "Low"
  else if (ratio < 60)
    return "Medium"
  else if (ratio < 70)
    return "High"
  else if (ratio < 85)
    return "Very High"
  else if (ratio <= 100)
    return "Extremely High"
  else
    return "Invalid"
}
villageApp.filter('describeRatio', function() { return describe_ratio; });

/////////////////////////////////////////////////////////////////////////////
function url(postfix) {
  return "/game/" + vid + "/" + postfix;
}

