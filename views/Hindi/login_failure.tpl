% include("Hindi/header.tpl")
% include("Hindi/banner.tpl")

<style>
h2 {color:red;}
</style>

<form class="w3-display-middle w3-round form" action="" method="POST">
	<h2>लॉग इन असफल! ग़लत उपयोगकर्ता नाम या पारण शब्द</h2>
	<label>उपयोगकर्ता नाम</label>
	<input class="w3-input" type="text" input name="un"><br>

	<label>पारण शब्द</label>
	<input class="w3-input" type="password" input name="pw"><br>

	<button type="Submit" class="w3-button w3-round w3-teal">प्रस्तुत</button>
</form>
	
% include("Hindi/footer.tpl")
