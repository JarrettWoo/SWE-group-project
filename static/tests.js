
function testColorChanging() {
	// let data = {task_id: 1, task_color: "red"};
	// $.ajax({
	// 	url: "api/color_task", type: "PUT",
	// 	data: JSON.stringify(data),
	// 	contentType: "application/json; charset=utf-8",
	// 	success: function() {
	// 		console.log("success");
	// 	}
	// });

	// data = {task_id: 2, task_color: "white"};
	// $.ajax({
	// 	url: "api/color_task", type: "PUT",
	// 	data: JSON.stringify(data),
	// 	contentType: "application/json; charset=utf-8",
	// });

	// data = {task_id: 3, task_color: "blue"};
	// $.ajax({
	// 	url: "api/color_task", type: "PUT",
	// 	data: JSON.stringify(data),
	// 	contentType: "application/json; charset=utf-8",
	// });

	// data = {task_id: 4, task_color: "yellow"};
	// $.ajax({
	// 	url: "api/color_task", type: "PUT",
	// 	data: JSON.stringify(data),
	// 	contentType: "application/json; charset=utf-8",
	// });

	const colors = ["red", "white", "blue", "yellow"];
	let ids = [];
	for (let i = 1; i <= 10; ++i) {
		let task = document.getElementById("description-"+i);
		if (task != null) {
			ids.push(i);
		}
	}
	for (let i = 0; i < ids.length; ++i) {
		let data = { task_id: ids[i], task_color: colors[ids[i] % 4] };
		$.ajax({
			url:"api/color_task", type: "PUT",
			data: JSON.stringify(data),
			contentType: "application/json; charset=utf-8",
		});
	}

	get_current_tasks();

	window.setTimeout(function() { 
		for (let i = 0; i < ids.length; ++i) {
			let task = document.getElementById("description-"+ids[i]);
			console.assert(task.style.backgroundColor == colors[ids[i] % 4]);
		}
		console.log("Done testing colors")
	}, 1000)

}
