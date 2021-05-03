% include("english/header.tpl")
% include("english/banner.tpl")

<style>
p {color:red;}
</style>

<form class="w3-display-middle w3-round form" action="" method="POST">
	<h1>Register new account</h1> <p>Passwords do not match!</p>
	<label>Username</label>
	<input class="w3-input" type="text" name="un" id="username"><br>

	<label>Password</label>
	<input class="w3-input" type="password" name="pw"><br>

	<label>Confirm Password</label>
	<input class="w3-input" type="password" name="pwConfirm"><br>

	<button type="Submit" class="w3-button w3-round w3-teal">Submit</button>
</form>

% include("english/footer.tpl")