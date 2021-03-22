
function testColorChanging() {
	let data = {task_id: 1, task_color: "red"};
	$.ajax({
		url: "api/color_task", type: "PUT",
		data: JSON.stringify(data),
		contentType: "application/json; charset=utf-8",
		success: function() {
			console.log("success");
		}
	});

	data = {task_id: 2, task_color: "white"};
	$.ajax({
		url: "api/color_task", type: "PUT",
		data: JSON.stringify(data),
		contentType: "application/json; charset=utf-8",
	});

	data = {task_id: 3, task_color: "blue"};
	$.ajax({
		url: "api/color_task", type: "PUT",
		data: JSON.stringify(data),
		contentType: "application/json; charset=utf-8",
	});

	data = {task_id: 4, task_color: "yellow"};
	$.ajax({
		url: "api/color_task", type: "PUT",
		data: JSON.stringify(data),
		contentType: "application/json; charset=utf-8",
	});

	get_current_tasks();

	window.setTimeout(function() { 
		const id1 = document.getElementById("description-1");
		const id2 = document.getElementById("description-2")
		const id3 = document.getElementById("description-3");
		const id4 = document.getElementById("description-4");

		console.assert(id1.style.backgroundColor == "red");
		console.assert(id2.style.backgroundColor == "white");
		console.assert(id3.style.backgroundColor == "blue");
		console.assert(id4.style.backgroundColor == "yellow");
		console.log("Done testing colors")
	}, 1000)

}