

<style>
* {box-sizing: border-box;}
ul {list-style-type: none;}
body {font-family: Verdana, sans-serif;}

.month {
  padding: 70px 25px;
  width: 100%;
  background: #1abc9c;
  text-align: center;
}

.month ul {
  margin: 0;
  padding: 0;
}

.month ul li {
  color: white;
  font-size: 20px;
  text-transform: uppercase;
  letter-spacing: 3px;
}

.month .prev {
  float: left;
  padding-top: 10px;
}

.month .next {
  float: right;
  padding-top: 10px;
}

.weekdays {
  margin: 0;
  padding: 10px 0;
  background-color: #ddd;
}

.weekdays li {
  display: inline-block;
  width: 13.6%;
  color: #666;
  text-align: center;
}

.days {
  padding: 10px 0;
  background: #eee;
  margin: 0;
}

.days li {
  list-style-type: none;
  display: inline-block;
  width: 13.6%;
  text-align: center;
  margin-bottom: 5px;
  font-size:12px;
  color: #777;
}

.days li .active {
  padding: 5px;
  background: #1abc9c;
  color: white !important
}

/* Add media queries for smaller screens */
@media screen and (max-width:720px) {
  .weekdays li, .days li {width: 13.1%;}
}

@media screen and (max-width: 420px) {
  .weekdays li, .days li {width: 12.5%;}
  .days li .active {padding: 2px;}
}

@media screen and (max-width: 290px) {
  .weekdays li, .days li {width: 12.2%;}
}
</style>
<body>

<div class="month">      
  <ul>
    <li class="prev">&#10094;</li>
    <li class="next">&#10095;</li>
    <li>
      August<br>
      <span style="font-size:18px">2021</span>
    </li>
  </ul>
</div>

<ul class="weekdays">
  <li>Mo</li>
  <li>Tu</li>
  <li>We</li>
  <li>Th</li>
  <li>Fr</li>
  <li>Sa</li>
  <li>Su</li>
</ul>

<ul class="days">  
  <li>1</li>
  <li>2</li>
  <li>3</li>
  <li>4</li>
  <li>5</li>
  <li>6</li>
  <li>7</li>
  <li>8</li>
  <li>9</li>
  <li>10</li>
  <li>11</li>
  <li>12</li>
  <li>13</li>
  <li>14</li>
  <li>15</li>
  <li>16</li>
  <li>17</li>
  <li>18</li>
  <li>19</li>
  <li>20</li>
  <li>21</li>
  <li>22</li>
  <li>23</li>
  <li>24</li>
  <li>25</li>
  <li>26</li>
  <li>27</li>
  <li>28</li>
  <li>29</li>
  <li>30</li>
  <li>31</li>
</ul>

</body>
=======
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
