% include("hindi/header.tpl")
% include("hindi/banner.tpl")

<style>
p {color:red;}
</style>

<form class="w3-display-middle w3-round form" action="" method="POST">
	<h1>नया खाता रजिस्टर करें</h1> <p>पारण शब्द मेल नहीं करता!</p>
	<label>उपयोगकर्ता नाम</label>
	<input class="w3-input" type="text" name="un" id="username"><br>

	<label>पारण शब्द</label>
	<input class="w3-input" type="password" name="pw"><br>

	<label>पारण शब्द पुष्टि करें</label>
	<input class="w3-input" type="password" name="pwConfirm"><br>

	<button type="Submit" class="w3-button w3-round w3-teal">Submit</button>
</form>

% include("hindi/footer.tpl")
