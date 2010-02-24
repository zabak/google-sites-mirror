<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN" "http://www.w3.org/TR/html4/loose.dtd">

<html>
<head>
  <title>$title</title>
  <meta http-equiv="Content-Type" content="text/html; charset=UTF-8" />
</head>



<body>
<h2>$title</h2>
<p>revision: $revision<p>
<p>updated: $updated<p>



<table>
#for $entry in $entries
<tr>
<td><a href="$entry.title.text">$entry.title.text</a></td>
<td>$entry.summary.text</td>
<td>$entry.author[0].name.text</TD>
<td><a href="mailto:$entry.author[0].email.text">$entry.author[0].email.text</a></td>
</tr>
#end for
</table>



</body>
</html>


