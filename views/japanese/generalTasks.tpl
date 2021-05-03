% include("japanese/header.tpl")
% include("japanese/banner.tpl")

<style>
  .save_edit, .undo_edit, .description, .edit_task, .delete_task, .choose_color {
    cursor: pointer;
  }
  .completed {text-decoration: line-through;}
  .description { padding-left:8px }

</style>

<div class="w3-row taskbook-container">
	<div class="w3-half w3-container s6" id="left-container">
		<div class="w3-row w3-xxlarge w3-margin-bottom">
			<h1 class="title">一般的なタスク:</h1>
		</div>
			<table id="task-list-general" class="w3-table">
			</table>
			<div class="w3-row  w3-margin-bottom w3-margin-top"></div>
	</div>
	<!-- <div class="stripe">&nbsp;</div> -->
	<span class="w3-button w3-display-bottomright w3-round w3-teal small-margin small-button">
		<a href="/remove">アカウントを消す</a>
	</span>
  <span class="w3-button w3-display-bottomleft w3-round w3-teal small-margin small-button">
		<a href="/tasks">タスクリスト</a>
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

function api_get_tasks(success_function) {
  $.ajax({url:"api/tasks-gen", type:"GET",
          success:success_function});
}

function api_create_task(task, success_function) {
  console.log("creating task with:", task)
  $.ajax({url:"api/tasks-gen", type:"POST",
          data:JSON.stringify(task),
          contentType:"application/json; charset=utf-8",
          success:success_function});
}

function api_update_task(task, success_function) {
  console.log("updating task with:", task)
  task.id = parseInt(task.id)
  $.ajax({url:"api/tasks-gen", type:"PUT",
          data:JSON.stringify(task),
          contentType:"application/json; charset=utf-8",
          success:success_function});
}

function api_delete_task(task, success_function) {
  console.log("deleting task with:", task)
  task.id = parseInt(task.id)
  $.ajax({url:"api/tasks-gen", type:"DELETE",
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



function complete_task(event) {
  if ($("#current_input").val() != "") { return }
  console.log("complete item", event.target.id )
  id = event.target.id.replace("description-","");
  completed = event.target.className.search("completed") > 0;
  console.log("updating :",{'id':id, 'completed':completed==false})
  api_update_task({'id':id, 'completed':completed==false},
                  function(result) {
                    console.log(result);
                    get_current_tasks();
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
  if (id != 'general') {
    api_update_task({'id':id, description:$("#input-" + id).val()},
                    function(result) {
                      console.log(result);
                      get_current_tasks();
                      $("#current_input").val("")
                    } );
  } else {
    api_create_task({description:$("#input-" + id).val(), list:id},
                    function(result) {
                      console.log(result);
                      get_current_tasks();
                      $("#current_input").val("")
                    } );
  }
}

function undo_edit(event) {
  id = event.target.id.replace("undo_edit-","")
  console.log("undo",[id])
  $("#input-" + id).val("");
  if (id != 'general') {
    // hide the editor
    $("#editor-"+id).prop('hidden', true);
    $("#save_edit-"+id).prop('hidden', true);
    $("#undo_edit-"+id).prop('hidden', true);
    // show the text display
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
                    get_current_tasks();
                  } );
}

function display_task(x) {
  let popup = "";
	let darkClass = "";
	if (darkmode) { darkClass = "darkmode"; }

  completed = x.completed ? " completed" : "";
  if ((x.id == "general")) {
      t = '<tr id="task-' + x.id + '" class="task '+darkClass+'">' +
    			'  <td style="width:36px"></td>' +
    			'  <td><span id="editor-' + x.id + '">' +
    			'        <input id="input-' + x.id + '" style="height:22px" class="w3-input '+darkClass+'" ' +
    			'          type="text" autofocus placeholder="アイテムを追加..."/>' +
    			'      </span>' +
    			'  </td>' +
    			'  <td style="width:72px">' +
    			// '    <span id="filler-' + x.id + '" class="material-icons">more_horiz</span>' +
    			'    <span id="save_edit-' + x.id + '"  class="save_edit w3-green btn '+darkClass+'">追加</span>' +
    			// '    <span id="undo_edit-' + x.id + '" hidden class="undo_edit material-icons">cancel</span>' +
    			'  </td>' +
    			'</tr>';
  } else {
    console.log(x.description)
    t = '<tr id="task-' + x.id + '" class="task '+darkClass+'">' +
      '  <td style="width:36px"></td>' +
			'  <td style="width:65%;"><span id="description-' + x.id + '" class="description' + completed + ' '+darkClass+' '+x.color+'">' + x.description + '</span>' +
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
				'		<option value="Yellow" class="'+darkClass+'">金色</option>' +
				'		<option value="Green" class="'+darkClass+'">緑</option>' +
				'		<option value="Blue" class="'+darkClass+'">青</option>' +
				'	</select><br>' +
				'	<input class="w3-btn w3-green w3-round small-button'+darkClass+'" type="button" value="確認" onclick="color_task('+x.id+')"/>' +
				'	<input class="w3-btn w3-red w3-round small-button'+darkClass+'" type="button" value="終了" onclick="close_popup('+x.id+')"/>' +
				'</div>';
  }
  $("#task-list-general").append(t);
  $("#current_input").val("")
  $("body").append(popup);
}

function get_current_tasks() {
  // remove the old tasks
  $(".task").remove();
  // display the new task editor
  display_task({id:"general", list:"general"})
  // display the tasks
  api_get_tasks(function(result){
    for (const task of result.tasks) {
      display_task(task);
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
      get_current_tasks();
    }
  });
}

$(document).ready(function() {
  get_current_tasks()
});

</script>
% include("japanese/footer.tpl")
