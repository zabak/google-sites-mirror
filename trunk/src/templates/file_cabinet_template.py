<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN" "http://www.w3.org/TR/html4/loose.dtd">

<html>
<head>
  <title>$file_cabinet.title</title>
  <meta http-equiv="Content-Type" content="text/html; charset=UTF-8" />
</head>



<body>
<h2>$file_cabinet.title</h2>
<p>revision: $file_cabinet.revision<p>
<p>updated: $file_cabinet.updated.cz<p>



<table>
#for $file in $file_cabinet.files
<tr>
<td><a href="$file.name">$file.name</a></td>
<td>$file.summary</td>
<td>$file.author.name</td>
<td><a href="mailto:$file.author.email">$file.author.email</a></td>
<td>$file.updated.en</td>
<td>$file.revision</td>
</tr>
#end for
</table>



</body>
</html>


