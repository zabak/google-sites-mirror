<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN" "http://www.w3.org/TR/html4/loose.dtd">

<html>
<head>
	<title>$page.title</title>
	<meta http-equiv="Content-Type" content="text/html; charset=UTF-8" />
</head>
<body>
<div>

#for $predecessor in $page.get_predecessors()
<a href="$predecessor.get_alternative_path_to($page)">$predecessor.title</a> -> 
#end for
$page.title
</div>
<div>
$page.content
</div>
<br/>

<div>
<table><tr>
#for $header in $page.list_items.headers
<th>$header</th>
#end for
<th>autor</th><th>updated</th><th>revision</th>
</tr>

#for $item in $page.list_items.items
<tr>
#for $cell in $item.cells
<td>$cell</td>
#end for
<td>$item.author.name</td>
<td>$item.updated.cz</td>
<td>$item.revision</td>
</tr>
#end for

</table>

</div>

<div>
<hr/>
<h3>Subpages</h3>
#for $child in $page.childs
<a href="$child.subpage_path">$child.title</a><br/>
#end for
</div>

<div>
<hr/>
<h3>Comments</h3>
<table>
#for $comment in $page.comments
<tr>
<td>
$comment.author.name, $comment.author.email, $comment.updated.en, revision: $comment.revision
<p>
$comment.text
</p>
</td>
</tr>
#end for
</table>
<hr/>
author: $page.author.name, $page.author.email<br/>
updated: $page.updated.cz<br/>
revision: $page.revision
</div>
<div>
<hr/>
<h2>Attachments</h3>
<table>
#for $attachment in $page.attachments
<tr>
<td>
$attachment.author.name, $attachment.author.email, $attachment.updated.en, revision: $attachment.revision
<p>
<a href="$attachment.link">$attachment.name</a>
</p>
</td>
</tr>
#end for
</div>
</body>
</html>

