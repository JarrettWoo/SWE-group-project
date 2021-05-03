% include("Hindi/header.tpl")
% include("Hindi/banner.tpl")

<style>
p {color:red;}
</style>

<form class="w3-display-middle w3-round form" action="" method="POST">
	<h1>खाता हटा दो</h1> <p>दिए गए उपयोगकर्ता नहीं लॉग इन अथवा ग़लत पारण शब्द.</p>
	<label>उपयोगकर्ता नाम</label>
	<input class="w3-input" type="text" name="un"><br>

	<label>पारण शब्द</label>
	<input class="w3-input" type="password" name="pw"><br>

	<label>पारण शब्द पुष्टि करें</label>
	<input class="w3-input" type="password" name="pwConfirm"><br>

	<button type="Submit" class="w3-button w3-round w3-teal">प्रस्तुत</button>
</form>
% include("Hindi/footer.tpl")
