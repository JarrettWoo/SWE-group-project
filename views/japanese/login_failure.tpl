% include("japanese/header.tpl")
% include("japanese/banner.tpl")

<style>
h2 {color:red;}
</style>

<form class="w3-display-middle w3-round form" action="" method="POST">
	<h2>ログインは失敗でした。 ユーザー名かパスワードが正解ではありません。</h2>
	<label>ユーザー名</label>
	<input class="w3-input" type="text" input name="un"><br>

	<label>パスワード</label>
	<input class="w3-input" type="password" input name="pw"><br>

	<button type="Submit" class="w3-button w3-round w3-teal">次へ</button>
</form>
	
% include("japanese/footer.tpl")