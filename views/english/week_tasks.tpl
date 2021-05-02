% include("header.tpl")
% include("banner.tpl")

% include("Calendar.tpl")

<style>
	.save_edit,
	.undo_edit,
	.move_task,
	.description,
	.edit_task,
	.delete_task,
	.choose_color {
		cursor: pointer;
	}

	.completed {
		text-decoration: line-through;
	}

	.description {
		padding-left: 8px
	}
</style>

<meta name="viewport" content="width=device-width, initial-scale=1">
<link rel="stylesheet" href="https://www.w3schools.com/w3css/4/w3.css">
<body>

<div class="w3-row taskbook-container">
	<div class="w3-col w3-container" style="width:14.28%" id="One-container">
		<div class="w3-row w3-xxlarge w3-margin-bottom">
			<h1 id="one-title" class="title">Day 1</h1>
		</div>
		<div id="Tasks_1">
			<table id="task-list-one" class="w3-table">
			</table>
			<div class="w3-row  w3-margin-bottom w3-margin-top"></div>
		</div>
	</div>
	<!-- <div class="stripe">&nbsp;</div> -->
	<div class="w3-col w3-container" style="width:14.28%" id="Two-container">
		<div class="w3-row w3-xxlarge  w3-margin-bottom">
			<h1 id="two-title" class="title">Day 2</h1>
		</div>
		<div id="Tasks_2">
			<table id="task-list-two" class="w3-table">
			</table>
			<div class="w3-row w3-margin-bottom w3-margin-top"></div>
		</div>
	</div>
        	<div class="w3-col w3-container" style="width:14.28%" id="Three-container">
		<div class="w3-row w3-xxlarge w3-margin-bottom">
			<h1 id="three-title" class="title">Day 3</h1>
		</div>
		<div id="Tasks_3">
			<table id="task-list-three" class="w3-table">
			</table>
			<div class="w3-row  w3-margin-bottom w3-margin-top"></div>
		</div>
	</div>
	<!-- <div class="stripe">&nbsp;</div> -->
	<div class="w3-col w3-container" style="width:14.28%" id="Four-container">
		<div class="w3-row w3-xxlarge  w3-margin-bottom">
			<h1 id="four-title" class="title">Day 4</h1>
		</div>
		<div id="Tasks_4">
			<table id="task-list-four" class="w3-table">
			</table>
			<div class="w3-row w3-margin-bottom w3-margin-top"></div>
		</div>
	</div>
    	<div class="w3-col w3-container" style="width:14.28%" id="Five-container">
		<div class="w3-row w3-xxlarge w3-margin-bottom">
			<h1 id="five-title" class="title">Day 5</h1>
		</div>
		<div id="Tasks_5">
			<table id="task-list-five" class="w3-table">
			</table>
			<div class="w3-row  w3-margin-bottom w3-margin-top"></div>
		</div>
	</div>
	<!-- <div class="stripe">&nbsp;</div> -->
	<div class="w3-col w3-container" style="width:14.28%" id="Six-container">
		<div class="w3-row w3-xxlarge  w3-margin-bottom">
			<h1 id="six-title" class="title">Day 6</h1>
		</div>
		<div id="Tasks_6">
			<table id="task-list-six" class="w3-table">
			</table>
			<div class="w3-row w3-margin-bottom w3-margin-top"></div>
		</div>
	</div>
        	<div class="w3-col w3-container" style="width:14.28%" id="Seven-container">
		<div class="w3-row w3-xxlarge w3-margin-bottom">
			<h1 id="seven-title" class="title">Day 7</h1>
		</div>
		<div id="Tasks_7">
			<table id="task-list-seven" class="w3-table">
			</table>
			<div class="w3-row  w3-margin-bottom w3-margin-top"></div>
		</div>
	</div>
<span class="w3-button w3-display-bottomright w3-round w3-teal small-margin small-button">
		<a href="/remove">Delete Account</a>
	</span>
	<span class="w3-button w3-display-bottomleft w3-round w3-teal small-margin small-button">
		<a href="/general">General Tasks</a>
	</span>
</div>
<input id="current_input" hidden value="" />
<script src="static/tests.js"></script>
<script>

	let darkmode = false;
	$("#darkModeBtn").click(function() {
		darkmode = !darkmode;

		if (darkmode === true) {
			//this nonsense just loops through the entire DOM
			$($("*").get().reverse()).each(function(index) {
				$(this).addClass("darkmode");
			})
		}
		else {
			$($("*").get().reverse()).each(function(index) {
				$(this).removeClass("darkmode");
			})
		}
	})

/* API CALLS */

function api_get_tasks(day, success_function) {
  var path = 'api/tasks/' + day + '/seven_day'
  $.ajax({url:path, type:"GET",
          success:success_function});
}

function api_get_days(day, success_function) {
  var path = 'api/get_days/'
  path += day
  path += '/seven_day'
  $.ajax({url:path, type:"GET",
          success:success_function});
}

function api_remember_days(success_function) {
    $.ajax({url:"api/remember", type:"GET",
            success:success_function});
}

function api_new_day(date) {
    console.log('changing the view date to: ', date);
    $.ajax({url:"api/study", type:"POST",
            data:JSON.stringify(date),
            contentType:"application/json; charset=utf-8"});
}

function api_get_today(success_function) {
    $.ajax({url:"api/today", type:"GET",
            success:success_function});
}

function api_create_task(task, success_function) {
  console.log("creating task with:", task)
  $.ajax({url:"api/tasks/seven_day", type:"POST",
          data:JSON.stringify(task),
          contentType:"application/json; charset=utf-8",
          success:success_function});
}

function api_update_task(task, success_function) {
  console.log("updating task with:", task)
  $.ajax({url:"api/tasks", type:"PUT",
          data:JSON.stringify(task),
          contentType:"application/json; charset=utf-8",
          success:success_function});
}

function api_delete_task(task, success_function) {
  console.log("deleting task with:", task)
  $.ajax({url:"api/tasks", type:"DELETE",
          data:JSON.stringify(task),
          contentType:"application/json; charset=utf-8",
          success:success_function});
}

/* KEYPRESS MONITOR */

function input_keypress(event) {
  if (event.target.id != "current_input") {
    $("#current_input").val(event.target.id)
  }
  id = event.target.id.replace("input-","");
  $("#filler-"+id).prop('hidden', true);
  $("#save_edit-"+id).prop('hidden', false);
  $("#undo_edit-"+id).prop('hidden', false);
}

/* EVENT HANDLERS */

function complete_task(event) {
  if ($("#current_input").val() != "") { return }
  console.log("complete item", event.target.id )
  id = event.target.id.replace("description-","");
  completed = event.target.className.search("completed") > 0;
  console.log("updating :",{'id':id, 'completed':completed==false})
  api_update_task({'id':id, 'completed':completed==false},
                  function(result) {
                    console.log(result);
                    api_remember_days(function(result) {
                        get_current_tasks(result['savedDate']);
                    });
                  } );
}

function edit_task(event) {
  if ($("#current_input").val() != "") { return }
  console.log("edit item", event.target.id)
  id = event.target.id.replace("edit_task-","");
  // move the text to the input editor
  $("#input-"+id).val($("#description-"+id).text());
  // hide the text display
  $("#description-"+id).prop('hidden', true);
  $("#edit_task-"+id).prop('hidden', true);
  $("#delete_task-"+id).prop('hidden', true);
  // show the editor
  $("#editor-"+id).prop('hidden', false);
  $("#save_edit-"+id).prop('hidden', false);
  $("#undo_edit-"+id).prop('hidden', false);
  // set the editing flag
  $("#current_input").val(event.target.id)
}

function save_edit(event) {
  console.log("save item", event.target.id)
  id = event.target.id.replace("save_edit-","");
  console.log("desc to save = ",$("#input-" + id).val())
  if ((id != "one") & (id != "two") & (id != "three") & (id != "four") & (id != "five") & (id != "six") & (id != "seven")) {
    api_update_task({'id':id, description:$("#input-" + id).val()},
                    function(result) {
                      console.log(result);
                      api_remember_days(function(result) {
                        get_current_tasks(result['savedDate']);
                    });
                      $("#current_input").val("")
                    } );
  } else {
    api_create_task({description:$("#input-" + id).val(), list:id},
                    function(result) {
                      console.log(result);
                      api_remember_days(function(result) {
                        get_current_tasks(result['savedDate']);
                    });
                      $("#current_input").val("")
                    } );
  }
}

function undo_edit(event) {
  console.log(event)
  id = event.target.id.replace("undo_edit-","")
  console.log("undo",[id])
  $("#input-" + id).val("");
  if ((id != "one") & (id != "two") & (id != "three") & (id != "four") & (id != "five") & (id != "six") & (id != "seven")) {
    // hide the editor
    $("#editor-"+id).prop('hidden', true);
    $("#save_edit-"+id).prop('hidden', true);
    $("#undo_edit-"+id).prop('hidden', true);
    // show the text display
    $("#move_task-"+id).prop('hidden', false);
    $("#description-"+id).prop('hidden', false);
    $("#filler-"+id).prop('hidden', false);
    $("#edit_task-"+id).prop('hidden', false);
    $("#delete_task-"+id).prop('hidden', false);
  }
  // set the editing flag
  $("#current_input").val("")
}

function delete_task(event) {
  if ($("#current_input").val() != "") { return }
  console.log("delete item", event.target.id )
  id = event.target.id.replace("delete_task-","");
  api_delete_task({'id':id},
                  function(result) {
                    console.log(result);
                    api_remember_days(function(result) {
                        console.log(result)
                        get_current_tasks(result['savedDate']);
                    });
                  } );
}

function display_task(x, converter) {
	let popup = "";
	let darkClass = "";
	if (darkmode) { darkClass = "darkmode"; }

	arrow = (x.list == "today") ? "arrow_forward" : "arrow_back";
	completed = x.completed ? " completed" : "";
	if ((x.id == "one") || (x.id == "two") || (x.id == "three") || (x.id == "four") || (x.id == "five") || (x.id == "six") || (x.id == "seven")) {
		t = '<tr id="task-' + x.id + '" class="task '+darkClass+'">' +
			'  <td style="width:36px"></td>' +
			'  <td><span id="editor-' + x.id + '">' +
			'        <input id="input-' + x.id + '" style="height:22px" class="w3-input '+darkClass+'" ' +
			'          type="text" autofocus placeholder="Add an item..."/>' +
			'      </span>' +
			'  </td>' +
			'  <td style="width:72px">' +
			// '    <span id="filler-' + x.id + '" class="material-icons">more_horiz</span>' +
			'    <span id="save_edit-' + x.id + '"  class="save_edit w3-green btn '+darkClass+'">Add</span>' +
			// '    <span id="undo_edit-' + x.id + '" hidden class="undo_edit material-icons">cancel</span>' +
			'  </td>' +
			'</tr>';
	} else {
		console.log(x)
		console.log(converter)

		if ((x.list == converter['Sunday'])) {
			x.list = 'one'
		}
		else if ((x.list == converter['Monday'])){
			x.list = 'two'
		}
		else if ((x.list == converter['Tuesday'])) {
		    x.list = 'three'
		}
		else if ((x.list == converter['Wednesday'])) {
		    x.list = 'four'
		}
		else if ((x.list == converter['Thursday'])) {
		    x.list = 'five'
		}
		else if ((x.list == converter['Friday'])) {
		    x.list = 'six'
		}
		else if ((x.list == converter['Saturday'])) {
		    x.list = 'seven'
		}

		t = '<tr id="task-' + x.id + '" class="task '+darkClass+'">' +
			'  <td><span id="move_task-' + x.id + '" class="move_task ' + x.list + ' material-icons '+darkClass+'">' + arrow + '</span></td>' +
			'  <td style="width:65%;"><span style="background-color:' + x.color + '" id="description-' + x.id + '" class="description' + completed + ' '+darkClass+'">' + x.description + '</span>' +
			'      <span id="editor-' + x.id + '" hidden>' +
			'        <input id="input-' + x.id + '" style="height:22px" class="w3-input '+darkClass+'" type="text" autofocus/>' +
			'      </span>' +
			'  </td>' +
			'  <td>' +
			'    <span id="edit_task-' + x.id + '" class="edit_task ' + x.list + ' material-icons '+darkClass+'">edit</span>' +
			'    <span id="delete_task-' + x.id + '" class="delete_task material-icons '+darkClass+'">delete</span>' +
			'    <span id="choose_color-' + x.id + '" class="choose_color material-icons '+darkClass+'" onclick="choose_color('+x.id+')">palette</span>' +
			'    <span id="save_edit-' + x.id + '" hidden class="save_edit material-icons '+darkClass+'">done</span>' +
			'    <span id="undo_edit-' + x.id + '" hidden class="undo_edit material-icons '+darkClass+'">cancel</span>' +
			'  </td>' +
			'</tr>';
		popup = '<div id="dropdown-'+x.id+'" class="dropdown '+darkClass+'">' +
				'	<h3>Select highlight color:</h3>' +
				'	<select id="selColor-'+x.id+'" class="'+darkClass+'">' +
				'		<option value="#FFFF00" class="'+darkClass+'">Yellow</option>' +
				'		<option value="#00FF00" class="'+darkClass+'">Green</option>' +
				'		<option value="lightblue" class="'+darkClass+'">Blue</option>' +
				'	</select><br>' +
				'	<input class="w3-btn w3-green w3-round small-button'+darkClass+'" type="button" value="Confirm" onclick="color_task('+x.id+')"/>' +
				'	<input class="w3-btn w3-red w3-round small-button'+darkClass+'" type="button" value="Close" onclick="close_popup('+x.id+')"/>' +
				'</div>';
	}
	$("#task-list-" + x.list).append(t);
	$("#current_input").val("")
	$("body").append(popup);
}


function get_current_tasks(day) {
	// remove the old tasks
	$(".task").remove();
	var dates;

	api_get_days(day, function (result) {
		dates = result
		console.log('Using these dates for the task')
		console.log(dates)
		// Changes the title of the days to be the date represented
	    document.getElementById("one-title").innerHTML = dates['Sunday'];
	    document.getElementById("two-title").innerHTML = dates['Monday'];
	    document.getElementById("three-title").innerHTML = dates['Tuesday'];
	    document.getElementById("four-title").innerHTML = dates['Wednesday'];
	    document.getElementById("five-title").innerHTML = dates['Thursday'];
	    document.getElementById("six-title").innerHTML = dates['Friday'];
	    document.getElementById("seven-title").innerHTML = dates['Saturday'];
	});

	// display the new task editor
	display_task({ id: "one", list: "one" }, {})
	display_task({ id: "two", list: "two" }, {})
	display_task({ id: "three", list: "three" }, {})
	display_task({ id: "four", list: "four" }, {})
	display_task({ id: "five", list: "five" }, {})
	display_task({ id: "six", list: "six" }, {})
	display_task({ id: "seven", list: "seven" }, {})


	// display the tasks
	api_get_tasks(day, function (result) {
		for (const task of result.tasks) {
			display_task(task, dates);
		}

		// wire the response events
		$(".description").click(complete_task)
		$(".edit_task").click(edit_task);
		$(".save_edit").click(save_edit);
		$(".undo_edit").click(undo_edit);
		$(".delete_task").click(delete_task);
		// set all inputs to set flag
		$("input").keypress(input_keypress);
	});
}

function choose_color(id) {
	const colSelect = document.getElementById("dropdown-"+id);
	colSelect.style.display = "block";
}
function close_popup(id) {
	const colSelect = document.getElementById("dropdown-"+id);
	colSelect.style.display = "none";
}
function color_task(id){
	const selColor = document.getElementById("selColor-" + id);
	const color = selColor.value;

	const data = {
		task_id: id,
		task_color: color
	};

	$.ajax({
		url: "api/color_task", type: "PUT",
		data: JSON.stringify(data),
		contentType: "application/json; charset=utf-8",
		success: function() {
			console.log("colored task successfully");
			api_remember_days(function(result) {
				get_current_tasks(result['savedDate']);
			});
		}
	});
}

$("#calBtn").click(function() {
	const container = document.getElementById("calContainer");
	if (container.style.display == "flex") {
		container.style.display = "none";
	}
	else {
		container.style.display = "flex";
	}
});


$(document).ready(function () {
	api_get_today(function (result) {
	    api_new_day(result);
		get_current_tasks(result);
	})
});

</script>
% include("footer.tpl")
