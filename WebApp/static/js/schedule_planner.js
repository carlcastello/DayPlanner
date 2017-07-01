
function initScheduler(stores) {
	for (var store in stores) {
		var employees = stores[store];
		for (var employee in employees) {
			var week = employees[employee];
			for (var schedule in week) {
				for (var date in schedule) {
					var id = "#" + employee.user.username + "-" + date.weekday;
					$(id).on('submit', function(event) { 
						event.preventDefault();
						window.location.replace("google.ca");
					});
				}
			}
		}
	}
}

// {% for store, employees in stores.items %}
// 	{% for employee, week in employees.items%}
// 		{% for schedule in week %}
// 			{% for date, day in schedule.items %}

// 				$(function() {
// 						$('#{{ employee.user.username }}-{{ date.weekday }}').on('submit', function(event) { 
//     				event.preventDefault();  

// 						window.location.replace("google.ca");
// 					});
// 				});
// 			{% endfor %}
// 		{% endfor %}
// 	{% endfor %}
// {% endfor %}
