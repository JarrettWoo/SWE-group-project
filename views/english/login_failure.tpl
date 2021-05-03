% include("english/header.tpl")
% include("english/banner.tpl")

<style>
h2 {color:red;}
</style>

<form class="w3-display-middle w3-round form" action="" method="POST">
	<h2>Login failed! Incorrect username or password</h2>
	<label>Username</label>
	<input class="w3-input" type="text" input name="un"><br>

	<label>Password</label>
	<input class="w3-input" type="password" input name="pw"><br>

	<button type="Submit" class="w3-button w3-round w3-teal">Submit</button>
</form>
	
% include("english/footer.tpl")
