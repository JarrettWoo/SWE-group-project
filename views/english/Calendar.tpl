<!-- <!DOCTYPE html>
<html lang"en">
<head>
<script src="https://ajax.googleapis.com/ajax/libs/jquery/3.5.1/jquery.min.js"></script> -->


<div class="cal container" id="calContainer">
	<div class="cal calendar">
		<div class="cal month">
			<i class="cal fas fa-angle-left prev"></i>
			<div class="cal date">
				<h1 id=mon></h1>
				<p></p>
			</div>
			<i class="cal fas fa-angle-right next"></i>
		</div>
		<div class="cal weekdays">
			<div>Sun</div>
			<div>Mon</div>
			<div>Tue</div>
			<div>Wed</div>
			<div>Thu</div>
			<div>Fri</div>
			<div>Sat</div>
		</div>
		<div class="cal days"></div>
	</div>
</div>

<script>
	function addClickEvents(selected, lastDay) {
		for (let i = 1; i <= lastDay; ++i) {
			if (i != selected) {
				let currElem = document.getElementById(i);
				let currMonth = date.getMonth() + 1;
				let currYear = date.getFullYear();
				currElem.addEventListener("click", function () {
					var day = String(currYear) + '-'
					day += String(currMonth) + '-'
					day += String(i)
					api_new_day(day);
					get_current_tasks(day);
					document.getElementById("calContainer").style.display = "none";
				});
			}
		}
	}
	const date = new Date();
	const renderCalendar = () => {
		let selectedDay = 0;
		date.setDate(1);
		const monthDays = document.querySelector(".days");
		const lastDay = new Date(
			date.getFullYear(),
			date.getMonth() + 1,
			0
		).getDate();
		const prevLastDay = new Date(
			date.getFullYear(),
			date.getMonth(),
			0
		).getDate();
		const firstDayIndex = date.getDay();
		const lastDayIndex = new Date(
			date.getFullYear(),
			date.getMonth() + 1,
			0
		).getDay();
		const nextDays = 7 - lastDayIndex - 1;
		const months = [
			"January",
			"February",
			"March",
			"April",
			"May",
			"June",
			"July",
			"August",
			"September",
			"October",
			"November",
			"December",
		];
		document.querySelector(".date h1").innerHTML = months[date.getMonth()];
		document.querySelector(".date p").innerHTML = new Date().toDateString();
		let days = "";
		for (let x = firstDayIndex; x > 0; x--) {
			days += `<div class="cal prev-date">${prevLastDay - x + 1}</div>`;
		}
		for (let i = 1; i <= lastDay; i++) {
			if (
				i === new Date().getDate() &&
				date.getMonth() === new Date().getMonth()
			) {
				days += `<div class="cal today">${i}</div>`;
				selectedDay = i;
			} else {
				days += `<div id="${i}">${i}</div>`;
			}
		}
		if (nextDays > 0) {
			for (let j = 1; j <= nextDays; j++) {
				days += `<div class="cal next-date">${j}</div>`;
				monthDays.innerHTML = days;
			}
		} else {
			monthDays.innerHTML = days;
		}
		addClickEvents(selectedDay, lastDay);
	};
	document.querySelector(".prev").addEventListener("click", () => {
		date.setMonth(date.getMonth() - 1);
		renderCalendar();
	});
	document.querySelector(".next").addEventListener("click", () => {
		date.setMonth(date.getMonth() + 1);
		renderCalendar();
	});
	renderCalendar();
</script>

<!-- <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/5.13.0/css/all.min.css" />
<link href="https://fonts.googleapis.com/css2?family=Quicksand:wght@300;400;500;600;700&display=swap"
	rel="stylesheet"/> -->
