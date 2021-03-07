% include("header.tpl")
% include("banner.tpl")
<form class="w3-display-middle w3-round form" action="" method="POST">
	<label>Username</label>
	<input class="w3-input" type="text" name="un"><br>

	<label>Password</label>
	<input class="w3-input" type="password" name="pw"><br>

	<label>Confirm Password</label>
	<input class="w3-input" type="password" name="pwConfirm"><br>

	<button type="Submit" class="w3-button w3-round w3-teal">Submit</button>
</form>
% include("footer.tpl")