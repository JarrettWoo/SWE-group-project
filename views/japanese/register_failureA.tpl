% include("japanese/header.tpl")
% include("japanese/banner.tpl")

<style>
p {color:red;}
</style>

<form class="w3-display-middle w3-round form" action="" method="POST">
	<h1>アカウントを作成</h1> <p>ユーザー名は利用できません。</p>
	<label>ユーザー名</label>
	<input class="w3-input" type="text" name="un" id="username"><br>

	<label>パスワード</label>
	<input class="w3-input" type="password" name="pw"><br>

	<label>パスワードを確認</label>
	<input class="w3-input" type="password" name="pwConfirm"><br>

	<button type="Submit" class="w3-button w3-round w3-teal">次へ</button>
</form>

% include("japanese/footer.tpl")